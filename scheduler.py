import schedule
import time
import subprocess
import os
from datetime import datetime
BASE_DIR = "/Users/james/AI-News-Agent"
CRAWLER_DIR = os.path.join(BASE_DIR, "crawler")
SUMMARY_DIR = os.path.join(BASE_DIR, "summary")

def run_command(command, workdir):

    print(
        f"\n[{datetime.now()}] 执行任务: {command}"
    )

    subprocess.run(
        command,
        shell=True,
        cwd=workdir
    )

# 每小时执行新闻采集任务
def crawl_news():

    print("\n开始抓取新闻...")

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

# 每12小时执行AI总结任务
def generate_summary():

    print("\n开始AI总结...")

    run_command(
        "python summarize.py",
        SUMMARY_DIR
    )

    print("AI日报生成完成")



# 设置定时任务
schedule.every(1).hours.do(crawl_news)

schedule.every(12).hours.do(generate_summary)

print(
"""
AI News Agent Scheduler

任务:
- 每小时:
  新闻抓取 + 数据库更新

- 每12小时:
  Qwen AI总结 + Markdown日报

启动成功
"""
)

# 持续监听任务
while True:

    schedule.run_pending()

    time.sleep(30)

    time.sleep(30)
