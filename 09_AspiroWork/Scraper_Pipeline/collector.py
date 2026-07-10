"""Stage 1 — Collect.

Fetches raw HTML for a URL and caches it to disk as an immutable snapshot,
so extraction can be re-run without re-hitting the network.

Known limitation: sites behind Cloudflare/WAF bot-protection (e.g.
mastersportal.com, ox.ac.uk) return 403 to a plain `requests` call even with
a real User-Agent — this was confirmed while building this pipeline. A
headless-browser fallback (Playwright) would clear that, but is a deliberate
non-goal here to keep this stage to one job: fetch and cache.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path

import requests

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
DEFAULT_TIMEOUT = 15
MAX_RETRIES = 2


class CollectionError(Exception):
    """Raised when a URL could not be fetched after retries."""


@dataclass
class Collected:
    url: str
    html: str
    raw_path: Path
    fetched_at: str


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def fetch_html(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch raw HTML for a URL, retrying transient failures once."""
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(1.5 * attempt)
            continue

        if response.status_code == 200:
            return response.text
        if response.status_code == 403:
            raise CollectionError(
                f"{url} returned 403 (likely bot-protected — Cloudflare/WAF). "
                "This collector does not include a headless-browser fallback."
            )
        if response.status_code >= 500:
            last_error = CollectionError(f"{url} returned {response.status_code}")
            time.sleep(1.5 * attempt)
            continue

        raise CollectionError(f"{url} returned {response.status_code}")

    raise CollectionError(f"Failed to fetch {url} after {MAX_RETRIES} attempts: {last_error}")


def save_raw(url: str, html: str, raw_dir: Path) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    file_id = _url_hash(url)
    html_path = raw_dir / f"{file_id}.html"
    meta_path = raw_dir / f"{file_id}.meta.json"

    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    html_path.write_text(html, encoding="utf-8")
    meta_path.write_text(
        json.dumps({"url": url, "fetched_at": fetched_at}, indent=2), encoding="utf-8"
    )
    return html_path


def collect(url: str, raw_dir: Path) -> Collected:
    html = fetch_html(url)
    raw_path = save_raw(url, html, raw_dir)
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return Collected(url=url, html=html, raw_path=raw_path, fetched_at=fetched_at)
