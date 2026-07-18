from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="AI News Agent API",
    description="AI新闻自动采集分析系统",
    version="1.0"
)


DB_PATH = "../data/news.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI News Agent API"
    }



@app.get("/news")
def get_news():

    conn = get_db()

    cursor = conn.cursor()

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


    rows = cursor.fetchall()

    conn.close()


    news=[]

    for row in rows:
        news.append({
            "id":row["id"],
            "title":row["title"],
            "url":row["url"],
            "source":row["source"],
            "time":row["time"],
            "content":row["content"],
            "summary":row["summary"]
        })


    return {
        "count":len(news),
        "data":news
    }
