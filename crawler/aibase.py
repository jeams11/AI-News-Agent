# 使用 Playwright 控制浏览器，获取动态网页内容
from playwright.sync_api import sync_playwright

# 使用 BeautifulSoup 解析 HTML 页面
from bs4 import BeautifulSoup

# 用于保存 JSON
import json

# 当前时间
import datetime


# 页面
url = "https://news.aibase.com/zh/news"



# 爬取 aibase 新闻列表
def crawl_aibase():

    # 启动 Playwright
    # 模拟真实浏览器访问网页
    with sync_playwright() as p:


        # 启动 Chromium 浏览器
        # headless=True 表示后台运行，不显示浏览器窗口
        browser = p.chromium.launch(
            headless=True
        )


        # 创建一个新的浏览器页面
        page = browser.new_page()


        # 打开 Aibase 新闻页面
        # networkidle 表示等待网页网络请求基本完成
        # 避免页面内容还没有加载完成就开始解析
        page.goto(
            url,
            wait_until="networkidle"
        )


        # 获取浏览器渲染后的完整 HTML
        # 因为很多网站内容由 JavaScript 动态生成
        # 直接 requests 获取不到完整内容
        html = page.content()


        # 关闭浏览器，释放资源
        browser.close()



    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    # 保存新闻数据
    articles = []



    # 遍历页面中所有 a 标签
    # 新闻标题和链接通常都放在 <a href=""> 中
    for a in soup.find_all("a"):


        # 获取新闻标题
        # strip=True 会自动删除前后空格
        title = a.get_text(
            strip=True
        )


        # 获取新闻链接
        link = a.get("href")



        # 判断标题和链接是否存在
        # 防止空数据进入数据库
        if title and link:


            # Aibase 新闻详情页链接格式:
            # /zh/news/xxxx
            # 过滤掉无关链接
            if "/zh/news/" in link:

                
                # 相对路径转换成完整网址:
                # https://news.aibase.com/zh/news/123
                if link.startswith("/"):

                    link = "https://news.aibase.com" + link



                # 保存新闻信息
                articles.append(
                    {
                        # 新闻标题
                        "title": title,

                        # 新闻地址
                        "url": link,

                        # 抓取时间
                        "time": str(datetime.datetime.now())
                    }
                )



    # 只返回前30条新闻
    # 防止一次抓取过多数据
    return articles[:30]





# 程序入口
# 只有直接运行这个文件时才执行下面代码
# 被其他文件 import 时不会执行
if __name__ == "__main__":



    # 执行爬虫
    data = crawl_aibase()



    # 输出抓取数量
    print(
        "抓取数量:",
        len(data)
    )



    # 打印每条新闻标题和链接
    for item in data:


        print(
            item["title"]
        )


        print(
            item["url"]
        )



    # 保存数据到 JSON 文件
    # ../data/aibase.json
    #
    # 当前文件位置:
    # crawler/aibase.py
    #
    # 保存位置:
    # data/aibase.json
    with open(
        "../data/aibase.json",
        "w",
        encoding="utf-8"
    ) as f:
        # 将 Python 字典列表转换为 JSON
        # 保留中文，不转换成 Unicode 编码
        # 格式化输出，方便阅读
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )
