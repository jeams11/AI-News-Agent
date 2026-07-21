from app import database


class TestInsertNews:
    def test_insert_returns_count(self, db_path, sample_articles):
        inserted = database.insert_news(sample_articles, db_path=db_path)
        assert inserted == 2

    def test_duplicate_url_is_ignored(self, db_path, sample_articles):
        database.insert_news(sample_articles, db_path=db_path)
        inserted_again = database.insert_news(sample_articles, db_path=db_path)

        assert inserted_again == 0
        assert database.get_stats(db_path=db_path)["total"] == 2


class TestAnalysisFlow:
    def test_pending_then_save(self, db_path, sample_articles):
        database.insert_news(sample_articles, db_path=db_path)

        pending = database.get_pending_analysis(limit=10, db_path=db_path)
        assert len(pending) == 2

        database.save_analysis(
            news_id=pending[0]["id"],
            summary="测试摘要",
            importance=5,
            category="人工智能",
            keywords="AI, 测试",
            db_path=db_path,
        )

        remaining = database.get_pending_analysis(limit=10, db_path=db_path)
        assert len(remaining) == 1

        stats = database.get_stats(db_path=db_path)
        assert stats["analyzed"] == 1
        assert stats["important"] == 1

    def test_no_content_not_pending(self, db_path):
        database.insert_news(
            [
                {
                    "title": "只有标题没有正文的新闻条目",
                    "url": "https://example.com/no-content",
                    "source": "BBC",
                    "content": None,
                }
            ],
            db_path=db_path,
        )
        assert database.get_pending_analysis(limit=10, db_path=db_path) == []


class TestQueryNews:
    def test_filter_by_source(self, db_path, sample_articles):
        database.insert_news(sample_articles, db_path=db_path)

        news, total = database.query_news(source="BBC", db_path=db_path)
        assert total == 1
        assert news[0]["source"] == "BBC"

    def test_pagination(self, db_path, sample_articles):
        database.insert_news(sample_articles, db_path=db_path)

        page1, total = database.query_news(page=1, limit=1, db_path=db_path)
        page2, _ = database.query_news(page=2, limit=1, db_path=db_path)

        assert total == 2
        assert len(page1) == 1
        assert page1[0]["id"] != page2[0]["id"]

    def test_get_by_id(self, db_path, sample_articles):
        database.insert_news(sample_articles, db_path=db_path)
        news, _ = database.query_news(db_path=db_path)

        found = database.get_news_by_id(news[0]["id"], db_path=db_path)
        assert found is not None
        assert found["title"] == news[0]["title"]

        assert database.get_news_by_id(99999, db_path=db_path) is None


class TestMigration:
    def test_old_schema_gets_new_columns(self, tmp_path):
        """旧版数据库（只有 6 列）应被自动补齐新列。"""
        import sqlite3

        old_db = tmp_path / "old.db"
        with sqlite3.connect(old_db) as conn:
            conn.execute(
                """
                CREATE TABLE news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT, url TEXT, time TEXT, content TEXT, source TEXT
                )
                """
            )

        database.init_db(old_db)

        with sqlite3.connect(old_db) as conn:
            columns = {
                row[1] for row in conn.execute("PRAGMA table_info(news)")
            }
        assert {"summary", "importance", "category", "keywords"} <= columns
