"""REST API 路由。

所有接口使用统一响应格式：
{"success": bool, "data": ..., "error": str | null, "meta": {...}}
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app import database
from app.config import settings
from app.services import pipeline

router = APIRouter(prefix="/api", tags=["news"])


def _envelope(data=None, error: str | None = None, meta: dict | None = None) -> dict:
    return {
        "success": error is None,
        "data": data,
        "error": error,
        "meta": meta or {},
    }


@router.get("/news")
def list_news(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    source: str | None = None,
    category: str | None = None,
    min_importance: int | None = Query(None, ge=1, le=5),
    analyzed_only: bool = False,
):
    """分页查询新闻，支持来源 / 分类 / 重要程度过滤。"""
    news, total = database.query_news(
        page=page,
        limit=limit,
        source=source,
        category=category,
        min_importance=min_importance,
        analyzed_only=analyzed_only,
    )
    return _envelope(
        data=news,
        meta={"total": total, "page": page, "limit": limit},
    )


@router.get("/news/{news_id}")
def get_news(news_id: int):
    """按 ID 查询单条新闻（含正文）。"""
    news = database.get_news_by_id(news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return _envelope(data=news)


@router.get("/stats")
def stats():
    """数据统计：总量、已分析数量、重要新闻数量、来源分布。"""
    return _envelope(data=database.get_stats())


@router.get("/report", response_class=PlainTextResponse)
def report():
    """获取最新生成的 Markdown 日报。"""
    if not settings.report_path.exists():
        raise HTTPException(status_code=404, detail="日报尚未生成")
    return settings.report_path.read_text(encoding="utf-8")


@router.post("/tasks/crawl", status_code=202)
def trigger_crawl(background_tasks: BackgroundTasks):
    """手动触发一轮新闻爬取（后台执行）。"""
    background_tasks.add_task(pipeline.run_crawl)
    return _envelope(data={"task": "crawl", "status": "started"})


@router.post("/tasks/summarize", status_code=202)
def trigger_summarize(background_tasks: BackgroundTasks):
    """手动触发一轮 AI 分析与日报生成（后台执行）。"""
    background_tasks.add_task(pipeline.run_summarize)
    return _envelope(data={"task": "summarize", "status": "started"})
