import sqlite3


DB_PATH = "../data/news.db"


def save_news(title, url, source, time):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    try:

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

        print("重复跳过:", title)


    finally:

        conn.close()
