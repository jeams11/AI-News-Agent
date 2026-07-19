import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

from db_save import save_news


# BBC中文新闻专题页面
URL = "https://www.bbc.com/zhongwen/topics/cpydz218gddt/trad"


# 请求头，模拟浏览器访问，避免部分网站拒绝爬虫请求
HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}


# JSON数据保存路径
DATA_PATH = "../data/bbc.json"



# 获取BBC新闻列表
def get_news():

    print("正在抓取 BBC...")


    # 请求BBC专题页面
    # timeout限制请求时间，避免网络异常导致程序一直等待
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )


    # 设置网页编码，避免中文乱码
    response.encoding = "utf-8"


    # 使用BeautifulSoup解析HTML页面
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # 保存新闻数据
    news_list = []


    # 获取页面中所有带链接的a标签
    links = soup.find_all(
        "a",
        href=True
    )


    # 用于保存已经出现过的新闻链接
    # 防止同一篇新闻重复保存
    seen = set()


    # 遍历所有链接
    for item in links:


        # 获取新闻标题
        title = item.get_text(
            strip=True
        )


        # 获取新闻URL
        link = item["href"]


        # 没有标题的数据跳过
        if not title:
            continue


        # 过滤掉非BBC中文新闻链接
        if "/zhongwen/" not in link:
            continue


        # BBC部分链接是相对地址
        # 转换为完整URL
        if link.startswith("/"):
            link = "https://www.bbc.com" + link


        # 如果链接已经存在，跳过
        if link in seen:
            continue


        # 保存已经处理过的链接
        seen.add(link)


        # 获取当前抓取时间
        now = str(
            datetime.datetime.now()
        )


        # 创建新闻数据结构
        data = {
            "title": title,
            "url": link,
            "time": now
        }


        # 添加到新闻列表
        news_list.append(data)



        # 同时保存到SQLite数据库
        # 后续AI总结和网页展示都会读取数据库
        save_news(
            title,
            link,
            "BBC",
            now
        )


    return news_list




# 保存新闻JSON文件
def save_json(data):


    # 如果data目录不存在则自动创建
    os.makedirs(
        "../data",
        exist_ok=True
    )


    # 写入JSON文件
    # ensure_ascii=False保证中文正常显示
    # indent=2方便人工查看
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




# 程序入口
# 直接运行bbc.py时执行
# 被其他文件调用时不会执行
if __name__ == "__main__":


    # 开始抓取BBC新闻
    news = get_news()


    # 保存JSON备份文件
    save_json(news)


    # 输出抓取结果数量
    print(
        "BBC抓取数量:",
        len(news)
    )
