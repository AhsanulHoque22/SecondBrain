"""CLI entrypoint — chains Collect -> Extract -> Clean for one or more URLs.

Usage:
    python pipeline.py --url https://example.com/program-page
    python pipeline.py --url-file urls.txt
    python pipeline.py --url <url> --output output/programs.csv --raw-dir raw/
    python pipeline.py --url-file urls.txt --delay 2.0 --block-cooldown 60
    python pipeline.py --url-file urls.txt --no-resume   # reprocess URLs already in the output CSV
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from cleaner import append_to_csv, clean_record, validate_required
from collector import CollectionError, HardBlockError, collect
from extractor import MODEL_PRICING, extract

DEFAULT_OUTPUT = Path("output/programs.csv")
DEFAULT_RAW_DIR = Path("raw")

# Politeness delay between URLs in a batch (+ jitter, so requests aren't
# perfectly periodic). No delay existed here before — a real batch hammering
# a site back-to-back is the leading suspect for a soft 403 escalating into
# a hard Cloudflare block, observed during this pipeline's own development.
DEFAULT_DELAY = 1.5
DEFAULT_JITTER = 1.0

# Extra one-time sleep after a HardBlockError, on top of the normal delay,
# before continuing to the next URL — retrying immediately into an active
# block just deepens it.
DEFAULT_BLOCK_COOLDOWN = 30.0


@dataclass
class RunResult:
    message: str
    usage: dict | None = None


def run(url: str, output_path: Path, raw_dir: Path) -> RunResult:
    collected = collect(url, raw_dir)
    raw_fields = extract(collected.html, url)
    row = clean_record(raw_fields, url)

    missing = validate_required(row)
    if missing:
        return RunResult(f"SKIPPED  {url}  missing required field(s): {', '.join(missing)}")

    written = append_to_csv(row, output_path)
    method = raw_fields.get("_extraction_method", "unknown")
    usage = raw_fields.get("_usage")
    if written:
        return RunResult(f"OK       {url}  ({method} extraction)", usage)
    return RunResult(f"DUPLICATE {url}  already in {output_path}", usage)


def _load_existing_source_urls(output_path: Path) -> set[str]:
    """Resume support: URLs already written to output_path are skipped
    entirely on a rerun — no re-fetch, no re-extraction, no LLM spend. Keyed
    on the exact source URL (cheaper and simpler than cleaner.py's own
    dedup, which needs the extracted fields first)."""
    if not output_path.exists():
        return set()
    with output_path.open("r", newline="", encoding="utf-8") as f:
        return {row["source_url"] for row in csv.DictReader(f) if row.get("source_url")}


def _print_cost_report(usages: list[dict]) -> None:
    if not usages:
        return
    by_model: dict[str, dict[str, int]] = {}
    for usage in usages:
        stats = by_model.setdefault(usage["model"], {"calls": 0, "input_tokens": 0, "output_tokens": 0})
        stats["calls"] += 1
        stats["input_tokens"] += usage["input_tokens"]
        stats["output_tokens"] += usage["output_tokens"]

    print("\nLLM cost (estimated, standard list pricing):")
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect -> Extract -> Clean pipeline")
    parser.add_argument("--url", action="append", default=[], help="A URL to process (repeatable)")
    parser.add_argument("--url-file", type=Path, help="File with one URL per line")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output CSV path")
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR, help="Raw HTML snapshot directory")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Seconds to wait between URLs")
    parser.add_argument(
        "--block-cooldown",
        type=float,
        default=DEFAULT_BLOCK_COOLDOWN,
        help="Extra seconds to wait after a hard Cloudflare block is detected",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Reprocess URLs even if already present in the output CSV (resume is on by default)",
    )
    args = parser.parse_args()

    urls = list(args.url)
    if args.url_file:
        urls.extend(
            line.strip()
            for line in args.url_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )

    if not urls:
        parser.error("Provide at least one URL via --url or --url-file")

    already_done = set() if args.no_resume else _load_existing_source_urls(args.output)

    results: list[str] = []
    usages: list[dict] = []
    for i, url in enumerate(urls):
        if url in already_done:
            results.append(f"RESUMED  {url}  already in {args.output}")
            continue

        try:
            result = run(url, args.output, args.raw_dir)
            results.append(result.message)
            if result.usage:
                usages.append(result.usage)
        except HardBlockError as exc:  # most specific first — HardBlockError is a CollectionError
            results.append(f"BLOCKED  {url}  {exc}")
            print(
                f"[pipeline] hard block detected — cooling down {args.block_cooldown}s before continuing",
                file=sys.stderr,
            )
            time.sleep(args.block_cooldown)
        except CollectionError as exc:
            results.append(f"FAILED   {url}  {exc}")
        except Exception as exc:  # keep going; one bad URL shouldn't kill the batch
            results.append(f"ERROR    {url}  {exc}")

        if i < len(urls) - 1:  # no point delaying after the last URL
            time.sleep(args.delay + random.uniform(0, DEFAULT_JITTER))

    for line in results:
        print(line)

    ok = sum(1 for r in results if r.startswith("OK"))
    dup = sum(1 for r in results if r.startswith("DUPLICATE"))
    resumed = sum(1 for r in results if r.startswith("RESUMED"))
    skipped = sum(1 for r in results if r.startswith("SKIPPED"))
    blocked = sum(1 for r in results if r.startswith("BLOCKED"))
    failed = sum(1 for r in results if r.startswith("FAILED") or r.startswith("ERROR"))
    print(
        f"\n{ok} written, {dup} duplicates, {resumed} resumed, {skipped} skipped, "
        f"{blocked} blocked, {failed} failed -> {args.output}"
    )

    _print_cost_report(usages)


if __name__ == "__main__":
    main()
