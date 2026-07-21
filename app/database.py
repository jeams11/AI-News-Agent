"""SQLite 数据访问层。

统一管理表结构与所有读写操作：
- news.url 上有 UNIQUE 约束，配合 INSERT OR IGNORE 实现去重；
- 包含 AI 分析结果列（summary / importance / category / keywords）；
- 对旧版本数据库自动补齐缺失列（轻量迁移）。
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    published_time TEXT,
    crawled_at TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    importance INTEGER,
    category TEXT,
    keywords TEXT,
    analyzed_at TEXT
)
"""

# 旧版数据库缺失的列，启动时自动补齐
_MIGRATION_COLUMNS = {
    "published_time": "TEXT",
    "crawled_at": "TEXT",
    "content": "TEXT",
    "summary": "TEXT",
    "importance": "INTEGER",
    "category": "TEXT",
    "keywords": "TEXT",
    "analyzed_at": "TEXT",
}


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path or settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path | None = None) -> None:
    """建表并对旧库补齐缺失列。应用启动时调用一次。"""
    with get_connection(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(_SCHEMA)

        existing = {
            row["name"] for row in conn.execute("PRAGMA table_info(news)")
        }
        for column, col_type in _MIGRATION_COLUMNS.items():
            if column not in existing:
                logger.info("数据库迁移: 添加缺失列 %s", column)
                conn.execute(f"ALTER TABLE news ADD COLUMN {column} {col_type}")

        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_news_url ON news(url)"
        )


def insert_news(items: list[dict], db_path: Path | None = None) -> int:
    """批量插入新闻，url 已存在时自动跳过。返回实际新增数量。"""
    now = datetime.now().isoformat(timespec="seconds")
    inserted = 0
    with get_connection(db_path) as conn:
        for item in items:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO news
                    (title, url, source, published_time, crawled_at, content)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item["title"],
                    item["url"],
                    item["source"],
                    item.get("published_time"),
                    now,
                    item.get("content"),
                ),
            )
            inserted += cursor.rowcount
    return inserted


def get_pending_analysis(
    limit: int, db_path: Path | None = None
) -> list[dict]:
    """获取尚未做过 AI 分析、且已有正文的新闻。"""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, title, content
            FROM news
            WHERE summary IS NULL
              AND content IS NOT NULL
              AND length(content) > 50
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_analysis(
    news_id: int,
    summary: str,
    importance: int,
    category: str,
    keywords: str,
    db_path: Path | None = None,
) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            UPDATE news
            SET summary = ?, importance = ?, category = ?,
                keywords = ?, analyzed_at = ?
            WHERE id = ?
            """,
            (
                summary,
                importance,
                category,
                keywords,
                datetime.now().isoformat(timespec="seconds"),
                news_id,
            ),
        )


def query_news(
    page: int = 1,
    limit: int = 20,
    source: str | None = None,
    category: str | None = None,
    min_importance: int | None = None,
    analyzed_only: bool = False,
    db_path: Path | None = None,
) -> tuple[list[dict], int]:
    """分页查询新闻，返回 (列表, 总数)。"""
    conditions = []
    params: list = []

    if source:
        conditions.append("source = ?")
        params.append(source)
    if category:
        conditions.append("category = ?")
        params.append(category)
    if min_importance is not None:
        conditions.append("importance >= ?")
        params.append(min_importance)
    if analyzed_only:
        conditions.append("summary IS NOT NULL")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    with get_connection(db_path) as conn:
        total = conn.execute(
            f"SELECT COUNT(*) FROM news {where}", params
        ).fetchone()[0]

        rows = conn.execute(
            f"""
            SELECT id, title, url, source, published_time, crawled_at,
                   summary, importance, category, keywords, analyzed_at
            FROM news {where}
            ORDER BY COALESCE(importance, 0) DESC, id DESC
            LIMIT ? OFFSET ?
            """,
            [*params, limit, (page - 1) * limit],
        ).fetchall()

    return [dict(row) for row in rows], total


def get_news_by_id(news_id: int, db_path: Path | None = None) -> dict | None:
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM news WHERE id = ?", (news_id,)
        ).fetchone()
    return dict(row) if row else None


def get_stats(db_path: Path | None = None) -> dict:
    with get_connection(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
        analyzed = conn.execute(
            "SELECT COUNT(*) FROM news WHERE summary IS NOT NULL"
        ).fetchone()[0]
        important = conn.execute(
            "SELECT COUNT(*) FROM news WHERE importance >= 4"
        ).fetchone()[0]
        sources = conn.execute(
            "SELECT source, COUNT(*) AS count FROM news GROUP BY source"
        ).fetchall()
    return {
        "total": total,
        "analyzed": analyzed,
        "important": important,
        "sources": {row["source"]: row["count"] for row in sources},
    }


def get_analyzed_news(
    limit: int = 50, db_path: Path | None = None
) -> list[dict]:
    """获取已完成 AI 分析的新闻（用于报告与首页）。"""
    rows, _ = query_news(
        page=1, limit=limit, analyzed_only=True, db_path=db_path
    )
    return rows
