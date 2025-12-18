"""SEO Roaster - Flask 應用程式"""

import os

from flask import Flask, jsonify, render_template, request

from .analyzer import SEOAnalyzer
from .roasts import (
    get_check_name,
    get_error_roast,
    get_grade_roast,
    get_roast,
)

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
def analyze():
    """分析 SEO"""
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "error": True,
            "message": "請輸入網址，不要讓我猜。",
        }), 400

    # 執行分析
    analyzer = SEOAnalyzer(timeout=15)
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


def create_app():
    """工廠函數，用於 Gunicorn"""
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
