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

There are two distinct kinds of "blocked" here, and this module tells them
apart (confirmed both actually happen, in the same session, against the
same site): a soft "checking your browser" JS challenge, which Playwright
clears on its own — vs. a hard Cloudflare block page ("Sorry, you have
been blocked"), which Playwright *fetches successfully* (200, real HTML)
but which isn't the page content at all. Treating that as a normal
successful fetch would silently cache a block page as if it were program
data. `HardBlockError` (a `CollectionError` subclass) exists so callers
can tell the two apart and back off harder on the real thing.
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


class HardBlockError(CollectionError):
    """Raised when the response is a Cloudflare/WAF hard-block page, not the
    real content. Distinct from a plain CollectionError so callers (e.g. the
    pipeline's batch loop) can apply a much longer cooldown than a normal
    retry — hitting this again immediately just deepens the block."""


# Text that only appears on an actual block page, never on real program
# content — confirmed against a real Cloudflare "Sorry, you have been
# blocked" page during development. Deliberately narrow (exact phrases, not
# just "blocked" or "cloudflare") to avoid ever mistaking real content for
# a block page.
HARD_BLOCK_MARKERS = (
    "Sorry, you have been blocked",
    "Attention Required! | Cloudflare",
    "cf-error-details",
)


def _is_hard_block(html: str) -> bool:
    return any(marker in html for marker in HARD_BLOCK_MARKERS)


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
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):                #transient nav failures happen (network blips) — same retry budget as the requests path
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    page = browser.new_page(user_agent=USER_AGENT)
                    page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                    try:
                        page.wait_for_load_state("networkidle", timeout=timeout_ms)
                    except Exception:
                        pass   #some pages keep background requests alive forever; content is ready either way
                    html = page.content()
                finally:
                    browser.close()
            # A hard block still returns a 200 with real HTML — a Cloudflare
            # block page, not the site's content. Playwright "succeeding"
            # here is not the same thing as the fetch actually working.
            if _is_hard_block(html):
                last_error = HardBlockError(f"{url} returned a Cloudflare hard-block page")
                time.sleep(1.5 * attempt)
                continue
            return html
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * attempt)

    if isinstance(last_error, HardBlockError):
        raise last_error
    raise CollectionError(f"Headless-browser fetch of {url} failed after {MAX_RETRIES} attempts: {last_error}")

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
            if _is_hard_block(response.text):   #block pages are usually served as 403, but not guaranteed
                raise HardBlockError(f"{url} returned a Cloudflare hard-block page (status 200)")
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
        if response.status_code == 429:
            # The one status code that most needs a backoff, not an
            # immediate failure — previously fell through to the final
            # `raise` below with zero retry. Honor Retry-After when the
            # server sends one; otherwise back off same as a 5xx.
            retry_after = response.headers.get("Retry-After")
            wait = float(retry_after) if retry_after and retry_after.strip().isdigit() else 1.5 * attempt
            print(
                f"[collect] {url} returned 429 (rate limited); waiting {wait:.1f}s before retry",
                file=sys.stderr,
            )
            last_error = CollectionError(f"{url} returned 429 (rate limited)")
            time.sleep(wait)
            continue

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
