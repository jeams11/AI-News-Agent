from playwright.sync_api import sync_playwright


url = "https://www.bbc.com/zhongwen/articles/c1jy6kjn762o/trad"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        url,
        wait_until="networkidle"
    )

    text = page.locator("body").inner_text()

    print(text[:1000])

    browser.close()
