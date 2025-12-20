"""吐槽文案庫 - 毒舌 SEO 專家的評論"""

import random
from typing import Optional

# 各項目的吐槽文案
# 風格：毒舌為主（70%），傲嬌點綴（30%）
# 原則：直接、尖銳、有記憶點，但不至於讓人生氣
ROASTS = {
    # ===== Title =====
    "title": {
        "missing": [
            "連標題都沒有？你是想讓 Google 叫你「無名氏」嗎？",
            "title 都不寫就上線...你的勇氣我是真心佩服。",
            "沒有標題的網頁，就像沒有招牌的店。你打算怎麼讓人找到你？",
            "搜尋引擎看到你的網站：「這是什麼？」然後就走了。",
            "SEO 第一課就沒過，後面不用看了。",
            "連門面都不要了？好，隨便你。",
        ],
        "empty": [
            "title 標籤寫了但是空的...所以你是在跟我開玩笑嗎？",
            "空白標題。恭喜，你成功浪費了一個標籤。",
            "寫了一個空的 title...這種操作我還真沒見過。",
        ],
        "too_short": [
            "{length} 個字的標題？字數比你的誠意還少。",
            "就 {length} 個字？你是按字付費嗎？",
            "標題這麼短，Google 都懶得看完整。",
            "才 {length} 個字...你對自己的網站就這麼沒話說？",
        ],
        "too_long": [
            "{length} 個字？你在寫作文嗎？後面會被截掉你知道吧。",
            "這麼長的標題，搜尋結果只會顯示「...」。寫心酸的？",
            "標題不是越長越好，60 字左右就夠了。你這是在湊字數？",
        ],
    },

    # ===== Meta Description =====
    "meta_description": {
        "missing": [
            "沒有 description？所以你打算讓 Google 自己編故事？祝你好運。",
            "連自我介紹都懶得寫...你是有多不想被人點進來？",
            "description 不寫，搜尋結果會顯示亂七八糟的內容。到時候別怪我沒提醒。",
            "沒有描述的連結，點擊率直接砍半。你知道嗎？現在知道了。",
        ],
        "empty": [
            "description 是空的...寫了等於沒寫，你在耍我嗎？",
            "空白描述，搜尋結果會很尷尬的。但你可能不在乎吧。",
        ],
        "too_short": [
            "{length} 個字的描述？這麼惜字如金是怕打字手痠？",
            "描述太短，Google 會自己抓其他內容來補。抓到什麼就看運氣囉。",
            "才 {length} 個字，連你的網站在幹嘛都說不清楚。",
        ],
        "too_long": [
            "{length} 個字...後面會被截掉，你知道吧？知道還寫這麼長？",
            "描述不是作文比賽。160 字左右就好，多的沒人看得到。",
            "寫這麼長是想展現文采嗎？可惜只有前面會顯示。",
        ],
    },

    # ===== Canonical =====
    "canonical": {
        "missing": [
            "沒有 canonical？等重複內容問題找上門再哭吧！...不是我詛咒你！",
            "canonical 都不設，Google：「這頁和那頁是雙胞胎嗎？」笨蛋！",
            "沒有 canonical 等於告訴搜尋引擎：「隨便選一個當正版吧！」真隨性！",
            "權重被分散掉也不在意？真是財大氣粗的網站呢！哼！",
        ],
        "empty": [
            "canonical 寫了是空的？這比沒寫還糟糕，你在搞什麼！",
            "空的 canonical 會讓爬蟲更困惑喔...你是故意找麻煩的嗎！",
        ],
    },

    # ===== Viewport =====
    "viewport": {
        "missing": [
            "沒有 viewport？手機用戶看你的網站要用放大鏡嗎！都 2025 年了！",
            "不設 viewport，行動裝置開啟會是桌面版縮小版...醜到爆！哼！",
            "現在一半以上流量來自手機，你就這樣放棄他們？真狠心！",
            "viewport 都沒有，Google 的行動優先索引會把你往後排喔！活該！",
        ],
        "empty": [
            "viewport 是空的...你是在測試我的耐心嗎？這種低級錯誤！",
        ],
    },

    # ===== Lang =====
    "lang": {
        "missing": [
            "html 沒有 lang 屬性，螢幕閱讀器：「這是什麼語言？」你很自私欸！",
            "不寫 lang，搜尋引擎怎麼知道你的內容給誰看？哼，真懶！",
            "沒有語言標記，對無障礙使用者超不友善的！...不是我在說教！",
        ],
        "no_html_tag": [
            "連 html 標籤都沒有...這真的是網頁嗎？還是記事本檔案？讓人傻眼！",
        ],
    },

    # ===== H1 =====
    "h1": {
        "missing": [
            "沒有 H1？所以這頁的主題是...薛丁格的標題？",
            "H1 都沒有，你打算讓搜尋引擎自己猜這頁在講什麼嗎？",
            "沒有主標題，就像文章沒有題目。你是在考驗讀者的通靈能力？",
            "缺少 H1，頁面結構直接亂掉。基本功欸。",
        ],
        "empty": [
            "H1 寫了但是空的...所以主標題是「虛無」的概念嗎？",
            "空白 H1，這種操作是故意的還是手滑？",
        ],
        "multiple": [
            "H1 有 {count} 個？每個都想當主角，結果誰都不是主角。",
            "一個頁面 {count} 個 H1...搜尋引擎表示：「你到底想說什麼？」",
            "{count} 個主標題，你是開記者會嗎？一個就夠了。",
            "H1 不是越多越好。真的。相信我。",
        ],
    },

    # ===== HTTPS =====
    "https": {
        "http_only": [
            "2025 年了還在用 HTTP？你是從哪個年代穿越來的？",
            "沒有 HTTPS，瀏覽器會直接標「不安全」。用戶看到就跑了，活該。",
            "HTTP 網站...Let's Encrypt 免費 SSL 都懶得裝？",
            "不安全的連線，使用者資料直接裸奔。你是故意的嗎？",
            "沒有 SSL 就上線，這種勇氣真的少見。不是誇你。",
        ],
    },

    # ===== Robots =====
    "robots": {
        "noindex": [
            "設了 noindex？所以你不想被搜尋到？那還做什麼 SEO！笨蛋！",
            "noindex 會讓這頁從搜尋結果消失喔...確定不是手殘設錯了嗎！",
            "故意擋掉索引？還是不小心的？如果是後者就太丟臉了！哼！",
        ],
    },

    # ===== Favicon =====
    "favicon": {
        "missing": [
            "沒有 favicon，分頁上會是醜醜的預設圖示喔！沒有品牌意識嗎！",
            "favicon 都不設...用戶開一堆分頁時，怎麼找到你的網站！笨蛋！",
            "沒有網站圖示，看起來就像是還沒做完的半成品...很廉價的感覺！",
        ],
    },

    # ===== Image Alt =====
    "img_alt": {
        "low_ratio": [
            "圖片 alt 只設了 {value}...視障用戶完全不知道圖片是什麼！太自私了！",
            "alt 覆蓋率這麼低，搜尋引擎也看不懂你的圖片欸！浪費流量機會！",
            "{value} 的覆蓋率？大部分圖片都沒描述...偷懶偷太大了吧！哼！",
        ],
        "medium_ratio": [
            "alt 覆蓋率 {value}...及格邊緣，還有進步空間！不是我挑剔！",
            "還有一些圖片沒寫 alt...差一點就完美了，可惜！哼！",
        ],
    },

    # ===== Open Graph =====
    "og_title": {
        "missing": [
            "沒有 og:title，分享到社群標題會亂抓。你不在意分享出去長怎樣嗎？",
            "og:title 沒設，社群預覽會很隨機。隨便你吧。",
        ],
        "empty": [
            "og:title 是空的...分享出去標題會是空白，很尷尬的。",
        ],
    },
    "og_description": {
        "missing": [
            "og:description 沒設，讓社群平台自己亂抓內容當描述？好大的賭注。",
            "沒有 og 描述，分享預覽會是一團亂。這樣誰想點？",
        ],
        "empty": [
            "og:description 空白...分享連結的描述會很可悲。",
        ],
    },
    "og_image": {
        "missing": [
            "沒有 og:image？社群分享沒有圖，點擊率直接腰斬。你知道嗎？",
            "og:image 沒設，分享出去沒有預覽圖。2025 年了欸。",
            "社群時代沒圖片等於沒流量。你是故意低調的嗎？",
        ],
        "empty": [
            "og:image 是空的...這比沒設還糟，會顯示錯誤圖示。",
        ],
    },

    # ===== Twitter Card =====
    "twitter_card": {
        "missing": [
            "沒有 Twitter Card，分享到 X 會很陽春。對，現在叫 X 了。",
            "twitter:card 沒設，社群預覽功能就這樣放棄了？",
        ],
    },

    # ===== JSON-LD Schema =====
    "json_ld": {
        "missing": [
            "沒有結構化資料，AI 搜尋時代會直接被邊緣化。你知道嗎？",
            "JSON-LD 沒寫，Rich Snippets 跟你無緣了。",
            "沒有 Schema，搜尋引擎只能猜你的內容是什麼。猜錯不要怪我。",
            "結構化資料都沒有...這在 2025 年有點落伍了。",
        ],
    },
    "json_ld_types": {
        "no_schema": [
            "沒有 Schema 可以分析，因為你根本沒寫。",
        ],
        "no_types": [
            "有 JSON-LD 但沒有 @type？這是什麼不明物體？",
        ],
    },
    "json_ld_valid": {
        "no_schema": [
            "沒有 Schema 可以驗證，因為根本沒寫。",
        ],
        "invalid_json": [
            "JSON-LD 語法錯誤：{value}。這種低級錯誤...你認真？",
            "Schema 格式壞掉了，解析器直接報錯。寫了比沒寫還慘。",
        ],
    },

    # ===== Hreflang =====
    "hreflang": {
        "not_applicable": [
            "（單語系網站，不需要 hreflang～這項就算你過吧，哼！）",
        ],
    },

    # ===== Published Time =====
    "published_time": {
        "missing": [
            "沒有發布時間標記，Google 不知道你的內容有多新鮮！會被當過期貨！",
            "日期都不標，新聞類內容會被排在後面喔！...才不是替你可惜！",
            "沒有 datePublished，內容時效性直接歸零！你知道嗎！笨蛋！",
        ],
    },

    # ===== Snippet Control =====
    "snippet_control": {
        # 這個項目通常沒有問題，留著以防萬一
    },
}

