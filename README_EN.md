# SEO Roaster

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg)](https://flask.palletsprojects.com/)

[<- Back to Muripo HQ](https://tznthou.github.io/muripo-hq/) | [Chinese](README.md)

Enter a URL, get a brutally honest SEO analysis report. Improve your website through savage roasts.

![SEO Roaster Demo](assets/demo.png)

> **Warning**
> The roasts are for entertainment, but the SEO advice is real.

---

## Features

- **20 SEO Checks**: Covers fundamentals, social, structured data, and more
- **Savage Tsundere Roasts**: Each issue comes with brutal + tsundere style commentary
- **Grade System**: S/A/B/C/F ratings with overall assessment
- **Contrast Cute UI**: Cute pink appearance × savage tsundere content (gap moe)
- **Zero Frontend Dependencies**: Pure HTML/CSS/JS, no npm required

---

## Checks Performed

### Basic SEO (10 items)

| Check | Description | Weight |
|-------|-------------|--------|
| Title | Existence + length check | 8% |
| Meta Description | Existence + length check | 8% |
| Canonical | Prevent duplicate content | 5% |
| Viewport | Mobile device support | 4% |
| Lang | Language attribute | 3% |
| H1 | Count check (should be 1) | 6% |
| HTTPS | Secure protocol | 8% |
| Robots | noindex status | 4% |
| Favicon | Site icon | 2% |
| Image Alt | Alt attribute coverage | 5% |

### Social Sharing (4 items)

| Check | Description | Weight |
|-------|-------------|--------|
| og:title | Open Graph title | 4% |
| og:description | Open Graph description | 4% |
| og:image | Open Graph image | 4% |
| Twitter Card | Twitter sharing card | 3% |

### Structured Data (3 items)

| Check | Description | Weight |
|-------|-------------|--------|
| JSON-LD | Structured data existence | 8% |
| Schema Types | Schema type identification | 4% |
| Schema Valid | JSON format validation | 4% |

### Advanced (3 items)

| Check | Description | Weight |
|-------|-------------|--------|
| hreflang | Multi-language markup | 4% |
| Published Time | Publication date markup | 4% |
| Snippet Control | AI snippet control | 3% |

---

## Grading Scale

| Grade | Score Range | Roast Level |
|-------|-------------|-------------|
| **S** | 90-100 | Reluctant approval ("Fine, you pass...") |
| **A** | 70-89 | Minor mockery ("Almost there, dummy!") |
| **B** | 50-69 | Medium roast ("So mediocre...") |
| **C** | 30-49 | Heavy roast ("What a mess!") |
| **F** | 0-29 | Total destruction ("Idiot!") |

---

## Roast Examples

**Missing Title:**
> "No title? This kindergarten-level mistake... Hmph, it's not like I want to help you!"

**Missing Meta Description:**
> "No description? Letting Google randomly grab content as your intro? Gambling, are we!"

**Wrong H1 Count:**
> "3 H1s? Are you holding a press conference where everyone's the headline? Idiot!"

**No HTTPS:**
> "Still using HTTP? It's 2025, your security is stuck in the stone age!"

---

## Tech Stack

| Technology | Purpose | Notes |
|------------|---------|-------|
| Python 3.11+ | Runtime | Managed with uv |
| Flask | Web Framework | Lightweight |
| BeautifulSoup4 | HTML Parsing | With lxml |
| Gunicorn | WSGI Server | Production |

---

## Security Updates

> **Updated**: 2025-12-18

This project has been patched for the following security issues and is safe for production deployment.

### 🔴 Critical (Fixed)

| Issue | Description | Fix |
|-------|-------------|-----|
| **SSRF Vulnerability** | Users could input internal IPs to access intranet resources | Added IP blocklist validation, DNS rebinding protection, redirect verification |
| **XSS Vulnerability** | Frontend innerHTML without escaping could execute malicious scripts | All dynamic content processed through `escapeHTML()` |

### 🟠 High Priority (Fixed)

| Issue | Description | Fix |
|-------|-------------|-----|
| **No URL Length Limit** | Could cause DoS or ReDoS | Frontend `maxlength="2048"`, backend validation |
| **No Rate Limiting** | Could be abused for attacks | Custom rate limiter, max 10 requests per minute |
| **No URL Format Validation** | Invalid inputs waste resources | Frontend regex validation |
| **Error Message Leakage** | Could expose internal paths | Unified error messages, detailed info logged |

### 🟡 Medium Priority (Fixed)

| Issue | Description | Fix |
|-------|-------------|-----|
| **Timeout Too Long** | 15 seconds made users wait too long | Adjusted to 8 seconds |
| **HTML Parsing Could Fail** | lxml might crash on malformed HTML | Added fallback to html.parser |
| **No Logging** | Unable to track errors | Added logging configuration |

### 🟢 Low Priority (Fixed)

| Issue | Description | Fix |
|-------|-------------|-----|
| **Magic Numbers** | Thresholds scattered throughout code | Extracted to class constants |
| **Animation Delay Accumulation** | Too long delay with many items | Max delay capped at 1 second |
| **Inconsistent Ports** | Different default ports in different files | Unified to 8080 |

---

## Technical Limitations

This is a **single-page crawler** with the following limitations:

| Limitation | Description |
|------------|-------------|
| **Single Page Only** | Only fetches the URL you enter, no recursive site crawling |
| **HTML Only** | Cannot analyze JavaScript-rendered content (SPA sites may be inaccurate) |
| **No Speed Detection** | Core Web Vitals (LCP, INP, CLS) require a real browser |
| **No Behavioral Signals** | CTR, Dwell Time, Bounce Rate are Google's internal data |
| **No Backlink Analysis** | Requires third-party APIs (Ahrefs, Moz, etc.) |
| **No Ranking Data** | Requires Google Search Console access |
| **8s Timeout** | Slow-responding sites will be marked as connection failure |

**What this tool CAN do**: Check HTML-based SEO fundamentals (tags, structured data, social sharing)

**What this tool CANNOT do**: Full SEO audit (requires professional tools like Screaming Frog, Ahrefs)

---

## Quick Start

### Local Development

```bash
# Enter project directory
cd day-20-seo-roaster

# Install dependencies
uv sync

# Start development server
uv run python -m src.seo_roaster.app

# Or use Flask CLI
uv run flask --app src.seo_roaster.app run --debug
```

Open browser at `http://localhost:5000`

### Production

```bash
# Using Gunicorn
uv run gunicorn --bind 0.0.0.0:8000 src.seo_roaster.app:app
```

---

## Deploy to Zeabur

### Step 1: Create Project

1. Login to [Zeabur](https://zeabur.com/)
2. Create a new project

### Step 2: Deploy Service

1. Choose "Git" deployment method
2. Connect your GitHub Repository
3. Select this project folder
4. Zeabur will auto-detect Python project and deploy

### Step 3: Configure Domain

1. Go to service settings
2. Add domain in "Networking"
3. Use free `.zeabur.app` subdomain

---

## Project Structure

```
day-20-seo-roaster/
├── src/
│   └── seo_roaster/
│       ├── __init__.py
│       ├── app.py              # Flask main app
│       ├── analyzer.py         # SEO analysis logic
│       ├── roasts.py           # Roast content library
│       ├── templates/
│       │   └── index.html      # Frontend page
│       └── static/
│           └── style.css       # Cute pink theme styles
├── pyproject.toml
├── Procfile                    # Gunicorn config
├── README.md
├── README_EN.md
└── LICENSE
```

---

## Customization Guide

### Adding New Checks

Add weight to `WEIGHTS` dict in `analyzer.py`, then implement corresponding `_check_xxx` method:

```python
WEIGHTS = {
    "your_new_check": 5,  # Add weight
    # ...
}

def _check_your_new_check(self, soup: BeautifulSoup) -> dict:
    # Implement check logic
    return {
        "passed": True,  # or False
        "message": "some_message",
        "value": "detected_value",
    }
```

### Adding Roasts

Add content to `ROASTS` dict in `roasts.py`:

```python
ROASTS = {
    "your_new_check": {
        "missing": [
            "Roast 1",
            "Roast 2",
            "Roast 3",
        ],
        "some_other_issue": [
            "Other roasts...",
        ],
    },
    # ...
}
```

### Modifying UI Style

Edit CSS variables in `static/style.css`:

```css
:root {
    --bg-cream: #fff5f8;         /* Cream pink background */
    --accent-pink: #ff6b9d;      /* Primary pink accent */
    --accent-coral: #ff8fab;     /* Coral pink */
    --success-mint: #7dd3a8;     /* Passed items mint green */
    /* ... */
}
```

---

## SEO Knowledge Sources

This tool's checks reference:

- Google Search Central official documentation
- Web.dev best practices
- Schema.org structured data specs
- Community practical experience

**Important Disclaimers**:
- Check thresholds (like Title 55-60 chars) are guidelines, not hard rules
- llms.txt is a community proposal, not official Google mechanism
- Behavioral signals (CTR, Dwell Time) cannot be detected from frontend

---

## Thoughts

### What Even Is SEO?

Today I randomly asked myself: What even is SEO?

Why do we do SEO? What does it actually help us with? Can SEO be quantified? Why is everyone so eager to get their SEO right?

Of course, SEO matters—who doesn't want their website to rank at the top of search results?

But practically speaking, what is SEO?

It's just Google's ranking order.

### The "Experience Value" Collection

Have you noticed that Google's ranking algorithm changes every year? Those rules like "Title should be 55-60 characters" or "Only one H1 per page" are actually experience values that people reverse-engineered from ranking results after spending countless hours.

Are these experience values accurate? Maybe. Maybe not.

Google has never publicly stated these numbers. We just noticed "websites that do this seem to rank better," then compiled them into one SEO checklist after another.

So what this tool checks isn't really "rules"—it's more like a "community-curated experience value collection."

### Why Roast?

Just doing plain SEO analysis on webpages seemed... boring.

So I thought, what if I turned cold detection reports into savage roasts? That would be more interesting, right?

Turns out: getting roasted is actually motivating.

### For Vibe Coders

The core of this project is simple:
1. `requests` fetches webpages
2. `BeautifulSoup` parses HTML
3. A bunch of `if-else` statements
4. A bunch of savage strings

No AI, no machine learning, no blockchain. Just basic Python and maximum roast.

---

## License

This project is licensed under the [MIT License](LICENSE).
