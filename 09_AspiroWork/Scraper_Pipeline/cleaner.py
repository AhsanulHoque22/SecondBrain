"""Stage 3 — Clean.

Normalizes an extracted-fields dict into the final CSV row: splits currency
out of the tuition string, joins repeatable fields into semicolon-separated
cells (matching the convention already used in Data Collection/), validates
the mandatory fields from Appendix A, stamps last_verified_date, and appends
to the output CSV (skipping exact duplicate rows).
"""

from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

from schema import FIELDNAMES, REQUIRED_FIELDS

CURRENCY_SYMBOLS = {
    "€": "EUR",
    "£": "GBP",
    "$": "USD",
    "C$": "CAD",
    "A$": "AUD",
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


def append_to_csv(row: dict, csv_path: Path) -> bool:
    """Append row to csv_path, skipping exact duplicates. Returns True if a row was written."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = csv_path.exists()

    existing_keys: set[tuple] = set()
    if file_exists:
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            for existing in csv.DictReader(f):
                existing_keys.add(
                    (
                        (existing.get("university_name") or "").lower(),
                        (existing.get("program_name") or "").lower(),
                        existing.get("source_url") or "",
                    )
                )

    if _row_key(row) in existing_keys:
        return False

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    return True
