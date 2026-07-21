import pytest
from fastapi.testclient import TestClient

from app import database
from app.config import settings
from app.main import app


@pytest.fixture()
def client():
    # lifespan 会在 settings.db_path（临时目录）上建表
    with TestClient(app) as test_client:
        yield test_client
    # 清空测试数据，保持用例隔离
    with database.get_connection() as conn:
        conn.execute("DELETE FROM news")


@pytest.fixture()
def seeded(client, sample_articles):
    database.insert_news(sample_articles)
    return sample_articles


class TestHealth:
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestNewsApi:
    def test_empty_list(self, client):
        body = client.get("/api/news").json()
        assert body["success"] is True
        assert body["data"] == []
        assert body["meta"]["total"] == 0

    def test_list_news(self, seeded, client):
        body = client.get("/api/news").json()
        assert body["meta"]["total"] == 2
        assert len(body["data"]) == 2

    def test_filter_by_source(self, seeded, client):
        body = client.get("/api/news", params={"source": "BBC"}).json()
        assert body["meta"]["total"] == 1
        assert body["data"][0]["source"] == "BBC"

    def test_get_by_id(self, seeded, client):
        news_id = client.get("/api/news").json()["data"][0]["id"]
        body = client.get(f"/api/news/{news_id}").json()
        assert body["success"] is True
        assert body["data"]["id"] == news_id

    def test_get_missing_returns_404(self, client):
        assert client.get("/api/news/99999").status_code == 404

    def test_invalid_params_rejected(self, client):
        assert client.get("/api/news", params={"page": 0}).status_code == 422
        assert (
            client.get("/api/news", params={"min_importance": 9}).status_code
            == 422
        )


class TestStats:
    def test_stats(self, seeded, client):
        body = client.get("/api/stats").json()
        assert body["data"]["total"] == 2
        assert body["data"]["sources"] == {"AIBase": 1, "BBC": 1}


class TestReport:
    def test_report_404_when_missing(self, client):
        settings.report_path.unlink(missing_ok=True)
        assert client.get("/api/report").status_code == 404

    def test_report_returns_markdown(self, seeded, client):
        from app.services.report import generate_report

        generate_report()
        response = client.get("/api/report")
        assert response.status_code == 200
        assert "AI 新闻日报" in response.text


class TestDashboard:
    def test_index_renders(self, seeded, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "AI News Agent" in response.text
