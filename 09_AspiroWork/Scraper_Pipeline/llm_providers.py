"""Provider-agnostic LLM adapter layer.

Two call shapes in, one result shape out, regardless of which LLM vendor is
configured:

    call_llm(model, system_prompt, user_content, schema, tool_name, tool_description)
        -> (parsed_fields: dict, usage: {"input_tokens": int, "output_tokens": int})

    call_llm_via_backend(backend, model, system_prompt, user_content, schema, tool_name, tool_description)
        -> same result shape, but backend-explicit instead of reading
           LLM_PROVIDER — see the BACKENDS registry below.

call_llm() is the original single-provider path, selected by the
LLM_PROVIDER environment variable: "anthropic" (default), "openai", or
"google". call_llm_via_backend() is what extractor.py's cross-backend
fallback chain (LLM_BACKEND_CHAIN) uses to try several independently
configured endpoints — e.g. groq, then google, then deepseek — in one pass
without any of them reading each other's credentials; see the BACKENDS
registry for the full list and how each one's credentials are resolved.
Each vendor SDK is imported lazily inside its own function, so a user who
only configures one backend never needs the others' packages installed.

Verification status — read before trusting a backend in production:
- anthropic: the original, single-provider implementation this module was
  extracted from; exercised against the live API repeatedly during this
  pipeline's development.
- openai: implemented against OpenAI's documented strict function-calling
  contract. Not exercised against a live OpenAI account in this project (no
  credentials were available while writing it) — review its output on a
  handful of real pages before trusting it for a full batch.
- google: implemented against the documented google-generativeai structured-
  output contract, including a schema translation step (Gemini's schema
  dialect isn't plain JSON Schema — see _to_gemini_schema). Exercised live
  end-to-end (auth + schema translation both confirmed working) but every
  attempt so far has been rejected at the account level with a 0-quota
  free-tier error — see BACKENDS' "google" comment. Review actual output
  once a key with real quota is available.
- groq (family="openai", different base URL/key): same request/response
  contract as openai above, not yet exercised live in this project.
- deepseek (family="openai", different base URL/key): same request/response
  contract as openai above. Exercised live — authentication and the
  request shape both confirmed working — but rejected with 402 Insufficient
  Balance (DeepSeek has no free tier; the account needs a funded balance).
"""

from __future__ import annotations

import json
import os


def get_provider() -> str:
    return os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()


# --- Multi-backend registry ----------------------------------------------
# A "backend" is a concrete, independently-configured LLM endpoint: which
# vendor SDK to call (`family`) and where its own credentials live. This is
# a finer grain than `family` — "groq" and "deepseek" are both OpenAI-
# compatible endpoints (family="openai") but each gets its own API key and
# base URL, so they can be tried as independent fallback options instead of
# fighting over the single OPENAI_API_KEY / OPENAI_BASE_URL pair the plain
# "openai" backend still uses.
#
# This registry only feeds the *optional* cross-backend fallback chain
# (LLM_BACKEND_CHAIN, resolved in extractor.py's _backend_chain). The
# original single-provider path (LLM_PROVIDER + call_llm below) is
# untouched and keeps working exactly as before for anyone who hasn't
# opted in.
BACKENDS: dict[str, dict] = {
    "anthropic": {"family": "anthropic", "api_key_env": "ANTHROPIC_API_KEY"},
    "google": {"family": "google", "api_key_env": "GOOGLE_API_KEY"},
    "openai": {"family": "openai", "api_key_env": "OPENAI_API_KEY", "base_url_env": "OPENAI_BASE_URL"},
    # Groq's free tier serves open-weight models behind an OpenAI-compatible
    # endpoint — genuinely free, no billing required, which makes it the
    # best default first link in a free-tier fallback chain.
    "groq": {
        "family": "openai",
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
    },
    # DeepSeek is also OpenAI-compatible, but pay-as-you-go only (no free
    # tier) — a request against an unfunded account fails with 402
    # Insufficient Balance rather than an auth error, and that failure is
    # caught and treated as "try the next backend" the same as any other.
    "deepseek": {
        "family": "openai",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
    },
}


