"""Stage 0 — Discover.

Given a search/listing page URL, extracts the individual program-page links
on it (and optionally walks `page=2..N` of the same search).

Cross-run dedup: every link found is merged into a persistent manifest at
state/discovered_urls.json (dedup key: exact URL match), so running this
twice against the same or an overlapping search doesn't lose track of what
was already found. --output (urls.txt) only ever contains links that are
*new* as of this run — the small, immediately-actionable batch to hand to
`pipeline.py --url-file`. See state/README.md for the full design (why
there's no "processed" status here — pipeline.py's own resume feature is
the single source of truth for that).

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
import json
import os
import re
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

from collector import CollectionError, fetch_html

PAGE_FETCH_DELAY = 1.5  # seconds between listing-page fetches — politeness, not a hard requirement
DEFAULT_STATE_PATH = Path("state/discovered_urls.json")


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


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load_discovered_urls(state_path: Path) -> dict[str, dict]:
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text(encoding="utf-8"))


def _save_discovered_urls(state_path: Path, manifest: dict[str, dict]) -> None:
    """Atomic write (temp file + os.replace) — same pattern as
    cleaner.append_to_csv. This manifest accumulates across every future
    run, so a crash mid-write must never corrupt what's already there."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=state_path.parent, prefix=f".{state_path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)
        os.replace(tmp_path, state_path)
    except BaseException:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def _merge_into_manifest(
    manifest: dict[str, dict], links: list[str], discovered_via: str, now: str
) -> list[str]:
    """Merges links into manifest in place. Dedup key is exact URL match —
    mastersportal's program links carry no tracking params or fragments, so
    there's nothing to normalize. Returns only the links that were new to
    the manifest (not already a key) before this call — the actionable
    output for a batch. A URL already present gets last_discovered_at
    bumped, not duplicated or reset."""
    new_links: list[str] = []
    for link in links:
        if link not in manifest:
            manifest[link] = {
                "first_discovered_at": now,
                "last_discovered_at": now,
                "discovered_via": discovered_via,
            }
            new_links.append(link)
        else:
            manifest[link]["last_discovered_at"] = now
    return new_links


def discover(listing_url: str, pages: int, state_path: Path = DEFAULT_STATE_PATH) -> list[str]:
    """Walks the listing pages, merges every link found into the persistent
    manifest at state_path, and returns only the links that are new as of
    this run (see module docstring for why "new" and "not yet processed"
    are deliberately different questions, answered by different files)."""
    site = _site_pattern_for(listing_url)
    manifest = _load_discovered_urls(state_path)
    now = _now_iso()
    new_links: dict[str, None] = {}  # preserves first-seen order, dedups across pages within this run

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
        for link in _merge_into_manifest(manifest, links, listing_url, now):
            new_links.setdefault(link, None)

        if page_num < pages:
            time.sleep(PAGE_FETCH_DELAY)

    _save_discovered_urls(state_path, manifest)
    print(
        f"[discover] manifest now has {len(manifest)} URLs total "
        f"({len(new_links)} new this run) -> {state_path}",
        file=sys.stderr,
    )
    return list(new_links.keys())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract individual program links from a search/listing page (see SITE_PATTERNS for supported sites)"
    )
    parser.add_argument("--url", required=True, help="Search/listing page URL")
    parser.add_argument("--pages", type=int, default=1, help="Number of result pages to walk (page=1..N)")
    parser.add_argument(
        "--output", type=Path, default=Path("urls.txt"), help="Output file — only links new as of this run"
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help="Persistent cross-run discovery manifest (default: state/discovered_urls.json)",
    )
    args = parser.parse_args()

    new_links = discover(args.url, args.pages, state_path=args.state)
    args.output.write_text("\n".join(new_links) + ("\n" if new_links else ""), encoding="utf-8")
    print(f"\n{len(new_links)} new program links written to {args.output}")


if __name__ == "__main__":
    main()
