"""Pure-logic tests for discover.py — no network."""

import pytest

from discover import _site_pattern_for, _with_page_param, extract_program_links


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