# 等級總評（毒舌為主，傲嬌點綴）
GRADE_ROASTS = {
    "S": [
        "嘖...居然挑不出什麼毛病。你今天運氣不錯。",
        "行吧，算你有兩把刷子。這話我不會說第二次。",
        "......沒什麼好嫌的。不是在誇你，只是陳述事實。",
        "哼，這次算你及格。別得意，下次不一定。",
        "90 分以上？好啦好啦，承認你還行。閉嘴。",
    ],
    "A": [
        "差一點就滿分，結果還是漏了幾個。可惜，真的可惜。",
        "A 級啊...不差，但也就「不差」而已。滿足了嗎？",
        "就差那麼一點點，你就是不肯做完整對吧？",
        "70 幾分...最後幾步都不想走？半吊子。",
        "嗯，還行吧。但我知道你可以更好。...不是在鼓勵你。",
    ],
    "B": [
        "B 級，中間值。恭喜你達成了「普通」的成就。",
        "不上不下，不好不壞。你人生是不是也這樣？",
        "及格邊緣...你對自己的標準就這麼低？",
        "普通到我都懶得吐槽了。真的。",
        "B 級就是「可以更好但你懶得弄」的意思。我說的對吧？",
    ],
    "C": [
        "C 級...你是認真的嗎？這網站真的有在經營？",
        "問題多到我不知道從哪裡開始講。傻眼。",
        "這個分數...我替你的用戶感到難過。",
        "SEO 基本功都沒做好就上線，勇氣可嘉啊。",
        "30 幾分欸...你之前都在幹嘛？真的很想知道。",
    ],
    "F": [
        "F 級。恭喜，你成功讓我無言了。",
        "......我看過很多爛的，但你這個特別突出。",
        "這是網站？你確定不是草稿？還是惡作劇？",
        "0 到 29 分...說真的，重做可能比較快。",
        "F 級，SEO 災難等級。我都不知道該同情你還是你的用戶。",
        "這個分數...好啦，深呼吸，我們從頭來過。",
    ],
}

