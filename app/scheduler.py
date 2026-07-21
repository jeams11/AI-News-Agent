"""定时任务调度：基于 APScheduler，随 Web 服务一起启动。"""

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.services import pipeline

logger = logging.getLogger(__name__)


def create_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

    scheduler.add_job(
        pipeline.run_crawl,
        trigger="interval",
        minutes=settings.crawl_interval_minutes,
        id="crawl_news",
        name="新闻爬取",
        max_instances=1,
        coalesce=True,
        # 服务启动 30 秒后先跑一轮，新部署无需等待整个间隔
        next_run_time=datetime.now() + timedelta(seconds=30),
    )

    scheduler.add_job(
        pipeline.run_summarize,
        trigger="interval",
        minutes=settings.summary_interval_minutes,
        id="summarize_news",
        name="AI 分析与日报",
        max_instances=1,
        coalesce=True,
    )

    logger.info(
        "调度器已配置: 爬取每 %d 分钟, AI 分析每 %d 分钟",
        settings.crawl_interval_minutes,
        settings.summary_interval_minutes,
    )
    return scheduler
