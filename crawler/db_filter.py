import sqlite3
import os


# 获取项目根目录
# 当前文件:
# AI-News-Agent/crawler/db_filter.py
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# 数据库位置
DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "news.db"
)


# 低质量新闻关键词
# 标题包含这些词时，认为价值较低
BAD_WORDS = [
    "点击",
    "免费下载",
    "下载",
    "直播",
    "即时更新",
    "海报",
    "图片",
    "图库",
    "视频",
    "专题入口",
    "点击这里",
    "一图看懂"
]



def is_low_quality(title):
    """
    判断新闻是否低质量

    返回:
    True  删除
    False 保留
    """

    if not title:
        return True


    # 标题过短
    if len(title) < 8:
        return True


    # 检查关键词
    for word in BAD_WORDS:

        if word in title:

            return True


    return False



def filter_news():

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # 获取所有新闻
    cursor.execute(
        """
        SELECT id,title
        FROM news
        """
    )


    rows = cursor.fetchall()


    delete_ids = []


    # 检查每条新闻
    for news_id, title in rows:


        if is_low_quality(title):

            delete_ids.append(news_id)

            print(
                "删除:",
                title
            )


    # 执行删除
    for news_id in delete_ids:

        cursor.execute(
            """
            DELETE FROM news
            WHERE id=?
            """,
            (news_id,)
        )


    conn.commit()

    conn.close()


    print()
    print(
        "原始数量:",
        len(rows)
    )

    print(
        "删除数量:",
        len(delete_ids)
    )

    print(
        "剩余数量:",
        len(rows)-len(delete_ids)
    )



if __name__ == "__main__":

    filter_news()
