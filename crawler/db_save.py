import sqlite3

# SQLite数据库路径
DB_PATH = "../data/news.db"

# 保存新闻基础信息到数据库
def save_news(title, url, source, time):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    try:

        # 插入新闻数据
        cursor.execute(
            """
            INSERT INTO news
            (
            title,
            url,
            source,
            time
            )

            VALUES
            (?,?,?,?)
            """,

            (
                title,
                url,
                source,
                time
            )
        )

        conn.commit()

        print("新增:", title)

    except sqlite3.IntegrityError:

        # 数据库存在重复记录时跳过
        print("重复跳过:", title)

    finally:
        conn.close()
