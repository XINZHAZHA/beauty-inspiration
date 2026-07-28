"""
微博热搜采集器
采集微博热搜榜中美妆护肤相关话题
"""
import requests
import json


# 美妆护肤相关关键词
BEAUTY_KEYWORDS = [
    "护肤", "美白", "防晒", "面膜", "精华", "面霜", "化妆",
    "口红", "粉底", "眼霜", "成分", "敏感肌", "痘痘", "抗老",
    "品牌名", "国货", "大牌", "平替", "功效", "配方", "防晒霜",
    "爽肤水", "卸妆", "洁面", "护肤品", "化妆品", "美容",
    "祛斑", "补水", "药监局", "质检", "不合格", "添加剂",
    "烟酰胺", "视黄醇", "玻尿酸", "维C", "VC", "A醇", "胜肽",
    "兰蔻", "雅诗兰黛", "欧莱雅", "珀莱雅", "薇诺娜", "花西子",
    "完美日记", "玉泽", "至本", "春日来信", "HBN", "优时颜",
    "修丽可", "SKII", "海蓝之谜", "赫莲娜", "资生堂",
]


def scrape_weibo() -> list[dict]:
    """采集微博热搜美妆相关话题"""
    results = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # 微博热搜 API
        url = "https://weibo.com/ajax/side/hotSearch"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        items = data.get("data", {}).get("realtime", [])
        for item in items[:50]:
            word = item.get("word", "")
            # 检查是否与美��护肤相关
            if any(kw in word for kw in BEAUTY_KEYWORDS):
                raw_hot = item.get("raw_hot", 0)
                results.append({
                    "source_platform": "微博",
                    "source_account": "微博热搜",
                    "source_link": f"https://s.weibo.com/weibo?q={word}",
                    "source_time": "",
                    "title": word[:100],
                    "content": f"微博热搜话题：{word}，热度{raw_hot}",
                    "heat_data": f"热搜热度 {raw_hot}",
                })
    except Exception as e:
        print(f"[Weibo] 采集失败: {e}")

    return results
