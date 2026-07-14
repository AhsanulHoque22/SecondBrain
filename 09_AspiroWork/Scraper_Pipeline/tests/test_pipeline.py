"""Pure-logic tests for pipeline.py — no network, no LLM calls."""

import csv
from unittest.mock import patch

import pipeline
from cleaner import append_to_csv, clean_record
from collector import Collected
from pipeline import RunResult, _load_existing_source_urls, _print_cost_report, refresh_if_changed


# ---------------------------------------------------------------------------
# _load_existing_source_urls — the resume feature
# ---------------------------------------------------------------------------


def test_load_existing_source_urls_empty_when_no_output_file(tmp_path):
    assert _load_existing_source_urls(tmp_path / "does_not_exist.csv") == set()


def test_load_existing_source_urls_returns_urls_already_written(tmp_path):
    csv_path = tmp_path / "programs.csv"
    row = clean_record(
        {"university_name": "Test University", "level": "MSc", "program_name": "Testing"},
        "https://example.com/1",
    )
    append_to_csv(row, csv_path)

    urls = _load_existing_source_urls(csv_path)
    assert urls == {"https://example.com/1"}


# ---------------------------------------------------------------------------
# _print_cost_report
# ---------------------------------------------------------------------------


def test_print_cost_report_empty_usages_prints_nothing(capsys):
    _print_cost_report([])
    assert capsys.readouterr().out == ""


def test_print_cost_report_sums_by_model(capsys):
    usages = [
        {"model": "claude-haiku-4-5", "input_tokens": 4000, "output_tokens": 800},
        {"model": "claude-haiku-4-5", "input_tokens": 3500, "output_tokens": 700},
        {"model": "claude-sonnet-5", "input_tokens": 4200, "output_tokens": 900},
    ]
    _print_cost_report(usages)
    out = capsys.readouterr().out
    assert "claude-haiku-4-5" in out
    assert "2 calls" in out  # two haiku calls summed into one line
    assert "claude-sonnet-5" in out
    assert "total" in out


def test_run_result_defaults_usage_to_none():
    result = RunResult("OK example")
    assert result.usage is None


# ---------------------------------------------------------------------------
# main() — resumed URLs must not sleep (regression: previously slept
# delay+jitter per resumed URL despite making no network call)
# ---------------------------------------------------------------------------


def test_resumed_urls_do_not_sleep(tmp_path):
    csv_path = tmp_path / "programs.csv"
    urls = ["https://example.com/1", "https://example.com/2"]
    for i, url in enumerate(urls):
        row = clean_record(
            {"university_name": "Test University", "level": "MSc", "program_name": f"Testing {i}"},
            url,
        )
        append_to_csv(row, csv_path)

    argv = ["pipeline.py", "--output", str(csv_path)]
    for url in urls:
        argv.extend(["--url", url])

    with patch("sys.argv", argv), patch("pipeline.time.sleep") as mock_sleep:
        pipeline.main()

    mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# refresh_if_changed — change-detection re-extraction path
# ---------------------------------------------------------------------------


def _fake_extraction(**overrides):
    base = {
        "program_image_url": None,
        "university_name": "Test University",
        "level": "MSc",
        "program_name": "Program One",
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
        "_extraction_method": "llm-haiku",
        "_usage": None,
    }
    base.update(overrides)
    return base


def test_refresh_if_changed_skips_extraction_when_content_unchanged(tmp_path):
    """The whole point of the feature: an unchanged page costs a fetch, not
    an LLM call."""
    csv_path = tmp_path / "programs.csv"
    state_path = tmp_path / "extraction_state.json"
    url = "https://example.com/1"

    collected = Collected(url=url, html="<html>same content</html>", raw_path=tmp_path / "x.html", fetched_at="T1")
    extract_calls = []

    with patch("pipeline.collect", return_value=collected), patch(
        "pipeline.extract", side_effect=lambda *a, **k: extract_calls.append(1) or _fake_extraction()
    ):
        # First pass establishes the baseline hash via run(), not refresh_if_changed
        from pipeline import run

        run(url, csv_path, tmp_path, state_path)
        assert extract_calls == [1]

        result = refresh_if_changed(url, csv_path, tmp_path, state_path)

    assert extract_calls == [1]  # NOT called a second time — content didn't change
    assert result.message.startswith("UNCHANGED")


def test_refresh_if_changed_reextracts_and_updates_row_when_content_changed(tmp_path):
    csv_path = tmp_path / "programs.csv"
    state_path = tmp_path / "extraction_state.json"
    url = "https://example.com/1"

    collected_v1 = Collected(url=url, html="<html>v1</html>", raw_path=tmp_path / "x.html", fetched_at="T1")
    collected_v2 = Collected(url=url, html="<html>v2 - tuition changed</html>", raw_path=tmp_path / "x.html", fetched_at="T2")

    from pipeline import run

    with patch("pipeline.collect", return_value=collected_v1), patch(
        "pipeline.extract", return_value=_fake_extraction(tuition_1st_year="15,000 EUR")
    ):
        run(url, csv_path, tmp_path, state_path)

    with patch("pipeline.collect", return_value=collected_v2), patch(
        "pipeline.extract", return_value=_fake_extraction(tuition_1st_year="20,000 EUR")
    ):
        result = refresh_if_changed(url, csv_path, tmp_path, state_path)

    assert result.message.startswith("UPDATED")
    rows = list(csv.DictReader(csv_path.open()))
    assert len(rows) == 1  # replaced in place, not appended
    assert rows[0]["tuition_1st_year"] == "20,000 EUR"
