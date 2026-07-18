import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

from db_save import save_news


URL = "https://www.bbc.com/zhongwen/topics/cpydz218gddt/trad"


HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}


DATA_PATH = "../data/bbc.json"



def get_news():

    print("正在抓取 BBC...")


    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )


    response.encoding = "utf-8"


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    news_list = []


    links = soup.find_all(
        "a",
        href=True
    )


    seen = set()


    for item in links:


        title = item.get_text(
            strip=True
        )


        link = item["href"]


        if not title:
            continue


        if "/zhongwen/" not in link:
            continue


        if link.startswith("/"):
            link = "https://www.bbc.com" + link


        if link in seen:
            continue


        seen.add(link)


        now = str(
            datetime.datetime.now()
        )


        data = {

            "title": title,

            "url": link,

            "time": now

        }


        news_list.append(data)



        # 写入数据库
        save_news(

            title,

            link,

            "BBC",

            now

        )



    return news_list




def save_json(data):


    os.makedirs(
        "../data",
        exist_ok=True
    )


    with open(
        DATA_PATH,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=2

        )




if __name__ == "__main__":


    news = get_news()


    save_json(news)


    print(
        "BBC抓取数量:",
        len(news)
    )

