"""
配置文件 — 所有预设参数和系统设置
"""

# ============================================================
# 微信推送配置
# ============================================================
WECHAT_OPENID_MAIN = "oAclh3HnEugIyJF9-mC-TJl2LXJo"
WECHAT_OPENID_SUB = "oAclh3K8_SQzrS69JNCmDsSOU8o0"

# ============================================================
# 内容筛选配置
# ============================================================
MAX_INSPIRATIONS = 10

CATEGORY_QUOTAS = {
    "regulation": (1, 2),      # 法规/新规 最少1条 最多2条
    "brand_news": (1, 2),      # 品牌/产品热点 最少1条 最多2条
    "other": (6, 8),           # 其他 6-8条（成分、新品、科普等）
}

# ============================================================
# 采集源配置
# ============================================================
# 药监局化妆品公告页
NMPA_URL = "https://www.nmpa.gov.cn/zwgk/ggtg/index.html"

# RSS源列表（美妆行业媒体 + 海外）
RSS_FEEDS = [
    # 国内美妆行业媒体
    {"name": "化妆品观察", "url": "https://www.hzpgc.com/feed"},
    {"name": "青眼", "url": "https://www.qingyan.com/feed"},
    {"name": "美妆头条", "url": "https://www.mztoutiao.com/feed"},
    # 海外美妆资讯
    {"name": "Allure Beauty", "url": "https://www.allure.com/feed/rss"},
    {"name": "Vogue Beauty", "url": "https://www.vogue.com/feed/rss/beauty"},
    {"name": "Cosmopolitan Beauty", "url": "https://www.cosmopolitan.com/beauty/rss.xml"},
    {"name": "Byrdie", "url": "https://www.byrdie.com/feed"},
    # Reddit 护肤
    {"name": "SkincareAddiction", "url": "https://www.reddit.com/r/SkincareAddiction/.rss"},
    {"name": "AsianBeauty", "url": "https://www.reddit.com/r/AsianBeauty/.rss"},
]

# ============================================================
# GitHub Pages 配置
# ============================================================
SITE_TITLE = "哦王小明 · 每日美妆灵感"
SITE_URL = "https://xinzhazha.github.io/beauty-inspiration/"
PAGE_OUTPUT_DIR = "docs"
