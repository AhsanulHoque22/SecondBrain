"""Pure-logic tests for extractor.py — no network, no LLM calls.

Covers the pieces that broke or almost broke during this pipeline's real
development: the level-backfill regex tiers (found missing "Master"/"LL.M."
on real mastersportal.com titles), the application_fee label-regex
false-positive (found "applicants from low-income countries;" leaking
through on ox.ac.uk), the validator's required/numeric/grounding checks,
and the Haiku->Sonnet->Opus escalation cascade (mocked — no live model
access from tests, ever).
"""

import json
from unittest.mock import patch

import pytest

from extractor import (
    backfill_level,
    content_hash,
    extract,
    extract_via_heuristics,
    has_content_changed,
    record_extraction_state,
    validate_extraction,
)


# ---------------------------------------------------------------------------
# backfill_level — the three-tier level-detection regex
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "program_name,expected",
    [
        # Tier 1: anchored bare abbreviation (Oxford's convention)
        ("MSc in Advanced Computer Science", "MSc"),
        ("MSt in Philosophy of Physics", "MSt"),
        ("MPhil in Theology", "MPhil"),
        # Tier 2: dotted abbreviation anywhere (real mastersportal.com title)
        ("Legal Research LL.M. at Utrecht University", "LL.M"),
        ("Data Science M.Sc. at TU Berlin", "M.Sc"),
        # Tier 3: plain word anywhere (real mastersportal.com title)
        (
            "Joint Master in Applied XR - Gamified Reality Applications for "
            "Real-world Challenges and Experiences (GRACE) Master at USTP",
            "Master",
        ),
        ("Master's in Data Science", "Master's"),
        ("Bachelor of Arts in History", "Bachelor"),
        ("PhD in Computer Science", "PhD"),
        # No degree word at all -> None, not a guess (real mastersportal.com title)
        ("Legal Research", None),
        # Adversarial: bare 2-letter forms must NOT match outside tier 1's
        # anchored position — "MA" as the Massachusetts abbreviation must
        # never be mistaken for a degree level.
        ("University of Massachusetts (MA) Program", None),
    ],
)
def test_backfill_level(program_name, expected):
    assert backfill_level(program_name) == expected


# ---------------------------------------------------------------------------
# extract_via_heuristics — application_fee false-positive regression
# ---------------------------------------------------------------------------


def test_application_fee_does_not_match_unrelated_prose():
    """Regression test for the real bug found on ox.ac.uk: an unbounded
    label-to-colon gap let 'Application fee waivers are available for the
    following applicants who meet the eligibility criteria:' match as the
    label, capturing the next line ('applicants from low-income
    countries;') as if it were the fee amount."""
    html = "<html><head><title>Test Program</title></head><body></body></html>"
    clean_text = (
        "An application fee of £75 is payable for each application to this course.\n"
        "Application fee waivers are available for the following applicants who meet "
        "the eligibility criteria:\n"
        "applicants from low-income countries;\n"
        "refugees and displaced persons;"
    )
    data = extract_via_heuristics(html, clean_text, "https://example.com/test")
    assert data["application_fee"] != "applicants from low-income countries;"


def test_application_fee_matches_close_colon_value():
    html = "<html><head><title>Test Program</title></head><body></body></html>"
    clean_text = "Application fee: £75\nSome other unrelated text with a colon: not this one"
    data = extract_via_heuristics(html, clean_text, "https://example.com/test")
    assert data["application_fee"] == "£75"


# ---------------------------------------------------------------------------
# validate_extraction — required fields, numeric shape, grounding
# ---------------------------------------------------------------------------


BASE_FIELDS = {
    "university_name": "Test University",
    "level": "MSc",
    "program_name": "MSc in Testing",
}


def test_validate_extraction_passes_clean_data():
    clean_text = "MSc in Testing at Test University. Tuition: 15,000 EUR per year."
    data = dict(BASE_FIELDS, tuition_1st_year="15,000 EUR")
    assert validate_extraction(data, clean_text) == []


def test_validate_extraction_flags_missing_required_field():
    data = dict(BASE_FIELDS, university_name="")
    problems = validate_extraction(data, "")
    assert any("university_name" in p for p in problems)


@pytest.mark.parametrize("placeholder", ["N/A", "n/a", "unknown", "-", "None"])
def test_validate_extraction_flags_placeholder_required_field(placeholder):
    data = dict(BASE_FIELDS, program_name=placeholder)
    problems = validate_extraction(data, "")
    assert any("program_name" in p for p in problems)


def test_validate_extraction_flags_non_numeric_numeric_field():
    data = dict(BASE_FIELDS, duration="several years")  # no digit at all
    problems = validate_extraction(data, "")
    assert any("duration" in p and "no digit" in p for p in problems)


def test_validate_extraction_flags_ungrounded_value():
    """The value has a digit and the right shape, but never appears on the
    page at all — this is the hallucination case shape-only checks miss."""
    clean_text = "MSc in Testing at Test University. Tuition: 15,000 EUR per year."
    data = dict(BASE_FIELDS, tuition_1st_year="99,999 EUR")
    problems = validate_extraction(data, clean_text)
    assert any("not grounded" in p for p in problems)


def test_validate_extraction_flags_bundled_eu_non_eu_tuition():
    """Regression test for the "tuition front-loading" bug the manual
    scrape had to catch and fix by hand (AspiroBrain Data Pipeline Plan) —
    a compound EU/Non-EU string has digits and both amounts are grounded,
    so only a shape-specific check catches it."""
    clean_text = (
        "MSc in Testing at Test University. "
        "Tuition: EU: 2695 EUR/yr; Non-EU: 18873 EUR/yr"
    )
    data = dict(BASE_FIELDS, tuition_1st_year="EU: 2695 EUR/yr; Non-EU: 18873 EUR/yr")
    problems = validate_extraction(data, clean_text)
    assert any("bundles multiple tuition tiers" in p for p in problems)