# 錯誤訊息（毒舌風格）
ERROR_ROASTS = {
    "timeout": [
        "網站回應太慢，等到我都想睡了。Core Web Vitals 肯定炸裂。",
        "逾時了。這網站是用撥接上網嗎？",
        "等了 8 秒還沒回應...你的用戶比我有耐心嗎？我猜沒有。",
    ],
    "ssl_error": [
        "SSL 憑證有問題。瀏覽器會顯示大大的「不安全」，你知道嗎？",
        "HTTPS 壞了...這比 SEO 還嚴重。先處理這個。",
        "SSL 錯誤，連基本的安全都搞不定，談什麼 SEO？",
    ],
    "connection_error": [
        "連不上。是網址打錯還是主機掛了？總之你的問題比 SEO 還大。",
        "連線失敗...網站都連不上，SEO 再好有什麼用？",
        "完全連不上。你確定這網站還活著嗎？",
    ],
    "http_error": [
        "HTTP 錯誤。網站在噴錯誤碼，先讓它正常運作再說吧。",
        "收到錯誤回應...你有比 SEO 更該優先處理的事情。",
    ],
    "unknown": [
        "發生未知錯誤...你的網站很特別，特別到我都分析不了。",
        "出了奇怪的問題。不知道該說是網站獨特還是寫得太爛。",
    ],
}


