"""Pure-logic tests for discover.py — no network."""

import json
from unittest.mock import Mock, patch

import pytest

from discover import (
    _load_discovered_urls,
    _merge_into_manifest,
    _save_discovered_urls,
    _site_pattern_for,
    _with_page_param,
    discover,
    extract_candidate_links,
    extract_program_links,
    extract_program_links_via_llm,
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


def test_load_discovered_urls_recovers_from_corrupted_json(tmp_path, capsys):
    state_path = tmp_path / "discovered_urls.json"
    state_path.write_text("{not valid json", encoding="utf-8")
    result = _load_discovered_urls(state_path)
    assert result == {}
    assert "corrupted" in capsys.readouterr().err


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


# ---------------------------------------------------------------------------
# extract_candidate_links — generic, site-agnostic first pass for --llm-discovery
# ---------------------------------------------------------------------------


def test_extract_candidate_links_finds_href_and_json_embedded_links():
    html = (
        '<a href="/studies/8798/legal-research.html">Legal Research</a>'
        '<script>var data = {"url":"/studies/9001/data-science.html"};</script>'
    )
    candidates = extract_candidate_links(html, "https://www.example.com/search")
    assert "https://www.example.com/studies/8798/legal-research.html" in candidates
    assert "https://www.example.com/studies/9001/data-science.html" in candidates


def test_extract_candidate_links_filters_asset_extensions():
    html = '<img src="/assets/logo.png"><link rel="stylesheet" href="/assets/site.css">'
    candidates = extract_candidate_links(html, "https://www.example.com/search")
    assert candidates == []


def test_extract_candidate_links_filters_other_domains():
    html = '<a href="https://tracker.example.org/pixel.gif">ad</a>'
    candidates = extract_candidate_links(html, "https://www.example.com/search")
    assert candidates == []


def test_extract_candidate_links_dedupes_and_caps():
    html = "".join(f'<a href="/studies/{i}/x.html">x</a>' for i in range(10))
    candidates = extract_candidate_links(html, "https://www.example.com/search", max_candidates=3)
    assert len(candidates) == 3


# ---------------------------------------------------------------------------
# extract_program_links_via_llm — LLM classification of candidates
# ---------------------------------------------------------------------------


def test_extract_program_links_via_llm_no_candidates_makes_no_llm_call():
    """The cheapest possible case: a page with nothing link-shaped on it
    should never spend an LLM call finding that out."""
    call_mock = Mock()
    with patch("discover.llm_providers.call_llm", call_mock):
        links, usage = extract_program_links_via_llm("<html><body>nothing here</body></html>", "https://example.com/search")
    assert links == []
    assert usage is None
    call_mock.assert_not_called()


def test_extract_program_links_via_llm_sends_paths_not_full_urls():
    html = '<a href="/studies/1/a.html">A</a>'
    captured = {}

    def fake_call_llm(model, system_prompt, user_content, schema, tool_name, tool_description):
        captured["user_content"] = user_content
        return {"program_page_paths": ["/studies/1/a.html"]}, {"input_tokens": 10, "output_tokens": 5}

    with patch("discover.llm_providers.call_llm", side_effect=fake_call_llm):
        links, usage = extract_program_links_via_llm(html, "https://www.example.com/search")

    assert links == ["https://www.example.com/studies/1/a.html"]
    assert usage == {"model": "claude-haiku-4-5", "input_tokens": 10, "output_tokens": 5}
    # The listing page's own URL is included once for context, but the
    # candidate list itself must be paths only, not repeated full URLs.
    candidate_section = captured["user_content"].split("Candidate link paths")[1]
    assert "https://www.example.com" not in candidate_section
    assert "/studies/1/a.html" in candidate_section


def test_extract_program_links_via_llm_drops_hallucinated_paths():
    """Defensive filter: a path the model returns that was never actually
    offered as a candidate must never be trusted, even if well-formed."""
    html = '<a href="/studies/1/a.html">A</a>'

    def fake_call_llm(model, system_prompt, user_content, schema, tool_name, tool_description):
        return (
            {"program_page_paths": ["/studies/1/a.html", "/studies/999/invented.html"]},
            {"input_tokens": 10, "output_tokens": 5},
        )

    with patch("discover.llm_providers.call_llm", side_effect=fake_call_llm):
        links, _usage = extract_program_links_via_llm(html, "https://www.example.com/search")

    assert links == ["https://www.example.com/studies/1/a.html"]


def test_extract_program_links_via_llm_uses_discovery_model_override(monkeypatch):
    monkeypatch.setenv("DISCOVERY_MODEL", "custom-model")
    html = '<a href="/studies/1/a.html">A</a>'
    captured = {}

    def fake_call_llm(model, system_prompt, user_content, schema, tool_name, tool_description):
        captured["model"] = model
        return {"program_page_paths": []}, {"input_tokens": 1, "output_tokens": 1}

    with patch("discover.llm_providers.call_llm", side_effect=fake_call_llm):
        extract_program_links_via_llm(html, "https://www.example.com/search")

    assert captured["model"] == "custom-model"


def test_discovery_model_raises_for_non_anthropic_provider_with_no_override(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("DISCOVERY_MODEL", raising=False)
    html = '<a href="/studies/1/a.html">A</a>'
    with pytest.raises(RuntimeError, match="no built-in default discovery model"):
        extract_program_links_via_llm(html, "https://www.example.com/search")


# ---------------------------------------------------------------------------
# discover(use_llm=True) — end-to-end, network and LLM mocked
# ---------------------------------------------------------------------------


def test_discover_with_llm_discovery_on_unregistered_domain(tmp_path):
    """The actual feature this exists for: a domain with no SITE_PATTERNS
    entry, which would otherwise raise ValueError outright, works via
    --llm-discovery instead."""
    state_path = tmp_path / "discovered_urls.json"
    html = '<a href="/studies/1/a.html">A</a><a href="/studies/2/b.html">B</a>'

    def fake_call_llm(model, system_prompt, user_content, schema, tool_name, tool_description):
        return (
            {"program_page_paths": ["/studies/1/a.html", "/studies/2/b.html"]},
            {"input_tokens": 300, "output_tokens": 30},
        )

    with patch("discover.fetch_html", return_value=html), patch(
        "discover.llm_providers.call_llm", side_effect=fake_call_llm
    ):
        links = discover("https://example.com/search", pages=1, state_path=state_path, use_llm=True)

    assert len(links) == 2


def test_discover_with_llm_discovery_falls_back_to_page_one_when_pagination_unknown(tmp_path):
    """An unregistered domain has no known pagination query-param — rather
    than guess one, multi-page requests silently collapse to a single fetch
    instead of crashing or silently walking the wrong param."""
    state_path = tmp_path / "discovered_urls.json"
    html = '<a href="/studies/1/a.html">A</a>'
    fetch_mock = Mock(return_value=html)

    def fake_call_llm(model, system_prompt, user_content, schema, tool_name, tool_description):
        return {"program_page_paths": ["/studies/1/a.html"]}, {"input_tokens": 10, "output_tokens": 5}

    with patch("discover.fetch_html", fetch_mock), patch("discover.llm_providers.call_llm", side_effect=fake_call_llm):
        discover("https://example.com/search", pages=5, state_path=state_path, use_llm=True)

    assert fetch_mock.call_count == 1  # not 5 — collapsed to a single page fetch


def test_discover_without_llm_still_raises_for_unregistered_domain(tmp_path):
    """Unchanged behavior: without --llm-discovery, an unregistered domain
    still raises immediately, same as before this feature existed."""
    state_path = tmp_path / "discovered_urls.json"
    with pytest.raises(ValueError, match="example.com"):
        discover("https://example.com/search", pages=1, state_path=state_path, use_llm=False)


def test_discover_with_llm_discovery_survives_one_page_failing(tmp_path):
    """Regression: an LLM classification failure on one page (bad key, rate
    limit past its retries, malformed JSON from a weak model) previously
    propagated straight out of discover() uncaught, aborting the whole
    multi-page walk — even though the exact same problem on the fetch side
    (CollectionError) has always just skipped that page and moved on."""
    state_path = tmp_path / "discovered_urls.json"
    html_ok = '<a href="/studies/1/a.html">A</a>'
    fetch_mock = Mock(return_value=html_ok)

    calls = {"n": 0}

    def flaky_call_llm(model, system_prompt, user_content, schema, tool_name, tool_description):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("simulated malformed model output")
        return {"program_page_paths": ["/studies/1/a.html"]}, {"input_tokens": 10, "output_tokens": 5}

    with patch("discover.fetch_html", fetch_mock), patch(
        "discover.llm_providers.call_llm", side_effect=flaky_call_llm
    ):
        # A registered domain (mastersportal.com) so pages=2 isn't collapsed
        # to a single fetch by the unregistered-pagination fallback.
        links = discover("https://www.mastersportal.com/search", pages=2, state_path=state_path, use_llm=True)

    assert fetch_mock.call_count == 2  # both pages were still fetched
    assert links == ["https://www.mastersportal.com/studies/1/a.html"]  # page 2's result survived page 1's failure
