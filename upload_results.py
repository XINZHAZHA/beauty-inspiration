"""
通过 GitHub API ��传每日生成的网页文件
解决 git push 权限问题（GitHub Actions 环境）
"""
import os, base64, json, urllib.request, sys
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "XINZHAZHA/beauty-inspiration")
DOCS_DIR = "docs"


def get_file_sha(path):
    """获取文件当前 SHA（如果存在）"""
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        return data.get("sha")
    except Exception:
        return None


def upload_file(path, content_bytes):
    """上传或更新文件"""
    sha = get_file_sha(path)
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    body = {
        "message": f"📅 更新 {path} ({datetime.now().strftime('%Y-%m-%d')})",
        "content": content_b64,
    }
    if sha:
        body["sha"] = sha

    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="PUT")
    req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")

    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f"  ✅ {path} 已上传")
    return result


def main():
    if not GITHUB_TOKEN:
        print("❌ 缺少 GITHUB_TOKEN")
        sys.exit(1)

    print("📤 上传生成的网页文件...")

    if not os.path.isdir(DOCS_DIR):
        print(f"⚠️ {DOCS_DIR} 目录不存在")
        return

    for root, dirs, files in os.walk(DOCS_DIR):
        for f in files:
            filepath = os.path.join(root, f)
            # 统一路径分隔符
            repo_path = filepath.replace("\\", "/")
            with open(filepath, "rb") as fh:
                upload_file(repo_path, fh.read())

    print("✅ 所有文件上传完成")


if __name__ == "__main__":
    main()
