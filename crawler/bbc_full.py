from playwright.sync_api import sync_playwright
import json
import time
# 获取单篇BBC新闻正文内容
def get_article_content(page, url):

    # 打开新闻页面
    # networkidle表示等待页面主要资源加载完成
    page.goto(
        url,
        wait_until="networkidle"
    )


    # 额外等待2秒
    # 防止部分JavaScript内容还没有完全渲染
    time.sleep(2)


    # 获取网页body中的全部文字
    # 当前版本会获取整个页面内容，包括导航等信息
    text = page.locator(
        "body"
    ).inner_text()


    return text

# 读取BBC新闻列表
# bbc.json由bbc.py生成，里面保存标题和URL
with open(
    "../data/bbc.json",
    "r",
    encoding="utf-8"
) as f:

    articles = json.load(f)

# 保存抓取完成的新闻正文
results = []

# 启动Playwright浏览器
with sync_playwright() as p:

    # 启动Chromium
    # headless=True表示后台运行
    browser = p.chromium.launch(
        headless=True
    )

    # 创建浏览页面
    # 后续循环复用这个页面，提高抓取效率
    page = browser.new_page()
    # 遍历所有新闻链接
    for index, article in enumerate(articles):


        # 显示当前抓取进度
        print(
            "正在抓取:",
            index + 1,
            article["title"]
        )



        try:


            # 获取新闻正文
            content = get_article_content(
                page,
                article["url"]
            )

            # 保存新闻完整数据
            results.append(
                {
                    "title": article["title"],
                    "url": article["url"],
                    "content": content,
                    "time": article["time"]
                }
            )

        except Exception as e:
            # 单篇新闻失败不影响后续任务
            print(
                "失败:",
                e
            )

    # 所有新闻完成后关闭浏览器
    browser.close()


# 保存包含正文的新闻数据
# bbc_full.json相比bbc.json多了:
# content 新闻正文
with open(
    "../data/bbc_full.json",
    "w",
    encoding="utf-8"
) as f:

    # 保存为JSON格式
    # ensure_ascii=False:
    # 保留中文
    # indent=2:
    # 方便查看
    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=2
    )



# 输出最终结果
print(
    "完成，共保存:",
    len(results)
)
