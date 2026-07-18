import json
import requests
from datetime import datetime


# ==========================
# 文件路径
# ==========================

input_file = "../data/all_news.json"

output_file = "../data/news_report.md"



# ==========================
# 读取新闻数据
# ==========================

with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:
    news = json.load(f)



# ==========================
# 构造新闻文本
# ==========================

news_text = ""


for i, item in enumerate(news[:30]):

    title = item.get(
        "title",
        "无标题"
    )

    content = item.get(
        "content",
        ""
    )

    source = item.get(
        "source",
        "未知来源"
    )


    # 如果没有正文，跳过
    if not content:
        continue


    news_text += f"""
新闻{i+1}

标题:
{title}

来源:
{source}

正文:
{content[:600]}

====================

"""



# ==========================
# 给模型的提示词
# ==========================

prompt = f"""
你是一名专业AI新闻编辑。

请根据下面新闻数据，生成一份中文AI新闻日报。


要求：

# 输出格式必须是 Markdown


结构：

# 今日AI新闻摘要


## 一、重点新闻

选择最重要的10条。


每条格式：

### 1. 新闻标题

**来源：**

**事件概述：**

**影响分析：**


## 二、行业趋势

总结今天AI行业出现的重要趋势。


## 三、值得关注

列出未来可能继续发展的方向。


注意：

- 不要编造新闻
- 只根据提供内容总结
- 保持客观


新闻数据：

{news_text}

"""



# ==========================
# 调用 Ollama
# ==========================

print("正在调用本地Qwen模型...")


response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False
    }
)



result = response.json().get(
    "response",
    ""
)



# ==========================
# 保存 Markdown
# ==========================

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("# AI新闻日报\n\n")

    f.write(
        "生成时间: "
        +
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        +
        "\n\n"
    )

    f.write(result)



print("======================")
print("生成完成")
print("文件:")
print(output_file)
print("======================")
