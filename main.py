"""
美妆灵感自动推送系统 — 主入口
每天 8:00 由 GitHub Actions 触发
流程：采集 → AI筛选 → 生成网页 → 微信推送
"""
import sys
import os
from datetime import datetime

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers import scrape_nmpa, scrape_weibo, scrape_zhihu, scrape_rss, scrape_overseas
from ai_filter import filter_inspirations
from push_wechat import push_to_wechat
from generate_page import generate_page


def main():
    print("=" * 60)
    print(f"🚀 美妆灵感推送系统启动 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ========== 第一步：采集 ==========
    print("\n📡 第一步：采集各平台内容...")
    all_raw = []

    # 并行采集各平台
    try:
        nmpa = scrape_nmpa()
        print(f"  ✅ 药监局: {len(nmpa)} 条")
        all_raw.extend(nmpa)
    except Exception as e:
        print(f"  ❌ 药监局: {e}")

    try:
        weibo = scrape_weibo()
        print(f"  ✅ 微博: {len(weibo)} 条")
        all_raw.extend(weibo)
    except Exception as e:
        print(f"  ❌ 微博: {e}")

    try:
        zhihu = scrape_zhihu()
        print(f"  ✅ 知乎: {len(zhihu)} 条")
        all_raw.extend(zhihu)
    except Exception as e:
        print(f"  ❌ 知乎: {e}")

    try:
        rss = scrape_rss()
        print(f"  ✅ RSS: {len(rss)} 条")
        all_raw.extend(rss)
    except Exception as e:
        print(f"  ❌ RSS: {e}")

    try:
        overseas = scrape_overseas()
        print(f"  ✅ 海外: {len(overseas)} 条")
        all_raw.extend(overseas)
    except Exception as e:
        print(f"  ❌ 海外: {e}")

    print(f"\n📊 共采集 {len(all_raw)} 条原始内容")

    if len(all_raw) == 0:
        print("⚠️ 未采集到任何内容，退出")
        return

    # ========== 第二步：AI 筛选 ==========
    print("\n🧠 第二步：智谱GLM 筛选加工...")
    inspirations = filter_inspirations(all_raw)

    if not inspirations:
        print("⚠️ AI 筛选无结果，退出")
        return

    print(f"✅ 筛选出 {len(inspirations)} 条灵感")

    # ========== 第三步：生成网页 ==========
    print("\n🌐 第三步：生成 GitHub Pages 网页...")
    page_path = generate_page(inspirations, raw_count=len(all_raw))
    if page_path:
        print(f"✅ 网页已生成")

    # ========== 第四步：微信推送 ==========
    print("\n📱 第四步：微信推送...")
    success = push_to_wechat(inspirations)
    if success:
        print("✅ 推送完成")
    else:
        print("⚠️ 推送部分失败（可能缺少配置或网络问题）")

    print("\n" + "=" * 60)
    print(f"🏁 任务完成 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
