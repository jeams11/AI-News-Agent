"""AIBase 新闻爬虫（页面由 JavaScript 渲染，使用 Playwright）。"""

import logging

from bs4 import BeautifulSoup
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from app.config import settings

logger = logging.getLogger(__name__)

SOURCE = "AIBase"
LIST_URL = "https://news.aibase.com/zh/news"

# 导航类链接文本，不是真正的新闻
_NAV_TITLES = {
    "首页",
    "AI资讯",
    "AI 产品库",
    "GEO 平台",
    "MCP 服务",
    "模型算力广场",
}


def _parse_list(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    seen: set[str] = set()
    articles: list[dict] = []
    for link in soup.find_all("a", href=True):
        title = link.get_text(strip=True)
        href = link["href"]

        if not title or title in _NAV_TITLES or "/zh/news/" not in href:
            continue
        if href.startswith("/"):
            href = "https://news.aibase.com" + href
        if href in seen:
            continue
        seen.add(href)

        articles.append({"title": title, "url": href, "source": SOURCE})

    return articles


def _parse_article(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article")
    if article:
        return article.get_text("\n", strip=True)

    # 备用方案：取页面中最长的文本块
    texts = [
        div.get_text(strip=True)
        for div in soup.find_all("div")
        if len(div.get_text(strip=True)) > 200
    ]
    return max(texts, key=len) if texts else ""


def crawl(max_articles: int | None = None) -> list[dict]:
    """完整抓取流程：用同一个浏览器实例抓列表和正文。"""
    limit = max_articles or settings.aibase_max_articles
    timeout_ms = settings.request_timeout_seconds * 1000

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(LIST_URL, wait_until="domcontentloaded", timeout=timeout_ms)
            # 等待 JavaScript 渲染出新闻列表
            page.wait_for_timeout(3000)
            articles = _parse_list(page.content())[:limit]
            logger.info("AIBase 列表抓取到 %d 条", len(articles))

            for article in articles:
                try:
                    page.goto(
                        article["url"],
                        wait_until="domcontentloaded",
                        timeout=timeout_ms,
                    )
                    page.wait_for_timeout(1000)
                    article["content"] = _parse_article(page.content())
                except PlaywrightError as exc:
                    logger.warning(
                        "AIBase 正文抓取失败 %s: %s", article["url"], exc
                    )
                    article["content"] = None
        finally:
            browser.close()

    return articles
