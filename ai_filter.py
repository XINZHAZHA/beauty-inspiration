"""
智谱GLM AI筛选器
将采集的原始内容发送给智谱GLM，筛选出10条最佳选题灵感
"""
import json
import os
import requests
from config.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from config.settings import MAX_INSPIRATIONS, CATEGORY_QUOTAS


ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_MODEL = "glm-4-flash"  # 免费额度可用


def get_api_key() -> str:
    """获取智谱API Key，优先从环境变量读取"""
    return os.environ.get("ZHIPU_API_KEY", "")


def filter_inspirations(raw_contents: list[dict]) -> list[dict]:
    """
    将原始采集内容发送给智谱GLM筛选
    返回10条精选灵感，JSON格式
    """
    api_key = get_api_key()
    if not api_key:
        print("[AI] 未设置 ZHIPU_API_KEY，跳过筛选")
        return []

    # 将原始内容格式化为文本
    raw_text = _format_raw_contents(raw_contents)

    # 构造 prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(raw_content=raw_text)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": ZHIPU_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
    }

    try:
        resp = requests.post(ZHIPU_API_URL, json=payload, headers=headers, timeout=60)
        data = resp.json()

        if "choices" not in data:
            print(f"[AI] API 错误: {data}")
            return []

        content = data["choices"][0]["message"]["content"]

        # 解析 JSON 输出
        inspirations = _parse_json_response(content)
        print(f"[AI] 成功筛选 {len(inspirations)} 条灵感")
        return inspirations

    except Exception as e:
        print(f"[AI] 筛选失败: {e}")
        return []


def _format_raw_contents(contents: list[dict]) -> str:
    """将采集内容格式化为纯文本"""
    lines = []
    for i, item in enumerate(contents, 1):
        lines.append(f"[{i}] {item.get('source_platform', '未知')}")
        lines.append(f"    标题: {item.get('title', '')}")
        lines.append(f"    内容: {item.get('content', '')[:200]}")
        lines.append(f"    链接: {item.get('source_link', '')}")
        lines.append(f"    时间: {item.get('source_time', '')}")
        lines.append(f"    热度: {item.get('heat_data', '')}")
        lines.append("")
    return "\n".join(lines)


def _parse_json_response(text: str) -> list[dict]:
    """从 AI 回复中提取 JSON 数组"""
    # 尝试找到 JSON 数组
    try:
        # 找到第一个 [ 和最后一个 ]
        start = text.find("[")
        end = text.rfind("]") + 1
        if start >= 0 and end > start:
            json_str = text[start:end]
            return json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[AI] JSON 解析失败: {e}")
        print(f"[AI] 原始输出: {text[:500]}")

    return []