def get_roast(check_key: str, message: Optional[str] = None, **kwargs) -> str:
    """
    取得吐槽文案

    Args:
        check_key: 檢測項目 key（如 'title', 'meta_description'）
        message: 問題類型（如 'missing', 'too_short'）
        **kwargs: 額外參數（如 length, count）

    Returns:
        str: 隨機選擇的吐槽文案
    """
    if check_key not in ROASTS:
        return f"這個 {check_key} 有問題喔...才不是擔心你！"

    roast_dict = ROASTS[check_key]

    if message and message in roast_dict:
        roasts = roast_dict[message]
    elif None in roast_dict:
        roasts = roast_dict[None]
    else:
        # 取得第一個可用的吐槽列表
        roasts = list(roast_dict.values())[0] if roast_dict else [f"{check_key} 需要改進喔！"]

    roast = random.choice(roasts)

    # 替換變數
    return roast.format(**kwargs)


def get_grade_roast(grade: str) -> str:
    """取得等級總評"""
    if grade in GRADE_ROASTS:
        return random.choice(GRADE_ROASTS[grade])
    return "這個等級...讓人不知道說什麼！"


def get_error_roast(error_type: str) -> str:
    """取得錯誤吐槽"""
    if error_type in ERROR_ROASTS:
        return random.choice(ERROR_ROASTS[error_type])
    return "出了點問題...不是我搞的喔！"


# 檢測項目的中文名稱
CHECK_NAMES = {
    "title": "網頁標題 (title)",
    "meta_description": "Meta 描述 (description)",
    "canonical": "Canonical 標籤",
    "viewport": "Viewport 設定",
    "lang": "語言標記 (lang)",
    "h1": "H1 標題",
    "https": "HTTPS 安全協定",
    "robots": "Robots 設定",
    "favicon": "網站圖示 (favicon)",
    "img_alt": "圖片替代文字 (alt)",
    "og_title": "Open Graph 標題",
    "og_description": "Open Graph 描述",
    "og_image": "Open Graph 圖片",
    "twitter_card": "Twitter Card",
    "json_ld": "結構化資料 (JSON-LD)",
    "json_ld_types": "Schema 類型",
    "json_ld_valid": "Schema 格式驗證",
    "hreflang": "多語系標記 (hreflang)",
    "published_time": "發布時間標記",
    "snippet_control": "摘要控制設定",
}


def get_check_name(check_key: str) -> str:
    """取得檢測項目的中文名稱"""
    return CHECK_NAMES.get(check_key, check_key)


