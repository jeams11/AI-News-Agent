# [Bug] news 表无唯一约束，定时任务导致重复数据无限累积

## 问题描述

有两条互相独立的入库路径，且都没有去重保护：

1. `crawler/db_save.py` 通过捕获 `sqlite3.IntegrityError` 来「跳过重复」，但 `news` 表的 `url` 列没有任何 UNIQUE 约束，这个异常永远不会触发，同一条新闻每次爬取都会重复插入。
2. `crawler/database.py` 的 `import_json()` 会把 `bbc_clean.json` / `aibase_full.json` 里的所有记录无条件 INSERT。`scheduler.py` 每小时执行一次 `database.py`，即使 JSON 文件没有更新，也会把同一批旧数据再插一遍。

结果：数据库以每小时几十条的速度膨胀，全是重复数据，Web 页面和 AI 总结都会重复处理同一条新闻（AI 总结还会重复消耗模型算力）。

## 复现

```bash
python crawler/database.py   # 第一次导入，例如 60 条
python crawler/database.py   # 再跑一次，变成 120 条，全是重复
```

## 建议修复

1. 建表时加约束：`url TEXT UNIQUE`。
2. 插入用 `INSERT OR IGNORE`（或先 `SELECT` 判断），让 `db_save.py` 的去重逻辑真正生效：

```sql
INSERT OR IGNORE INTO news (title, url, source, time) VALUES (?, ?, ?, ?)
```

3. 统一入库路径：爬虫直接写库，或统一走 JSON 导入，二选一，避免同一条新闻从两条路径入库两次。
