"""Pure-logic tests for collector.py — no network."""

from collector import CollectionError, HardBlockError, _is_hard_block, _url_hash


def test_url_hash_is_deterministic_and_short():
    a = _url_hash("https://example.com/program")
    b = _url_hash("https://example.com/program")
    c = _url_hash("https://example.com/other-program")
    assert a == b
    assert a != c
    assert len(a) == 16


def test_hard_block_detected_on_real_cloudflare_block_page_text():
    """Regression test: this exact page was actually returned by
    mastersportal.com mid-session during development (confirmed via
    screenshot) — a 200 response with real HTML, not a 403, so only content
    inspection catches it."""
    html = (
        "<html><body><h1>Sorry, you have been blocked</h1>"
        "<p>You are unable to access mastersportal.com</p></body></html>"
    )
    assert _is_hard_block(html) is True


def test_hard_block_not_falsely_detected_on_normal_page():
    html = "<html><head><title>MSc in Advanced Computer Science</title></head><body>Normal page content.</body></html>"
    assert _is_hard_block(html) is False


def test_hard_block_error_is_a_collection_error():
    """Must stay a CollectionError subclass so existing `except
    CollectionError` handlers (pipeline.py's per-URL error handling)
    continue to catch it without change — only callers that specifically
    want the distinction (for the longer cooldown) need to catch
    HardBlockError first."""
    assert issubclass(HardBlockError, CollectionError)
