"""核心任务流水线：爬取入库、AI 分析、报告生成。

调度器和 API 手动触发都调用这里的函数；
用非阻塞锁防止同一任务并发重复执行。
"""

import logging
import threading

from opencc import OpenCC

from app import database
from app.config import settings
from app.crawlers import aibase, bbc
from app.services import cleaner, report, summarizer

logger = logging.getLogger(__name__)

_cc = OpenCC("t2s")

_crawl_lock = threading.Lock()
_summary_lock = threading.Lock()


def _to_simplified(articles: list[dict]) -> list[dict]:
    """繁体转简体（BBC 中文页面为繁体），返回新列表。"""
    return [
        {
            **article,
            "title": _cc.convert(article.get("title") or ""),
            "content": (
                _cc.convert(article["content"]) if article.get("content") else None
            ),
        }
        for article in articles
    ]


def run_crawl() -> dict:
    """执行一轮完整爬取：BBC + AIBase → 清洗 → 入库。"""
    if not _crawl_lock.acquire(blocking=False):
        logger.info("已有爬取任务在运行，跳过本次触发")
        return {"status": "skipped", "reason": "crawl already running"}

    try:
        results: dict[str, int] = {}
        all_articles: list[dict] = []

        for crawler in (bbc, aibase):
            try:
                articles = crawler.crawl()
                results[crawler.SOURCE] = len(articles)
                all_articles.extend(articles)
            except Exception:
                logger.exception("%s 爬取失败", crawler.SOURCE)
                results[crawler.SOURCE] = 0

        cleaned = cleaner.clean_articles(_to_simplified(all_articles))
        inserted = database.insert_news(cleaned)

        logger.info(
            "爬取完成: 抓取 %d 条, 清洗后 %d 条, 新增入库 %d 条",
            len(all_articles),
            len(cleaned),
            inserted,
        )
        return {
            "status": "ok",
            "crawled": results,
            "after_clean": len(cleaned),
            "inserted": inserted,
        }
    finally:
        _crawl_lock.release()


def run_summarize() -> dict:
    """执行一轮 AI 分析：取未分析的新闻 → LLM → 写回数据库 → 生成日报。"""
    if not _summary_lock.acquire(blocking=False):
        logger.info("已有 AI 分析任务在运行，跳过本次触发")
        return {"status": "skipped", "reason": "summarize already running"}

    try:
        pending = database.get_pending_analysis(limit=settings.llm_batch_size)
        logger.info("待分析新闻: %d 条", len(pending))

        analyzed = 0
        failed = 0
        for item in pending:
            result = summarizer.analyze(item["title"], item["content"])
            if result is None:
                failed += 1
                continue

            database.save_analysis(
                news_id=item["id"],
                summary=result["summary"],
                importance=result["importance"],
                category=result["category"],
                keywords=result["keywords"],
            )
            analyzed += 1
            logger.info("已分析: %s", item["title"])

        report_path = None
        if analyzed:
            report_path = str(report.generate_report())

        return {
            "status": "ok",
            "pending": len(pending),
            "analyzed": analyzed,
            "failed": failed,
            "report": report_path,
        }
    finally:
        _summary_lock.release()
