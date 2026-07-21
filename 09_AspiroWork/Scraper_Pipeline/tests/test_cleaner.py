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
    upsert_to_csv,
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
        # Regression: C$/A$ both contain "$" — must not be mislabeled USD.
        ("C$ 25,000", "CAD"),
        ("A$ 30,000", "AUD"),
    ],
)
def test_normalize_currency(text, expected_code):
    amount, code = normalize_currency(text)
    assert code == expected_code


def test_normalize_currency_preserves_original_amount_text():
    amount, _ = normalize_currency("15,000 EUR")
    assert amount == "15,000 EUR"


def test_normalize_currency_does_not_crash_on_non_string_input():
    """A wrong-typed value (e.g. a loosely-typed model returning a number
    instead of a string) previously crashed on `.strip()` since `not text`
    is False for any truthy non-str value too."""
    assert normalize_currency(12345) == ("", "")
    assert normalize_currency(["15,000 EUR"]) == ("", "")


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


def test_normalize_repeatable_drops_non_string_items_instead_of_crashing():
    """A malformed LLM response (e.g. tags/intake_terms items not shaped as
    expected) previously crashed on `.strip()` for any non-str item."""
    result = normalize_repeatable(["Fall 2027", 2027, None, {"not": "a string"}])
    assert result == "Fall 2027"


def test_normalize_requirement_pairs_drops_non_dict_items_instead_of_crashing():
    items = [{"title": "Bachelor's degree", "description": None}, "TOEFL 90"]
    assert normalize_requirement_pairs(items) == "Bachelor's degree"


def test_normalize_tag_entries_drops_non_dict_items_instead_of_crashing():
    items = [{"name": "STEM", "category": None, "details": None}, "Physics"]
    assert normalize_tag_entries(items) == "STEM"


# ---------------------------------------------------------------------------
# clean_record — must not crash on a wrong-typed scalar field
# ---------------------------------------------------------------------------


def test_clean_record_treats_non_string_scalar_as_missing_instead_of_crashing():
    """`(value or "").strip()` crashes on any non-None, non-str truthy value
    — a wrong-shaped LLM response (e.g. university_name returned as a list)
    previously took down the whole row instead of just losing that field."""
    raw = {
        "university_name": ["Test University"],  # wrong type
        "level": "MSc",
        "program_name": "MSc in Testing",
    }
    row = clean_record(raw, "https://example.com/1")
    assert row["university_name"] == ""
    assert row["level"] == "MSc"


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


# ---------------------------------------------------------------------------
# upsert_to_csv — change-detection's update-in-place path
# ---------------------------------------------------------------------------


def test_upsert_to_csv_inserts_when_no_matching_row(tmp_path):
    csv_path = tmp_path / "programs.csv"
    outcome = upsert_to_csv(_row(), csv_path)
    assert outcome == "inserted"
    rows = list(csv.DictReader(csv_path.open()))
    assert len(rows) == 1


def test_upsert_to_csv_replaces_matching_row_in_place(tmp_path):
    """The actual scenario this exists for: a program's tuition changed on
    the source page. append_to_csv would see the same (university, program,
    url) key and silently refuse to write the new data — upsert_to_csv must
    replace the stale row instead of leaving it stuck or duplicating it."""
    csv_path = tmp_path / "programs.csv"
    append_to_csv(_row(), csv_path)  # tuition_1st_year is empty in _row()'s raw fields

    raw = {
        "university_name": "Test University",
        "level": "MSc",
        "program_name": "Program One",
        "tuition_1st_year": "20,000 EUR",
    }
    updated_row = clean_record(raw, "https://example.com/1")

    outcome = upsert_to_csv(updated_row, csv_path)
    assert outcome == "updated"

    rows = list(csv.DictReader(csv_path.open()))
    assert len(rows) == 1  # replaced, not appended as a second row
    assert rows[0]["tuition_1st_year"] == "20,000 EUR"


def test_upsert_to_csv_leaves_no_temp_file_on_success(tmp_path):
    csv_path = tmp_path / "programs.csv"
    upsert_to_csv(_row(), csv_path)
    assert list(tmp_path.glob(f".{csv_path.name}.*.tmp")) == []
