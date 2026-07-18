import schedule
import time
import subprocess
import os
from datetime import datetime


BASE_DIR = "/Users/james/AI-News-Agent"

CRAWLER_DIR = os.path.join(BASE_DIR, "crawler")
SUMMARY_DIR = os.path.join(BASE_DIR, "summary")


def run_command(command, workdir):
    print("\n==============================")
    print("执行:", command)
    print("时间:", datetime.now())
    print("==============================")

    subprocess.run(
        command,
        shell=True,
        cwd=workdir
    )


# 每小时抓取新闻
def crawl_news():

    print("开始抓取新闻...")

    run_command(
        "python bbc.py",
        CRAWLER_DIR
    )

    run_command(
        "python aibase.py",
        CRAWLER_DIR
    )

    run_command(
        "python database.py",
        CRAWLER_DIR
    )

    print("新闻抓取完成")


# 每12小时生成AI日报
def generate_summary():

    print("开始AI总结...")

    run_command(
        "python summarize.py",
        SUMMARY_DIR
    )

    print("AI日报生成完成")


# 每小时执行
schedule.every(1).hours.do(crawl_news)

# 每12小时执行
schedule.every(12).hours.do(generate_summary)


print("""
==============================
 AI News Agent Scheduler
==============================

任务:

1小时:
  新闻抓取 + 数据库更新

12小时:
  Qwen AI总结 + Markdown日报

启动成功...
==============================
""")


while True:

    schedule.run_pending()

    time.sleep(30)
