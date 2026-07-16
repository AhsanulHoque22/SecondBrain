"""Stage 2 — Extract.

Turns raw HTML into a dict of the fields in schema.EXTRACTED_KEYS.

Multi-tier cascade, cheapest/fastest model first, escalating only when
needed:
- Tier 1: sends cleaned page text to an LLM (see llm_providers.py for the
  supported vendors) with a strict structured-output schema, so extraction
  generalizes across arbitrary site layouts instead of hand-written
  per-site selectors. The model is instructed to use null for anything not
  present on the page — never invent a plausible-looking value. A
  deterministic (non-LLM) validator checks the output; most well-structured
  pages pass here and stop.
- Later tiers: only run if the validator rejected the previous tier's
  output. Each retry gets the validator's specific complaints appended to
  the prompt, so escalation is a correction, not a blind re-roll. The
  models used at each tier, and how many tiers exist, are configured via
  EXTRACTION_MODEL_CASCADE — see README.md.
- Cross-backend fallback (LLM_BACKEND_CHAIN, optional): the tier list above
  is normally all within one provider (e.g. three Anthropic models). Set
  LLM_BACKEND_CHAIN to a comma-separated list of backend names (e.g.
  "groq,google,deepseek,anthropic") to chain several *independently
  configured* backends — each contributes its own model cascade, and the
  whole sequence is tried in order before falling through to the heuristic
  tier. This is what makes a single unreachable backend (bad key, zero
  quota, no billing) a non-blocking event instead of an aborted run — see
  _backend_chain below. Unset means the original single-backend behavior:
  just LLM_PROVIDER's own cascade.
- Heuristic fallback (used if every LLM tier across every configured
  backend fails outright — no API credentials, network error, exhausted
  quota — or every tier's output fails validation): JSON-LD (schema.org
  Course/EducationalOccupationalProgram), og:title/og:site_name, and
  label/regex matching for common patterns. Lower recall, but works with
  zero setup and never blocks the batch.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

from bs4 import BeautifulSoup

import llm_providers
from schema import EXTRACTED_KEYS, REQUIRED_FIELDS

DEFAULT_EXTRACTION_STATE_PATH = Path("state/extraction_state.json")

# Only the Anthropic path ships with a default cascade — it's the one
# provider this pipeline has been exercised against live, so a default here
# is a real, tested claim rather than a guess. Any other backend requires
# EXTRACTION_MODEL_CASCADE (single-backend mode) or {BACKEND}_MODEL_CASCADE
# (multi-backend chain) to be set explicitly — see _cascade_for_backend
# below — rather than this module guessing a current model ID for a vendor
# it can't verify against.
DEFAULT_ANTHROPIC_CASCADE = ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-4-8"]

# Human-readable tags for the well-known Anthropic cascade tiers, used to
# label which tier produced a given row. A model not in this dict (any
# custom cascade, any non-Anthropic backend) falls back to a generic
# "llm:<backend>:<model>" tag instead of raising — see _extraction_tag below.
MODEL_TAGS = {
    "claude-haiku-4-5": "llm-haiku",
    "claude-sonnet-5": "llm-sonnet",
    "claude-opus-4-8": "llm-opus",
}

# Standard list price, $ per million tokens (input, output) — Anthropic
# models only, since these are the only prices this project can vouch for.
# A model not listed here (custom cascade, non-Anthropic provider) prices
# at $0.00 in the cost report rather than guessing a number — see
# pipeline.py's _print_cost_report, which already handles a missing key via
# MODEL_PRICING.get(model, (0.0, 0.0)). Deliberately NOT using Sonnet 5's
# temporary introductory discount ($2/$10 through 2026-08-31) here — a cost
# *estimate* that quietly becomes wrong the day the discount ends is worse
# than one that's always a few cents pessimistic.
MODEL_PRICING = {
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-opus-4-8": (5.00, 25.00),
}


# Built-in default cascades for backends whose current model IDs this
# pipeline has actually exercised live — auth and request shape both
# confirmed working end-to-end, even where an account-level limit (zero
# quota, no billing) blocked seeing real output. Every other backend must
# set {BACKEND}_MODEL_CASCADE (e.g. OPENAI_MODEL_CASCADE) explicitly rather
# than have this module guess a current model ID for a vendor it can't
# verify against — same policy as the original single-provider cascade.
DEFAULT_BACKEND_CASCADES: dict[str, list[str]] = {
    "anthropic": DEFAULT_ANTHROPIC_CASCADE,
    # Live-tested against a real (new) Google Cloud key: gemini-2.0-flash
    # and gemini-2.5-pro both returned a real 429 RESOURCE_EXHAUSTED (valid
    # model ID, blocked only by account-level zero quota). gemini-2.5-flash
    # returned 404 "no longer available to new users" on that same key —
    # apparently restricted for newly created accounts specifically, not a
    # dead model ID — left in the cascade since an older/differently
    # provisioned account may still have access to it.
    "google": ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"],
    # All six live-tested against a real Groq free-tier key with a strict
    # tool-calling schema (the same shape EXTRACTION_SCHEMA uses) — every
    # one returned valid structured output. Ordered smallest/fastest first,
    # escalating in roughly increasing parameter count/capability. Pulled
    # from GET /openai/v1/models on that key; the account also listed
    # Whisper (audio-only), Orpheus (text-to-speech), Llama Prompt Guard
    # (a safety classifier, not a generation model), and groq/compound(-mini)
    # (an agentic meta-model with its own built-in tools that could conflict
    # with this pipeline's own tool-calling schema) — all excluded as
    # unsuited to structured-field extraction, not because they failed.
    "groq": [
        "llama-3.1-8b-instant",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "openai/gpt-oss-20b",
        "qwen/qwen3-32b",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b",
    ],
    # deepseek-chat is the only tier: deepseek-reasoner (R1) doesn't support
    # function/tool calling, so it can't serve this pipeline's structured-
    # output extraction at all, cheap or not.
    "deepseek": ["deepseek-chat"],
}


def _cascade_for_backend(backend: str) -> list[str]:
    """Returns the ordered list of models to try for one backend.
    {BACKEND}_MODEL_CASCADE (e.g. GROQ_MODEL_CASCADE) always wins when set.
    Otherwise, for whichever backend is the primary LLM_PROVIDER, falls
    back to the legacy EXTRACTION_MODEL_CASCADE var so existing
    single-backend .env files keep working unchanged. With neither set,
    falls back to this module's own built-in default for a backend this
    pipeline has verified live (DEFAULT_BACKEND_CASCADES); any other
    backend raises, same as the original single-provider behavior."""
    override = os.environ.get(f"{backend.upper()}_MODEL_CASCADE", "").strip()
    if override:
        return [m.strip() for m in override.split(",") if m.strip()]
    if backend == llm_providers.get_provider():
        legacy = os.environ.get("EXTRACTION_MODEL_CASCADE", "").strip()
        if legacy:
            return [m.strip() for m in legacy.split(",") if m.strip()]
    if backend in DEFAULT_BACKEND_CASCADES:
        return DEFAULT_BACKEND_CASCADES[backend]
    raise RuntimeError(
        f"Backend {backend!r} has no model cascade configured. Set "
        f"{backend.upper()}_MODEL_CASCADE to a comma-separated list of model IDs for "
        "this backend (check its own docs for current model names)."
    )


def _backend_chain() -> list[tuple[str, str]]:
    """Returns the ordered list of (backend, model) attempts across every
    configured backend — the cross-backend fallback chain.

    Set LLM_BACKEND_CHAIN (comma-separated backend names, e.g.
    "groq,google,deepseek,anthropic") to try several independent backends
    in order — each contributes its own model cascade via
    _cascade_for_backend — before extract() gives up and drops to the
    heuristic extractor. This is the "try a few others before aborting"
    behavior: a backend that's entirely unreachable (bad key, zero quota,
    no billing) no longer aborts the run, it just contributes zero usable
    attempts and the chain moves on.

    Unset means the original single-backend behavior: just LLM_PROVIDER's
    own cascade (what _model_cascade used to return on its own).

    A backend with no credential configured is skipped, not attempted —
    no point burning a call (and a stderr line) on a backend nobody set a
    key for. A backend that's misconfigured in a way that *would* block it
    outright even in legacy single-backend mode (no cascade available at
    all — see _cascade_for_backend) still raises, since that's a genuine
    setup mistake worth surfacing loudly rather than silently dropping.
    """
    override = os.environ.get("LLM_BACKEND_CHAIN", "").strip()
    backends = [b.strip() for b in override.split(",") if b.strip()] if override else [llm_providers.get_provider()]

    chain: list[tuple[str, str]] = []
    for backend in backends:
        if backend not in llm_providers.BACKENDS:
            print(f"[extract] skipping unknown backend {backend!r} in LLM_BACKEND_CHAIN", file=sys.stderr)
            continue
        if not llm_providers.is_backend_configured(backend):
            print(f"[extract] skipping backend {backend!r} — no credential configured", file=sys.stderr)
            continue
        chain.extend((backend, model) for model in _cascade_for_backend(backend))
    return chain


def _extraction_tag(backend: str, model: str) -> str:
    return MODEL_TAGS.get(model, f"llm:{backend}:{model}")

# Values a model might return that are semantically "nothing" but aren't the
# null the schema asks for — treated the same as a missing required field.
PLACEHOLDER_VALUES = {"n/a", "na", "none", "unknown", "not specified", "not available", "-", "tbd"}
NUMERIC_FIELDS = ("tuition_1st_year", "application_fee", "duration", "success_rate")

# Degree abbreviations that commonly open a program's <title>/og:title, e.g.
# "MSc in Statistical Science | Oxford University" — used by the heuristic
# fallback to backfill `level` when there's no JSON-LD to read it from.
# Anchored to the start only: these are short enough (MA, BA...) that
# matching them anywhere in the text risks false positives (e.g. "MA" as
# the US-state abbreviation), so this tier stays conservative.
DEGREE_LEVEL_PATTERN = re.compile(
    r"^(MSc|MPhil|MSt|MBA|MEng|MRes|LLM|PGCert|PGDip|PhD|DPhil|BSc|BEng|MA|BA)\b",
    re.IGNORECASE,
)

# Unabbreviated degree words, searched anywhere in the program name (not
# just the start) — sites like mastersportal.com put the university name
# first, e.g. "Joint Master in Applied XR ... at University of X", so the
# degree word isn't the first token. These words are unambiguous enough as
# whole words that a search anywhere in the title is safe.
DEGREE_WORD_PATTERN = re.compile(
    r"\b(Master's|Masters|Master|Bachelor's|Bachelors|Bachelor|Doctorate|Doctoral)\b",
    re.IGNORECASE,
)

# Dotted abbreviations ("LL.M.", "M.Sc."), searched anywhere — e.g.
# mastersportal.com's "Legal Research LL.M. at Utrecht University". The
# internal period is mandatory in the pattern (only the trailing one is
# optional), which is what keeps this safe to search anywhere: unlike bare
# "MA"/"BA" (DEGREE_LEVEL_PATTERN, anchored-only for that reason), a literal
# ".", e.g. in "LL.M", isn't going to show up by coincidence.
DEGREE_DOTTED_PATTERN = re.compile(
    r"\b(LL\.M|M\.Sc|M\.A|M\.Phil|M\.St|M\.B\.A|M\.Eng|M\.Res|Ph\.D|D\.Phil|B\.Sc|B\.A|B\.Eng)\.?",
    re.IGNORECASE,
)

EXTRACTION_TOOL_NAME = "extract_program_fields"
EXTRACTION_TOOL_DESCRIPTION = (
    "Extract structured master's program data fields from the given webpage "
    "text for an education database. Use null for any field not present on "
    "the page (or an empty array for list fields) — never guess or infer a "
    "plausible-sounding value."
)

# Provider-agnostic JSON Schema for the extraction output. Every provider
# adapter in llm_providers.py wraps this the same way regardless of vendor
# (Anthropic tool-use input_schema, OpenAI function-calling parameters,
# Google's translated response_schema) — this is the one schema definition
# all three read from.
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "program_image_url": {"type": ["string", "null"]},
        "university_name": {"type": ["string", "null"]},
        "level": {"type": ["string", "null"]},
        "program_name": {"type": ["string", "null"]},
        "destination": {"type": ["string", "null"]},
        "location": {"type": ["string", "null"]},
        "campus_city": {"type": ["string", "null"]},
        "tuition_1st_year": {"type": ["string", "null"]},
        "application_fee": {"type": ["string", "null"]},
        "duration": {"type": ["string", "null"]},
        "success_rate": {"type": ["string", "null"]},
        "intake_terms": {"type": "array", "items": {"type": "string"}},
        "deadlines": {"type": "array", "items": {"type": "string"}},
        "prerequisites": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": ["string", "null"]},
                },
                "required": ["title", "description"],
                "additionalProperties": False,
            },
        },
        "must_requirements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": ["string", "null"]},
                },
                "required": ["title", "description"],
                "additionalProperties": False,
            },
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "category": {"type": ["string", "null"]},
                    "details": {"type": ["string", "null"]},
                },
                "required": ["name", "category", "details"],
                "additionalProperties": False,
            },
        },
    },
    "required": EXTRACTED_KEYS,
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You extract structured program data from webpage text for an "
    "education database that a study-abroad advisory assistant relies on. "
    "Only use information present in the provided text. If a field is not "
    "present, use null (or an empty array for list fields) — never guess or "
    "infer a plausible-sounding value. A missing field reported honestly is "
    "far better than an invented one. If a page lists separate tuition "
    "rates for different applicant groups (e.g. EU vs non-EU, domestic vs "
    "international), tuition_1st_year must be a single figure — the "
    "non-EU/international rate, since that's the one a foreign applicant "
    "actually pays — never multiple amounts joined together."
)

MAX_INPUT_CHARS = 15000


def clean_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def content_hash(clean_text: str) -> str:
    return "sha256:" + hashlib.sha256(clean_text.encode("utf-8")).hexdigest()


def _load_extraction_state(state_path: Path) -> dict[str, dict]:
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text(encoding="utf-8"))


def _save_extraction_state(state_path: Path, state: dict[str, dict]) -> None:
    """Atomic write (temp file + os.replace) — same pattern as
    cleaner.append_to_csv and discover.py's discovery manifest."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=state_path.parent, prefix=f".{state_path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, sort_keys=True)
        os.replace(tmp_path, state_path)
    except BaseException:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def has_content_changed(url: str, clean_text: str, state_path: Path = DEFAULT_EXTRACTION_STATE_PATH) -> bool:
    """True if this URL has no prior extraction record (never checked
    before — treated as needing extraction, not as an error) or its content
    hash differs from what was last recorded.

    Hashes clean_text_from_html's output, not the raw HTML: raw HTML is too
    noisy for a pre-extraction cheap check (ads, trackers, per-request
    markup variance would trigger false "changed" signals on pages where
    nothing about the actual program data moved). clean_text is much closer
    to what a human would call "the page content," and it's nearly free to
    compute — no LLM call, no extra fetch beyond the one already needed to
    check.
    """
    state = _load_extraction_state(state_path)
    prior = state.get(url)
    if prior is None:
        return True
    return prior.get("content_hash") != content_hash(clean_text)


