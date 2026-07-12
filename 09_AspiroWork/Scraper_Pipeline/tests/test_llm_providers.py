"""Pure-logic tests for llm_providers.py — provider dispatch and Gemini
schema translation. No network, no live LLM calls, no vendor SDKs required
to be installed (the anthropic/openai/google call paths are only exercised
via extractor.py's mocked cascade tests, never live from this suite)."""

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
