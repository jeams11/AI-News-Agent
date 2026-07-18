from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time


# 读取 AIBase 新闻列表
with open(
    "../data/aibase.json",
    "r",
    encoding="utf-8"
) as f:
    articles = json.load(f)



results = []


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()


    for index, item in enumerate(articles):

        print(
            "正在抓取:",
            index + 1,
            item["title"][:40]
        )


        try:

            page.goto(
                item["url"],
                wait_until="networkidle",
                timeout=30000
            )


            html = page.content()


            soup = BeautifulSoup(
                html,
                "html.parser"
            )


            # 获取正文
            content = ""


            # AIBase正文区域
            article = soup.find(
                "article"
            )


            if article:

                content = article.get_text(
                    "\n",
                    strip=True
                )


            else:

                # 备用方案
                divs = soup.find_all(
                    "div"
                )

                texts = []

                for div in divs:

                    text = div.get_text(
                        strip=True
                    )

                    if len(text) > 200:

                        texts.append(text)


                if texts:

                    content = max(
                        texts,
                        key=len
                    )


            results.append(
                {
                    "title": item["title"],
                    "url": item["url"],
                    "content": content
                }
            )


            time.sleep(1)


        except Exception as e:

            print(
                "失败:",
                e
            )



    browser.close()



# 保存

with open(
    "../data/aibase_full.json",
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    "完成，共保存:",
    len(results)
)