def record_extraction_state(
    url: str, clean_text: str, extraction_method: str, state_path: Path = DEFAULT_EXTRACTION_STATE_PATH
) -> None:
    """Called after every successful extraction (new URL or refreshed one)
    so a future has_content_changed() call has a baseline to compare
    against."""
    state = _load_extraction_state(state_path)
    state[url] = {
        "last_extracted_at": _now_iso(),
        "content_hash": content_hash(clean_text),
        "extraction_method": extraction_method,
    }
    _save_extraction_state(state_path, state)


def extract_via_llm(
    clean_text: str, url: str, backend: str, model: str, feedback: list[str] | None = None
) -> tuple[dict, dict]:
    """Returns (extracted_fields, usage) — usage is {"input_tokens": int,
    "output_tokens": int} straight off the API response, so callers can
    track real spend instead of estimating from characters sent.

    Thin wrapper over llm_providers.call_llm_via_backend — kept as its own
    function (rather than inlined into extract()) so the name and signature
    stay stable for callers and tests that mock this one call site
    regardless of which backend is configured underneath."""
    user_content = f"Source URL: {url}\n\nPage text:\n{clean_text[:MAX_INPUT_CHARS]}"
    if feedback:
        # Escalation retry — tell the stronger model exactly what the previous
        # tier got wrong instead of just re-rolling with more capability.
        user_content = (
            "A previous extraction attempt had these problems — fix them:\n"
            + "\n".join(f"- {problem}" for problem in feedback)
            + f"\n\n{user_content}"
        )
    return llm_providers.call_llm_via_backend(
        backend, model, SYSTEM_PROMPT, user_content, EXTRACTION_SCHEMA, EXTRACTION_TOOL_NAME, EXTRACTION_TOOL_DESCRIPTION
    )


