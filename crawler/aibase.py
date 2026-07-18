from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import datetime


url = "https://news.aibase.com/zh/news"


def crawl_aibase():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()


        page.goto(
            url,
            wait_until="networkidle"
        )


        html = page.content()


        browser.close()


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    articles = []


    for a in soup.find_all("a"):

        title = a.get_text(
            strip=True
        )

        link = a.get("href")


        if title and link:


            if "/zh/news/" in link:


                if link.startswith("/"):

                    link = "https://news.aibase.com" + link


                articles.append(
                    {
                        "title": title,
                        "url": link,
                        "time": str(datetime.datetime.now())
                    }
                )


    return articles[:30]



if __name__ == "__main__":


    data = crawl_aibase()


    print(
        "抓取数量:",
        len(data)
    )


    for item in data:

        print(
            item["title"]
        )

        print(
            item["url"]
        )


    with open(
        "../data/aibase.json",
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )
