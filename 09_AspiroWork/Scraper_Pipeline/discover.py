"""Stage 0 — Discover.

Given a mastersportal.com search/listing page URL, extracts the individual
program-page links on it (and optionally walks `page=2..N` of the same
search) and writes them one per line to a URL list file — ready to feed
straight into `pipeline.py --url-file`.

Reuses collector.fetch_html (same requests -> 403 -> headless-browser
fallback as the main pipeline) rather than a separate fetch path. Listing
pages are client-rendered, but the program links are present in the fetched
HTML as embedded JSON data, not <a href="..."> tags — the regex below
matches the bare "/studies/<id>/<slug>.html" substring so it finds them
either way.

Usage:
    python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands"
    python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands" --pages 5 --output urls.txt
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

from collector import CollectionError, fetch_html

PROGRAM_LINK_PATTERN = re.compile(r"/studies/\d+/[a-zA-Z0-9-]+\.html")
PAGE_FETCH_DELAY = 1.5  # seconds between listing-page fetches — politeness, not a hard requirement


def extract_program_links(html: str, base_url: str) -> list[str]:
    """Pull unique program-page links out of a listing page's HTML,
    resolved to absolute URLs, in first-seen order."""
    seen: dict[str, None] = {}
    for match in PROGRAM_LINK_PATTERN.finditer(html):
        absolute = urljoin(base_url, match.group(0))
        seen.setdefault(absolute, None)
    return list(seen.keys())


def _with_page_param(url: str, page: int) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["page"] = [str(page)]
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def discover(listing_url: str, pages: int) -> list[str]:
    all_links: dict[str, None] = {}
    for page_num in range(1, pages + 1):
        page_url = _with_page_param(listing_url, page_num) if pages > 1 else listing_url
        print(f"[discover] fetching page {page_num}/{pages}: {page_url}", file=sys.stderr)
        try:
            html = fetch_html(page_url)
        except CollectionError as exc:
            print(f"[discover] page {page_num} failed: {exc}", file=sys.stderr)
            continue

        links = extract_program_links(html, page_url)
        print(f"[discover] page {page_num}: {len(links)} program links", file=sys.stderr)
        for link in links:
            all_links.setdefault(link, None)

        if page_num < pages:
            time.sleep(PAGE_FETCH_DELAY)

    return list(all_links.keys())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract individual mastersportal.com program links from a search/listing page"
    )
    parser.add_argument("--url", required=True, help="Search/listing page URL")
    parser.add_argument("--pages", type=int, default=1, help="Number of result pages to walk (page=1..N)")
    parser.add_argument("--output", type=Path, default=Path("urls.txt"), help="Output file, one URL per line")
    args = parser.parse_args()

    links = discover(args.url, args.pages)
    args.output.write_text("\n".join(links) + ("\n" if links else ""), encoding="utf-8")
    print(f"\n{len(links)} unique program links written to {args.output}")


if __name__ == "__main__":
    main()