def _digits_only(text: str) -> str:
    return re.sub(r"\D", "", text)


def _looks_like_bundled_tuition(value: str) -> bool:
    """True if tuition_1st_year looks like it bundles multiple tiers (e.g.
    "EU: 2695 EUR/yr; Non-EU: 18873 EUR/yr") instead of one first-year
    figure — this is the exact "tuition front-loading" bug the manual
    scrape had to catch and fix by hand (see AspiroBrain Data Pipeline
    Plan). A bundled value still has digits and every amount is grounded in
    the page, so the checks below in validate_extraction don't catch it —
    this one specifically looks at shape (multiple amounts / tier labels),
    not correctness of any single number."""
    if ";" in value:
        return True
    has_eu = re.search(r"\beu\b", value, re.IGNORECASE)
    has_non_eu = re.search(r"\bnon-?eu\b", value, re.IGNORECASE)
    if has_eu and has_non_eu:
        return True
    amounts = re.findall(r"\d[\d,.]{2,}", value)
    return len(amounts) > 1


def validate_extraction(data: dict, clean_text: str) -> list[str]:
    """Deterministic (no LLM call) sanity check on an LLM extraction.

    Empty return means the extraction is trustworthy enough to keep. A
    non-empty return triggers escalation to the next model tier, with these
    problems fed back into the retry prompt so the stronger model corrects
    them instead of guessing again from scratch.
    """
    problems = []
    for field in REQUIRED_FIELDS:
        value = (data.get(field) or "").strip()
        if not value or value.lower() in PLACEHOLDER_VALUES:
            problems.append(f"{field} is required but missing or placeholder-like ({value!r})")

    clean_text_digits = _digits_only(clean_text)
    for field in NUMERIC_FIELDS:
        value = data.get(field)
        if not value:
            continue
        if not re.search(r"\d", value):
            problems.append(f"{field} = {value!r} has no digit — doesn't look like a real value")
            continue
        # Grounding check: the model was told to use only what's on the
        # page, but strict-schema tool use only guarantees the *shape* is
        # right, not that the value is real. Comparing digit-only substrings
        # sidesteps formatting noise (currency symbols, "£15,000" vs
        # "15000") while still catching a number that's simply not anywhere
        # on the page. Skipped for very short digit runs (<3) — a 1-2 digit
        # coincidental match (e.g. a duration of "2" years) is too likely to
        # false-positive to be worth flagging.
        value_digits = _digits_only(value)
        if len(value_digits) >= 3 and value_digits not in clean_text_digits:
            problems.append(
                f"{field} = {value!r} doesn't appear anywhere in the source text "
                "(not grounded in the page — possible hallucination)"
            )

    tuition = (data.get("tuition_1st_year") or "").strip()
    if tuition and _looks_like_bundled_tuition(tuition):
        problems.append(
            f"tuition_1st_year = {tuition!r} looks like it bundles multiple tuition "
            "tiers (e.g. EU/Non-EU, or several amounts) instead of a single first-year "
            "figure — return only the non-EU/international rate as one amount"
        )
    return problems


