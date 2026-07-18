import json


bbc_file = "../data/bbc_clean.json"
aibase_file = "../data/aibase_clean.json"

output_file = "../data/all_news.json"



# 读取BBC
with open(bbc_file, "r", encoding="utf-8") as f:
    bbc = json.load(f)



# 读取AIBase
with open(aibase_file, "r", encoding="utf-8") as f:
    aibase = json.load(f)



# 合并
all_news = bbc + aibase



# 保存
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        all_news,
        f,
        ensure_ascii=False,
        indent=2
    )


print("合并完成")
print("BBC数量:", len(bbc))
print("AIBase数量:", len(aibase))
print("总数量:", len(all_news))
print("保存:", output_file)

