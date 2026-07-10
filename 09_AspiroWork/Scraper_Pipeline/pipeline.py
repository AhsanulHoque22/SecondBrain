"""CLI entrypoint — chains Collect -> Extract -> Clean for one or more URLs.

Usage:
    python pipeline.py --url https://example.com/program-page
    python pipeline.py --url-file urls.txt
    python pipeline.py --url <url> --output output/programs.csv --raw-dir raw/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cleaner import append_to_csv, clean_record, validate_required
from collector import CollectionError, collect
from extractor import extract

DEFAULT_OUTPUT = Path("output/programs.csv")
DEFAULT_RAW_DIR = Path("raw")


def run(url: str, output_path: Path, raw_dir: Path) -> str:
    collected = collect(url, raw_dir)
    raw_fields = extract(collected.html, url)
    row = clean_record(raw_fields, url)

    missing = validate_required(row)
    if missing:
        return f"SKIPPED  {url}  missing required field(s): {', '.join(missing)}"

    written = append_to_csv(row, output_path)
    method = raw_fields.get("_extraction_method", "unknown")
    if written:
        return f"OK       {url}  ({method} extraction)"
    return f"DUPLICATE {url}  already in {output_path}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect -> Extract -> Clean pipeline")
    parser.add_argument("--url", action="append", default=[], help="A URL to process (repeatable)")
    parser.add_argument("--url-file", type=Path, help="File with one URL per line")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output CSV path")
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR, help="Raw HTML snapshot directory")
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

    results = []
    for url in urls:
        try:
            results.append(run(url, args.output, args.raw_dir))
        except CollectionError as exc:
            results.append(f"FAILED   {url}  {exc}")
        except Exception as exc:  # keep going; one bad URL shouldn't kill the batch
            results.append(f"ERROR    {url}  {exc}")

    for line in results:
        print(line)

    ok = sum(1 for r in results if r.startswith("OK"))
    dup = sum(1 for r in results if r.startswith("DUPLICATE"))
    skipped = sum(1 for r in results if r.startswith("SKIPPED"))
    failed = sum(1 for r in results if r.startswith("FAILED") or r.startswith("ERROR"))
    print(f"\n{ok} written, {dup} duplicates, {skipped} skipped, {failed} failed -> {args.output}")


if __name__ == "__main__":
    main()
