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

**Alternative: --llm-discovery.** Instead of registering a SitePattern,
pass --llm-discovery to classify links with an LLM instead of a per-site
regex — works on any site, no code changes, at a small per-page cost (see
extract_program_links_via_llm and README.md's Discover section for the
cost breakdown and design rationale). Pagination still needs a registered
SitePattern's page_param to know the site's query-string convention; an
unregistered domain with --llm-discovery and --pages > 1 falls back to
fetching page 1 only.

Usage:
    python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands"
    python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands" --pages 5 --output urls.txt
    python discover.py --url "https://example.com/programs" --llm-discovery   # any site, no SitePattern needed
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

import llm_providers
from collector import CollectionError, fetch_html
from extractor import MODEL_PRICING

try:
    from dotenv import load_dotenv

    load_dotenv()  # optional: loads a local .env if python-dotenv is installed and one exists
except ImportError:
    pass

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


def _lookup_site_pattern(url: str) -> SitePattern | None:
    domain = urlparse(url).netloc.lower()
    domain = domain[4:] if domain.startswith("www.") else domain
    for known_domain, pattern in SITE_PATTERNS.items():
        if domain == known_domain or domain.endswith(f".{known_domain}"):
            return pattern
    return None


def _site_pattern_for(url: str) -> SitePattern:
    pattern = _lookup_site_pattern(url)
    if pattern is not None:
        return pattern
    domain = urlparse(url).netloc.lower()
    domain = domain[4:] if domain.startswith("www.") else domain
    supported = ", ".join(sorted(SITE_PATTERNS))
    raise ValueError(
        f"No link-discovery pattern registered for {domain!r}. "
        f"Currently supported: {supported}. To add a new site, add a "
        "SitePattern entry to SITE_PATTERNS in discover.py with its own "
        "link regex and pagination query-param name — or pass "
        "--llm-discovery to classify links with an LLM instead, no "
        "SitePattern required."
    )


def extract_program_links(html: str, base_url: str, link_pattern: re.Pattern) -> list[str]:
    """Pull unique program-page links out of a listing page's HTML,
    resolved to absolute URLs, in first-seen order."""
    seen: dict[str, None] = {}
    for match in link_pattern.finditer(html):
        absolute = urljoin(base_url, match.group(0))
        seen.setdefault(absolute, None)
    return list(seen.keys())


# --- LLM-based discovery (--llm-discovery) --------------------------------
#
# Generalizes discovery to any site without a registered SitePattern, at the
# cost of one small LLM call per listing page. Two-stage design to keep that
# call cheap and reliable: extract_candidate_links does a broad, free regex
# pass first (same-domain, page-like URLs only — no site-specific knowledge
# needed, unlike link_pattern above), then extract_program_links_via_llm
# asks the LLM to classify that short list of paths rather than parse the
# raw page itself. Classifying ~100-300 short paths is both cheaper and far
# more reliable for an LLM than finding needles in 100KB+ of raw HTML.

DEFAULT_DISCOVERY_MODEL = "claude-haiku-4-5"  # Anthropic only — see _discovery_model
MAX_DISCOVERY_CANDIDATES = 300  # bounds worst-case prompt size regardless of page size

# Any extension a listing page could plausibly link to that is never itself
# a program's own detail page — filtering these out of the candidate pool
# before the LLM ever sees it costs nothing and shrinks the prompt for free.
NON_PAGE_EXTENSIONS = (
    ".css", ".js", ".mjs", ".json", ".xml", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".map", ".pdf",
)

# Any quoted string shaped like an absolute URL or an absolute-path link —
# deliberately not site-specific (covers both <a href="..."> tags and links
# embedded as raw JSON, the same "not just href" case extract_program_links
# above was built for a single site). Over-inclusive on purpose: real
# program links plus navigation/ads/assets — extract_candidate_links filters
# what it can for free, and extract_program_links_via_llm's classification
# step is what actually separates the two.
CANDIDATE_URL_PATTERN = re.compile(r'["\'](?P<url>https?://[^"\'<>\s]+|/[a-zA-Z0-9][^"\'<>\s]{2,200})["\']')

