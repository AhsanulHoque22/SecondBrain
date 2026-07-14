"""Pure-logic tests for canary.py — no network, no live LLM calls.

Covers the credential-aware heuristic-fallback check: a canary run that
silently falls back to the heuristic path while a provider credential is
configured must FAIL, not PASS, since that means the LLM path isn't
actually working (see README/discussion — a broken key previously gave
false confidence)."""

from pathlib import Path
from unittest.mock import patch

from canary import _llm_should_be_reachable, check_url
from collector import Collected


def test_llm_should_be_reachable_false_with_no_credential(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    assert _llm_should_be_reachable() is False


def test_llm_should_be_reachable_true_with_credential_set(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-fake-key-for-test")
    assert _llm_should_be_reachable() is True


def _fake_extraction(method):
    return {
        "university_name": "Test University",
        "level": "MSc",
        "program_name": "MSc in Testing",
        "_extraction_method": method,
        "_usage": None,
    }


def test_check_url_passes_heuristic_when_no_credential_configured(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    collected = Collected(
        url="https://example.com/1", html="<html></html>", raw_path=tmp_path / "x.html", fetched_at="T1"
    )
    with patch("canary.collect", return_value=collected), patch(
        "canary.extract", return_value=_fake_extraction("heuristic")
    ):
        ok, detail = check_url("https://example.com/1", Path(tmp_path))
    assert ok is True
    assert "heuristic" in detail


def test_check_url_fails_heuristic_when_credential_configured():
    """The regression this file exists for: a broken/misconfigured key
    silently falling back to heuristic must not report PASS."""
    with patch("canary._llm_should_be_reachable", return_value=True), patch(
        "canary.collect",
        return_value=Collected(url="https://example.com/1", html="<html></html>", raw_path=Path("x"), fetched_at="T1"),
    ), patch("canary.extract", return_value=_fake_extraction("heuristic")):
        ok, detail = check_url("https://example.com/1", Path("."))
    assert ok is False
    assert "isn't actually working" in detail


def test_check_url_passes_when_llm_tier_actually_used():
    with patch("canary._llm_should_be_reachable", return_value=True), patch(
        "canary.collect",
        return_value=Collected(url="https://example.com/1", html="<html></html>", raw_path=Path("x"), fetched_at="T1"),
    ), patch("canary.extract", return_value=_fake_extraction("llm-haiku")):
        ok, detail = check_url("https://example.com/1", Path("."))
    assert ok is True
    assert "llm-haiku" in detail
