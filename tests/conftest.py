"""测试全局配置：必须在导入 app 之前设置环境变量。"""

import os
import tempfile

# 测试数据写入临时目录，且不启动调度器
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="ai-news-test-")
os.environ["ENABLE_SCHEDULER"] = "false"

import pytest

from app import database


@pytest.fixture()
def db_path(tmp_path):
    """每个测试用例独立的临时数据库。"""
    path = tmp_path / "test.db"
    database.init_db(path)
    return path


@pytest.fixture()
def sample_articles():
    return [
        {
            "title": "OpenAI 发布新一代模型",
            "url": "https://example.com/news/1",
            "source": "AIBase",
            "content": "这是一条测试新闻的正文内容。" * 10,
        },
        {
            "title": "某公司宣布重大人工智能合作计划",
            "url": "https://example.com/news/2",
            "source": "BBC",
            "content": "这是另一条测试新闻的正文内容。" * 10,
        },
    ]
