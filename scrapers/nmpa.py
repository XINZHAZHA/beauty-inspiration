"""
药监局化妆品公告采集器
采集国家药监局发布的化妆品相关公告、抽检结果、新规通知
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def scrape_nmpa() -> list[dict]:
    """采集药监局化妆品相关公告"""
    results = []
    try:
        # 化妆品公告列表页
        url = "https://www.nmpa.gov.cn/zwgk/ggtg/hzhpggtg/index.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")

        # 解析公告列表
        items = soup.select(".list-item, .cl-item, li a")[:10]
        for item in items:
            link_tag = item if item.name == "a" else item.find("a")
            if not link_tag or not link_tag.get("href"):
                continue

            title = link_tag.get("title") or link_tag.get_text(strip=True)
            href = link_tag.get("href", "")
            if href and not href.startswith("http"):
                href = "https://www.nmpa.gov.cn" + href

            # 尝试提取日期
            date_tag = item.find(class_="date") or item.find("span")
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            results.append({
                "source_platform": "药监局",
                "source_account": "国家药品监督管理局",
                "source_link": href,
                "source_time": date_str,
                "title": title[:100],
                "content": title[:200],
                "heat_data": "官方公告",
            })
    except Exception as e:
        print(f"[NMPA] 采集失败: {e}")

    return results
