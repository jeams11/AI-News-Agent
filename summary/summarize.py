import sqlite3
import requests
import os
from datetime import datetime


# 获取项目根目录
# 当前文件:
# AI-News-Agent/summary/summarize.py
#
# dirname一次:
# AI-News-Agent/summary
#
# dirname两次:
# AI-News-Agent
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# 数据库路径
# AI-News-Agent/data/news.db
DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "news.db"
)


# Ollama接口
# 本地Qwen模型通过此地址调用
OLLAMA_URL = "http://localhost:11434/api/generate"


# 使用模型
MODEL = "qwen2.5:7b"



def get_news():
    """
    获取还没有AI分析的新闻

    summary为空:
    表示该新闻还没有处理
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            content

        FROM news

        WHERE summary IS NULL

        LIMIT 10
    """)

    data = cursor.fetchall()

    conn.close()

    return data



def summarize(content):
    """
    调用Qwen生成新闻分析
    """


    prompt = f"""
你是一名专业新闻分析师。

请分析下面新闻：

{content}

请严格按照以下格式输出：

【核心内容】
用2-3句话总结新闻发生了什么。

【背后原因】
分析事件发生的背景和主要原因。

【影响分析】
分析该事件可能带来的影响。

【关键词】
列出3-5个重要关键词，用逗号分隔。

要求：
1. 使用简体中文。
2. 内容客观专业。
3. 不重复新闻标题。
4. 不输出额外说明。
"""


    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }


    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )


        result = response.json()


        if "response" in result:

            return result["response"]


        print("Ollama返回异常:")
        print(result)

        return "总结失败"


    except Exception as e:

        print(
            "调用模型失败:",
            e
        )

        return "总结失败"



def save_summary(news_id, summary):
    """
    保存AI生成结果
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE news

        SET summary=?

        WHERE id=?
        """,
        (
            summary,
            news_id
        )
    )


    conn.commit()

    conn.close()



def create_report():
    """
    生成Markdown日报
    """

    report_path = os.path.join(
        BASE_DIR,
        "data",
        "news_report.md"
    )


    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            title,
            summary

        FROM news

        WHERE summary IS NOT NULL

        ORDER BY id DESC
    """)


    rows = cursor.fetchall()

    conn.close()



    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "# AI新闻日报\n\n"
        )

        f.write(
            "生成时间: "
            +
            str(datetime.now())
            +
            "\n\n"
        )


        for i, item in enumerate(rows, 1):

            f.write(
                f"## {i}. {item[0]}\n\n"
            )

            f.write(
                item[1]
                +
                "\n\n"
            )



def main():

    news = get_news()


    print(
        "待总结数量:",
        len(news)
    )


    for item in news:

        news_id, title, content = item


        print("\n正在总结:")
        print(title)


        result = summarize(content)


        save_summary(
            news_id,
            result
        )


    create_report()


    print(
        "\n完成，已生成 news_report.md"
    )



if __name__ == "__main__":

    main()
