"""Pure-logic tests for cleaner.py — no network."""

import csv

import pytest

from cleaner import (
    append_to_csv,
    clean_record,
    normalize_currency,
    normalize_repeatable,
    normalize_requirement_pairs,
    normalize_tag_entries,
    validate_required,
)


# ---------------------------------------------------------------------------
# normalize_currency
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected_code",
    [
        ("15,000 EUR", "EUR"),
        ("£12,500", "GBP"),
        ("$40,000", "USD"),
        ("kr 200,000", "SEK"),
        ("no currency info here", ""),
        (None, ""),
        ("", ""),
    ],
)
def test_normalize_currency(text, expected_code):
    amount, code = normalize_currency(text)
    assert code == expected_code


def test_normalize_currency_preserves_original_amount_text():
    amount, _ = normalize_currency("15,000 EUR")
    assert amount == "15,000 EUR"


# ---------------------------------------------------------------------------
# normalize_repeatable / normalize_requirement_pairs / normalize_tag_entries
# ---------------------------------------------------------------------------


def test_normalize_repeatable_dedupes_and_strips():
    result = normalize_repeatable(["  Fall 2027  ", "Fall 2027", "Spring 2028", ""])
    assert result == "Fall 2027; Spring 2028"


def test_normalize_requirement_pairs_skips_empty_title():
    items = [
        {"title": "Bachelor's degree", "description": "In a related field"},
        {"title": "", "description": "should be skipped, no title"},
        {"title": "IELTS", "description": None},
    ]
    result = normalize_requirement_pairs(items)
    assert result == "Bachelor's degree: In a related field; IELTS"


def test_normalize_tag_entries_formats_category_and_details():
    items = [
        {"name": "Scholarship", "category": "Funding", "details": "Merit-based"},
        {"name": "STEM", "category": None, "details": None},
    ]
    result = normalize_tag_entries(items)
    assert result == "Scholarship (Funding): Merit-based; STEM"


# ---------------------------------------------------------------------------
# validate_required
# ---------------------------------------------------------------------------


def test_validate_required_reports_missing_fields():
    row = {"university_name": "Test", "level": "", "program_name": "Testing"}
    assert validate_required(row) == ["level"]


def test_validate_required_passes_when_all_present():
    row = {"university_name": "Test", "level": "MSc", "program_name": "Testing"}
    assert validate_required(row) == []


# ---------------------------------------------------------------------------
# append_to_csv — dedup + atomic write
# ---------------------------------------------------------------------------


def _row(program_name="Program One", source_url="https://example.com/1"):
    raw = {"university_name": "Test University", "level": "MSc", "program_name": program_name}
    return clean_record(raw, source_url)


def test_append_to_csv_writes_and_dedupes(tmp_path):
    csv_path = tmp_path / "programs.csv"

    assert append_to_csv(_row(), csv_path) is True
    assert append_to_csv(_row(program_name="Program Two", source_url="https://example.com/2"), csv_path) is True
    assert append_to_csv(_row(), csv_path) is False  # exact duplicate (same uni+program+url)

    rows = list(csv.DictReader(csv_path.open()))
    assert len(rows) == 2


def test_append_to_csv_leaves_no_temp_file_on_success(tmp_path):
    csv_path = tmp_path / "programs.csv"
    append_to_csv(_row(), csv_path)
    leftovers = list(tmp_path.glob(f".{csv_path.name}.*.tmp"))
    assert leftovers == []


def test_append_to_csv_is_atomic_on_crash(tmp_path, monkeypatch):
    """A crash mid-write must never leave a corrupted/partial output file —
    the original content must be exactly what it was before the failed
    call, and no stray temp file should be left behind."""
    csv_path = tmp_path / "programs.csv"
    append_to_csv(_row(), csv_path)
    before = csv_path.read_text()

    import cleaner

    class ExplodingWriter:
        def __init__(self, *a, **k):
            pass

        def writeheader(self):
            pass

        def writerows(self, rows):
            raise RuntimeError("simulated crash mid-write")

        def writerow(self, row):
            pass

    monkeypatch.setattr(cleaner.csv, "DictWriter", ExplodingWriter)

    with pytest.raises(RuntimeError):
        append_to_csv(_row(program_name="Program Two", source_url="https://example.com/2"), csv_path)

    assert csv_path.read_text() == before
    assert list(tmp_path.glob(f".{csv_path.name}.*.tmp")) == []
