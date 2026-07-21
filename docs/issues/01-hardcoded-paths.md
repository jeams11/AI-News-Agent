# [Bug] 硬编码绝对路径导致项目无法在其他机器运行

## 问题描述

项目中多处硬编码了开发者本机的绝对路径，其他人克隆后无法直接运行：

- `scheduler.py:6`：`BASE_DIR = "/Users/james/AI-News-Agent"`
- `crawler/database.py:11`：`BASE_DIR = "/Users/james/AI-News-Agent"`

另外大量脚本使用 `../data/xxx.json` 这种相对路径（如 `crawler/bbc.py`、`crawler/db_save.py`、`crawler/api.py`），必须先 `cd crawler` 才能运行，从项目根目录执行会报 `FileNotFoundError`，也无法被调度器或 Docker 可靠调用。

## 复现

```bash
git clone https://github.com/jeams11/AI-News-Agent.git
cd AI-News-Agent
python scheduler.py   # 路径 /Users/james/AI-News-Agent 不存在，所有子任务失败
python crawler/bbc.py # 相对路径 ../data 解析错误
```

## 建议修复

统一用 `__file__` 推导项目根目录（项目里 `crawler/db_filter.py` 和 `summary/summarize.py` 已经是这种正确写法，可以推广到所有文件）：

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
```

更进一步可以把路径收敛到一个 `config.py`，配合环境变量覆盖（见配置管理相关 issue）。
