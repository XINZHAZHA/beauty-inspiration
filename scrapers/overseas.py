"""
海外美妆资讯采集器
从海外主流美妆媒体、Reddit社区采集最新趋势和成分资讯
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Google News RSS 美妆关键词搜索
NEWS_QUERIES = [
    "skincare ingredient",
    "cosmetic regulation",
    "beauty product launch",
    "sunscreen new research",
    "K-beauty trend",
    "retinol skincare",
    "vitamin C serum",
]


def scrape_overseas() -> list[dict]:
    """采集海外美妆资讯"""
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for query in NEWS_QUERIES:
        try:
            # 使用 Google News RSS
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            import feedparser
            feed = feedparser.parse(url)

            for entry in feed.entries[:3]:
                title = entry.get("title", "")

                results.append({
                    "source_platform": "海外",
                    "source_account": "Google News",
                    "source_link": entry.get("link", ""),
                    "source_time": _parse_time(entry.get("published", "")),
                    "title": title[:100],
                    "content": entry.get("summary", title)[:200],
                    "heat_data": "海外资讯",
                })
        except Exception as e:
            print(f"[Overseas] {query} 采集失败: {e}")
            continue

    return results


def _parse_time(time_str: str) -> str:
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(time_str)
        return dt.strftime("%Y-%m-%d")
    except:
        return ""
