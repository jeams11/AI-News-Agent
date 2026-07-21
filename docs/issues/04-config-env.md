# [Enhancement] 配置全部硬编码，建议引入 .env 环境变量管理

## 问题描述

所有配置分散硬编码在各个脚本里：

- `summary/summarize.py:34`：`OLLAMA_URL = "http://localhost:11434/api/generate"`、`MODEL = "qwen2.5:7b"`
- `crawler/summarize.py:126`：同一个 Ollama 地址和模型又硬编码了一遍
- `web/app.py:147`：端口 8000 硬编码
- `scheduler.py`：调度间隔（1 小时 / 12 小时）硬编码

存在的问题：

1. README 宣称支持 DeepSeek API / Qwen API / OpenAI Compatible API，`requirements.txt` 也安装了 `openai` SDK，但代码里实际只调用了本地 Ollama 的私有接口，两者不符。
2. `requirements.txt` 安装了 `python-dotenv`，但整个项目没有任何地方使用它，也没有 `.env.example`。
3. 换模型、换端口、换 API 地址都要改源码。

## 建议修复

1. 项目根目录增加 `.env.example`：

```dotenv
# LLM（OpenAI 兼容接口，Ollama/DeepSeek/Qwen 均可）
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=qwen2.5:7b

# Web
API_HOST=0.0.0.0
API_PORT=8000

# 调度
CRAWL_INTERVAL_MINUTES=60
SUMMARY_INTERVAL_MINUTES=720
```

2. 新增 `config.py`，用 `python-dotenv` 加载 `.env`，全项目只从这里读配置。
3. 用 `openai` SDK + 可配置的 `base_url` 调用模型：Ollama 本身提供 OpenAI 兼容端点（`/v1`），这样一套代码就能同时支持 Ollama、DeepSeek、通义千问，与 README 描述一致。
4. `.gitignore` 增加 `.env`，避免密钥被提交。
