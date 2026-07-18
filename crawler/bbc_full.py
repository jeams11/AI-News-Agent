from playwright.sync_api import sync_playwright
import json
import time


def get_article_content(page, url):

    page.goto(
        url,
        wait_until="networkidle"
    )

    time.sleep(2)

    text = page.locator(
        "body"
    ).inner_text()

    return text



with open(
    "../data/bbc.json",
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


    for index, article in enumerate(articles):

        print(
            "正在抓取:",
            index + 1,
            article["title"]
        )


        try:

            content = get_article_content(
                page,
                article["url"]
            )


            results.append(
                {
                    "title": article["title"],
                    "url": article["url"],
                    "content": content,
                    "time": article["time"]
                }
            )


        except Exception as e:

            print(
                "失败:",
                e
            )


    browser.close()



with open(
    "../data/bbc_full.json",
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
