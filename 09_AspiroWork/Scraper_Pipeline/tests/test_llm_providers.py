"""Pure-logic tests for llm_providers.py — provider dispatch and Gemini
schema translation. No network, no live LLM calls, no vendor SDKs required
to be installed (the anthropic/openai/google call paths are only exercised
via extractor.py's mocked cascade tests, never live from this suite)."""

from unittest.mock import patch

import pytest

import llm_providers


# ---------------------------------------------------------------------------
# get_provider / call_llm dispatch
# ---------------------------------------------------------------------------


def test_get_provider_defaults_to_anthropic(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    assert llm_providers.get_provider() == "anthropic"


def test_get_provider_reads_env_case_insensitively(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", " OpenAI ")
    assert llm_providers.get_provider() == "openai"


def test_call_llm_raises_on_unknown_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "not-a-real-provider")
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        llm_providers.call_llm("some-model", "sys", "user", {}, "tool", "desc")


# ---------------------------------------------------------------------------
# _to_gemini_schema — JSON Schema -> Gemini response_schema translation
# ---------------------------------------------------------------------------


def test_to_gemini_schema_translates_nullable_type_union():
    schema = {"type": ["string", "null"]}
    assert llm_providers._to_gemini_schema(schema) == {"type": "STRING", "nullable": True}


def test_to_gemini_schema_translates_plain_type():
    schema = {"type": "array", "items": {"type": "string"}}
    result = llm_providers._to_gemini_schema(schema)
    assert result["type"] == "ARRAY"
    assert result["items"] == {"type": "STRING"}


def test_to_gemini_schema_drops_additional_properties():
    schema = {"type": "object", "properties": {"x": {"type": "string"}}, "additionalProperties": False}
    result = llm_providers._to_gemini_schema(schema)
    assert "additionalProperties" not in result


def test_to_gemini_schema_recurses_into_nested_objects():
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": ["string", "null"]},
        },
        "required": ["title", "description"],
    }
    result = llm_providers._to_gemini_schema(schema)
    assert result["properties"]["title"] == {"type": "STRING"}
    assert result["properties"]["description"] == {"type": "STRING", "nullable": True}
    assert result["required"] == ["title", "description"]


# ---------------------------------------------------------------------------
# BACKENDS registry — is_backend_configured / call_llm_via_backend dispatch
# ---------------------------------------------------------------------------


def test_is_backend_configured_false_with_no_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    assert llm_providers.is_backend_configured("groq") is False


