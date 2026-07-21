# [Bug] 数据流水线各环节脱节：调度器缺少步骤、两套 Web 框架和两个 summarize 并存

## 问题描述

### 1. scheduler 调度的流水线是断的

`scheduler.py` 每小时只执行 `bbc.py → aibase.py → database.py`，但：

- `database.py` 导入的是 `bbc_clean.json` 和 `aibase_full.json`；
- `bbc_clean.json` 由 `bbc_full.py → clean.py` 生成，`aibase_full.json` 由 `data/aibase_full.py` 生成（这个脚本还放错了目录，在 `data/` 里）；
- 这些脚本**从未被调度器调用**。

结果：调度器每小时重复导入仓库里 commit 进来的旧 JSON 数据，新爬到的内容永远进不了正文抓取和清洗环节。

### 2. 两套 Web 框架并存

- `web/app.py` 用 Flask 提供页面 + `/api`
- `crawler/api.py` 用 FastAPI 提供 `/news`

功能重叠，`requirements.txt` 同时安装 flask + fastapi + uvicorn。README 技术栈只写了 FastAPI，建议保留一套（推荐 FastAPI，可同时渲染模板和提供 API 文档）。

### 3. 两个互相矛盾的 summarize.py

- `summary/summarize.py`：从数据库读，写回 `summary` 列（README 使用的是这个）
- `crawler/summarize.py`：从 `all_news.json` 读，直接生成 Markdown

两者模型调用代码重复，且后者 `requests.post` 没有设置 timeout，Ollama 卡住时脚本会永久挂起。

### 4. 其他

- `scheduler.py:83-85`：循环里连续两个 `time.sleep(30)`，应为笔误。
- `crawler/bbc_full.py`、`crawler/merge.py`、`data/aibase_full.py` 等脚本逻辑全部写在模块顶层，无法被 import 复用，只能靠 `cd` 到特定目录执行。
- 爬到的 `data/*.json` 数据文件被 commit 进了仓库，建议加入 `.gitignore`。

## 建议修复

1. 把「列表爬取 → 正文抓取 → 清洗 → 入库 → AI 分析 → 报告」整理成一个可以被 import 的 pipeline 模块，调度器直接调用函数而不是 `subprocess` 拉起脚本。
2. 删除重复实现（保留一个 Web 框架、一个 summarize 实现）。
3. 脚本逻辑包进 `main()` 函数 + `if __name__ == "__main__"`，配合绝对路径（见路径相关 issue）实现任意目录可执行。
