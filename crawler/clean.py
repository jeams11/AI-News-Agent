import json
import os


# 项目根目录
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# 原始新闻文件
INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "bbc_full.json"
)


# 清洗后的文件
OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "bbc_clean.json"
)



# 低质量标题关键词
# 如果标题包含这些词，则认为价值较低
BAD_WORDS = [
    "点击",
    "免费下载",
    "下载",
    "直播",
    "即时更新",
    "图片",
    "海报",
    "视频",
    "图库",
    "合集",
    "专题入口"
]



def is_valid(title):
    """
    判断新闻标题是否值得保留

    返回:
    True  保留
    False 删除
    """


    if not title:
        return False


    # 标题过短通常没有新闻价值
    if len(title) < 8:
        return False


    # 检查垃圾关键词
    for word in BAD_WORDS:

        if word in title:

            return False


    return True



def clean_news():

    # 读取原始数据
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        news = json.load(f)



    result = []


    # 遍历新闻
    for item in news:


        title = item.get(
            "title",
            ""
        )


        # 通过过滤才保存
        if is_valid(title):

            result.append(item)



    # 保存结果
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2
        )



    print(
        "原始数量:",
        len(news)
    )


    print(
        "过滤后:",
        len(result)
    )



if __name__ == "__main__":

    clean_news()
