"""Post-run report for the 100-URL pipeline test.

Reads the pipeline's own outputs (output CSV, extraction_state.json) plus
urls.txt to answer the three things the test was asked to answer:
  - how many of the 100 records came through correctly (vs skipped)
  - which fields are missing/broken, and how often
  - a real correctness comparison against the OLD method's output, for
    whichever of the 100 URLs the old method also covered (found by
    matching source_url against Data Collection/*.csv) — this is the only
    honest way to answer "correctness % vs source data" without fabricating
    a number for URLs where no independently-collected ground truth exists.

Does not call any LLM, make any network request, or modify anything —
read-only analysis of files the pipeline run already produced. Run this
AFTER pipeline.py finishes, not during.

Usage:
    ./.venv/bin/python generate_report.py
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from schema import FIELDNAMES, REQUIRED_FIELDS

DEFAULT_URLS_FILE = Path("urls.txt")
DEFAULT_OUTPUT_CSV = Path("output/programs.csv")
DEFAULT_STATE_FILE = Path("state/extraction_state.json")
DEFAULT_OLD_METHOD_DIR = Path("../Data Collection")

# Columns both the new pipeline's CSV and the old method's CSV share —
# everything except source_url (the join key) and the two columns the new
# schema added that the old one never had (tuition_currency,
# last_verified_date), which have no old-method value to compare against.
COMPARABLE_FIELDS = [f for f in FIELDNAMES if f not in ("source_url", "tuition_currency", "last_verified_date")]


def load_urls(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_output_rows(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open("r", newline="", encoding="utf-8") as f:
        return {row["source_url"]: row for row in csv.DictReader(f)}


def load_extraction_state(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_old_method_rows(directory: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if not directory.exists():
        return rows
    for csv_path in directory.glob("*.csv"):
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                url = row.get("source_url")
                if url:
                    rows[url] = row
    return rows


def normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report on a completed pipeline test run")
    parser.add_argument("--urls", type=Path, default=DEFAULT_URLS_FILE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE_FILE)
    parser.add_argument("--old-method-dir", type=Path, default=DEFAULT_OLD_METHOD_DIR)
    args = parser.parse_args()

    urls = load_urls(args.urls)
    output_rows = load_output_rows(args.output)
    state = load_extraction_state(args.state)
    old_rows = load_old_method_rows(args.old_method_dir)

    # --- 1. How many came through correctly -------------------------------
    print_section("1. RECORDS PROCESSED")
    attempted = len(urls)
    written = sum(1 for u in urls if u in output_rows)
    skipped = attempted - written
    print(f"URLs in urls.txt:        {attempted}")
    print(f"Written to output CSV:   {written}")
    print(f"Skipped/failed:          {skipped}")
    if skipped:
        print("  (skipped = missing a required field [university_name/level/program_name]")
        print("   after every LLM tier + heuristic fallback failed to find it, or a hard")
        print("   collection failure — check the pipeline run's stdout log for which)")

    # --- 2. Extraction method breakdown (what actually produced each row) -
    print_section("2. EXTRACTION METHOD BREAKDOWN")
    method_counts: dict[str, int] = {}
    for url in urls:
        method = state.get(url, {}).get("extraction_method", "not attempted")
        method_counts[method] = method_counts.get(method, 0) + 1
    for method, count in sorted(method_counts.items(), key=lambda kv: -kv[1]):
        pct = 100 * count / attempted
        print(f"  {method:30} {count:4}  ({pct:5.1f}%)")
    heuristic_count = method_counts.get("heuristic", 0)
    if heuristic_count:
        print(
            f"\n  Note: {heuristic_count} row(s) came from the zero-setup heuristic fallback, "
            "not an LLM — expect lower recall on optional fields for these specifically "
            "(see README Limitations)."
        )

    # --- 3. Field completeness across all written rows ---------------------
    print_section("3. FIELD COMPLETENESS (of rows actually written)")
    if written:
        for field in FIELDNAMES:
            filled = sum(1 for row in output_rows.values() if (row.get(field) or "").strip())
            pct = 100 * filled / written
            required_tag = " (required)" if field in REQUIRED_FIELDS else ""
            print(f"  {field:22} {filled:4}/{written:<4} filled  ({pct:5.1f}%){required_tag}")
    else:
        print("  No rows written yet — run pipeline.py first.")

    # --- 4. Correctness vs the OLD method's own data, where it exists -----
    print_section("4. CORRECTNESS VS OLD-METHOD DATA (real ground truth, not assumed)")
    overlap = [u for u in urls if u in output_rows and u in old_rows]
    print(f"URLs in this test set also present in the old method's CSVs: {len(overlap)}/{attempted}")
    if not overlap:
        print(
            "  No overlap found — cannot compute a real correctness percentage against the "
            "old method for this batch. Report field-completeness (section 3) and manually "
            "review a sample instead; do not report a fabricated accuracy number."
        )
    else:
        total_field_checks = 0
        total_field_matches = 0
        mismatch_lines: list[str] = []
        per_url_exact = 0
        for url in overlap:
            new_row = output_rows[url]
            old_row = old_rows[url]
            url_matches = 0
            for field in COMPARABLE_FIELDS:
                total_field_checks += 1
                if normalize(new_row.get(field)) == normalize(old_row.get(field)):
                    total_field_matches += 1
                    url_matches += 1
                else:
                    mismatch_lines.append(
                        f"  {url}\n    field: {field}\n"
                        f"    old : {old_row.get(field)!r}\n"
                        f"    new : {new_row.get(field)!r}"
                    )
            if url_matches == len(COMPARABLE_FIELDS):
                per_url_exact += 1

        field_pct = 100 * total_field_matches / total_field_checks if total_field_checks else 0
        row_pct = 100 * per_url_exact / len(overlap) if overlap else 0
        print(f"\nField-level exact-match rate:  {total_field_matches}/{total_field_checks}  ({field_pct:.1f}%)")
        print(f"Row-level fully-exact rate:    {per_url_exact}/{len(overlap)}  ({row_pct:.1f}%)")
        print(
            "\n(Field-level counts every column separately — a tuition string that's "
            "formatted differently but means the same thing will show as a mismatch here; "
            "read the mismatch list below before treating every one as a real error.)"
        )
        if mismatch_lines:
            print(f"\n--- {len(mismatch_lines)} field mismatches ---")
            for line in mismatch_lines:
                print(line)

    print_section("DONE")
    print("Paste sections 1-4 into the report. Section 4 is the only one that can honestly")
    print("claim a 'correctness % vs source data' — it's scoped to the URLs where real")
    print("independently-collected ground truth exists, not all 100.")


if __name__ == "__main__":
    main()
