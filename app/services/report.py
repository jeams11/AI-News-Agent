"""生成 Markdown 格式的新闻日报。"""

from datetime import datetime
from pathlib import Path

from app import database
from app.config import settings


def generate_report(db_path: Path | None = None) -> Path:
    """根据已分析的新闻生成日报文件，返回文件路径。"""
    news = database.get_analyzed_news(limit=50, db_path=db_path)

    lines = [
        "# AI 新闻日报",
        "",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"共收录 {len(news)} 条已分析新闻，按重要程度排序。",
        "",
    ]

    for index, item in enumerate(news, 1):
        stars = "⭐" * (item.get("importance") or 0)
        lines.append(f"## {index}. {item['title']}")
        lines.append("")
        lines.append(
            f"**来源：** {item['source']} | "
            f"**分类：** {item.get('category') or '未分类'} | "
            f"**重要程度：** {stars}"
        )
        if item.get("keywords"):
            lines.append("")
            lines.append(f"**关键词：** {item['keywords']}")
        lines.append("")
        lines.append(item.get("summary") or "")
        lines.append("")
        lines.append(f"[原文链接]({item['url']})")
        lines.append("")

    report_path = settings.report_path
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
