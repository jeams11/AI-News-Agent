import sqlite3
from datetime import datetime
from flask import Flask, render_template, jsonify
import os

# 创建Flask应用
# Flask负责接收浏览器请求，并返回网页内容
app = Flask(__name__)

# 获取当前app.py所在目录
# 这样无论从哪里启动程序，都能正确找到数据库
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 拼接数据库完整路径
# 当前文件:
# web/app.py
#
# 数据库:
# data/news.db
DB_PATH = os.path.join(BASE_DIR, "../data/news.db")


def get_news():
    # 创建数据库连接
    # SQLite不需要额外服务器，直接操作文件即可
    conn = sqlite3.connect(DB_PATH)

    # 设置返回格式
    # 开启后可以使用:
    # item["title"]
    # 而不是:
    # item[0]
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # 查询新闻数据
    #
    # summary不为空:
    # 代表这条新闻已经经过AI分析
    #
    # CAST(importance AS INTEGER):
    # 把数据库里的评分字符串转换成数字
    # 方便按照5、4、3星排序
    cursor.execute("""
        SELECT
            title,
            source,
            category,
            importance,
            keywords,
            summary
        FROM news
        WHERE summary IS NOT NULL
        ORDER BY CAST(importance AS INTEGER) DESC
        LIMIT 50
    """)

    news = cursor.fetchall()

    # 关闭数据库连接
    # 避免长期运行时占用数据库资源
    conn.close()

    return news


def get_stats():
    # 获取首页需要显示的统计数据
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # 新闻总数量
    cursor.execute(
        "SELECT COUNT(*) FROM news"
    )
    total = cursor.fetchone()[0]

    # 已经完成AI分析的数量
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM news
        WHERE summary IS NOT NULL
        """
    )
    analyzed = cursor.fetchone()[0]

    # 重要新闻数量
    # importance 4和5代表高价值新闻
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM news
        WHERE CAST(importance AS INTEGER)>=4
        """
    )
    important = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "analyzed": analyzed,
        "important": important
    }



@app.route("/")
def index():
    # 获取新闻列表
    news = get_news()

    # 获取统计数据
    stats = get_stats()

    # 将数据发送给HTML模板
    return render_template(
        "index.html",
        news=news,
        stats=stats,
        time=datetime.now()
    )



@app.route("/api")
def api():
    # 简单接口，用于检测服务是否正常
    return jsonify(
        {
            "status":"running",
            "message":"AI News Agent API"
        }
    )



if __name__=="__main__":
    # Flask启动入口
    # host允许局域网访问
    # port指定8000端口
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )
