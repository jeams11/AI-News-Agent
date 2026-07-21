"""AI 新闻分析：通过 OpenAI 兼容接口调用 LLM。

base_url 可配置，同一套代码支持：
- Ollama 本地模型（http://localhost:11434/v1）
- DeepSeek（https://api.deepseek.com）
- 通义千问（https://dashscope.aliyuncs.com/compatible-mode/v1）
"""

import json
import logging

from openai import OpenAI, OpenAIError

from app.config import settings

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = """你是一名专业新闻分析师。请分析下面这条新闻：

标题：{title}

正文：
{content}

请严格输出一个 JSON 对象（不要输出任何其他文字、不要用 Markdown 代码块），格式如下：
{{
  "summary": "2-4句话的新闻分析，包含核心内容、背景原因和可能影响",
  "importance": 3,
  "category": "新闻分类，如：人工智能/国际/科技/财经/社会",
  "keywords": ["关键词1", "关键词2", "关键词3"]
}}

要求：
1. 使用简体中文；
2. importance 是 1-5 的整数，5 表示最重要；
3. keywords 为 3-5 个关键词；
4. 内容客观专业，不编造事实。"""

_MAX_CONTENT_CHARS = 4000


def _get_client() -> OpenAI:
    return OpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        timeout=settings.llm_timeout_seconds,
    )


def _parse_response(text: str) -> dict | None:
    """解析模型返回的 JSON，容忍代码块包裹等常见偏差。"""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    # 截取第一个 { 到最后一个 } 之间的内容
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        return None

    try:
        data = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError:
        return None

    summary = str(data.get("summary", "")).strip()
    if not summary:
        return None

    try:
        importance = int(data.get("importance", 3))
    except (TypeError, ValueError):
        importance = 3
    importance = max(1, min(5, importance))

    keywords = data.get("keywords", [])
    if isinstance(keywords, list):
        keywords = ", ".join(str(k) for k in keywords)

    return {
        "summary": summary,
        "importance": importance,
        "category": str(data.get("category", "未分类")).strip() or "未分类",
        "keywords": str(keywords).strip(),
    }


def analyze(title: str, content: str) -> dict | None:
    """分析一条新闻，失败时返回 None（下一轮任务会自动重试）。"""
    prompt = _PROMPT_TEMPLATE.format(
        title=title, content=(content or "")[:_MAX_CONTENT_CHARS]
    )

    try:
        response = _get_client().chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
    except OpenAIError as exc:
        logger.error("LLM 调用失败: %s", exc)
        return None

    text = response.choices[0].message.content or ""
    result = _parse_response(text)
    if result is None:
        logger.warning("LLM 返回内容无法解析: %.200s", text)
    return result
