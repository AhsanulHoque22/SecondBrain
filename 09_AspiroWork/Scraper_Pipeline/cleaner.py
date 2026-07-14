"""Stage 3 — Clean.

Normalizes an extracted-fields dict into the final CSV row: splits currency
out of the tuition string, joins repeatable fields into semicolon-separated
cells, validates the required fields (schema.REQUIRED_FIELDS), stamps
last_verified_date, and appends to the output CSV (skipping exact duplicate
rows).
"""

from __future__ import annotations

import csv
import os
import re
import tempfile
from datetime import date
from pathlib import Path

from schema import FIELDNAMES, REQUIRED_FIELDS

# Order matters: "C$"/"A$" must be checked before the bare "$" they both
# contain, or "C$ 25,000" would match "$" first and get mislabeled USD
# instead of CAD (the actual bug this ordering fixes — was previously
# listed $ before C$/A$ with no test covering either).
CURRENCY_SYMBOLS = {
    "€": "EUR",
    "£": "GBP",
    "C$": "CAD",
    "A$": "AUD",
    "$": "USD",
    "kr": "SEK",
}
CURRENCY_CODES = ["EUR", "GBP", "USD", "CAD", "AUD", "SEK", "BDT", "NOK", "DKK", "CHF"]


def normalize_currency(text: str | None) -> tuple[str, str]:
    if not text:
        return "", ""
    text = text.strip()
    for code in CURRENCY_CODES:
        if re.search(rf"\b{code}\b", text):
            return text, code
    for symbol, code in CURRENCY_SYMBOLS.items():
        if symbol in text:
            return text, code
    return text, ""


def normalize_repeatable(items: list[str]) -> str:
    seen: list[str] = []
    for item in items:
        cleaned = (item or "").strip()
        if cleaned and cleaned not in seen:
            seen.append(cleaned)
    return "; ".join(seen)


def normalize_requirement_pairs(items: list[dict]) -> str:
    parts = []
    for item in items:
        title = (item.get("title") or "").strip()
        description = (item.get("description") or "").strip()
        if not title:
            continue
        parts.append(f"{title}: {description}" if description else title)
    return "; ".join(parts)


def normalize_tag_entries(items: list[dict]) -> str:
    parts = []
    for item in items:
        name = (item.get("name") or "").strip()
        if not name:
            continue
        category = (item.get("category") or "").strip()
        details = (item.get("details") or "").strip()
        label = f"{name} ({category})" if category else name
        parts.append(f"{label}: {details}" if details else label)
    return "; ".join(parts)


def validate_required(row: dict) -> list[str]:
    return [field for field in REQUIRED_FIELDS if not row.get(field)]


def clean_record(raw: dict, url: str) -> dict:
    tuition_amount, tuition_currency = normalize_currency(raw.get("tuition_1st_year"))

    return {
        "program_image_url": (raw.get("program_image_url") or "").strip(),
        "university_name": (raw.get("university_name") or "").strip(),
        "level": (raw.get("level") or "").strip(),
        "program_name": (raw.get("program_name") or "").strip(),
        "destination": (raw.get("destination") or "").strip(),
        "location": (raw.get("location") or "").strip(),
        "campus_city": (raw.get("campus_city") or "").strip(),
        "tuition_1st_year": tuition_amount,
        "tuition_currency": tuition_currency,
        "application_fee": (raw.get("application_fee") or "").strip(),
        "duration": (raw.get("duration") or "").strip(),
        "success_rate": (raw.get("success_rate") or "").strip(),
        "intake_terms": normalize_repeatable(raw.get("intake_terms") or []),
        "deadlines": normalize_repeatable(raw.get("deadlines") or []),
        "prerequisites": normalize_requirement_pairs(raw.get("prerequisites") or []),
        "must_requirements": normalize_requirement_pairs(raw.get("must_requirements") or []),
        "tags": normalize_tag_entries(raw.get("tags") or []),
        "source_url": url,
        "last_verified_date": date.today().isoformat(),
    }


def _row_key(row: dict) -> tuple:
    return (row["university_name"].lower(), row["program_name"].lower(), row["source_url"])


def _load_csv_rows(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv_atomic(rows: list[dict], csv_path: Path) -> None:
    """Writes atomically: the full row set is written to a temp file in the
    same directory, then swapped in with os.replace() — atomic on POSIX and
    Windows. A crash or kill mid-write leaves the original file exactly as
    it was, never a truncated or half-written CSV. Trade-off: this is an
    O(rows) rewrite per call rather than a true O(1) append, which is the
    right call at this pipeline's scale (hundreds to low thousands of
    program rows) but wouldn't be for a much larger file.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=csv_path.parent, prefix=f".{csv_path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, csv_path)
    except BaseException:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def append_to_csv(row: dict, csv_path: Path) -> bool:
    """Append row to csv_path, skipping exact duplicates. Returns True if a
    row was written."""
    existing_rows = _load_csv_rows(csv_path)
    existing_keys = {
        (
            (existing.get("university_name") or "").lower(),
            (existing.get("program_name") or "").lower(),
            existing.get("source_url") or "",
        )
        for existing in existing_rows
    }

    if _row_key(row) in existing_keys:
        return False

    existing_rows.append(row)
    _write_csv_atomic(existing_rows, csv_path)
    return True


def upsert_to_csv(row: dict, csv_path: Path) -> str:
    """Like append_to_csv, but replaces an existing row with the same
    (university_name, program_name, source_url) key instead of treating it
    as a duplicate to skip. Used by pipeline.py's change-detection refresh
    path once extractor.has_content_changed() has confirmed a program's
    source page actually changed — the old row's data would otherwise be
    stuck stale forever, since append_to_csv would just see the same key
    and refuse to write. Returns "inserted" (no prior row existed) or
    "updated" (an existing row was replaced)."""
    existing_rows = _load_csv_rows(csv_path)
    key = _row_key(row)
    for i, existing in enumerate(existing_rows):
        existing_key = (
            (existing.get("university_name") or "").lower(),
            (existing.get("program_name") or "").lower(),
            existing.get("source_url") or "",
        )
        if existing_key == key:
            existing_rows[i] = row
            _write_csv_atomic(existing_rows, csv_path)
            return "updated"

    existing_rows.append(row)
    _write_csv_atomic(existing_rows, csv_path)
    return "inserted"
