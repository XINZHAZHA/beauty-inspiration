"""
行业RSS采集器
从美妆行业媒体、海外美容资讯RSS源采集最新内容
"""
import feedparser
from datetime import datetime, timedelta
from config.settings import RSS_FEEDS


# 美妆护肤相关关键词过滤
BEAUTY_FILTER_KEYWORDS = [
    "skincare", "beauty", "sunscreen", "美白", "护肤", "防晒",
    "成分", "cosmetic", "serum", "moisturizer", "anti-aging",
    "抗老", "精华", "面霜", "retinol", "vitamin c", "niacinamide",
    "hyaluronic", "peptide", "sensitive", "acne", "痘痘",
    "cleanser", "toner", "essence", "makeup", "口红", "粉底",
    "化妆品", "护肤品", "面膜", "眼霜", "卸妆", "洁面",
]


def scrape_rss() -> list[dict]:
    """从RSS源采集最新美妆内容"""
    results = []
    cutoff = datetime.now() - timedelta(days=3)

    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                summary = entry.get("summary", "") or entry.get("description", "")

                # 过滤：标题或摘要包含美妆关键词
                combined = (title + " " + summary).lower()
                if not any(kw.lower() in combined for kw in BEAUTY_FILTER_KEYWORDS):
                    continue

                # 提取发布时间
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                time_str = ""
                if published:
                    try:
                        dt = datetime(*published[:6])
                        time_str = dt.strftime("%Y-%m-%d")
                    except:
                        pass

                results.append({
                    "source_platform": feed_info["name"],
                    "source_account": feed_info["name"],
                    "source_link": entry.get("link", ""),
                    "source_time": time_str,
                    "title": title[:100],
                    "content": _strip_html(summary)[:300],
                    "heat_data": "RSS来源",
                })
        except Exception as e:
            print(f"[RSS] {feed_info['name']} 采集失败: {e}")
            continue

    return results


def _strip_html(text: str) -> str:
    """简单去除HTML标签"""
    import re
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()
