"""Provider-agnostic LLM adapter layer.

One call shape in, one result shape out, regardless of which LLM vendor is
configured:

    call_llm(model, system_prompt, user_content, schema, tool_name, tool_description)
        -> (parsed_fields: dict, usage: {"input_tokens": int, "output_tokens": int})

The provider is selected by the LLM_PROVIDER environment variable:
"anthropic" (default), "openai", or "google". Each vendor SDK is imported
lazily inside its own function, so a user who only configures one provider
never needs the other two packages installed.

Verification status — read before trusting a provider in production:
- anthropic: the original, single-provider implementation this module was
  extracted from; exercised against the live API repeatedly during this
  pipeline's development.
- openai: implemented against OpenAI's documented strict function-calling
  contract. Not exercised against a live OpenAI account in this project (no
  credentials were available while writing it) — review its output on a
  handful of real pages before trusting it for a full batch.
- google: implemented against the documented google-generativeai structured-
  output contract, including a schema translation step (Gemini's schema
  dialect isn't plain JSON Schema — see _to_gemini_schema). This is the
  least-verified of the three providers; review carefully before relying on
  it.
"""

from __future__ import annotations

import json
import os


def get_provider() -> str:
    return os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()


def call_llm(
    model: str,
    system_prompt: str,
    user_content: str,
    schema: dict,
    tool_name: str,
    tool_description: str,
) -> tuple[dict, dict]:
    provider = get_provider()
    if provider == "anthropic":
        return _call_anthropic(model, system_prompt, user_content, schema, tool_name, tool_description)
    if provider == "openai":
        return _call_openai(model, system_prompt, user_content, schema, tool_name, tool_description)
    if provider == "google":
        return _call_google(model, system_prompt, user_content, schema, tool_name, tool_description)
    raise ValueError(
        f"Unknown LLM_PROVIDER {provider!r} — expected 'anthropic', 'openai', or 'google'. "
        "Set the LLM_PROVIDER environment variable to one of those."
    )


def _call_anthropic(
    model: str, system_prompt: str, user_content: str, schema: dict, tool_name: str, tool_description: str
) -> tuple[dict, dict]:
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic") from exc

    client = anthropic.Anthropic()
    tool = {
        "name": tool_name,
        "description": tool_description,
        "strict": True,
        "input_schema": schema,
    }
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        tools=[tool],
        tool_choice={"type": "tool", "name": tool_name},
        messages=[{"role": "user", "content": user_content}],
    )
    tool_use = next(block for block in response.content if block.type == "tool_use")
    usage = {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}
    return dict(tool_use.input), usage


def _call_openai(
    model: str, system_prompt: str, user_content: str, schema: dict, tool_name: str, tool_description: str
) -> tuple[dict, dict]:
    """OpenAI's strict function-calling mode requires every object in the
    schema to set additionalProperties: false and list every property as
    required (optional fields are expressed as nullable types instead of
    being left out of `required`) — schema.py's EXTRACTION_SCHEMA already
    follows that shape because the Anthropic path needed the same
    discipline, so no translation step is needed here, unlike Google."""
    try:
        import openai
    except ImportError as exc:
        raise RuntimeError("openai package not installed. Run: pip install openai") from exc

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": schema,
                    "strict": True,
                },
            }
        ],
        tool_choice={"type": "function", "function": {"name": tool_name}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    data = json.loads(tool_call.function.arguments)
    usage = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }
    return data, usage


def _to_gemini_schema(schema: dict) -> dict:
    """Translates a JSON-Schema-shaped dict (the dialect the Anthropic and
    OpenAI paths both consume directly) into Gemini's response_schema
    dialect, which differs in two ways this pipeline's schema actually uses:

    - `"type": ["string", "null"]` (a type union expressing "optional")
      becomes `"type": "STRING", "nullable": true`. Gemini has no type-union
      syntax.
    - `additionalProperties` isn't a recognized key and is dropped — Gemini
      has no equivalent, closed objects are the only behavior.

    Every other key (properties, items, required, description, enum) passes
    through unchanged, recursing into nested objects/arrays.
    """
    if not isinstance(schema, dict):
        return schema

    result: dict = {}
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        non_null = [t for t in schema_type if t != "null"]
        result["type"] = (non_null[0] if non_null else "string").upper()
        if "null" in schema_type:
            result["nullable"] = True
    elif isinstance(schema_type, str):
        result["type"] = schema_type.upper()

    if "properties" in schema:
        result["properties"] = {k: _to_gemini_schema(v) for k, v in schema["properties"].items()}
    if "items" in schema:
        result["items"] = _to_gemini_schema(schema["items"])
    if "required" in schema:
        result["required"] = schema["required"]
    if "description" in schema:
        result["description"] = schema["description"]

    return result


def _call_google(
    model: str, system_prompt: str, user_content: str, schema: dict, tool_name: str, tool_description: str
) -> tuple[dict, dict]:
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "google-generativeai package not installed. Run: pip install google-generativeai"
        ) from exc

    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        # Explicit over relying on SDK auto-detection of the env var — keeps
        # this path's credential source unambiguous and easy to grep for.
        genai.configure(api_key=api_key)

    generative_model = genai.GenerativeModel(model, system_instruction=system_prompt)
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=_to_gemini_schema(schema),
    )
    response = generative_model.generate_content(user_content, generation_config=generation_config)
    data = json.loads(response.text)
    usage = {
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
    }
    return data, usage
