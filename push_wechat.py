"""
微信测试号推送模块
通过微信公众号测试号模板消息推送给指定用户
"""
import json
import os
import requests
from config.settings import WECHAT_OPENID_MAIN, WECHAT_OPENID_SUB, SITE_URL


WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
WECHAT_SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"


def _get_appid() -> str:
    return os.environ.get("WECHAT_APPID", "")


def _get_appsecret() -> str:
    return os.environ.get("WECHAT_APPSECRET", "")


def _get_template_id() -> str:
    return os.environ.get("WECHAT_TEMPLATE_ID", "")


def _get_access_token() -> str:
    """获取微信 access_token"""
    appid = _get_appid()
    secret = _get_appsecret()
    if not appid or not secret:
        print("[WeChat] 未配置 appid/appsecret")
        return ""

    try:
        resp = requests.get(
            WECHAT_TOKEN_URL,
            params={
                "grant_type": "client_credential",
                "appid": appid,
                "secret": secret,
            },
            timeout=10,
        )
        data = resp.json()
        token = data.get("access_token", "")
        if token:
            print(f"[WeChat] 获取 access_token 成功")
        else:
            print(f"[WeChat] 获取 token 失败: {data}")
        return token
    except Exception as e:
        print(f"[WeChat] 获取 token 异常: {e}")
        return ""


def generate_summary(inspirations: list[dict]) -> str:
    """生成推送摘要文本"""
    cat_map = {
        "regulation": "法规新规",
        "brand_news": "品牌热点",
        "ingredient": "成分分析",
        "science": "护肤科普",
        "new_product": "新品动态",
    }
    cats = {}
    for item in inspirations:
        c = item.get("category", "other")
        cats[c] = cats.get(c, 0) + 1

    parts = []
    for c, count in cats.items():
        name = cat_map.get(c, c)
        parts.append(f"{name}{count}条")
    return " · ".join(parts)


def push_to_wechat(inspirations: list[dict]) -> bool:
    """推送到微信测试号"""
    template_id = _get_template_id()
    if not template_id:
        print("[WeChat] 未配置模板ID，跳过推送")
        return False

    token = _get_access_token()
    if not token:
        print("[WeChat] 无法获取 access_token，跳过推送")
        return False

    from datetime import date
    today = date.today().strftime("%Y年%m月%d日")
    count = len(inspirations)
    summary = generate_summary(inspirations)

    payload_template = {
        "touser": "",
        "template_id": template_id,
        "url": SITE_URL,
        "data": {
            "date": {"value": today, "color": "#333333"},
            "count": {"value": str(count), "color": "#FF6B6B"},
            "summary": {"value": summary, "color": "#666666"},
        },
    }

    openids = []
    if WECHAT_OPENID_MAIN:
        openids.append(("主号", WECHAT_OPENID_MAIN))
    if WECHAT_OPENID_SUB:
        openids.append(("小号", WECHAT_OPENID_SUB))

    success = True
    for label, openid in openids:
        try:
            payload = dict(payload_template)
            payload["touser"] = openid
            url = f"{WECHAT_SEND_URL}?access_token={token}"
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            if data.get("errcode") == 0:
                print(f"[WeChat] 推送{label}成功")
            else:
                print(f"[WeChat] 推送{label}失败: {data}")
                success = False
        except Exception as e:
            print(f"[WeChat] 推送{label}异常: {e}")
            success = False

    return success
