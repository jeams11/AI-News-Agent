"""新闻质量过滤：剔除导航、广告、多媒体入口等低价值条目。"""

MIN_TITLE_LENGTH = 8

BAD_WORDS = (
    "点击",
    "免费下载",
    "下载",
    "直播",
    "即时更新",
    "海报",
    "图片",
    "图库",
    "视频",
    "专题入口",
    "点击这里",
    "一图看懂",
    "合集",
)


def is_valid_title(title: str | None) -> bool:
    """标题过短或包含低质量关键词时返回 False。"""
    if not title or len(title) < MIN_TITLE_LENGTH:
        return False
    return not any(word in title for word in BAD_WORDS)


def clean_articles(articles: list[dict]) -> list[dict]:
    """过滤低质量新闻，返回新列表（不修改原数据）。"""
    return [a for a in articles if is_valid_title(a.get("title"))]