DISCOVERY_TOOL_NAME = "select_program_page_links"
DISCOVERY_TOOL_DESCRIPTION = (
    "From the candidate links found on this program-listing/search page, "
    "return only the ones that link to an individual program's own detail "
    "page. Exclude navigation, category/filter links, pagination controls, "
    "ads, social links, the listing page itself, and anything unrelated."
)
DISCOVERY_SCHEMA = {
    "type": "object",
    "properties": {
        "program_page_paths": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Paths copied verbatim from the candidate list — never invented or modified.",
        }
    },
    "required": ["program_page_paths"],
    "additionalProperties": False,
}
DISCOVERY_SYSTEM_PROMPT = (
    "You identify which links on a program-listing/search page lead to an "
    "individual program's own detail page, as opposed to navigation, "
    "filters, pagination, ads, or unrelated content. Only return paths that "
    "appear verbatim in the candidate list provided — never invent or "
    "modify one."
)


def extract_candidate_links(
    html: str, base_url: str, max_candidates: int = MAX_DISCOVERY_CANDIDATES
) -> list[str]:
    """Site-agnostic first pass for --llm-discovery: every quoted,
    URL-shaped string on the page, resolved to absolute, filtered to the
    same domain as base_url and to extensions that could plausibly be a
    page (not a stylesheet/script/image/font/etc.), deduped, capped at
    max_candidates. This is the free filtering step that keeps the LLM
    classification call small — see the module comment above."""
    base_domain = urlparse(base_url).netloc.lower()
    base_domain = base_domain[4:] if base_domain.startswith("www.") else base_domain

    seen: dict[str, None] = {}
    for match in CANDIDATE_URL_PATTERN.finditer(html):
        absolute = urljoin(base_url, match.group("url"))
        parsed = urlparse(absolute)
        domain = parsed.netloc.lower()
        domain = domain[4:] if domain.startswith("www.") else domain
        if domain != base_domain:
            continue
        if parsed.path.lower().endswith(NON_PAGE_EXTENSIONS):
            continue
        seen.setdefault(absolute, None)
        if len(seen) >= max_candidates:
            break
    return list(seen.keys())


def _discovery_model(explicit: str | None = None) -> str:
    """Same rule as extractor._model_cascade: only the Anthropic provider
    gets a built-in default (the only one this call has been run against
    live). Any other provider must set DISCOVERY_MODEL explicitly rather
    than have this module guess a current model ID for a vendor it can't
    verify against."""
    if explicit:
        return explicit
    override = os.environ.get("DISCOVERY_MODEL", "").strip()
    if override:
        return override
    if llm_providers.get_provider() == "anthropic":
        return DEFAULT_DISCOVERY_MODEL
    raise RuntimeError(
        f"LLM_PROVIDER={llm_providers.get_provider()!r} has no built-in default discovery model. "
        "Set DISCOVERY_MODEL to a model ID for this provider."
    )


def extract_program_links_via_llm(
    html: str, base_url: str, model: str | None = None
) -> tuple[list[str], dict | None]:
    """Returns (links, usage) — usage is None when no LLM call was made at
    all (no candidates found, so nothing to classify — the common case for
    a page with zero program listings)."""
    candidates = extract_candidate_links(html, base_url)
    if not candidates:
        return [], None

    # Send paths only (not full absolute URLs) — every candidate already
    # shares base_url's domain, so repeating the scheme+host on every line
    # is pure prompt weight for no informational gain.
    path_to_absolute: dict[str, str] = {}
    for absolute in candidates:
        parsed = urlparse(absolute)
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        path_to_absolute[path] = absolute

    user_content = (
        f"Listing page: {base_url}\n\nCandidate link paths (one per line):\n"
        + "\n".join(path_to_absolute.keys())
    )
    resolved_model = _discovery_model(model)
    data, usage = llm_providers.call_llm(
        resolved_model,
        DISCOVERY_SYSTEM_PROMPT,
        user_content,
        DISCOVERY_SCHEMA,
        DISCOVERY_TOOL_NAME,
        DISCOVERY_TOOL_DESCRIPTION,
    )
    selected_paths = data.get("program_page_paths", [])
    # Defensive: only trust a path that was actually offered as a candidate
    # — never let a hallucinated path through the classification step, even
    # one that looks plausible.
    links = [path_to_absolute[p] for p in selected_paths if p in path_to_absolute]
    return links, {"model": resolved_model, **usage}


