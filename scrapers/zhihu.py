"""
知乎热榜采集器
采集知乎护肤、美妆相关热门话题
"""
import requests
import json


BEAUTY_TOPICS = [
    "护肤", "美白", "化妆品", "防晒", "面膜", "成分",
]


def scrape_zhihu() -> list[dict]:
    """采集知乎热榜美妆相关话题"""
    results = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # 知乎热榜 API
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        items = data.get("data", [])
        for item in items:
            target = item.get("target", {})
            title = target.get("title", "")
            # 检查是否美妆护肤相关
            if any(kw in title for kw in BEAUTY_TOPICS):
                qid = target.get("id", "")
                results.append({
                    "source_platform": "知乎",
                    "source_account": "知乎热榜",
                    "source_link": f"https://www.zhihu.com/question/{qid}",
                    "source_time": "",
                    "title": title[:100],
                    "content": target.get("excerpt", title)[:200],
                    "heat_data": f"知乎热榜",
                })
    except Exception as e:
        print(f"[Zhihu] 采集失败: {e}")

    return results
