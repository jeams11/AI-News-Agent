"""应用入口：FastAPI（页面 + API）+ 内置定时调度。

启动方式：
    python -m app.main
或：
    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app import database
from app.api import router as api_router
from app.config import settings
from app.scheduler import create_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.init_db()
    logger.info("数据库就绪: %s", settings.db_path)

    scheduler = None
    if settings.enable_scheduler:
        scheduler = create_scheduler()
        scheduler.start()

    yield

    if scheduler:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="AI News Agent",
    description="AI 新闻自动采集与分析系统",
    version="2.0",
    lifespan=lifespan,
)
app.include_router(api_router)


@app.get("/health")
def health():
    """健康检查，供 Docker HEALTHCHECK 与监控使用。"""
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def index(request: Request):
    """新闻仪表盘页面。"""
    news = database.get_analyzed_news(limit=50)
    stats = database.get_stats()
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "news": news,
            "stats": stats,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
    )
