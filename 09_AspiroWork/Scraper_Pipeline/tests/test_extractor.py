"""Pure-logic tests for extractor.py — no network, no LLM calls.

Covers the pieces that broke or almost broke during this pipeline's real
development: the level-backfill regex tiers (found missing "Master"/"LL.M."
on real mastersportal.com titles), the application_fee label-regex
false-positive (found "applicants from low-income countries;" leaking
through on ox.ac.uk), the validator's required/numeric/grounding checks,
and the Haiku->Sonnet->Opus escalation cascade (mocked — no live model
access from tests, ever).
"""

from unittest.mock import patch

import pytest

from extractor import (
    backfill_level,
    extract,
    extract_via_heuristics,
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
