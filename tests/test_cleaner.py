from app.services.cleaner import clean_articles, is_valid_title


class TestIsValidTitle:
    def test_normal_title_is_valid(self):
        assert is_valid_title("OpenAI 发布新一代大语言模型产品")

    def test_empty_title_is_invalid(self):
        assert not is_valid_title("")
        assert not is_valid_title(None)

    def test_short_title_is_invalid(self):
        assert not is_valid_title("短标题")

    def test_bad_word_title_is_invalid(self):
        assert not is_valid_title("点击这里查看更多精彩内容")
        assert not is_valid_title("重大新闻事件现场视频直播中")


class TestCleanArticles:
    def test_filters_low_quality(self):
        articles = [
            {"title": "OpenAI 发布新一代大语言模型产品"},
            {"title": "点击免费下载"},
            {"title": "短"},
        ]
        result = clean_articles(articles)
        assert len(result) == 1
        assert result[0]["title"] == "OpenAI 发布新一代大语言模型产品"

    def test_does_not_mutate_input(self):
        articles = [{"title": "点击免费下载"}]
        clean_articles(articles)
        assert len(articles) == 1
