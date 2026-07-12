"""Canary / smoke test — verify known-good real URLs still extract correctly.

Catches the pipeline breaking silently: a site changes its page layout,
`collector.py`'s fetch stops working, or the heuristic extractor's
selectors go stale, and a real batch quietly comes back mostly-empty with
no obvious error. Run this periodically (manually, or on a schedule) against
one known-good URL per supported site; it exits non-zero if any of them
stop producing the required fields, so it's safe to wire into a monitoring
script.

Uses a throwaway temp directory for raw HTML — a canary run never touches
the real raw/ cache or output CSV.

Usage:
    python canary.py
    python canary.py --verbose
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from cleaner import clean_record, validate_required
from collector import CollectionError, collect
from extractor import extract

try:
    from dotenv import load_dotenv

    load_dotenv()  # optional: loads a local .env if python-dotenv is installed and one exists
except ImportError:
    pass

# One known-good URL per supported site. Each comment records when/how it
# was last confirmed working, so a future canary failure has a clear
# "this used to work as of X" baseline instead of an unexplained regression.
CANARY_URLS = [
    # mastersportal.com — confirmed working end-to-end (Cloudflare 403 ->
    # Playwright fallback -> heuristic extraction, including the dotted
    # LL.M level-backfill tier) during this pipeline's own development.
    "https://www.mastersportal.com/studies/8798/legal-research.html",
    # ox.ac.uk — confirmed working end-to-end (Cloudflare 403 -> Playwright
    # fallback -> heuristic extraction via og:title/og:site_name fallback)
    # during this pipeline's own development.
    "https://www.ox.ac.uk/admissions/graduate/courses/msc-advanced-computer-science",
]


def check_url(url: str, raw_dir: Path) -> tuple[bool, str]:
    try:
        collected = collect(url, raw_dir)
    except CollectionError as exc:
        return False, f"collect failed: {exc}"

    raw_fields = extract(collected.html, url)
    row = clean_record(raw_fields, url)
    missing = validate_required(row)
    method = raw_fields.get("_extraction_method", "unknown")
    if missing:
        return False, f"missing required field(s): {', '.join(missing)} (via {method})"
    return True, f"OK (via {method})"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smoke test: verify known-good URLs still extract the required fields"
    )
    parser.add_argument("--verbose", action="store_true", help="Print detail for passing URLs too")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="canary_raw_") as tmp_raw:
        raw_dir = Path(tmp_raw)
        all_ok = True
        for url in CANARY_URLS:
            ok, detail = check_url(url, raw_dir)
            all_ok = all_ok and ok
            status = "PASS" if ok else "FAIL"
            if ok and not args.verbose:
                print(f"{status}  {url}")
            else:
                print(f"{status}  {url}  {detail}")

    if not all_ok:
        print(
            "\nCanary FAILED — a supported site's layout may have changed. "
            "Investigate before trusting a real batch.",
            file=sys.stderr,
        )
        sys.exit(1)
    print("\nAll canaries passed.")


if __name__ == "__main__":
    main()
