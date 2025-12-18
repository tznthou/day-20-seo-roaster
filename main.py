"""Zeabur 入口點"""
from src.seo_roaster.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