def _print_discovery_cost_report(usages: list[dict]) -> None:
    if not usages:
        return
    by_model: dict[str, dict[str, int]] = {}
    for usage in usages:
        stats = by_model.setdefault(usage["model"], {"calls": 0, "input_tokens": 0, "output_tokens": 0})
        stats["calls"] += 1
        stats["input_tokens"] += usage["input_tokens"]
        stats["output_tokens"] += usage["output_tokens"]

    print("\nLLM discovery cost (estimated, standard list pricing):")
    total_cost = 0.0
    for model, stats in sorted(by_model.items()):
        price_in, price_out = MODEL_PRICING.get(model, (0.0, 0.0))
        cost = (stats["input_tokens"] / 1_000_000) * price_in + (stats["output_tokens"] / 1_000_000) * price_out
        total_cost += cost
        print(
            f"  {model:20} {stats['calls']:3} calls   "
            f"{stats['input_tokens']:8} in / {stats['output_tokens']:7} out tokens   ~${cost:.4f}"
        )
    print(f"  {'total':20}     {'':>19}   ~${total_cost:.4f}")


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


def discover(
    listing_url: str,
    pages: int,
    state_path: Path = DEFAULT_STATE_PATH,
    use_llm: bool = False,
    llm_model: str | None = None,
) -> list[str]:
    """Walks the listing pages, merges every link found into the persistent
    manifest at state_path, and returns only the links that are new as of
    this run (see module docstring for why "new" and "not yet processed"
    are deliberately different questions, answered by different files).

    use_llm switches link extraction from the SITE_PATTERNS registry to
    extract_program_links_via_llm — works on any site, at a small per-page
    LLM cost, reported at the end via _print_discovery_cost_report. Pagination
    still needs a registered SitePattern's page_param to know the site's
    query-string convention; an unregistered domain with use_llm and
    pages > 1 falls back to fetching page 1 only rather than guessing one."""
    if use_llm:
        site = _lookup_site_pattern(listing_url)
        if pages > 1 and site is None:
            print(
                f"[discover] no registered pagination pattern for this domain — "
                f"fetching page 1 only ({pages} requested; register a SitePattern "
                "to enable multi-page --llm-discovery for this site)",
                file=sys.stderr,
            )
            pages = 1
        page_param = site.page_param if site else None
    else:
        site = _site_pattern_for(listing_url)  # raises for an unregistered domain — unchanged behavior
        page_param = site.page_param

    manifest = _load_discovered_urls(state_path)
    now = _now_iso()
    new_links: dict[str, None] = {}  # preserves first-seen order, dedups across pages within this run
    usages: list[dict] = []

    for page_num in range(1, pages + 1):
        page_url = _with_page_param(listing_url, page_num, page_param) if pages > 1 else listing_url
        print(f"[discover] fetching page {page_num}/{pages}: {page_url}", file=sys.stderr)
        try:
            html = fetch_html(page_url)
        except CollectionError as exc:
            print(f"[discover] page {page_num} failed: {exc}", file=sys.stderr)
            continue

        if use_llm:
            links, usage = extract_program_links_via_llm(html, page_url, model=llm_model)
            if usage:
                usages.append(usage)
        else:
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
    _print_discovery_cost_report(usages)
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
    parser.add_argument(
        "--llm-discovery",
        action="store_true",
        help=(
            "Classify links with an LLM instead of the SITE_PATTERNS registry — works on any "
            "site with no code changes, at a small per-page LLM cost (see README)"
        ),
    )
    parser.add_argument(
        "--llm-discovery-model",
        type=str,
        default=None,
        help="Override the model used for --llm-discovery (default: DISCOVERY_MODEL env var, "
        "or claude-haiku-4-5 for the Anthropic provider)",
    )
    args = parser.parse_args()

    new_links = discover(
        args.url,
        args.pages,
        state_path=args.state,
        use_llm=args.llm_discovery,
        llm_model=args.llm_discovery_model,
    )
    args.output.write_text("\n".join(new_links) + ("\n" if new_links else ""), encoding="utf-8")
    print(f"\n{len(new_links)} new program links written to {args.output}")


if __name__ == "__main__":
    main()
