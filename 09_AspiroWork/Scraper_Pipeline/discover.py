"""Stage 0 — Discover.

Given a search/listing page URL, extracts the individual program-page links
on it (and optionally walks `page=2..N` of the same search) and writes them
one per line to a URL list file — ready to feed straight into
`pipeline.py --url-file`.

Reuses collector.fetch_html (same requests -> 403 -> headless-browser
fallback as the main pipeline) rather than a separate fetch path.

Site support is a small registry (SITE_PATTERNS below), keyed by domain —
today that's just mastersportal.com, whose listing pages are client-rendered
but whose program links are present in the fetched HTML as embedded JSON
data ("url":"/studies/8997/....html"), not <a href="..."> tags, which is
why the pattern matches the bare substring rather than an href attribute.
Adding a second site is meant to be a small addition here (one new
SitePattern entry with that site's own link regex + pagination param name),
not a rewrite — though no second site's pattern has actually been
discovered/tested yet, so only mastersportal.com is registered. An
unrecognized domain raises a clear error rather than silently finding
nothing.

Usage:
    python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands"
    python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands" --pages 5 --output urls.txt
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

from collector import CollectionError, fetch_html

PAGE_FETCH_DELAY = 1.5  # seconds between listing-page fetches — politeness, not a hard requirement


@dataclass(frozen=True)
class SitePattern:
    link_pattern: re.Pattern
    page_param: str  # query-string param name used for pagination on this site


SITE_PATTERNS: dict[str, SitePattern] = {
    "mastersportal.com": SitePattern(
        link_pattern=re.compile(r"/studies/\d+/[a-zA-Z0-9-]+\.html"),
        page_param="page",
    ),
}


def _site_pattern_for(url: str) -> SitePattern:
    domain = urlparse(url).netloc.lower()
    domain = domain[4:] if domain.startswith("www.") else domain
    for known_domain, pattern in SITE_PATTERNS.items():
        if domain == known_domain or domain.endswith(f".{known_domain}"):
            return pattern
    supported = ", ".join(sorted(SITE_PATTERNS))
    raise ValueError(
        f"No link-discovery pattern registered for {domain!r}. "
        f"Currently supported: {supported}. To add a new site, add a "
        "SitePattern entry to SITE_PATTERNS in discover.py with its own "
        "link regex and pagination query-param name."
    )


def extract_program_links(html: str, base_url: str, link_pattern: re.Pattern) -> list[str]:
    """Pull unique program-page links out of a listing page's HTML,
    resolved to absolute URLs, in first-seen order."""
    seen: dict[str, None] = {}
    for match in link_pattern.finditer(html):
        absolute = urljoin(base_url, match.group(0))
        seen.setdefault(absolute, None)
    return list(seen.keys())


def _with_page_param(url: str, page: int, page_param: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query[page_param] = [str(page)]
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def discover(listing_url: str, pages: int) -> list[str]:
    site = _site_pattern_for(listing_url)
    all_links: dict[str, None] = {}
    for page_num in range(1, pages + 1):
        page_url = (
            _with_page_param(listing_url, page_num, site.page_param) if pages > 1 else listing_url
        )
        print(f"[discover] fetching page {page_num}/{pages}: {page_url}", file=sys.stderr)
        try:
            html = fetch_html(page_url)
        except CollectionError as exc:
            print(f"[discover] page {page_num} failed: {exc}", file=sys.stderr)
            continue

        links = extract_program_links(html, page_url, site.link_pattern)
        print(f"[discover] page {page_num}: {len(links)} program links", file=sys.stderr)
        for link in links:
            all_links.setdefault(link, None)

        if page_num < pages:
            time.sleep(PAGE_FETCH_DELAY)

    return list(all_links.keys())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract individual program links from a search/listing page (see SITE_PATTERNS for supported sites)"
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
