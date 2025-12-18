# SEO Roaster 吐槽器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg)](https://flask.palletsprojects.com/)

[<- Back to Muripo HQ](https://tznthou.github.io/muripo-hq/) | [English](README_EN.md)

輸入網址，獲得激烈毒舌的 SEO 分析報告。讓你的網站在被吐槽中進步。

![SEO Roaster Demo](assets/demo.webp)

> **Warning**
> 本工具的吐槽內容純屬娛樂，但 SEO 建議是認真的。

---

## 功能特色

- **20 項 SEO 檢測**：涵蓋基礎、社交、結構化資料等面向
- **毒舌傲嬌吐槽**：每個問題都附帶隨機抽取的毒舌+傲嬌評論
- **等級評分系統**：S/A/B/C/F 五級評分，附等級總評
- **軟糖黏土 UI**：Claymorphism 風格，Q 彈立體的 3D 黏土視覺
- **零依賴前端**：純 HTML/CSS/JS，無需 npm

---

## 檢測項目

### 基礎 SEO（10 項）

| 項目 | 說明 | 權重 |
|------|------|------|
| Title | 標題存在 + 長度檢查 | 8% |
| Meta Description | 描述存在 + 長度檢查 | 8% |
| Canonical | 避免重複內容 | 5% |
| Viewport | 行動裝置適配 | 4% |
| Lang | 語言標記 | 3% |
| H1 | 數量檢查（應為 1 個） | 6% |
| HTTPS | 安全協定 | 8% |
| Robots | noindex 狀態 | 4% |
| Favicon | 網站圖示 | 2% |
| Image Alt | 圖片替代文字覆蓋率 | 5% |

### 社交分享（4 項）

| 項目 | 說明 | 權重 |
|------|------|------|
| og:title | Open Graph 標題 | 4% |
| og:description | Open Graph 描述 | 4% |
| og:image | Open Graph 圖片 | 4% |
| Twitter Card | Twitter 分享卡片 | 3% |

### 結構化資料（3 項）

| 項目 | 說明 | 權重 |
|------|------|------|
| JSON-LD | 結構化資料存在 | 8% |
| Schema Types | Schema 類型識別 | 4% |
| Schema Valid | JSON 格式驗證 | 4% |

### 進階項目（3 項）

| 項目 | 說明 | 權重 |
|------|------|------|
| hreflang | 多語系標記 | 4% |
| Published Time | 發布時間標記 | 4% |
| Snippet Control | AI 摘要控制 | 3% |

---

## 評分等級

| 等級 | 分數區間 | 吐槽烈度 |
|------|---------|---------|
| **S** | 90-100 | 傲嬌式認可（勉強誇你） |
| **A** | 70-89 | 小問題嘲諷（差一點啦） |
| **B** | 50-69 | 中度毒舌（普通到不行） |
| **C** | 30-49 | 激烈吐槽（問題一堆） |
| **F** | 0-29 | 無情摧毀（笨蛋！） |

---

## 吐槽範例

**沒有 Title：**
> 「連標題都沒有？這種幼稚園等級的錯誤...哼，才不是想幫你呢！」

**沒有 Meta Description：**
> 「沒有 description？讓 Google 自己亂抓一段當介紹？賭運氣是吧！」

**H1 數量錯誤：**
> 「H1 有 3 個？你是在開記者會嗎，每個都是頭條？笨蛋！」

**沒有 HTTPS：**
> 「還在用 HTTP？都 2025 年了，你的網站安全性停留在石器時代！」

---

## 技術棧

| 技術 | 用途 | 備註 |
|------|------|------|
| Python 3.11+ | 執行環境 | 使用 uv 管理 |
| Flask | Web 框架 | 輕量簡潔 |
| BeautifulSoup4 | HTML 解析 | 搭配 lxml |
| Gunicorn | WSGI Server | 生產環境 |

---

## 安全性更新

> **更新時間**：2025-12-18

本專案已修復以下安全性問題，可安全部署於生產環境。

### 🔴 嚴重（已修復）

| 問題 | 說明 | 修復內容 |
|------|------|----------|
| **SSRF 漏洞** | 用戶可輸入內部 IP 存取內網資源 | 加入 IP 黑名單驗證、DNS rebinding 防護、重定向檢查 |
| **XSS 漏洞** | 前端 innerHTML 未跳脫，可能執行惡意腳本 | 所有動態內容經過 `escapeHTML()` 跳脫處理 |

### 🟠 高優先度（已修復）

| 問題 | 說明 | 修復內容 |
|------|------|----------|
| **URL 長度未限制** | 可能造成 DoS 或 ReDoS | 前端 `maxlength="2048"`，後端驗證 |
| **缺乏速率限制** | 可被濫用發起攻擊 | 自製 rate limiter，每分鐘最多 10 次 |
| **URL 格式未驗證** | 無效輸入浪費資源 | 前端正規表達式驗證 |
| **錯誤訊息洩露** | 可能暴露內部路徑 | 統一錯誤訊息，詳細資訊記錄到日誌 |

### 🟡 中優先度（已修復）

| 問題 | 說明 | 修復內容 |
|------|------|----------|
| **timeout 過長** | 15 秒讓用戶等太久 | 調整為 8 秒 |
| **HTML 解析可能失敗** | lxml 遇到破損 HTML 可能崩潰 | 加入 fallback 到 html.parser |
| **缺乏日誌記錄** | 無法追蹤錯誤 | 加入 logging 配置 |

### 🟢 低優先度（已修復）

| 問題 | 說明 | 修復內容 |
|------|------|----------|
| **魔法數字** | 閾值散佈各處 | 提取為類別常數 |
| **動畫延遲累積** | 多項目時延遲過長 | 最大延遲限制為 1 秒 |
| **port 不一致** | 不同檔案預設 port 不同 | 統一為 8080 |

---

## 技術限制

這是一個**單頁爬蟲**，有以下限制：

| 限制 | 說明 |
|------|------|
| **只分析單一頁面** | 只爬取你輸入的 URL，不會遞迴爬整站 |
| **只分析 HTML** | 無法分析 JavaScript 動態渲染的內容（SPA 網站可能不準） |
| **無法檢測速度** | Core Web Vitals（LCP、INP、CLS）需要真實瀏覽器，這裡沒有 |
| **無法檢測行為訊號** | CTR、Dwell Time、跳出率等是 Google 內部數據 |
| **無法檢測反向連結** | 需要第三方 API（Ahrefs、Moz 等） |
| **無法檢測排名** | 需要 Google Search Console 權限 |
| **8 秒逾時** | 回應太慢的網站會被判定為連線失敗 |

**這個工具能做的**：檢查 HTML 裡的 SEO 基本功（標籤、結構化資料、社交分享設定）

**這個工具不能做的**：完整的 SEO 審計（需要更專業的工具如 Screaming Frog、Ahrefs）

---

## 快速開始

### 本地開發

```bash
# 進入專案目錄
cd day-20-seo-roaster

# 安裝依賴
uv sync

# 啟動開發伺服器
uv run python -m src.seo_roaster.app

# 或使用 Flask CLI
uv run flask --app src.seo_roaster.app run --debug
```

開啟瀏覽器訪問 `http://localhost:5000`

### 生產環境

```bash
# 使用 Gunicorn
uv run gunicorn --bind 0.0.0.0:8000 src.seo_roaster.app:app
```

---

## 部署到 Zeabur

### 步驟 1：建立專案

1. 登入 [Zeabur](https://zeabur.com/)
2. 建立新專案

### 步驟 2：部署服務

1. 選擇「Git」部署方式
2. 連接你的 GitHub Repository
3. 選擇此專案資料夾
4. Zeabur 會自動偵測 Python 專案並部署

### 步驟 3：設定網域

1. 進入服務設定
2. 在「Networking」新增網域
3. 可使用免費的 `.zeabur.app` 子網域

---

## 專案結構

```
day-20-seo-roaster/
├── src/
│   └── seo_roaster/
│       ├── __init__.py
│       ├── app.py              # Flask 主程式
│       ├── analyzer.py         # SEO 分析邏輯
│       ├── roasts.py           # 吐槽文案庫
│       ├── templates/
│       │   └── index.html      # 前端頁面
│       └── static/
│           └── v1-candy-clay.css  # 軟糖黏土風格樣式
├── pyproject.toml
├── Procfile                    # Gunicorn 啟動設定
├── README.md
├── README_EN.md
└── LICENSE
```

---

## 客製化指南

### 新增檢測項目

在 `analyzer.py` 的 `WEIGHTS` 字典新增權重，然後實作對應的 `_check_xxx` 方法：

```python
WEIGHTS = {
    "your_new_check": 5,  # 新增權重
    # ...
}

def _check_your_new_check(self, soup: BeautifulSoup) -> dict:
    # 實作檢測邏輯
    return {
        "passed": True,  # 或 False
        "message": "some_message",
        "value": "detected_value",
    }
```

### 新增吐槽文案

在 `roasts.py` 的 `ROASTS` 字典新增文案：

```python
ROASTS = {
    "your_new_check": {
        "missing": [
            "吐槽文案 1",
            "吐槽文案 2",
            "吐槽文案 3",
        ],
        "some_other_issue": [
            "其他吐槽...",
        ],
    },
    # ...
}
```

### 修改 UI 風格

編輯 `static/v1-candy-clay.css` 中的 CSS 變數：

```css
:root {
    --bg-primary: #fff0f5;       /* 草莓牛奶背景 */
    --candy-pink: #ff7eb3;       /* 草莓軟糖 */
    --candy-mint: #7ee8c7;       /* 薄荷糖 */
    --candy-coral: #ff9a8b;      /* 珊瑚糖 */
    --shadow-clay: ...;          /* 黏土立體陰影 */
    /* ... */
}
```

---

## SEO 知識來源

本工具的檢測項目參考以下來源：

- Google Search Central 官方文件
- Web.dev 最佳實踐指南
- Schema.org 結構化資料規範
- 社群實務經驗彙整

**重要聲明**：
- 檢測項目的「經驗值」（如 Title 55-60 字）並非硬性規定
- llms.txt 屬於社群提案，非 Google 官方機制
- 行為訊號（CTR、Dwell Time）無法從前端檢測

---

## 隨想

### SEO 到底是什麼？

今天心血來潮，突然想問自己：SEO 到底是什麼？

我們為什麼要做 SEO？做了對我們有什麼幫助？SEO 能量化嗎？為什麼大家急急忙忙想把 SEO 做好？

當然，SEO 很重要——誰不希望自己的網站排在搜尋結果的前面？

但實務上來講，SEO 是什麼？

它就是 Google 排名的順序。

### 經驗值整理包

你有沒有發現，Google 每年的排名機制都在變？那些「Title 要 55-60 字」、「H1 只能有一個」的規則，其實都是大家花了很多時間，從排名結果反推出來的經驗值。

這些經驗值是真的嗎？也許是，也許不是。

Google 從來沒有公開說過這些數字。我們只是發現「好像這樣做的網站排名比較前面」，然後把它整理成一個又一個的 SEO 檢查清單。

所以這個工具檢測的，與其說是「規則」，不如說是「社群整理出來的經驗值整理包」。

### 為什麼要吐槽？

單純做網頁 SEO 檢索，好像有點無聊。

所以我想，如果把冷冰冰的檢測報告變成毒舌吐槽，應該會比較有趣吧？

結果發現：被罵確實比較有動力改。

### 給 Vibe Coder 的話

這個專案的核心很簡單：
1. `requests` 抓網頁
2. `BeautifulSoup` 解析 HTML
3. 一堆 `if-else` 判斷
4. 一堆毒舌字串

---

## 授權

本專案採用 [MIT License](LICENSE) 授權。
