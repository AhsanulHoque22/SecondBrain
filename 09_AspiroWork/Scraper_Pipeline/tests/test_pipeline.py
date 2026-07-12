"""Pure-logic tests for pipeline.py — no network, no LLM calls."""

import csv

from cleaner import append_to_csv, clean_record
from pipeline import RunResult, _load_existing_source_urls, _print_cost_report


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
