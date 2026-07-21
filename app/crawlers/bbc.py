"""BBC 中文新闻爬虫（requests + BeautifulSoup，页面为服务端渲染）。"""

import logging

import requests
from bs4 import BeautifulSoup

from app.config import settings

logger = logging.getLogger(__name__)

SOURCE = "BBC"
LIST_URL = "https://www.bbc.com/zhongwen/topics/cpydz218gddt/trad"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch_list() -> list[dict]:
    """抓取 BBC 中文专题页的新闻标题与链接。"""
    response = requests.get(
        LIST_URL, headers=HEADERS, timeout=settings.request_timeout_seconds
    )
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    seen: set[str] = set()
    articles: list[dict] = []
    for link in soup.find_all("a", href=True):
        title = link.get_text(strip=True)
        href = link["href"]

        # 只保留新闻正文页，过滤导航 / 专题入口等链接
        if not title or "/zhongwen/articles/" not in href:
            continue
        if href.startswith("/"):
            href = "https://www.bbc.com" + href
        if href in seen:
            continue
        seen.add(href)

        articles.append({"title": title, "url": href, "source": SOURCE})

    return articles


def fetch_article(url: str) -> str:
    """抓取单篇新闻正文（只取 main 区域的段落，避免混入导航文本）。"""
    response = requests.get(
        url, headers=HEADERS, timeout=settings.request_timeout_seconds
    )
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.find("main") or soup
    paragraphs = [
        p.get_text(strip=True)
        for p in main.find_all("p")
        if p.get_text(strip=True)
    ]
    return "\n".join(paragraphs)


def crawl(max_articles: int | None = None) -> list[dict]:
    """完整抓取流程：列表 + 每篇正文。单篇失败不影响整体。"""
    limit = max_articles or settings.bbc_max_articles
    articles = fetch_list()[:limit]
    logger.info("BBC 列表抓取到 %d 条", len(articles))

    for article in articles:
        try:
            article["content"] = fetch_article(article["url"])
        except requests.RequestException as exc:
            logger.warning("BBC 正文抓取失败 %s: %s", article["url"], exc)
            article["content"] = None

    return articles
