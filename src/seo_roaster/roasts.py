"""吐槽文案庫 - 傲嬌風格的 SEO 評論"""

import random
from typing import Optional

# 各項目的吐槽文案（毒舌+傲嬌風格）
# 原則：先狠狠罵，再用傲嬌收尾
ROASTS = {
    # ===== Title =====
    "title": {
        "missing": [
            "連標題都沒有？這種幼稚園等級的錯誤...哼，才不是想幫你呢！",
            "title 都不寫，你是想當網路隱形人嗎？笨蛋！...不是我在意啦！",
            "沒有標題的網頁，就像沒有名字的人——不存在。哼，隨便你啦！",
            "搜尋引擎：「這頁是什麼？」你：「...」真是讓人無言！",
            "SEO 入門第一課都沒過，就敢上線？...才不是替你丟臉呢！",
        ],
        "empty": [
            "title 標籤寫了卻是空的？這比沒寫還蠢！你是認真的嗎！",
            "空白標題...所以你花時間寫了一個空氣？哼，真有創意！",
            "標題留空白，你的腦袋也是嗎？...不是我在嘲諷你！",
        ],
        "too_short": [
            "{length} 個字的標題？連推文都比你長！這也太敷衍了吧！",
            "標題這麼短，是按字收費怕花錢嗎？哼，真小氣！",
            "才 {length} 個字...你對自己的網站就這麼沒話說？可悲！",
        ],
        "too_long": [
            "{length} 個字的標題？你在寫小說嗎！後面會被截成「...」喔！",
            "標題寫成論文長度，Google 表示：「讀到一半就放棄了」。哼！",
            "這麼長的標題，用戶看到就累了，笨蛋！...不是我同情他們！",
        ],
    },

    # ===== Meta Description =====
    "meta_description": {
        "missing": [
            "沒有 description？讓 Google 自己亂抓一段當介紹？賭運氣是吧！",
            "連自我介紹都懶得寫，你的網站是有多不想被人認識？哼！",
            "description 不寫，搜尋結果會顯示亂七八糟的內容喔，活該！",
            "這是「請勿點擊」的暗示嗎？沒有描述的連結誰敢點！笨蛋！",
        ],
        "empty": [
            "description 是空的...寫了等於沒寫，你在浪費人類的時間！",
            "空白描述...所以你是故意要讓搜尋結果看起來很糟的對吧？",
        ],
        "too_short": [
            "{length} 個字的描述？這是推特時代的遺產嗎？太短了啦！",
            "描述這麼短，Google 會自己抓其他內容來補...品質不保證喔！",
            "才 {length} 個字，你對自己的內容就這麼沒自信？可憐！",
        ],
        "too_long": [
            "{length} 個字的描述...後面會被截斷成「...」，寫那麼多幹嘛！",
            "描述寫成作文，但只有前面會被顯示，後面等於白寫！哼！",
            "這麼長...160 字左右就好，多的都是你的自我感動！",
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
            "沒有 H1？所以這頁的主題是個謎嗎？連重點都不說！笨蛋！",
            "H1 都沒有，頁面結構亂七八糟的...搜尋引擎看了頭痛！哼！",
            "沒有主標題，就像文章沒有題目...這是在考驗讀者的通靈能力嗎！",
            "缺少 H1，SEO 基本分直接扣掉...才不是替你心疼呢！",
        ],
        "empty": [
            "H1 寫了是空的？所以主標題是「虛無」嗎？太哲學了吧！",
            "空白 H1...你是在嘲諷 HTML 規範嗎？有夠無聊！",
        ],
        "multiple": [
            "H1 有 {count} 個？你是在開記者會嗎，每個都是頭條？笨蛋！",
            "一個頁面 {count} 個 H1...每個都想當主角，結果沒有人是主角！",
            "{count} 個主標題，搜尋引擎：「到底哪個才是重點！」你說呢？",
            "H1 不是越多越好啦！一個就夠了！...不是我囉嗦！",
        ],
    },

    # ===== HTTPS =====
    "https": {
        "http_only": [
            "還在用 HTTP？都 2025 年了，你的網站安全性停留在石器時代！",
            "沒有 HTTPS，瀏覽器會標記「不安全」喔！用戶看到就跑了！活該！",
            "HTTP 網站...Let's Encrypt 免費 SSL 都懶得裝嗎？真是的！",
            "不安全的連線...使用者的資料就這樣裸奔？太可怕了！哼！",
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
            "沒有 og:title，分享到 Facebook 會很醜喔！標題亂抓的！笨蛋！",
            "og:title 都不設，社群分享預覽會很隨機...這樣也行？太隨便！",
        ],
        "empty": [
            "og:title 是空的...分享出去會很尷尬的，標題變空白！",
        ],
    },
    "og_description": {
        "missing": [
            "og:description 沒設，讓 Facebook 自己亂抓內容當描述？隨便你！",
            "沒有 og 描述，社群預覽的說明會是一團亂...這樣誰想點！哼！",
        ],
        "empty": [
            "og:description 空白...分享連結的描述會很可悲的！真是的！",
        ],
    },
    "og_image": {
        "missing": [
            "沒有 og:image？社群分享沒有圖片，點擊率直接砍半！活該！",
            "og:image 都不設，分享連結會沒有預覽圖，看起來很陽春！笨蛋！",
            "社群時代沒圖片等於沒流量...你是故意要低調的嗎？哼！",
        ],
        "empty": [
            "og:image 是空的...這比沒設還糟糕，會顯示錯誤！真厲害啊！",
        ],
    },

    # ===== Twitter Card =====
    "twitter_card": {
        "missing": [
            "沒有 Twitter Card，分享到 X 會很陽春喔！現在叫 X 了啦！笨蛋！",
            "twitter:card 都不設，社群預覽功能就這樣放棄了？太可惜！哼！",
        ],
    },

    # ===== JSON-LD Schema =====
    "json_ld": {
        "missing": [
            "沒有結構化資料，AI 時代不用 Schema 會被當成普通內容處理！落伍！",
            "JSON-LD 都不寫，Rich Snippets 跟你無緣了！可憐！",
            "沒有 Schema，搜尋引擎只能用猜的來理解你的內容...笨蛋！",
            "結構化資料都沒有，在 AI 搜尋時代等於被邊緣化！...不是我擔心你！",
        ],
    },
    "json_ld_types": {
        "no_schema": [
            "沒有 Schema 可以分析...因為你根本沒寫！真是的！",
        ],
        "no_types": [
            "有 JSON-LD 但沒有 @type？這是什麼不明物體...寫了等於沒寫！",
        ],
    },
    "json_ld_valid": {
        "no_schema": [
            "沒有 Schema 可以驗證，因為根本沒寫啊！笨蛋！",
        ],
        "invalid_json": [
            "JSON-LD 語法錯誤！{value}...這種低級錯誤也能犯？太丟臉了！",
            "Schema 格式壞掉了，解析器直接報錯！寫了比沒寫還慘！哼！",
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

# 等級總評（毒舌+傲嬌風格）
GRADE_ROASTS = {
    "S": [
        "哼...90 分以上嗎？勉強算是及格了，別得意！",
        "S 級...算你有點本事。但也就「有點」而已！不是在誇你！",
        "居然拿到 S 級？運氣不錯嘛！...才不是佩服你呢！",
        "這個分數...好吧，承認你還行。但別驕傲！哼！",
    ],
    "A": [
        "A 級...差一點就滿分，結果功虧一簣？可惜啊！哼！",
        "70 幾分，還有幾個問題沒處理乾淨...這樣也好意思？",
        "A 級不錯，但不是頂尖。你滿足於「不錯」嗎？笨蛋！",
        "快到頂了卻沒到頂...最後一哩路都不想走？真遺憾！",
    ],
    "B": [
        "B 級...中規中矩的平庸表現。你甘於平庸嗎？哼！",
        "50-69 分，勉強及格的邊緣...這種分數也敢拿出來？",
        "B 級就是「普通」的意思，普通到讓人提不起勁評論！",
        "剛好在及格線上掙扎...你的目標就這麼低嗎？笨蛋！",
    ],
    "C": [
        "C 級...問題一堆，這網站是認真在經營的嗎？讓人懷疑！",
        "30-49 分，不及格。SEO 基本功都沒做好，太混了！哼！",
        "這個分數...說實話，改都不知道從哪裡改起！真慘！",
        "C 級...不是想打擊你，但這真的很糟糕！快醒醒！笨蛋！",
    ],
    "F": [
        "F 級！不及格中的不及格！這網站是來搞笑的嗎！",
        "這個分數...你確定這是正式上線的網站？太離譜了！哼！",
        "F 級...說你是 SEO 災難一點都不誇張！可悲！",
        "0-29 分，基本上是從零開始。你之前在幹嘛？笨蛋！",
        "F 級...雖然很想幫你，但這個爛攤子真的讓人頭痛！哼！",
    ],
}

# 錯誤訊息（毒舌+傲嬌風格）
ERROR_ROASTS = {
    "timeout": [
        "網站回應太慢，等到我都想睡了！Core Web Vitals 肯定爆炸！笨蛋！",
        "Timeout！15 秒都連不上...這網站是用撥接上網嗎？太落伍了！哼！",
        "回應時間長到像在等冰川融化...用戶早就跑光了！活該！",
    ],
    "ssl_error": [
        "SSL 憑證有問題！瀏覽器會顯示大大的「不安全」喔！你想嚇跑用戶嗎！",
        "HTTPS 憑證壞了...這比 SEO 還嚴重！趕快處理！笨蛋！",
        "SSL 錯誤...連基本的安全都搞不定，談什麼 SEO？先活下來再說！哼！",
    ],
    "connection_error": [
        "連不上網站！是網址打錯還是主機掛了？總之你的問題比 SEO 還大！",
        "連線失敗...網站都連不上，SEO 再好有什麼用？笨蛋！先讓網站活著！",
        "完全連不上...你確定這網站還存在嗎？讓人懷疑！哼！",
    ],
    "http_error": [
        "HTTP 錯誤！網站在噴錯誤碼...先讓網站正常運作再談 SEO 吧！笨蛋！",
        "收到錯誤回應...這網站比 SEO 問題更早該處理的事情還很多！哼！",
    ],
    "unknown": [
        "發生未知錯誤...你的網站太特別了，特別到我都分析不了！厲害啊！哼！",
        "出了奇怪的問題...不知道該說網站獨特還是該說寫得太爛了！笨蛋！",
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
