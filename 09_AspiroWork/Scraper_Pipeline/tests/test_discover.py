"""Pure-logic tests for discover.py — no network."""

import json
from unittest.mock import patch

import pytest

from discover import (
    _load_discovered_urls,
    _merge_into_manifest,
    _save_discovered_urls,
    _site_pattern_for,
    _with_page_param,
    discover,
    extract_program_links,
)


def test_site_pattern_recognizes_mastersportal_with_and_without_www():
    a = _site_pattern_for("https://www.mastersportal.com/search/master/netherlands")
    b = _site_pattern_for("https://mastersportal.com/search/master/netherlands")
    assert a is b  # same registry entry


def test_site_pattern_raises_clear_error_for_unregistered_domain():
    with pytest.raises(ValueError, match="ox.ac.uk"):
        _site_pattern_for("https://www.ox.ac.uk/admissions/graduate/courses")


def test_extract_program_links_finds_json_embedded_links_not_just_href():
    """Regression test: the real links on mastersportal.com listing pages
    are embedded as JSON data ("url":"/studies/...html"), not <a href>
    tags — the first version of this pattern only matched href= and found
    zero links on a page that had 40 real ones."""
    pattern = _site_pattern_for("https://www.mastersportal.com/search").link_pattern
    html = '{"url":"/studies/8997/social-and-cultural-science.html","other":1}'
    links = extract_program_links(html, "https://www.mastersportal.com/search", pattern)
    assert links == ["https://www.mastersportal.com/studies/8997/social-and-cultural-science.html"]


def test_extract_program_links_dedupes_and_preserves_order():
    pattern = _site_pattern_for("https://www.mastersportal.com/search").link_pattern
    html = (
        '{"url":"/studies/8997/a.html"}'
        '{"url":"/studies/8996/b.html"}'
        '<a href="/studies/8997/a.html">dup, different location</a>'
    )
    links = extract_program_links(html, "https://www.mastersportal.com/search", pattern)
    assert links == [
        "https://www.mastersportal.com/studies/8997/a.html",
        "https://www.mastersportal.com/studies/8996/b.html",
    ]


def test_with_page_param_preserves_existing_query_params():
    url = "https://www.mastersportal.com/search?utm_source=google&gclid=abc"
    result = _with_page_param(url, 3, "page")
    assert "page=3" in result
    assert "utm_source=google" in result
    assert "gclid=abc" in result


# ---------------------------------------------------------------------------
# _merge_into_manifest — cross-run discovery dedup
# ---------------------------------------------------------------------------


def test_merge_into_manifest_dedupes_within_one_call_and_preserves_order():
    manifest = {}
    new_links = _merge_into_manifest(manifest, ["a", "b", "a"], "search1", "T1")
    assert new_links == ["a", "b"]
    assert manifest["a"] == {"first_discovered_at": "T1", "last_discovered_at": "T1", "discovered_via": "search1"}


def test_merge_into_manifest_dedupes_across_calls_and_bumps_last_seen():
    """Regression test for the real bug: discover.py used to overwrite
    urls.txt on every run, losing all memory of links found before."""
    manifest = {}
    _merge_into_manifest(manifest, ["a", "b"], "search1", "T1")

    new_links = _merge_into_manifest(manifest, ["a", "c"], "search2", "T2")

    assert new_links == ["c"]  # "a" was already known -> not reported as new
    assert manifest["a"]["first_discovered_at"] == "T1"  # unchanged
    assert manifest["a"]["last_discovered_at"] == "T2"  # bumped
    assert manifest["a"]["discovered_via"] == "search1"  # not overwritten by the second search
    assert manifest["c"]["first_discovered_at"] == "T2"


# ---------------------------------------------------------------------------
# _load_discovered_urls / _save_discovered_urls
# ---------------------------------------------------------------------------


def test_load_discovered_urls_empty_when_missing(tmp_path):
    assert _load_discovered_urls(tmp_path / "does_not_exist.json") == {}


def test_save_and_load_discovered_urls_roundtrip(tmp_path):
    state_path = tmp_path / "discovered_urls.json"
    manifest = {"https://example.com/a": {"first_discovered_at": "T1"}}
    _save_discovered_urls(state_path, manifest)
    assert _load_discovered_urls(state_path) == manifest


def test_save_discovered_urls_leaves_no_temp_file(tmp_path):
    state_path = tmp_path / "discovered_urls.json"
    _save_discovered_urls(state_path, {"a": {}})
    assert list(tmp_path.glob(f".{state_path.name}.*.tmp")) == []


def test_save_discovered_urls_is_atomic_on_crash(tmp_path, monkeypatch):
    state_path = tmp_path / "discovered_urls.json"
    _save_discovered_urls(state_path, {"a": {"first_discovered_at": "T1"}})
    before = state_path.read_text()

    import discover as discover_module

    def exploding_dump(*a, **k):
        raise RuntimeError("simulated crash mid-write")

    monkeypatch.setattr(discover_module.json, "dump", exploding_dump)

    with pytest.raises(RuntimeError):
        _save_discovered_urls(state_path, {"a": {}, "b": {}})

    assert state_path.read_text() == before
    assert list(tmp_path.glob(f".{state_path.name}.*.tmp")) == []


# ---------------------------------------------------------------------------
# discover() — end-to-end merge behavior, network mocked
# ---------------------------------------------------------------------------


def test_discover_second_run_against_same_search_finds_nothing_new(tmp_path):
    """The actual scenario that was broken: running discover.py twice
    against the same search used to silently produce the same URLs again
    (or lose them, depending on overwrite timing) instead of recognizing
    them as already known."""
    state_path = tmp_path / "discovered_urls.json"
    html = '{"url":"/studies/8997/a.html"}{"url":"/studies/8996/b.html"}'

    with patch("discover.fetch_html", return_value=html):
        first_run = discover("https://www.mastersportal.com/search", pages=1, state_path=state_path)
        second_run = discover("https://www.mastersportal.com/search", pages=1, state_path=state_path)

    assert len(first_run) == 2
    assert second_run == []  # nothing new — both links already in the manifest

    manifest = _load_discovered_urls(state_path)
    assert len(manifest) == 2  # not duplicated, not lost
