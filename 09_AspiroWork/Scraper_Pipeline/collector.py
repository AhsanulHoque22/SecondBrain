"""Stage 1 — Collect.

Fetches raw HTML for a URL and caches it to disk as an immutable snapshot,
so extraction can be re-run without re-hitting the network.

Sites behind Cloudflare/WAF bot-protection (e.g. mastersportal.com,
ox.ac.uk) return 403 to a plain `requests` call even with a real
User-Agent — confirmed while building this pipeline. On a 403 this stage
now automatically retries once with a headless browser (Playwright), which
executes the page's JS and clears most Cloudflare "checking your browser"
challenges. If Playwright isn't installed, or the fallback is also
blocked, the URL is reported as FAILED and the batch keeps going.
"""

from __future__ import annotations  #Allows using modern type hints without immediately evaluating them.
import hashlib                      #generate unique filename from URL
import json                         #save metadata
import sys                          #stderr logging for the playwright fallback
import time                         #timestamps and retry delays
from dataclasses import dataclass   #easy data container
from pathlib import Path            #safer file handling

import requests                     #Used to make HTTP requests.

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
) #Pretends to be a normal Chrome browser. Without this: requests.get(url) many sites block the request.

DEFAULT_TIMEOUT = 15
MAX_RETRIES = 2

#Custom Exception
class CollectionError(Exception):
    """Raised when a URL could not be fetched after retries."""


#Stores collection result
@dataclass
class Collected:
    url: str
    html: str
    raw_path: Path
    fetched_at: str


"""
Collected(
    url="https://example.com",
    html="<html>...</html>",
    raw_path="data/raw/a1b2c3.html",
    fetched_at="2026-07-11T12:00:00Z"
)
"""

#Creates unique ID for URL
def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]                 #only first 16 chars

#Headless-browser fallback, used only when plain requests gets a 403.
def fetch_html_playwright(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch HTML via a real (headless) browser so Cloudflare/WAF's JS
    challenge gets executed, instead of just sent a User-Agent string."""
    try:
        from playwright.sync_api import sync_playwright   #lazy import: only needed on the 403 fallback path
    except ImportError as exc:
        raise CollectionError(
            "Playwright not installed. Run: "
            "./.venv/bin/pip install playwright && ./.venv/bin/playwright install chromium"
        ) from exc

    timeout_ms = max(timeout, 30) * 1000   #headless nav + challenge wait needs more room than a plain GET
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(user_agent=USER_AGENT)
            page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
            except Exception:
                pass   #some pages keep background requests alive forever; content is ready either way
            return page.content()
        finally:
            browser.close()

#Main network function.
def fetch_html(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch raw HTML for a URL, retrying transient failures once."""
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}   #Makes request look more like a real browser.
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.RequestException as exc:                                #Handle Network Errors. Catches: timeout, connection refused, DNS failure
            last_error = exc
            time.sleep(1.5 * attempt)
            continue

        if response.status_code == 200:
            return response.text
        if response.status_code == 403:
            print(
                f"[collect] {url} returned 403 (likely bot-protected); retrying with headless browser",
                file=sys.stderr,
            )
            try:
                return fetch_html_playwright(url, timeout)
            except CollectionError:
                raise
            except Exception as exc:                                            #playwright's own errors (timeout, still blocked, etc.)
                raise CollectionError(
                    f"{url} returned 403 and the headless-browser fallback also failed: {exc}"
                ) from exc
        if response.status_code >= 500:
            last_error = CollectionError(f"{url} returned {response.status_code}")
            time.sleep(1.5 * attempt)
            continue

        raise CollectionError(f"{url} returned {response.status_code}")

    raise CollectionError(f"Failed to fetch {url} after {MAX_RETRIES} attempts: {last_error}")


def save_raw(url: str, html: str, raw_dir: Path) -> Path:   #Responsible for disk storage.
    raw_dir.mkdir(parents=True, exist_ok=True)              #Create Directory. Ex: data/raw/ created automaticllly 
    file_id = _url_hash(url)                                #Generate Filename
    html_path = raw_dir / f"{file_id}.html"                 #Ex: data/raw/9c4a1d82ab12ef45.html
    meta_path = raw_dir / f"{file_id}.meta.json"            #Ex: data/raw/9c4a1d82ab12ef45.meta.json

    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) #Ex: 2026-07-11T15:30:00Z

    #Save HTML -> Writes raw page source.
    html_path.write_text(html, encoding="utf-8")

    #Save Metadata -> Saved as JSON.
    meta_path.write_text(
        json.dumps({"url": url, "fetched_at": fetched_at}, indent=2), encoding="utf-8"
    )
    return html_path        #Returns location of saved HTML file.


#High-level orchestration function. This is the function users should call.
def collect(url: str, raw_dir: Path) -> Collected:
    html = fetch_html(url)                                              #Download Page
    raw_path = save_raw(url, html, raw_dir)                             #Store Page
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())     #Create timestamp.
    return Collected(url=url, html=html, raw_path=raw_path, fetched_at=fetched_at)



""""
Example Flow

Suppose:

result = collect(
    "https://example.com",
    Path("data/raw")
)
Fetch
GET https://example.com

↓

Save
data/raw/
 ├─ a8f19c2d4e7f1234.html
 └─ a8f19c2d4e7f1234.meta.json

↓

Return
Collected(
    url="https://example.com",
    html="<html>...</html>",
    raw_path=Path("data/raw/a8f19c2d4e7f1234.html"),
    fetched_at="2026-07-11T15:30:00Z"
)



Design Pattern Used

This follows a common ETL/Data Pipeline pattern:

Stage 1: Collect
        ↓
Stage 2: Extract
        ↓
Stage 3: Transform
        ↓
Stage 4: Load/Search/RAG

The key benefit is that network access happens only once. If your extraction logic changes, you can re-run extraction on the cached HTML files without hitting the website again.
"""
