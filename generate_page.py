"""
网页生成器
将筛选后的灵感生成 GitHub Pages 静态网页
"""
import json
import os
from datetime import date, datetime
from config.settings import SITE_TITLE, PAGE_OUTPUT_DIR


CATEGORY_LABELS = {
    "regulation": "法规新规",
    "brand_news": "品牌热点",
    "ingredient": "成分分析",
    "science": "护肤科普",
    "new_product": "新品动态",
}

CATEGORY_EMOJI = {
    "regulation": "📋",
    "brand_news": "🔥",
    "ingredient": "🧪",
    "science": "📚",
    "new_product": "🆕",
}


def generate_page(inspirations: list[dict], raw_count: int = 0) -> str:
    """生成完整 HTML 页面并保存到 docs/ 目录"""
    if not inspirations:
        print("[Page] 没有灵感数据，跳过页面生成")
        return ""

    today = date.today()
    date_str = today.strftime("%Y年%m月%d日")
    date_iso = today.strftime("%Y-%m-%d")

    cards_html = "\n".join(
        _render_card(i, item) for i, item in enumerate(inspirations, 1)
    )

    # 分类统计
    cat_counts = {}
    for item in inspirations:
        c = item.get("category", "other")
        cat_counts[c] = cat_counts.get(c, 0) + 1
    stats_html = " · ".join(
        f"{CATEGORY_EMOJI.get(c,'')} {CATEGORY_LABELS.get(c,c)} {n}条"
        for c, n in cat_counts.items()
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_TITLE} · {date_str}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 50%, #fdf4ff 100%);
    color: #1a1a2e;
    min-height: 100vh;
}}
.header {{
    background: linear-gradient(135deg, #ec4899, #8b5cf6);
    color: white;
    padding: 32px 24px;
    text-align: center;
}}
.header h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; }}
.header .subtitle {{ font-size: 0.9rem; opacity: 0.85; }}
.header .stats {{
    margin-top: 12px;
    font-size: 0.85rem;
    background: rgba(255,255,255,0.15);
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
}}
.container {{
    max-width: 720px;
    margin: 0 auto;
    padding: 20px 16px 40px;
}}
.card {{
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: transform 0.15s;
}}
.card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
.card-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}}
.card-num {{
    background: linear-gradient(135deg, #ec4899, #8b5cf6);
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}
.card-category {{
    font-size: 0.75rem;
    font-weight: 600;
    color: #ec4899;
    background: #fdf2f8;
    padding: 2px 10px;
    border-radius: 10px;
}}
.card-title {{
    font-size: 1.05rem;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 10px;
    line-height: 1.5;
}}
.source-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    font-size: 0.8rem;
    color: #6b7280;
    margin-bottom: 8px;
}}
.source-row span {{ display: flex; align-items: center; gap: 4px; }}
.heat-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: #fff7ed;
    color: #ea580c;
    font-size: 0.78rem;
    padding: 2px 10px;
    border-radius: 10px;
    font-weight: 500;
}}
.section-label {{
    font-size: 0.78rem;
    font-weight: 700;
    color: #8b5cf6;
    margin-top: 12px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
}}
.section-content {{
    font-size: 0.9rem;
    color: #374151;
    line-height: 1.6;
    margin-bottom: 6px;
}}
.link-btn {{
    display: inline-block;
    font-size: 0.8rem;
    color: #8b5cf6;
    text-decoration: none;
    margin-top: 4px;
    word-break: break-all;
}}
.link-btn:hover {{ text-decoration: underline; }}
.score-bar {{
    display: flex;
    gap: 12px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #f3f4f6;
}}
.score-btn {{
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 16px;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    background: white;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
    color: #6b7280;
}}
.score-btn:hover {{ background: #fdf2f8; border-color: #ec4899; color: #ec4899; }}
.score-btn.active {{ background: #fdf2f8; border-color: #ec4899; color: #ec4899; font-weight: 600; }}
.score-btn .count {{ font-size: 0.75rem; color: #9ca3af; margin-left: 2px; }}
.footer {{
    text-align: center;
    padding: 24px;
    font-size: 0.78rem;
    color: #9ca3af;
}}
.footer a {{ color: #8b5cf6; text-decoration: none; }}
.archive-link {{
    display: block;
    text-align: center;
    margin: 12px auto 32px;
    color: #8b5cf6;
    font-size: 0.9rem;
}}
@media (max-width: 480px) {{
    .header h1 {{ font-size: 1.3rem; }}
    .card {{ padding: 16px; }}
    .source-row {{ font-size: 0.75rem; gap: 8px; }}
}}
</style>
</head>
<body>

<div class="header">
    <h1>🎯 哦王小明 · 每日美妆灵感</h1>
    <div class="subtitle">{date_str} · 精选 {len(inspirations)} 条</div>
    <div class="stats">{stats_html}</div>
</div>

<div class="container">
{cards_html}
</div>

<div class="footer">
    <p>🤖 由 AI 自动筛选 · 每日 8:00 更新</p>
    <p>采集源：药监局 · 微博 · 知乎 · 行业RSS · 海外美妆媒体</p>
    <p>Powered by GitHub Actions + 智谱GLM</p>
</div>

<script>
// 打分逻辑：点击切换，数据存 localStorage
document.querySelectorAll('.score-btn').forEach(btn => {{
    btn.addEventListener('click', function() {{
        const bar = this.parentElement;
        const card = bar.closest('.card');
        const cardId = card.dataset.id;
        const score = this.dataset.score;

        // 清除同卡片其他按钮状态
        bar.querySelectorAll('.score-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        // 存储评分
        const scores = JSON.parse(localStorage.getItem('inspiration_scores') || '{{}}');
        scores[cardId] = {{ score: score, time: new Date().toISOString() }};
        localStorage.setItem('inspiration_scores', JSON.stringify(scores));
    }});

    // 恢复历史评分
    const card = this.closest('.card');
    const cardId = card.dataset.id;
    const scores = JSON.parse(localStorage.getItem('inspiration_scores') || '{{}}');
    if (scores[cardId] && scores[cardId].score === this.dataset.score) {{
        this.classList.add('active');
    }}
}});
</script>

</body>
</html>"""

    # 保存文件
    os.makedirs(PAGE_OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(PAGE_OUTPUT_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Page] 网页已生成: {output_path}")

    # 同时保存一份按日期的历史记录
    history_dir = os.path.join(PAGE_OUTPUT_DIR, "history")
    os.makedirs(history_dir, exist_ok=True)
    history_path = os.path.join(history_dir, f"{date_iso}.html")
    with open(history_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 保存 JSON 数据
    json_path = os.path.join(PAGE_OUTPUT_DIR, "data", f"{date_iso}.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(inspirations, f, ensure_ascii=False, indent=2)

    return output_path


def _render_card(index: int, item: dict) -> str:
    """渲染单条灵感卡片"""
    cat = item.get("category", "other")
    cat_label = CATEGORY_LABELS.get(cat, cat)
    cat_emoji = CATEGORY_EMOJI.get(cat, "")

    title = item.get("title", "无标题")
    platform = item.get("source_platform", "未知")
    account = item.get("source_account", "")
    link = item.get("source_link", "#")
    time_str = item.get("source_time", "")
    heat = item.get("heat_data", "")
    summary = item.get("summary", "")
    angle = item.get("angle", "")
    headline = item.get("headline_suggestion", "")
    framework = item.get("shooting_framework", "")
    extra = item.get("ai_extra", "")

    heat_html = ""
    if heat:
        heat_html = f'<span class="heat-badge">📊 {heat}</span>'

    return f"""
<div class="card" data-id="{index}">
    <div class="card-header">
        <div class="card-num">{index}</div>
        <div class="card-category">{cat_emoji} {cat_label}</div>
    </div>

    <div class="card-title">{title}</div>

    <div class="source-row">
        <span>📌 {platform}</span>
        {f'<span>👤 {account}</span>' if account else ''}
        {f'<span>🕐 {time_str}</span>' if time_str else ''}
        {heat_html}
    </div>

    {f'<div class="section-label">📝 原文摘要</div><div class="section-content">{summary}</div>' if summary else ''}

    {f'<div class="section-label">💡 选题角度</div><div class="section-content">{angle}</div>' if angle else ''}

    {f'<div class="section-label">✏️ 标题建议</div><div class="section-content">{headline}</div>' if headline else ''}

    {f'<div class="section-label">🎬 拍摄框架</div><div class="section-content">{framework}</div>' if framework else ''}

    {f'<div class="section-label">➕ AI补充</div><div class="section-content">{extra}</div>' if extra else ''}

    <a class="link-btn" href="{link}" target="_blank" rel="noopener">🔗 查看原文 →</a>

    <div class="score-bar">
        <button class="score-btn" data-score="useful">👍 有用</button>
        <button class="score-btn" data-score="useless">👎 没用</button>
        <button class="score-btn" data-score="super">⭐ 超赞</button>
    </div>
</div>"""