def test_is_backend_configured_true_with_key_set(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gsk-fake-key-for-test")
    assert llm_providers.is_backend_configured("groq") is True


def test_is_backend_configured_false_for_unknown_backend():
    assert llm_providers.is_backend_configured("not-a-real-backend") is False


def test_backend_credentials_are_isolated_between_openai_family_backends(monkeypatch):
    """groq and deepseek are both family="openai" but must never read each
    other's (or plain "openai"'s) API key/base URL — this is the whole
    point of the per-backend registry: several OpenAI-compatible endpoints
    configured side by side without clobbering each other."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setenv("GROQ_API_KEY", "gsk-groq-key")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-deepseek-key")

    assert llm_providers._backend_credentials("openai") == ("sk-openai-key", "https://api.openai.com/v1")
    assert llm_providers._backend_credentials("groq") == ("gsk-groq-key", "https://api.groq.com/openai/v1")
    assert llm_providers._backend_credentials("deepseek") == ("sk-deepseek-key", "https://api.deepseek.com")


def test_call_llm_via_backend_dispatches_anthropic_family():
    with patch("llm_providers._call_anthropic", return_value=({"x": 1}, {"input_tokens": 1, "output_tokens": 1})) as mock_call:
        result = llm_providers.call_llm_via_backend("anthropic", "claude-haiku-4-5", "sys", "user", {}, "tool", "desc")
    assert result == ({"x": 1}, {"input_tokens": 1, "output_tokens": 1})
    mock_call.assert_called_once_with("claude-haiku-4-5", "sys", "user", {}, "tool", "desc", api_key=None)


def test_call_llm_via_backend_dispatches_openai_family_with_backend_specific_credentials(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gsk-groq-key")
    with patch("llm_providers._call_openai", return_value=({}, {})) as mock_call:
        llm_providers.call_llm_via_backend("groq", "llama-3.1-8b-instant", "sys", "user", {}, "tool", "desc")
    mock_call.assert_called_once_with(
        "llama-3.1-8b-instant", "sys", "user", {}, "tool", "desc",
        api_key="gsk-groq-key", base_url="https://api.groq.com/openai/v1",
    )


def test_call_llm_via_backend_dispatches_google_family(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "AIza-fake-key")
    with patch("llm_providers._call_google", return_value=({}, {})) as mock_call:
        llm_providers.call_llm_via_backend("google", "gemini-2.0-flash", "sys", "user", {}, "tool", "desc")
    mock_call.assert_called_once_with("gemini-2.0-flash", "sys", "user", {}, "tool", "desc", api_key="AIza-fake-key")


def test_call_llm_via_backend_raises_on_unknown_backend():
    with pytest.raises(ValueError, match="Unknown backend"):
        llm_providers.call_llm_via_backend("not-a-real-backend", "some-model", "sys", "user", {}, "tool", "desc")


# ---------------------------------------------------------------------------
# Rate-limit handling — _estimate_tokens / _throttle / _retry_on_rate_limit
# ---------------------------------------------------------------------------


def test_estimate_tokens_scales_with_input_length():
    small = llm_providers._estimate_tokens("short")
    large = llm_providers._estimate_tokens("x" * 4000)
    assert small < large
    assert large == 1000  # 4000 chars / 4 chars-per-token


def test_estimate_tokens_sums_multiple_texts():
    assert llm_providers._estimate_tokens("aaaa", "bbbb") == llm_providers._estimate_tokens("aaaabbbb")


def test_throttle_is_no_op_for_backend_without_rate_limit(monkeypatch):
    """anthropic/google/deepseek/openai have no published free-tier limit
    in BACKENDS — _throttle must never sleep for them."""
    monkeypatch.setattr(llm_providers, "_last_call_at", {})
    with patch("time.sleep") as mock_sleep:
        llm_providers._throttle("anthropic", estimated_tokens=100000)
    mock_sleep.assert_not_called()


def test_throttle_does_not_sleep_on_first_call(monkeypatch):
    monkeypatch.setattr(llm_providers, "_last_call_at", {})
    with patch("time.sleep") as mock_sleep:
        llm_providers._throttle("groq", estimated_tokens=100)
    mock_sleep.assert_not_called()


def test_throttle_sleeps_to_respect_requests_per_minute(monkeypatch):
    """30 requests/min -> minimum 2s between calls. A tiny token estimate
    means the RPM floor, not the TPM ceiling, is what's driving the wait
    here."""
    monkeypatch.setattr(llm_providers, "_last_call_at", {"groq": 1000.0})
    with patch("time.monotonic", return_value=1000.5), patch("time.sleep") as mock_sleep:
        llm_providers._throttle("groq", estimated_tokens=10)
    mock_sleep.assert_called_once()
    (waited,), _ = mock_sleep.call_args
    assert waited == pytest.approx(1.5, abs=0.01)  # 2.0s floor - 0.5s already elapsed


def test_throttle_sleeps_to_respect_tokens_per_minute(monkeypatch):
    """A near-cap token estimate (4500 of Groq's 6,000 TPM) should demand a
    much longer wait than the bare 2s RPM floor."""
    monkeypatch.setattr(llm_providers, "_last_call_at", {"groq": 1000.0})
    with patch("time.monotonic", return_value=1000.0), patch("time.sleep") as mock_sleep:
        llm_providers._throttle("groq", estimated_tokens=4500)
    mock_sleep.assert_called_once()
    (waited,), _ = mock_sleep.call_args
    assert waited == pytest.approx(45.0, abs=0.01)  # 4500/6000 * 60s


def test_retry_on_rate_limit_retries_then_succeeds():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("simulated rate limit")
        return "ok"

    with patch("time.sleep") as mock_sleep:
        result = llm_providers._retry_on_rate_limit(flaky, (ValueError,))
    assert result == "ok"
    assert calls["n"] == 3
    assert mock_sleep.call_count == 2  # backoff before attempt 2 and attempt 3


def test_retry_on_rate_limit_raises_after_exhausting_retries():
    def always_fails():
        raise ValueError("simulated rate limit")

    with patch("time.sleep"), pytest.raises(ValueError, match="simulated rate limit"):
        llm_providers._retry_on_rate_limit(always_fails, (ValueError,))


def test_retry_on_rate_limit_does_not_retry_other_exception_types():
    """Only the named rate-limit exception type(s) get retried — an auth
    error or insufficient-balance error won't fix itself by waiting, so it
    must propagate on the first attempt."""
    calls = {"n": 0}

    def fails_with_wrong_type():
        calls["n"] += 1
        raise RuntimeError("not a rate limit")

    with patch("time.sleep") as mock_sleep, pytest.raises(RuntimeError, match="not a rate limit"):
        llm_providers._retry_on_rate_limit(fails_with_wrong_type, (ValueError,))
    assert calls["n"] == 1
    mock_sleep.assert_not_called()


def test_is_daily_rate_limit_detects_per_day_message():
    exc = ValueError(
        "Rate limit reached for model `openai/gpt-oss-20b` ... on tokens per day (TPD): "
        "Limit 200000, Used 198525, Requested 3866. Please try again in 17m12.912s."
    )
    assert llm_providers._is_daily_rate_limit(exc) is True


def test_is_daily_rate_limit_false_for_per_minute_message():
    exc = ValueError("Rate limit reached on requests per minute (RPM). Please try again in 2s.")
    assert llm_providers._is_daily_rate_limit(exc) is False


def test_retry_on_rate_limit_skips_backoff_for_daily_limit():
    """A per-day quota won't recover within any short backoff this
    function is willing to wait through — it should propagate immediately
    on the first attempt, not burn through the full retry budget first."""
    calls = {"n": 0}

    def hits_daily_limit():
        calls["n"] += 1
        raise ValueError("exceeded tokens per day (TPD) limit, try again in 17m")

    with patch("time.sleep") as mock_sleep, pytest.raises(ValueError, match="tokens per day"):
        llm_providers._retry_on_rate_limit(hits_daily_limit, (ValueError,))
    assert calls["n"] == 1  # no retries attempted at all
    mock_sleep.assert_not_called()
