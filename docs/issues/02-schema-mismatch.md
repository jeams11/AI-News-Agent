# [Bug] 数据库表结构缺少 summary/importance 等列，AI 总结与 Web 页面无法运行

## 问题描述

`crawler/database.py` 建表语句只创建了 6 列：

```sql
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, url TEXT, time TEXT, content TEXT, source TEXT
)
```

但下游代码全部依赖不存在的列：

- `summary/summarize.py:54`：`WHERE summary IS NULL`
- `summary/summarize.py:165`：`UPDATE news SET summary=?`
- `web/app.py:45`：`SELECT title, source, category, importance, keywords, summary ...`
- `crawler/api.py:64`：`SELECT ... summary FROM news`

按 README 的步骤跑完爬虫后，执行 AI 总结或打开 Web 页面会直接抛出：

```
sqlite3.OperationalError: no such column: summary
```

也就是说「爬取 → AI 分析 → Web 展示」这条主链路目前是断的。

## 建议修复

1. 在建表语句中补全所有需要的列：`summary`、`importance`（建议 INTEGER 类型，避免 `CAST(importance AS INTEGER)`）、`category`、`keywords`。
2. 建表逻辑收敛到一个模块（现在 `database.py` 和 `db_save.py` 各自假设了不同的表结构），所有读写共用。
3. 对已存在的旧库，可以用 `ALTER TABLE news ADD COLUMN ...` 做一次简单迁移。
