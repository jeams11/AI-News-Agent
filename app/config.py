"""全局配置模块。

所有配置从环境变量 / 项目根目录的 .env 文件读取，
其余模块只从这里获取配置，不允许散落硬编码。
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- LLM（OpenAI 兼容接口：Ollama / DeepSeek / 通义千问 均可）----
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"
    llm_model: str = "qwen2.5:7b"
    llm_timeout_seconds: int = 300
    # 每轮 AI 分析最多处理的新闻条数
    llm_batch_size: int = 10

    # ---- Web 服务 ----
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # ---- 定时任务 ----
    enable_scheduler: bool = True
    crawl_interval_minutes: int = 60
    summary_interval_minutes: int = 720

    # ---- 爬虫 ----
    bbc_max_articles: int = 20
    aibase_max_articles: int = 30
    request_timeout_seconds: int = 20

    # ---- 数据存储 ----
    data_dir: Path = BASE_DIR / "data"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "news.db"

    @property
    def report_path(self) -> Path:
        return self.data_dir / "news_report.md"


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
