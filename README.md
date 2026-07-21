# AI-News-Agent

基于大语言模型（LLM）的智能新闻自动化系统。

自动爬取新闻 → AI 分析（摘要 / 重要程度 / 分类 / 关键词）→ Web 仪表盘与 REST API → Markdown 日报，全流程自动运行。

## 功能

- **新闻采集**：BBC 中文（requests + BeautifulSoup）、AIBase（Playwright 处理 JS 渲染页面），自动繁转简、去重、低质量内容过滤
- **AI 分析**：通过 OpenAI 兼容接口调用任意 LLM（Ollama 本地模型 / DeepSeek / 通义千问），生成摘要、1-5 星重要程度、分类和关键词
- **Web 仪表盘**：新闻浏览页面 + 完整 REST API（自带 Swagger 文档 `/docs`）
- **定时任务**：内置调度器，默认每小时爬取、每 12 小时 AI 分析并生成日报
- **一键部署**：Docker Compose 单命令启动，数据持久化到宿主机

## 快速开始（Docker，推荐）

```bash
git clone https://github.com/jeams11/AI-News-Agent.git
cd AI-News-Agent

# 1. 创建配置文件并按需修改（LLM 地址、密钥、端口等）
cp .env.example .env

# 2. 一键启动
docker compose up -d --build

# 3. 打开仪表盘
open http://localhost:8000
```

数据库和日报保存在宿主机 `./data/` 目录，容器重建不丢数据。

### 搭配本地 Ollama（可选）

```bash
docker compose --profile ollama up -d --build
docker exec ai-news-ollama ollama pull qwen2.5:7b
```

并在 `.env` 中设置：

```dotenv
LLM_BASE_URL=http://ollama:11434/v1
```

## 本地开发运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium

cp .env.example .env
python -m app.main          # 启动服务（含定时任务）
pytest                      # 运行测试
```

## 配置（.env）

所有配置通过环境变量 / `.env` 文件管理，完整说明见 [.env.example](.env.example)。常用项：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI 兼容接口地址（Ollama / DeepSeek / 通义千问） |
| `LLM_API_KEY` | `ollama` | API 密钥（本地 Ollama 随意填写） |
| `LLM_MODEL` | `qwen2.5:7b` | 模型名称 |
| `API_PORT` | `8000` | Web 服务端口 |
| `ENABLE_SCHEDULER` | `true` | 是否启用内置定时任务 |
| `CRAWL_INTERVAL_MINUTES` | `60` | 爬取间隔（分钟） |
| `SUMMARY_INTERVAL_MINUTES` | `720` | AI 分析间隔（分钟） |

`.env` 已加入 `.gitignore`，密钥不会被提交。

## API

启动后访问 `http://localhost:8000/docs` 查看交互式 Swagger 文档。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/news` | 新闻列表（分页，支持 `source` / `category` / `min_importance` / `analyzed_only` 过滤） |
| GET | `/api/news/{id}` | 单条新闻详情（含正文） |
| GET | `/api/stats` | 数据统计 |
| GET | `/api/report` | 最新 Markdown 日报 |
| POST | `/api/tasks/crawl` | 手动触发一轮爬取 |
| POST | `/api/tasks/summarize` | 手动触发一轮 AI 分析 |

统一响应格式：

```json
{"success": true, "data": [...], "error": null, "meta": {"total": 100, "page": 1, "limit": 20}}
```

## 项目结构

```text
AI-News-Agent
├── app/
│   ├── config.py            # 全局配置（.env 加载）
│   ├── database.py          # SQLite 数据层（去重、迁移）
│   ├── main.py              # FastAPI 入口
│   ├── api.py               # REST API 路由
│   ├── scheduler.py         # APScheduler 定时任务
│   ├── crawlers/
│   │   ├── bbc.py           # BBC 中文爬虫
│   │   └── aibase.py        # AIBase 爬虫（Playwright）
│   ├── services/
│   │   ├── cleaner.py       # 低质量内容过滤
│   │   ├── summarizer.py    # LLM 新闻分析
│   │   ├── report.py        # Markdown 日报生成
│   │   └── pipeline.py      # 任务流水线编排
│   └── templates/index.html # 仪表盘页面
├── tests/                   # pytest 测试
├── data/                    # 数据库与日报（运行时生成，不入库）
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.12+ | 核心语言 |
| FastAPI + Uvicorn | Web 服务与 API |
| Playwright | 浏览器自动化（JS 渲染页面） |
| BeautifulSoup | HTML 解析 |
| SQLite | 数据存储 |
| OpenAI SDK | LLM 调用（兼容 Ollama / DeepSeek / 通义千问） |
| APScheduler | 定时任务 |
| Docker Compose | 一键部署 |

## License

MIT License
