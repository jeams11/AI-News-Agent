import sqlite3
import json
import os
from opencc import OpenCC


# 繁体转简体
cc = OpenCC("t2s")


BASE_DIR = "/Users/james/AI-News-Agent"

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


DB_PATH = os.path.join(
    DATA_DIR,
    "news.db"
)


BBC_JSON = os.path.join(
    DATA_DIR,
    "bbc_clean.json"
)


AIBASE_JSON = os.path.join(
    DATA_DIR,
    "aibase_full.json"
)



def init_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        url TEXT,

        time TEXT,

        content TEXT,

        source TEXT
    )
    """)


    conn.commit()
    conn.close()


    print("数据库初始化完成")
    print(DB_PATH)




def insert_news(item, source):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    title = cc.convert(
        item.get("title", "")
    )


    content = cc.convert(
        item.get("content", "")
    )


    cursor.execute(
        """
        INSERT INTO news
        (
            title,
            url,
            time,
            content,
            source
        )
        VALUES
        (?,?,?,?,?)
        """,
        (
            title,

            item.get("url",""),

            item.get("time",""),

            content,

            source
        )
    )


    conn.commit()

    conn.close()




def import_json():

    total = 0



    # BBC

    if os.path.exists(BBC_JSON):

        with open(
            BBC_JSON,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        for item in data:

            insert_news(
                item,
                "BBC"
            )

            total += 1




    # AIBase

    if os.path.exists(AIBASE_JSON):

        with open(
            AIBASE_JSON,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        for item in data:

            insert_news(
                item,
                "AIBase"
            )

            total += 1



    print(
        f"新闻数据导入完成，共 {total} 条"
    )




if __name__ == "__main__":

    init_database()

    import_json()