def backfill_level(program_name: str) -> str | None:
    """Try the three level-detection tiers in order (anchored bare
    abbreviation, dotted abbreviation anywhere, plain word anywhere).
    Returns None if none matched — a genuinely absent degree word (e.g. a
    program name with no level info at all) is expected, not an error."""
    level_match = DEGREE_LEVEL_PATTERN.match(program_name)
    if not level_match:
        level_match = DEGREE_DOTTED_PATTERN.search(program_name)
    if not level_match:
        level_match = DEGREE_WORD_PATTERN.search(program_name)
    return level_match.group(1) if level_match else None


def extract_via_heuristics(html: str, clean_text: str, url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    data: dict = {key: None for key in EXTRACTED_KEYS}
    data["intake_terms"] = []
    data["deadlines"] = []
    data["prerequisites"] = []
    data["must_requirements"] = []
    data["tags"] = []

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            payload = json.loads(script.string or "{}")
        except (json.JSONDecodeError, TypeError):
            continue
        entries = payload if isinstance(payload, list) else [payload]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("@type") in ("Course", "EducationalOccupationalProgram"):
                data["program_name"] = data["program_name"] or entry.get("name")
                provider = entry.get("provider") or entry.get("publisher") or {}
                if isinstance(provider, dict):
                    data["university_name"] = data["university_name"] or provider.get("name")

    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        data["program_image_url"] = og_image["content"]

    # JSON-LD Course/EducationalOccupationalProgram markup is rare in practice
    # (confirmed absent on ox.ac.uk course pages during pipeline testing) —
    # og:title/<title> and og:site_name are far more common and usually carry
    # the same information, so fall back to those before giving up.
    if not data["program_name"]:
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            data["program_name"] = og_title["content"].strip()
        elif soup.title and soup.title.string:
            data["program_name"] = soup.title.string.split("|")[0].strip()

    if not data["university_name"]:
        og_site = soup.find("meta", property="og:site_name")
        if og_site and og_site.get("content"):
            data["university_name"] = og_site["content"].strip()

    if not data["level"] and data["program_name"]:
        backfilled = backfill_level(data["program_name"])
        if backfilled:
            data["level"] = backfilled

    # Gap between label and colon is capped at 30 chars (was unbounded) so a
    # later, unrelated colon far down the page — e.g. "Application fee
    # waivers are available ... eligibility criteria:" on ox.ac.uk — can't
    # get matched as if it were the label's own colon.
    label_patterns = {
        "tuition_1st_year": r"Tuition.{0,30}?:\s*([^\n]+)",
        "application_fee": r"Application [Ff]ee.{0,30}?:\s*([^\n]+)",
        "duration": r"Duration.{0,30}?:\s*([^\n]+)",
        "success_rate": r"Success [Rr]ate.{0,30}?:\s*([^\n]+)",
    }
    for field, pattern in label_patterns.items():
        match = re.search(pattern, clean_text)
        if match:
            value = match.group(1).strip()
            # These fields are always numeric/currency — a captured value with
            # no digit is prose that happened to follow the label, not a real
            # value (this is what let "applicants from low-income countries;"
            # through as an application_fee on ox.ac.uk).
            if re.search(r"\d", value):
                data[field] = value

    # The LLM path gets this check via validate_extraction (which rejects
    # and escalates to a stronger tier on a bundled value); heuristic has no
    # further tier to escalate to, so the only safe move is to null the
    # field out rather than keep a merged EU/non-EU-style figure masquerading
    # as a single first-year amount — same "missing beats wrong" philosophy
    # validate_extraction already applies to the LLM tiers.
    if data["tuition_1st_year"] and _looks_like_bundled_tuition(data["tuition_1st_year"]):
        print(
            f"[extract] heuristic tuition_1st_year for {url} looked bundled "
            f"({data['tuition_1st_year']!r}) — dropping rather than keeping a merged figure",
            file=sys.stderr,
        )
        data["tuition_1st_year"] = None

    return data


def extract(html: str, url: str) -> dict:
    """Returns the extracted-fields dict, plus two internal bookkeeping
    keys: `_extraction_method` (which tier served the row) and `_usage`
    (token usage + model, or None for the heuristic path — there's no API
    call to bill)."""
    clean_text = clean_text_from_html(html)

    feedback: list[str] | None = None
    for backend, model in _backend_chain():
        try:
            data, usage = extract_via_llm(clean_text, url, backend, model, feedback=feedback)
        except Exception as exc:  # this backend/tier's call failed outright — try the next one
            print(f"[extract] {backend}:{model} call failed for {url} ({exc})", file=sys.stderr)
            feedback = None
            continue

        problems = validate_extraction(data, clean_text)
        if not problems:
            data["_extraction_method"] = _extraction_tag(backend, model)
            data["_usage"] = {"model": model, "backend": backend, **usage}
            return data
        print(f"[extract] {backend}:{model} output for {url} failed validation: {'; '.join(problems)}", file=sys.stderr)
        feedback = problems

    # deliberate fallback boundary, not silent — logged above per backend/tier
    print(f"[extract] all LLM backends/tiers failed for {url}; using heuristic fallback", file=sys.stderr)
    data = extract_via_heuristics(html, clean_text, url)
    data["_extraction_method"] = "heuristic"
    data["_usage"] = None
    return data