def is_backend_configured(backend: str) -> bool:
    """True if the credential this backend needs is actually set. Used to
    skip an unconfigured backend in a fallback chain silently — no point
    burning a call (and a stderr line) on a backend the user never set a
    key for."""
    config = BACKENDS.get(backend)
    if config is None:
        return False
    return bool(os.environ.get(config["api_key_env"], "").strip())


def _backend_credentials(backend: str) -> tuple[str | None, str | None]:
    """Returns (api_key, base_url) for a backend, resolved from its own env
    vars — never the plain "openai" backend's OPENAI_API_KEY/OPENAI_BASE_URL,
    even for other family="openai" backends like groq/deepseek, so several
    OpenAI-compatible endpoints can be configured side by side without
    clobbering each other."""
    config = BACKENDS[backend]
    api_key = os.environ.get(config["api_key_env"], "").strip() or None
    base_url = config.get("base_url")
    if base_url is None and "base_url_env" in config:
        base_url = os.environ.get(config["base_url_env"], "").strip() or None
    return api_key, base_url


def call_llm_via_backend(
    backend: str,
    model: str,
    system_prompt: str,
    user_content: str,
    schema: dict,
    tool_name: str,
    tool_description: str,
) -> tuple[dict, dict]:
    """Same call shape as call_llm below, but backend-explicit instead of
    reading LLM_PROVIDER from the environment — this is what the
    cross-backend fallback chain (extractor._backend_chain) uses so it can
    try, say, google then groq then deepseek in one pass without any of
    them reading each other's credentials."""
    config = BACKENDS.get(backend)
    if config is None:
        raise ValueError(f"Unknown backend {backend!r} — expected one of {sorted(BACKENDS)}.")
    api_key, base_url = _backend_credentials(backend)
    family = config["family"]
    if family == "anthropic":
        return _call_anthropic(
            model, system_prompt, user_content, schema, tool_name, tool_description, api_key=api_key
        )
    if family == "openai":
        return _call_openai(
            model, system_prompt, user_content, schema, tool_name, tool_description,
            api_key=api_key, base_url=base_url,
        )
    if family == "google":
        return _call_google(
            model, system_prompt, user_content, schema, tool_name, tool_description, api_key=api_key
        )
    raise ValueError(f"Backend {backend!r} has unknown family {family!r}.")


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
    model: str,
    system_prompt: str,
    user_content: str,
    schema: dict,
    tool_name: str,
    tool_description: str,
    *,
    api_key: str | None = None,
) -> tuple[dict, dict]:
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic") from exc

    # api_key=None is equivalent to omitting it — the SDK itself falls back
    # to reading ANTHROPIC_API_KEY, so the legacy call_llm() path (which
    # never passes this kwarg) behaves exactly as before.
    client = anthropic.Anthropic(api_key=api_key)
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
    model: str,
    system_prompt: str,
    user_content: str,
    schema: dict,
    tool_name: str,
    tool_description: str,
    *,
    api_key: str | None = None,
    base_url: str | None = None,
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

    # base_url/api_key=None falls back to OPENAI_BASE_URL/OPENAI_API_KEY —
    # this is what lets this same adapter target any OpenAI-compatible
    # endpoint (Groq, DeepSeek, ...) without a separate implementation, and
    # keeps the legacy call_llm() path (which never passes these kwargs)
    # behaving exactly as before. call_llm_via_backend passes both
    # explicitly instead, sourced from that backend's own env vars, so
    # multiple OpenAI-compatible backends can be configured side by side.
    if base_url is None:
        base_url = os.environ.get("OPENAI_BASE_URL", "").strip() or None
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
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
    model: str,
    system_prompt: str,
    user_content: str,
    schema: dict,
    tool_name: str,
    tool_description: str,
    *,
    api_key: str | None = None,
) -> tuple[dict, dict]:
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "google-generativeai package not installed. Run: pip install google-generativeai"
        ) from exc

    if api_key is None:
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
