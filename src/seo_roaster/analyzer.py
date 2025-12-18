"""SEO 分析器 - 解析網頁 HTML 並檢測 SEO 元素"""

import ipaddress
import json
import logging
import re
import socket
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# 設定日誌
logger = logging.getLogger(__name__)


class SEOAnalyzer:
    """SEO 分析器"""

    # SEO 閾值常數
    TITLE_MIN_LENGTH = 10
    TITLE_MAX_LENGTH = 70
    META_DESC_MIN_LENGTH = 50
    META_DESC_MAX_LENGTH = 160
    IMAGE_ALT_LOW_THRESHOLD = 0.5
    IMAGE_ALT_MEDIUM_THRESHOLD = 0.8
    MAX_REDIRECTS = 5

    # 各項目的權重（總和 = 100）
    WEIGHTS = {
        "title": 8,
        "meta_description": 8,
        "canonical": 5,
        "viewport": 4,
        "lang": 3,
        "h1": 6,
        "https": 8,
        "robots": 4,
        "favicon": 2,
        "img_alt": 5,
        "og_title": 4,
        "og_description": 4,
        "og_image": 4,
        "twitter_card": 3,
        "json_ld": 8,
        "json_ld_types": 4,
        "json_ld_valid": 4,
        "hreflang": 4,
        "published_time": 4,
        "snippet_control": 3,
    }

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SEORoaster/1.0; +https://github.com/tznthou/seo-roaster)"
        }

    def _is_safe_ip(self, ip_str: str) -> bool:
        """
        檢查 IP 是否安全（非內部網路）

        Args:
            ip_str: IP 位址字串

        Returns:
            bool: True 表示安全，False 表示危險
        """
        try:
            ip = ipaddress.ip_address(ip_str)
            # 阻擋私有網路、本地迴環、保留 IP、連結本地
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                return False
            # 阻擋 AWS/GCP metadata endpoint
            if ip_str.startswith("169.254."):
                return False
            return True
        except ValueError:
            return False

    def _validate_url(self, url: str, redirect_count: int = 0) -> str:
        """
        驗證 URL 安全性（SSRF 防護）

        Args:
            url: 要驗證的 URL
            redirect_count: 重定向計數（防止無限迴圈）

        Returns:
            str: 驗證後的 URL

        Raises:
            ValueError: URL 不安全或無效
        """
        if redirect_count > self.MAX_REDIRECTS:
            raise ValueError("重定向次數過多")

        # 確保 URL 有 scheme
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)

        # 只允許 http/https
        if parsed.scheme not in ("http", "https"):
            raise ValueError("只支援 HTTP/HTTPS 協定")

        hostname = parsed.hostname
        if not hostname:
            raise ValueError("無效的網址")

        # 阻擋 file:// 等協定
        if parsed.scheme == "file":
            raise ValueError("不支援本地檔案存取")

        # 檢查是否為 IP 位址
        try:
            ip = ipaddress.ip_address(hostname)
            if not self._is_safe_ip(str(ip)):
                raise ValueError("不允許存取內部網路位址")
        except ValueError:
            # 不是 IP，是域名，進行 DNS 解析檢查
            try:
                resolved_ip = socket.gethostbyname(hostname)
                if not self._is_safe_ip(resolved_ip):
                    raise ValueError("域名解析到內部網路位址，已阻擋")
            except socket.gaierror:
                raise ValueError("無法解析域名")

        return url

    def fetch_html(self, url: str) -> tuple[str, str, int]:
        """
        抓取網頁 HTML（含 SSRF 防護）

        Returns:
            tuple: (html, final_url, status_code)

        Raises:
            ValueError: URL 不安全
            requests.exceptions.*: 網路相關錯誤
        """
        # SSRF 防護：驗證 URL
        url = self._validate_url(url)

        # 先不自動重定向，手動檢查每個重定向目標
        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout,
            allow_redirects=False,
        )

        # 處理重定向
        redirect_count = 0
        current_url = url
        while response.status_code in (301, 302, 303, 307, 308):
            redirect_count += 1
            if redirect_count > self.MAX_REDIRECTS:
                raise ValueError("重定向次數過多")

            redirect_url = response.headers.get("Location")
            if not redirect_url:
                break

            # 處理相對路徑重定向（如 "/path" 或 "../page"）
            redirect_url = urljoin(current_url, redirect_url)

            # 驗證重定向目標
            redirect_url = self._validate_url(redirect_url, redirect_count)
            current_url = redirect_url

            response = requests.get(
                redirect_url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=False,
            )

        response.raise_for_status()
        return response.text, response.url, response.status_code

    def analyze(self, url: str) -> dict:
        """
        分析網站 SEO

        Returns:
            dict: 分析結果
        """
        try:
            html, final_url, status_code = self.fetch_html(url)
        except ValueError as e:
            # SSRF 防護或 URL 驗證錯誤
            return {"error": "invalid_url", "message": str(e)}
        except requests.exceptions.Timeout:
            return {"error": "timeout", "message": "網站回應太慢，可能在睡覺"}
        except requests.exceptions.SSLError:
            return {"error": "ssl_error", "message": "SSL 憑證有問題，安全性堪憂"}
        except requests.exceptions.ConnectionError:
            return {"error": "connection_error", "message": "連不上網站，確定網址沒打錯？"}
        except requests.exceptions.HTTPError as e:
            # 不洩露完整錯誤，只回傳狀態碼
            status_code = e.response.status_code if e.response else "未知"
            return {"error": "http_error", "message": f"HTTP 錯誤：{status_code}"}
        except Exception as e:
            # 記錄完整錯誤到日誌，但只回傳通用訊息給使用者
            logger.error(f"Unexpected error analyzing {url}: {str(e)}", exc_info=True)
            return {"error": "unknown", "message": "發生未知錯誤，請稍後再試"}

        # HTML 解析（lxml 失敗時改用 html.parser）
        try:
            soup = BeautifulSoup(html, "lxml")
        except Exception as e:
            logger.warning(f"lxml parser failed, falling back to html.parser: {e}")
            soup = BeautifulSoup(html, "html.parser")

        parsed_url = urlparse(final_url)

        # 執行所有檢測
        results = {
            "url": final_url,
            "status_code": status_code,
            "is_https": parsed_url.scheme == "https",
            "checks": {},
            "score": 0,
            "grade": "F",
            "issues": [],
            "passed": [],
        }

        # 執行各項檢測
        checks = [
            ("title", self._check_title(soup)),
            ("meta_description", self._check_meta_description(soup)),
            ("canonical", self._check_canonical(soup)),
            ("viewport", self._check_viewport(soup)),
            ("lang", self._check_lang(soup)),
            ("h1", self._check_h1(soup)),
            ("https", self._check_https(parsed_url)),
            ("robots", self._check_robots(soup)),
            ("favicon", self._check_favicon(soup)),
            ("img_alt", self._check_img_alt(soup)),
            ("og_title", self._check_og_tag(soup, "og:title")),
            ("og_description", self._check_og_tag(soup, "og:description")),
            ("og_image", self._check_og_tag(soup, "og:image")),
            ("twitter_card", self._check_twitter_card(soup)),
            ("json_ld", self._check_json_ld(soup)),
            ("json_ld_types", self._check_json_ld_types(soup)),
            ("json_ld_valid", self._check_json_ld_valid(soup)),
            ("hreflang", self._check_hreflang(soup)),
            ("published_time", self._check_published_time(soup)),
            ("snippet_control", self._check_snippet_control(soup)),
        ]

        total_score = 0
        for check_name, check_result in checks:
            results["checks"][check_name] = check_result
            weight = self.WEIGHTS.get(check_name, 5)

            if check_result["passed"]:
                total_score += weight
                results["passed"].append(check_name)
            else:
                results["issues"].append({
                    "key": check_name,
                    "message": check_result.get("message", ""),
                    "value": check_result.get("value"),
                    "weight": weight,
                })

        results["score"] = total_score
        results["grade"] = self._calculate_grade(total_score)

        return results

    def _calculate_grade(self, score: int) -> str:
        """計算等級"""
        if score >= 90:
            return "S"
        elif score >= 70:
            return "A"
        elif score >= 50:
            return "B"
        elif score >= 30:
            return "C"
        else:
            return "F"

    def _check_title(self, soup: BeautifulSoup) -> dict:
        """檢查 title 標籤"""
        title = soup.find("title")
        if not title:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        # 使用 get_text() 而非 .string，避免 title 有子元素時回傳 None
        title_text = title.get_text(strip=True)
        length = len(title_text)

        if length == 0:
            return {
                "passed": False,
                "message": "empty",
                "value": "",
            }
        elif length < self.TITLE_MIN_LENGTH:
            return {
                "passed": False,
                "message": "too_short",
                "value": title_text,
                "length": length,
            }
        elif length > self.TITLE_MAX_LENGTH:
            return {
                "passed": False,
                "message": "too_long",
                "value": title_text,
                "length": length,
            }

        return {
            "passed": True,
            "value": title_text,
            "length": length,
        }

    def _check_meta_description(self, soup: BeautifulSoup) -> dict:
        """檢查 meta description"""
        meta = soup.find("meta", attrs={"name": "description"})
        if not meta:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        content = meta.get("content", "").strip()
        length = len(content)

        if length == 0:
            return {
                "passed": False,
                "message": "empty",
                "value": "",
            }
        elif length < self.META_DESC_MIN_LENGTH:
            return {
                "passed": False,
                "message": "too_short",
                "value": content,
                "length": length,
            }
        elif length > self.META_DESC_MAX_LENGTH:
            return {
                "passed": False,
                "message": "too_long",
                "value": content,
                "length": length,
            }

        return {
            "passed": True,
            "value": content,
            "length": length,
        }

    def _check_canonical(self, soup: BeautifulSoup) -> dict:
        """檢查 canonical 標籤"""
        canonical = soup.find("link", attrs={"rel": "canonical"})
        if not canonical:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        href = canonical.get("href", "").strip()
        if not href:
            return {
                "passed": False,
                "message": "empty",
                "value": "",
            }

        return {
            "passed": True,
            "value": href,
        }

    def _check_viewport(self, soup: BeautifulSoup) -> dict:
        """檢查 viewport 設定"""
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if not viewport:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        content = viewport.get("content", "").strip()
        if not content:
            return {
                "passed": False,
                "message": "empty",
                "value": "",
            }

        return {
            "passed": True,
            "value": content,
        }

    def _check_lang(self, soup: BeautifulSoup) -> dict:
        """檢查 html lang 屬性"""
        html = soup.find("html")
        if not html:
            return {
                "passed": False,
                "message": "no_html_tag",
                "value": None,
            }

        lang = html.get("lang", "").strip()
        if not lang:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        return {
            "passed": True,
            "value": lang,
        }

    def _check_h1(self, soup: BeautifulSoup) -> dict:
        """檢查 H1 標籤"""
        h1_tags = soup.find_all("h1")
        count = len(h1_tags)

        if count == 0:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
                "count": 0,
            }
        elif count > 1:
            return {
                "passed": False,
                "message": "multiple",
                "value": [h1.get_text(strip=True)[:50] for h1 in h1_tags],
                "count": count,
            }

        h1_text = h1_tags[0].get_text(strip=True)
        if not h1_text:
            return {
                "passed": False,
                "message": "empty",
                "value": "",
                "count": 1,
            }

        return {
            "passed": True,
            "value": h1_text,
            "count": 1,
        }

    def _check_https(self, parsed_url) -> dict:
        """檢查 HTTPS"""
        is_https = parsed_url.scheme == "https"
        return {
            "passed": is_https,
            "message": "http_only" if not is_https else None,
            "value": parsed_url.scheme,
        }

    def _check_robots(self, soup: BeautifulSoup) -> dict:
        """檢查 robots meta"""
        robots = soup.find("meta", attrs={"name": "robots"})
        if not robots:
            # 沒有 robots meta 標籤是正常的（預設可索引）
            return {
                "passed": True,
                "value": "default (index, follow)",
            }

        content = robots.get("content", "").lower()
        if "noindex" in content:
            return {
                "passed": False,
                "message": "noindex",
                "value": content,
            }

        return {
            "passed": True,
            "value": content,
        }

    def _check_favicon(self, soup: BeautifulSoup) -> dict:
        """檢查 favicon"""
        # 檢查多種 favicon 格式
        favicon_selectors = [
            {"rel": "icon"},
            {"rel": "shortcut icon"},
            {"rel": "apple-touch-icon"},
        ]

        for selector in favicon_selectors:
            favicon = soup.find("link", attrs=selector)
            if favicon and favicon.get("href"):
                return {
                    "passed": True,
                    "value": favicon.get("href"),
                }

        return {
            "passed": False,
            "message": "missing",
            "value": None,
        }

    def _check_img_alt(self, soup: BeautifulSoup) -> dict:
        """檢查圖片 alt 屬性"""
        images = soup.find_all("img")
        if not images:
            # 沒有圖片，跳過此檢測
            return {
                "passed": True,
                "value": "no_images",
                "total": 0,
                "with_alt": 0,
            }

        total = len(images)
        with_alt = sum(1 for img in images if img.get("alt", "").strip())
        ratio = with_alt / total if total > 0 else 0

        if ratio < self.IMAGE_ALT_LOW_THRESHOLD:
            return {
                "passed": False,
                "message": "low_ratio",
                "value": f"{with_alt}/{total}",
                "total": total,
                "with_alt": with_alt,
                "ratio": ratio,
            }
        elif ratio < self.IMAGE_ALT_MEDIUM_THRESHOLD:
            return {
                "passed": False,
                "message": "medium_ratio",
                "value": f"{with_alt}/{total}",
                "total": total,
                "with_alt": with_alt,
                "ratio": ratio,
            }

        return {
            "passed": True,
            "value": f"{with_alt}/{total}",
            "total": total,
            "with_alt": with_alt,
            "ratio": ratio,
        }

    def _check_og_tag(self, soup: BeautifulSoup, property_name: str) -> dict:
        """檢查 Open Graph 標籤"""
        og = soup.find("meta", attrs={"property": property_name})
        if not og:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        content = og.get("content", "").strip()
        if not content:
            return {
                "passed": False,
                "message": "empty",
                "value": "",
            }

        return {
            "passed": True,
            "value": content[:100] + "..." if len(content) > 100 else content,
        }

    def _check_twitter_card(self, soup: BeautifulSoup) -> dict:
        """檢查 Twitter Card"""
        twitter = soup.find("meta", attrs={"name": "twitter:card"})
        if not twitter:
            # 也接受 property 形式
            twitter = soup.find("meta", attrs={"property": "twitter:card"})

        if not twitter:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
            }

        content = twitter.get("content", "").strip()
        return {
            "passed": True,
            "value": content,
        }

    def _check_json_ld(self, soup: BeautifulSoup) -> dict:
        """檢查 JSON-LD 存在"""
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        if not scripts:
            return {
                "passed": False,
                "message": "missing",
                "value": None,
                "count": 0,
            }

        return {
            "passed": True,
            "value": f"{len(scripts)} schema(s) found",
            "count": len(scripts),
        }

    def _check_json_ld_types(self, soup: BeautifulSoup) -> dict:
        """檢查 JSON-LD 類型"""
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        if not scripts:
            return {
                "passed": False,
                "message": "no_schema",
                "value": None,
            }

        types = []
        for script in scripts:
            try:
                data = json.loads(script.string or "{}")
                if isinstance(data, list):
                    for item in data:
                        if "@type" in item:
                            types.append(item["@type"])
                elif "@type" in data:
                    types.append(data["@type"])
                elif "@graph" in data:
                    for item in data["@graph"]:
                        if "@type" in item:
                            types.append(item["@type"])
            except json.JSONDecodeError:
                continue

        if not types:
            return {
                "passed": False,
                "message": "no_types",
                "value": None,
            }

        return {
            "passed": True,
            "value": types,
        }

    def _check_json_ld_valid(self, soup: BeautifulSoup) -> dict:
        """檢查 JSON-LD 格式是否有效"""
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        if not scripts:
            return {
                "passed": False,
                "message": "no_schema",
                "value": None,
            }

        valid_count = 0
        invalid_count = 0

        for script in scripts:
            try:
                json.loads(script.string or "{}")
                valid_count += 1
            except json.JSONDecodeError:
                invalid_count += 1

        if invalid_count > 0:
            return {
                "passed": False,
                "message": "invalid_json",
                "value": f"{invalid_count} invalid schema(s)",
                "valid": valid_count,
                "invalid": invalid_count,
            }

        return {
            "passed": True,
            "value": f"All {valid_count} schema(s) valid",
            "valid": valid_count,
            "invalid": 0,
        }

    def _check_hreflang(self, soup: BeautifulSoup) -> dict:
        """檢查 hreflang 標籤"""
        hreflangs = soup.find_all("link", attrs={"rel": "alternate", "hreflang": True})
        if not hreflangs:
            # hreflang 不是必須的，只是加分項
            return {
                "passed": True,
                "message": "not_applicable",
                "value": "No hreflang (single language site)",
            }

        langs = [link.get("hreflang") for link in hreflangs]
        return {
            "passed": True,
            "value": langs,
        }

    def _check_published_time(self, soup: BeautifulSoup) -> dict:
        """檢查發布時間標記"""
        # 檢查 article:published_time
        published = soup.find("meta", attrs={"property": "article:published_time"})
        if published and published.get("content"):
            return {
                "passed": True,
                "value": published.get("content"),
            }

        # 檢查 article:modified_time
        modified = soup.find("meta", attrs={"property": "article:modified_time"})
        if modified and modified.get("content"):
            return {
                "passed": True,
                "value": modified.get("content"),
            }

        # 檢查 datePublished in JSON-LD
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        for script in scripts:
            try:
                data = json.loads(script.string or "{}")
                if "datePublished" in data:
                    return {
                        "passed": True,
                        "value": data["datePublished"],
                    }
                if "@graph" in data:
                    for item in data["@graph"]:
                        if "datePublished" in item:
                            return {
                                "passed": True,
                                "value": item["datePublished"],
                            }
            except json.JSONDecodeError:
                continue

        return {
            "passed": False,
            "message": "missing",
            "value": None,
        }

    def _check_snippet_control(self, soup: BeautifulSoup) -> dict:
        """檢查 AI 摘要控制"""
        robots = soup.find("meta", attrs={"name": "robots"})
        if not robots:
            # 沒有特別設定，表示允許所有摘要
            return {
                "passed": True,
                "value": "default (allow all)",
            }

        content = robots.get("content", "").lower()

        # 檢查各種 snippet 控制
        controls = []
        if "nosnippet" in content:
            controls.append("nosnippet")
        if "max-snippet" in content:
            match = re.search(r"max-snippet:(-?\d+)", content)
            if match:
                controls.append(f"max-snippet:{match.group(1)}")

        if controls:
            return {
                "passed": True,
                "value": ", ".join(controls),
            }

        return {
            "passed": True,
            "value": "default (allow all)",
        }
