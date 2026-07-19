from playwright.sync_api import sync_playwright

# 测试Playwright浏览器控制是否正常
with sync_playwright() as p:

    # 启动Chromium浏览器
    # headless=False表示显示浏览器窗口，方便调试
    browser = p.chromium.launch(headless=False)

    # 创建浏览器页面
    page = browser.new_page()

    # 打开BBC中文页面
    page.goto(
        "https://www.bbc.com/zhongwen"
    )

    # 输出网页标题，用于确认页面加载成功
    print(page.title())

    # 关闭浏览器释放资源
    browser.close()
