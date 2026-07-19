# FastAPI 是一个现代化 Python Web 框架
# 用于快速创建 API 服务
from fastapi import FastAPI
    # Python 内置 SQLite 数据库模块
    # 用来读取 news.db 中的新闻数据
import sqlite3
    # 创建 FastAPI 应用实例
    # API 文档显示的项目名称
app = FastAPI(
    title="AI News Agent API",
    description="AI新闻自动采集分析系统",
    version="1.0"
)
DB_PATH = "../data/news.db"


# 创建数据库连接函数
# 每次 API 请求数据库时调用
def get_db():


    # 连接 SQLite 数据库
    conn = sqlite3.connect(DB_PATH)


    # 设置返回格式
    conn.row_factory = sqlite3.Row


    # 返回数据库连接
    return conn


# 检测 API 是否正常运行
@app.get("/")
def home():


    return {

        # 当前服务状态
        "status": "running",

        # 返回提示信息
        "message": "AI News Agent API"
    }



# 返回数据库中的新闻列表
@app.get("/news")
def get_news():


    # 创建数据库连接
    conn = get_db()


    # 创建 SQL 操作对象
    cursor = conn.cursor()


    # LIMIT 50 每次最多返回50条
    cursor.execute(
        """
        SELECT 
            id,
            title,
            url,
            source,
            time,
            content,
            summary
        FROM news
        ORDER BY id DESC
        LIMIT 50
        """
    )



    # 获取查询结果
    rows = cursor.fetchall()


    # 关闭数据库连接
    # 避免长期运行导致数据库占用
    conn.close()


    # 创建返回数据列表
    news = []


    # 遍历数据库结果
    for row in rows:


        # 将 SQLite 数据转换成 JSON 格式
        #
        # FastAPI 会自动转换为 JSON 返回给用户
        news.append({

            # 新闻ID
            "id": row["id"],


            # 新闻标题
            "title": row["title"],


            # 原文地址
            "url": row["url"],


            # 来源
            "source": row["source"],


            # 发布时间
            "time": row["time"],


            # 新闻正文
            "content": row["content"],


            # AI总结内容
            "summary": row["summary"]

        })

    # 返回 API 数据
    return {

        "count": len(news),

        "data": news
    }
