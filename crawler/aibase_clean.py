import json
import os
from datetime import datetime


# 数据文件位置
input_file = "../data/aibase_full.json"
output_file = "../data/aibase_clean.json"


# 读取原始数据
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)


clean_data = []


for item in data:

    title = item.get("title", "")
    url = item.get("url", "")
    content = item.get("content", "")


    # 去除空内容
    if not title or not url:
        continue


    # 去除导航类内容
    if title in [
        "首页",
        "AI资讯",
        "AI 产品库",
        "GEO 平台",
        "MCP 服务",
        "模型算力广场"
    ]:
        continue


    clean_item = {
        "title": title.strip(),
        "url": url.strip(),
        "content": content.strip(),
        "source": "AIBase",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


    clean_data.append(clean_item)



# 保存
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        clean_data,
        f,
        ensure_ascii=False,
        indent=2
    )


print("清洗完成:", len(clean_data))
print("保存位置:", output_file)
