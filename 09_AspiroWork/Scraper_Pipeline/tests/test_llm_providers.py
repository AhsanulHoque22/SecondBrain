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