# 修改建議（正經版，給 AI 工具看的）
SUGGESTIONS = {
    "title": {
        "missing": "請新增 <title> 標籤",
        "empty": "請填寫 <title> 標籤內容",
        "too_short": "建議標題長度 30-60 字元",
        "too_long": "建議標題長度 30-60 字元，目前過長會被截斷",
    },
    "meta_description": {
        "missing": '請新增 <meta name="description" content="..."> 標籤，長度建議 120-160 字元',
        "empty": "請填寫 meta description 內容，長度建議 120-160 字元",
        "too_short": "建議描述長度 120-160 字元",
        "too_long": "建議描述長度 120-160 字元，目前過長會被截斷",
    },
    "canonical": {
        "missing": '請新增 <link rel="canonical" href="頁面完整網址"> 標籤',
        "empty": "請填寫 canonical 標籤的 href 值",
    },
    "viewport": {
        "missing": '請新增 <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "empty": "請設定 viewport 的 content 值",
    },
    "lang": {
        "missing": '請在 <html> 標籤加上 lang 屬性，例如 <html lang="zh-TW">',
        "no_html_tag": "請確保有完整的 <html> 標籤結構",
    },
    "h1": {
        "missing": "請新增 <h1> 標題，作為頁面主標題",
        "empty": "請填寫 <h1> 標題內容",
        "multiple": "建議頁面只保留一個 <h1> 標題，其他改用 <h2> 或更低層級",
    },
    "https": {
        "http_only": "建議使用 HTTPS 協定，可使用 Let's Encrypt 免費 SSL 憑證",
    },
    "robots": {
        "noindex": "請檢查 robots meta 標籤或 X-Robots-Tag，移除 noindex 設定（如果想被搜尋引擎索引）",
    },
    "favicon": {
        "missing": '請新增 <link rel="icon" href="favicon.ico"> 或使用 SVG/PNG 格式的網站圖示',
    },
    "img_alt": {
        "low_ratio": "請為所有 <img> 標籤加上 alt 屬性，描述圖片內容",
        "medium_ratio": "建議提高 alt 覆蓋率，為更多圖片加上描述",
    },
    "og_title": {
        "missing": '請新增 <meta property="og:title" content="分享標題">',
        "empty": "請填寫 og:title 的內容",
    },
    "og_description": {
        "missing": '請新增 <meta property="og:description" content="分享描述">',
        "empty": "請填寫 og:description 的內容",
    },
    "og_image": {
        "missing": '請新增 <meta property="og:image" content="圖片完整網址">，建議尺寸 1200x630',
        "empty": "請填寫 og:image 的圖片網址",
    },
    "twitter_card": {
        "missing": '請新增 <meta name="twitter:card" content="summary_large_image">',
    },
    "json_ld": {
        "missing": "建議新增 JSON-LD 結構化資料，參考 schema.org 選擇適合的類型",
    },
    "json_ld_types": {
        "no_schema": "請新增 JSON-LD 結構化資料",
        "no_types": '請在 JSON-LD 中加入 @type 屬性，例如 "@type": "WebPage"',
    },
    "json_ld_valid": {
        "no_schema": "請新增 JSON-LD 結構化資料",
        "invalid_json": "請修正 JSON-LD 語法錯誤，確保 JSON 格式正確",
    },
    "hreflang": {
        "not_applicable": "（單語系網站可略過此項）",
        "missing": '如有多語言版本，請新增 <link rel="alternate" hreflang="語言代碼" href="對應網址">',
    },
    "published_time": {
        "missing": '文章類型建議新增 <meta property="article:published_time" content="ISO8601日期">',
    },
    "snippet_control": {
        "missing": '可考慮使用 <meta name="robots" content="max-snippet:-1"> 控制搜尋結果呈現',
    },
}


def get_suggestion(check_key: str, message: Optional[str] = None) -> str:
    """
    取得修改建議

    Args:
        check_key: 檢測項目 key（如 'title', 'meta_description'）
        message: 問題類型（如 'missing', 'too_short'）

    Returns:
        str: 對應的修改建議
    """
    if check_key not in SUGGESTIONS:
        return ""

    suggestion_dict = SUGGESTIONS[check_key]

    if message and message in suggestion_dict:
        return suggestion_dict[message]

    # 嘗試取得 default，否則回傳第一個建議
    if "default" in suggestion_dict:
        return suggestion_dict["default"]

    if suggestion_dict:
        return list(suggestion_dict.values())[0]

    return ""
