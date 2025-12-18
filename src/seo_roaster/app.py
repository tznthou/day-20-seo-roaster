"""SEO Roaster - Flask 應用程式"""

import logging
import os
from functools import wraps
from time import time

from flask import Flask, jsonify, render_template, request

from .analyzer import SEOAnalyzer
from .roasts import (
    get_check_name,
    get_error_roast,
    get_grade_roast,
    get_roast,
)

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [%(name)s:%(lineno)d]'
)
logger = logging.getLogger(__name__)

# 簡易速率限制器（記憶體版）
RATE_LIMIT_STORE: dict[str, list[float]] = {}


def rate_limit(max_requests: int = 10, window: int = 60):
    """
    速率限制裝飾器

    Args:
        max_requests: 時間窗口內最大請求數
        window: 時間窗口（秒）
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 取得客戶端 IP（考慮反向代理）
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip:
                ip = ip.split(',')[0].strip()  # 取第一個 IP

            now = time()

            # 清理過期記錄
            if ip in RATE_LIMIT_STORE:
                RATE_LIMIT_STORE[ip] = [t for t in RATE_LIMIT_STORE[ip] if now - t < window]
            else:
                RATE_LIMIT_STORE[ip] = []

            # 檢查是否超過限制
            if len(RATE_LIMIT_STORE[ip]) >= max_requests:
                logger.warning(f"Rate limit exceeded for IP: {ip}")
                return jsonify({
                    "error": True,
                    "message": "請求太頻繁了，休息一下吧！",
                    "roast": "你是機器人嗎？連喘口氣都不會？",
                }), 429

            RATE_LIMIT_STORE[ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)


@app.route("/")
def index():
    """首頁"""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
@rate_limit(max_requests=10, window=60)  # 每分鐘最多 10 次分析
def analyze():
    """分析 SEO"""
    data = request.get_json()
    url = data.get("url", "").strip()

    # 驗證 URL 長度
    if len(url) > 2048:
        return jsonify({
            "error": True,
            "message": "網址太長了，你是在貼論文嗎？",
            "roast": "連網址都這麼長，你的人生是不是也很複雜？",
        }), 400

    if not url:
        return jsonify({
            "error": True,
            "message": "請輸入網址，不要讓我猜。",
        }), 400

    # 執行分析（timeout 8 秒較合理）
    analyzer = SEOAnalyzer(timeout=8)
    result = analyzer.analyze(url)

    # 處理錯誤
    if "error" in result:
        return jsonify({
            "error": True,
            "type": result["error"],
            "message": result["message"],
            "roast": get_error_roast(result["error"]),
        })

    # 生成吐槽報告
    roast_report = {
        "url": result["url"],
        "score": result["score"],
        "grade": result["grade"],
        "grade_roast": get_grade_roast(result["grade"]),
        "issues": [],
        "passed": [],
        "total_checks": len(result["checks"]),
        "passed_count": len(result["passed"]),
        "issue_count": len(result["issues"]),
    }

    # 處理問題項目
    for issue in result["issues"]:
        check_key = issue["key"]
        check_data = result["checks"][check_key]
        message = check_data.get("message")

        # 準備吐槽參數
        roast_params = {
            "length": check_data.get("length"),
            "count": check_data.get("count"),
            "value": check_data.get("value"),
        }
        # 移除 None 值
        roast_params = {k: v for k, v in roast_params.items() if v is not None}

        roast_report["issues"].append({
            "key": check_key,
            "name": get_check_name(check_key),
            "message": message,
            "value": check_data.get("value"),
            "roast": get_roast(check_key, message, **roast_params),
            "weight": issue["weight"],
        })

    # 處理通過項目
    for check_key in result["passed"]:
        check_data = result["checks"][check_key]
        roast_report["passed"].append({
            "key": check_key,
            "name": get_check_name(check_key),
            "value": check_data.get("value"),
        })

    return jsonify(roast_report)


@app.route("/health")
def health():
    """健康檢查端點"""
    return jsonify({"status": "ok", "message": "SEO Roaster is alive and roasting!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
