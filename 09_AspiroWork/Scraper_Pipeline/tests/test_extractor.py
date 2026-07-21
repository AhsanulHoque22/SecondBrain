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

import extractor
from cleaner import clean_record
from extractor import (
    DEFAULT_ANTHROPIC_CASCADE,
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


def test_heuristic_nulls_out_bundled_tuition_instead_of_keeping_it():
    """The LLM path escalates to a stronger tier on a bundled EU/non-EU
    tuition figure (validate_extraction); heuristic has no further tier to
    escalate to, so it must null the field instead of keeping a merged
    value that looks like a single first-year figure but isn't."""
    html = "<html><head><title>Test Program</title></head><body></body></html>"
    clean_text = "Tuition: EU: 2695 EUR/yr; Non-EU: 18873 EUR/yr"
    data = extract_via_heuristics(html, clean_text, "https://example.com/test")
    assert data["tuition_1st_year"] is None


def test_heuristic_keeps_a_clean_single_tuition_figure():
    html = "<html><head><title>Test Program</title></head><body></body></html>"
    clean_text = "Tuition: 28000 GBP per year"
    data = extract_via_heuristics(html, clean_text, "https://example.com/test")
    assert data["tuition_1st_year"] == "28000 GBP per year"


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
# validate_extraction — regression checks for the manual accuracy audit
# (Accuracy_Audit_Manual_Verification.txt) findings on programs_test_1.csv
# ---------------------------------------------------------------------------


def test_validate_extraction_flags_approximate_conversion_tuition():
    """Row 20: tuition_1st_year was the '≈ 15,063 EUR / year' parenthetical
    conversion note instead of the page's primary '2,120,681 BDT / year'
    figure — the '≈' character is never legitimately part of a real value."""
    clean_text = "Tuition: 2,120,681 BDT / year (≈ 15,063 EUR / year)"
    data = dict(BASE_FIELDS, tuition_1st_year="≈ 15,063 EUR")
    problems = validate_extraction(data, clean_text)
    assert any("approximate/converted estimate" in p for p in problems)


def test_validate_extraction_flags_tuition_shifted_into_application_fee():
    """Row 9: tuition_1st_year was left blank while the tuition figure was
    written into application_fee instead — the page had no real application
    fee at all."""
    clean_text = "Tuition: 2,775,483 BDT / year"
    data = dict(BASE_FIELDS, tuition_1st_year=None, application_fee="2,775,483")
    problems = validate_extraction(data, clean_text)
    assert any("written into application_fee by mistake" in p for p in problems)


def test_validate_extraction_flags_ranking_badge_as_success_rate():
    """Row 9: the 'Studyportals University Meta Ranking' badge ('Top 1%
    worldwide') was mislabeled as success_rate, which is an admission/
    graduate-outcome statistic, not a site ranking."""
    clean_text = "Studyportals University Meta Ranking: Top 1% worldwide"
    data = dict(BASE_FIELDS, success_rate="Top 1% worldwide")
    problems = validate_extraction(data, clean_text)
    assert any("site ranking badge" in p for p in problems)


def test_validate_extraction_flags_intake_terms_missing_year():
    """Rows 2, 5, 13, 16, 17, 18: intake_terms kept only the month
    ('September'), dropping the year the page actually printed."""
    clean_text = "Starting September 2027"
    data = dict(BASE_FIELDS, intake_terms=["September"])
    problems = validate_extraction(data, clean_text)
    assert any("has no year" in p for p in problems)


def test_validate_extraction_passes_intake_terms_with_year():
    clean_text = "Starting September 2027"
    data = dict(BASE_FIELDS, intake_terms=["September 2027"])
    assert validate_extraction(data, clean_text) == []


def test_validate_extraction_flags_empty_tags_with_disciplines_section():
    """15 of 20 rows in the audit left tags blank despite the page's own
    'Disciplines' section clearly listing one or more subject tags."""
    clean_text = "Disciplines\nPublic Health"
    data = dict(BASE_FIELDS, tags=[])
    problems = validate_extraction(data, clean_text)
    assert any("Disciplines" in p for p in problems)


def test_validate_extraction_flags_blank_location_with_campus_section():
    """Row 2 (GRACE joint programme): both location and campus_city were
    left blank even though the page's Campus Location widget listed all
    three partner cities/countries."""
    clean_text = "Campus Location\nSankt Pölten, Austria\nValmiera, Latvia\nEnschede, Netherlands"
    data = dict(BASE_FIELDS, location="", campus_city="")
    problems = validate_extraction(data, clean_text)
    assert any("Campus Location" in p for p in problems)


def test_validate_extraction_flags_swapped_location_campus_city():
    """Row 20: location was 'Netherlands' (missing the city) while
    campus_city held 'Nijmegen, Netherlands' (the full pair) — the two
    fields' content was swapped/overlapping."""
    clean_text = "Campus Location: Nijmegen, Netherlands"
    data = dict(BASE_FIELDS, location="Netherlands", campus_city="Nijmegen, Netherlands")
    problems = validate_extraction(data, clean_text)
    assert any("look inconsistent" in p for p in problems)


def test_validate_extraction_passes_correctly_split_location():
    clean_text = "Campus Location: Nijmegen, Netherlands"
    data = dict(BASE_FIELDS, location="Nijmegen, Netherlands", campus_city="Nijmegen")
    assert validate_extraction(data, clean_text) == []


def test_validate_extraction_flags_dropped_english_test_score():
    """Rows 6, 9, 10, 12, 18: a concrete 'TOEFL iBT 90 / IELTS 6.5'
    requirement on the page was dropped entirely from both requirement
    fields."""
    clean_text = "English requirements: TOEFL iBT 90 or IELTS 6.5"
    data = dict(BASE_FIELDS, prerequisites=[], must_requirements=[{"title": "Bachelor's diploma", "description": None}])
    problems = validate_extraction(data, clean_text)
    assert any("TOEFL/IELTS score" in p for p in problems)


def test_validate_extraction_passes_captured_english_test_score():
    clean_text = "English requirements: TOEFL iBT 90 or IELTS 6.5"
    data = dict(
        BASE_FIELDS,
        prerequisites=[],
        must_requirements=[{"title": "English requirements", "description": "TOEFL iBT 90 or IELTS 6.5"}],
    )
    assert validate_extraction(data, clean_text) == []


def test_validate_extraction_does_not_flag_scholarship_ad_as_english_requirement():
    """Regression test for a real false positive found live (2026-07-21) on
    two mastersportal.com program pages: a Studyportals scholarship/test-
    prep ad widget ("The Annual IELTS from 6 to 9 Scholarship", "Cathoven
    IELTS Preparation... Register for TOEFL now!") is not the programme's
    own English requirement — it's unrelated marketing boilerplate, same
    category of bug as the "Student Insurance via Studyportals Partner"
    must_requirements contamination found in the original manual audit.
    Both real pages had NO actual English-score requirement at all (one
    model correctly reported "we are not aware of any English requirements
    for this programme"), but this check rejected every LLM tier's output
    over it, forcing an unnecessary fall-through to the heuristic
    extractor."""
    clean_text = (
        "The Annual IELTS from 6 to 9 Scholarship\n"
        "IELTS from 6 to 9\n"
        "Cathoven IELTS Preparation\n"
        "Get your real, reliable IELTS score in seconds, free, with accurate scoring.\n"
        "Discover your IELTS Score now!\n"
        "TOEFL\n"
        "Stand out with the English test trusted by top universities and employers worldwide. "
        "Take TOEFL and open doors to your future!\n"
        "Register for TOEFL now!\n"
    )
    data = dict(
        BASE_FIELDS,
        prerequisites=[],
        must_requirements=[
            {"title": "English requirements", "description": "We are not aware of any English requirements for this programme"}
        ],
    )
    problems = validate_extraction(data, clean_text)
    assert not any("TOEFL/IELTS score" in p for p in problems)


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


def test_extract_stops_at_tier_one_on_clean_result(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    calls = []

    def fake_llm(clean_text, url, backend, model, feedback=None):
        calls.append((backend, model))
        return _fake_llm_result(university_name="Oxford", level="MSc", program_name="MSc in Testing"), {
            "input_tokens": 300,
            "output_tokens": 50,
        }

    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract("<html></html>", "https://example.com/happy")

    assert calls == [("anthropic", "claude-haiku-4-5")]
    assert result["_extraction_method"] == "llm-haiku"
    assert result["_usage"] == {
        "model": "claude-haiku-4-5",
        "backend": "anthropic",
        "input_tokens": 300,
        "output_tokens": 50,
    }


def test_extract_escalates_with_feedback_on_validation_failure(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    calls = []

    def fake_llm(clean_text, url, backend, model, feedback=None):
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


def test_extract_falls_back_to_heuristic_when_all_tiers_fail(monkeypatch, capsys):
    """Configured but every call fails outright (bad key, network error,
    exhausted quota) — distinct from test_extract_falls_back_to_heuristic_
    with_no_backend_configured below, where nothing is even attempted."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    calls = []

    def fake_llm(clean_text, url, backend, model, feedback=None):
        calls.append((backend, model))
        raise RuntimeError("simulated API failure")

    html = "<html><head><title>Legal Research</title></head><body></body></html>"
    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract(html, "https://example.com/no-credentials")

    assert calls == [("anthropic", m) for m in DEFAULT_ANTHROPIC_CASCADE]
    assert result["_extraction_method"] == "heuristic"
    assert result["_usage"] is None
    assert "all LLM backends/tiers failed" in capsys.readouterr().err


def test_extract_falls_back_to_heuristic_with_no_backend_configured(monkeypatch, capsys):
    """No credential set at all for the active backend (or chain) — the new
    pre-filter in _backend_chain skips straight to heuristic without
    attempting a single call, since there's nothing to call with. Regression:
    this used to print the exact same "all LLM backends/tiers failed"
    message as the case above, even though zero calls were ever attempted —
    real confusion when debugging why a batch never called the LLM (e.g.
    .env silently not loaded), since the message implied real attempts had
    been made and failed."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")

    def fake_llm(clean_text, url, backend, model, feedback=None):
        raise AssertionError("should never be called — no backend is configured")

    html = "<html><head><title>Legal Research</title></head><body></body></html>"
    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract(html, "https://example.com/no-credentials")

    assert result["_extraction_method"] == "heuristic"
    assert result["_usage"] is None
    stderr = capsys.readouterr().err
    assert "no LLM backend is configured" in stderr
    assert "all LLM backends/tiers failed" not in stderr


# ---------------------------------------------------------------------------
# _coerce_extracted_shapes — defensive normalization of a loosely-typed LLM
# response, so a weak/free-tier model's malformed output can't crash
# cleaner.py's normalize_* helpers downstream (AttributeError deep in
# clean_record, turning one odd response into a whole-URL ERROR)
# ---------------------------------------------------------------------------


def test_coerce_extracted_shapes_nulls_out_wrong_typed_scalar():
    data = extractor._coerce_extracted_shapes(dict(BASE_FIELDS, university_name=["Test University"]))
    assert data["university_name"] is None


def test_coerce_extracted_shapes_keeps_valid_scalar():
    data = extractor._coerce_extracted_shapes(dict(BASE_FIELDS))
    assert data["university_name"] == "Test University"


def test_coerce_extracted_shapes_empties_non_list_repeatable_field():
    data = extractor._coerce_extracted_shapes(dict(BASE_FIELDS, intake_terms="September 2027"))
    assert data["intake_terms"] == []


def test_coerce_extracted_shapes_drops_non_str_items_from_repeatable_field():
    data = extractor._coerce_extracted_shapes(dict(BASE_FIELDS, deadlines=["May 2027", 2027, None]))
    assert data["deadlines"] == ["May 2027"]


def test_coerce_extracted_shapes_drops_non_dict_items_from_requirement_pairs():
    """Regression shape: a model returning bare strings instead of
    {"title":..., "description":...} objects for must_requirements —
    normalize_requirement_pairs would crash calling .get() on a string."""
    data = extractor._coerce_extracted_shapes(
        dict(BASE_FIELDS, must_requirements=[{"title": "Bachelor's", "description": None}, "TOEFL 90"])
    )
    assert data["must_requirements"] == [{"title": "Bachelor's", "description": None}]


def test_coerce_extracted_shapes_drops_non_dict_items_from_tags():
    data = extractor._coerce_extracted_shapes(dict(BASE_FIELDS, tags=[{"name": "Physics", "category": None, "details": None}, "Chemistry"]))
    assert data["tags"] == [{"name": "Physics", "category": None, "details": None}]


def test_coerce_extracted_shapes_does_not_crash_cleaner_on_malformed_llm_output():
    """End-to-end guard: feed clean_record the exact kind of malformed shape
    a loosely-typed model could produce and confirm it no longer raises."""
    malformed = dict(
        BASE_FIELDS,
        tags=["Physics", "Chemistry"],  # should be list[dict], not list[str]
        must_requirements=["Bachelor's diploma"],  # same issue
        intake_terms="September 2027",  # should be a list, not a bare string
    )
    coerced = extractor._coerce_extracted_shapes(malformed)
    row = clean_record(coerced, "https://example.com/test")
    assert row["tags"] == ""
    assert row["must_requirements"] == ""
    assert row["intake_terms"] == ""


# ---------------------------------------------------------------------------
# _load_extraction_state — corrupted state file must not crash the batch
# ---------------------------------------------------------------------------


def test_load_extraction_state_recovers_from_corrupted_json(tmp_path, capsys):
    state_path = tmp_path / "extraction_state.json"
    state_path.write_text("{not valid json", encoding="utf-8")
    result = extractor._load_extraction_state(state_path)
    assert result == {}
    assert "corrupted" in capsys.readouterr().err


def test_load_extraction_state_reads_valid_state(tmp_path):
    state_path = tmp_path / "extraction_state.json"
    state_path.write_text('{"https://example.com": {"content_hash": "sha256:abc"}}', encoding="utf-8")
    result = extractor._load_extraction_state(state_path)
    assert result == {"https://example.com": {"content_hash": "sha256:abc"}}


# ---------------------------------------------------------------------------
# _backend_chain / _cascade_for_backend — cross-backend fallback config
# ---------------------------------------------------------------------------


def test_cascade_for_backend_uses_builtin_default_for_verified_backend(monkeypatch):
    monkeypatch.delenv("GROQ_MODEL_CASCADE", raising=False)
    monkeypatch.delenv("EXTRACTION_MODEL_CASCADE", raising=False)
    assert extractor._cascade_for_backend("groq") == extractor.DEFAULT_BACKEND_CASCADES["groq"]


def test_cascade_for_backend_prefers_explicit_backend_env_var(monkeypatch):
    monkeypatch.setenv("GROQ_MODEL_CASCADE", "custom-model-a,custom-model-b")
    assert extractor._cascade_for_backend("groq") == ["custom-model-a", "custom-model-b"]


def test_cascade_for_backend_raises_when_nothing_configured_for_unverified_backend(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL_CASCADE", raising=False)
    monkeypatch.delenv("EXTRACTION_MODEL_CASCADE", raising=False)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)  # provider defaults to anthropic, so "openai" != primary
    with pytest.raises(RuntimeError, match="no model cascade configured"):
        extractor._cascade_for_backend("openai")


def test_default_groq_cascade_has_no_known_dead_model_ids():
    """Regression test for the real bug found via a live canary run
    (2026-07-21): meta-llama/llama-4-scout-17b-16e-instruct and
    qwen/qwen3-32b both started 404ing ("does not exist or you do not have
    access to it") against Groq's own GET /openai/v1/models — Groq had
    retired/renamed them since this cascade was last live-tested. A dead
    model ID silently wastes a call (and a throttle wait) on every single
    URL before the cascade ever reaches a working tier, and nothing before
    this test would have caught that regressing again."""
    known_dead_model_ids = {"meta-llama/llama-4-scout-17b-16e-instruct", "qwen/qwen3-32b"}
    assert not known_dead_model_ids & set(extractor.DEFAULT_BACKEND_CASCADES["groq"])


def test_backend_chain_defaults_to_single_legacy_provider(monkeypatch):
    monkeypatch.delenv("LLM_BACKEND_CHAIN", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    assert extractor._backend_chain() == [("anthropic", m) for m in DEFAULT_ANTHROPIC_CASCADE]


def test_backend_chain_skips_unconfigured_backends(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND_CHAIN", "groq,anthropic")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)  # groq: no key -> skipped entirely
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    assert extractor._backend_chain() == [("anthropic", m) for m in DEFAULT_ANTHROPIC_CASCADE]


def test_backend_chain_combines_multiple_configured_backends_in_order(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND_CHAIN", "groq,anthropic")
    monkeypatch.setenv("GROQ_API_KEY", "gsk-fake-key-for-test")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    chain = extractor._backend_chain()
    assert chain[: len(extractor.DEFAULT_BACKEND_CASCADES["groq"])] == [
        ("groq", m) for m in extractor.DEFAULT_BACKEND_CASCADES["groq"]
    ]
    assert chain[-len(DEFAULT_ANTHROPIC_CASCADE) :] == [("anthropic", m) for m in DEFAULT_ANTHROPIC_CASCADE]


def test_backend_chain_skips_unknown_backend_name(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND_CHAIN", "not-a-real-backend,anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    assert extractor._backend_chain() == [("anthropic", m) for m in DEFAULT_ANTHROPIC_CASCADE]


def test_extract_falls_through_to_second_backend_when_first_is_entirely_unreachable(monkeypatch):
    """The actual "try a few others before aborting" behavior: backend A
    (e.g. a Gemini key blocked by zero quota) fails outright on every one
    of its models, and extract() moves on to backend B instead of dropping
    straight to the heuristic path."""
    monkeypatch.setenv("LLM_BACKEND_CHAIN", "google,anthropic")
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-google-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")

    calls = []

    def fake_llm(clean_text, url, backend, model, feedback=None):
        calls.append((backend, model))
        if backend == "google":
            raise RuntimeError("429 RESOURCE_EXHAUSTED — simulated zero quota")
        return _fake_llm_result(university_name="Oxford", level="MSc", program_name="MSc in Testing"), {
            "input_tokens": 300,
            "output_tokens": 50,
        }

    with patch("extractor.extract_via_llm", side_effect=fake_llm):
        result = extract("<html></html>", "https://example.com/failover")

    assert calls[: len(extractor.DEFAULT_BACKEND_CASCADES["google"])] == [
        ("google", m) for m in extractor.DEFAULT_BACKEND_CASCADES["google"]
    ]
    assert calls[-1] == ("anthropic", "claude-haiku-4-5")
    assert result["_extraction_method"] == "llm-haiku"
    assert result["_usage"]["backend"] == "anthropic"


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