def test_validate_extraction_passes_single_clean_tuition_figure():
    clean_text = "MSc in Testing at Test University. Tuition: 18873 EUR/yr (non-EU)"
    data = dict(BASE_FIELDS, tuition_1st_year="18873 EUR/yr")
    assert validate_extraction(data, clean_text) == []


def test_validate_extraction_skips_grounding_check_for_short_digit_runs():
    """A 1-2 digit value (e.g. "7 years") is too likely to coincidentally
    not appear verbatim even when correct — skip the grounding check rather
    than risk false-positive escalation on nearly every short number."""
    clean_text = "MSc in Testing at Test University."
    data = dict(BASE_FIELDS, duration="7 years")
    assert validate_extraction(data, clean_text) == []


# ---------------------------------------------------------------------------
# extract() — the Haiku -> Sonnet -> Opus escalation cascade (mocked)
# ---------------------------------------------------------------------------


def _fake_llm_result(**overrides):
    base = {
        "program_image_url": None,
        "university_name": None,
        "level": None,
        "program_name": None,
        "destination": None,
        "location": None,
        "campus_city": None,
        "tuition_1st_year": None,
        "application_fee": None,
        "duration": None,
        "success_rate": None,
        "intake_terms": [],
        "deadlines": [],
        "prerequisites": [],
        "must_requirements": [],
        "tags": [],
    }
    base.update(overrides)
    return base


def test_extract_stops_at_tier_one_on_clean_result():
    calls = []

    def fake_llm(clean_text, url, model, feedback=None):
        calls.append(model)
        return _fake_llm_result(university_name="Oxford", level="MSc", program_name="MSc in Testing"), {
            "input_tokens": 300,
            "output_tokens": 50,
        }

    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract("<html></html>", "https://example.com/happy")

    assert calls == ["claude-haiku-4-5"]
    assert result["_extraction_method"] == "llm-haiku"
    assert result["_usage"] == {"model": "claude-haiku-4-5", "input_tokens": 300, "output_tokens": 50}


def test_extract_escalates_with_feedback_on_validation_failure():
    calls = []

    def fake_llm(clean_text, url, model, feedback=None):
        calls.append((model, feedback))
        if model == "claude-haiku-4-5":
            # missing university_name -> validator should reject this
            return _fake_llm_result(level="MSc", program_name="MSc in Testing"), {
                "input_tokens": 400,
                "output_tokens": 60,
            }
        return _fake_llm_result(
            university_name="Test University", level="MSc", program_name="MSc in Testing"
        ), {"input_tokens": 400, "output_tokens": 60}

    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract("<html></html>", "https://example.com/needs-escalation")

    assert [c[0] for c in calls] == ["claude-haiku-4-5", "claude-sonnet-5"]
    assert calls[1][1] is not None and any("university_name" in p for p in calls[1][1])
    assert result["_extraction_method"] == "llm-sonnet"


def test_extract_falls_back_to_heuristic_when_all_tiers_fail():
    def fake_llm(clean_text, url, model, feedback=None):
        raise RuntimeError("simulated API failure")

    html = "<html><head><title>Legal Research</title></head><body></body></html>"
    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract(html, "https://example.com/no-credentials")

    assert result["_extraction_method"] == "heuristic"
    assert result["_usage"] is None


# ---------------------------------------------------------------------------
# content_hash / has_content_changed / record_extraction_state — change detection
# ---------------------------------------------------------------------------


def test_content_hash_is_deterministic_and_sensitive_to_change():
    a = content_hash("MSc in Testing at Test University")
    b = content_hash("MSc in Testing at Test University")
    c = content_hash("MSc in Testing at Test University, tuition raised to 20000 EUR")
    assert a == b
    assert a != c
    assert a.startswith("sha256:")


def test_has_content_changed_true_when_no_prior_record(tmp_path):
    """No history yet is treated as needing extraction, not as an error —
    covers both a genuinely new URL and a URL scraped before this feature
    existed."""
    state_path = tmp_path / "extraction_state.json"
    assert has_content_changed("https://example.com/new", "some page text", state_path) is True


def test_has_content_changed_false_when_hash_matches(tmp_path):
    state_path = tmp_path / "extraction_state.json"
    url = "https://example.com/program"
    record_extraction_state(url, "MSc in Testing, tuition 15000 EUR", "llm-haiku", state_path)

    assert has_content_changed(url, "MSc in Testing, tuition 15000 EUR", state_path) is False


def test_has_content_changed_true_when_page_content_differs(tmp_path):
    """The actual scenario this feature exists for: a program's page was
    scraped once, then its data changed (e.g. tuition increased) — the next
    check must recognize that and flag it for re-extraction."""
    state_path = tmp_path / "extraction_state.json"
    url = "https://example.com/program"
    record_extraction_state(url, "MSc in Testing, tuition 15000 EUR", "llm-haiku", state_path)

    assert has_content_changed(url, "MSc in Testing, tuition 20000 EUR", state_path) is True


def test_record_extraction_state_roundtrip(tmp_path):
    state_path = tmp_path / "extraction_state.json"
    record_extraction_state("https://example.com/a", "page text", "llm-sonnet", state_path)

    state = json.loads(state_path.read_text())
    entry = state["https://example.com/a"]
    assert entry["extraction_method"] == "llm-sonnet"
    assert entry["content_hash"] == content_hash("page text")
    assert "last_extracted_at" in entry
