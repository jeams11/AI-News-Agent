from app.services.summarizer import _parse_response


class TestParseResponse:
    def test_plain_json(self):
        text = (
            '{"summary": "测试摘要", "importance": 4,'
            ' "category": "人工智能", "keywords": ["AI", "模型"]}'
        )
        result = _parse_response(text)
        assert result == {
            "summary": "测试摘要",
            "importance": 4,
            "category": "人工智能",
            "keywords": "AI, 模型",
        }

    def test_json_in_code_fence(self):
        text = '```json\n{"summary": "摘要", "importance": 3, "category": "科技", "keywords": []}\n```'
        result = _parse_response(text)
        assert result is not None
        assert result["summary"] == "摘要"

    def test_json_with_surrounding_text(self):
        text = '好的，以下是分析结果：{"summary": "摘要", "importance": 2, "category": "财经", "keywords": ["经济"]}希望有帮助'
        result = _parse_response(text)
        assert result is not None
        assert result["category"] == "财经"

    def test_importance_clamped_to_range(self):
        result = _parse_response('{"summary": "a", "importance": 99}')
        assert result["importance"] == 5

        result = _parse_response('{"summary": "a", "importance": -1}')
        assert result["importance"] == 1

    def test_invalid_importance_defaults_to_3(self):
        result = _parse_response('{"summary": "a", "importance": "很重要"}')
        assert result["importance"] == 3

    def test_missing_summary_returns_none(self):
        assert _parse_response('{"importance": 3}') is None

    def test_garbage_returns_none(self):
        assert _parse_response("模型输出了一段无法解析的文字") is None
        assert _parse_response("") is None
