from playwright.sync_api import sync_playwright
# BBC新闻文章地址
url = "https://www.bbc.com/zhongwen/articles/c1jy6kjn762o/trad"


# 启动Playwright浏览器环境
with sync_playwright() as p:

    # 启动Chromium，headless=True表示后台运行
    browser = p.chromium.launch(headless=True)

    # 创建浏览器页面
    page = browser.new_page()

    # 打开新闻页面，等待网络请求基本完成后再获取内容
    # BBC页面包含JavaScript动态加载内容，需要等待页面渲染完成
    page.goto(url, wait_until="networkidle")

    # 获取网页body中的全部可见文字
    text = page.locator("body").inner_text()

    # 打印前1000个字符，避免终端输出过长
    print(text[:1000])

    # 关闭浏览器释放资源
    browser.close()
