"""Stage 2 — Extract.

Turns raw HTML into a dict of the fields in schema.EXTRACTED_KEYS.

Two modes:
- LLM mode (used whenever the Claude API is reachable): sends cleaned page
  text to Claude with a strict tool schema, so extraction generalizes across
  arbitrary site layouts instead of hand-written per-site selectors. The
  model is instructed to use null for anything not present on the page —
  never invent a plausible-looking value.
- Heuristic fallback (used if the LLM call fails for any reason — no API
  credentials, network error, etc.): JSON-LD (schema.org Course /
  EducationalOccupationalProgram) plus label/regex matching for common
  patterns. Lower recall, but works with zero setup.
"""

from __future__ import annotations

import json
import re
import sys

import anthropic
from bs4 import BeautifulSoup

from schema import EXTRACTED_KEYS

MODEL = "claude-opus-4-8"

EXTRACTION_TOOL = {
    "name": "extract_program_fields",
    "description": (
        "Extract structured master's program data fields from the given webpage "
        "text for an education database. Use null for any field not present on "
        "the page (or an empty array for list fields) — never guess or infer a "
        "plausible-sounding value."
    ),
    "strict": True,
    "input_schema": {
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
    },
}

SYSTEM_PROMPT = (
    "You extract structured program data from webpage text for an "
    "education database that a study-abroad advisory assistant relies on. "
    "Only use information present in the provided text. If a field is not "
    "present, use null (or an empty array for list fields) — never guess or "
    "infer a plausible-sounding value. A missing field reported honestly is "
    "far better than an invented one."
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


def extract_via_llm(clean_text: str, url: str) -> dict:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[EXTRACTION_TOOL],
        tool_choice={"type": "tool", "name": "extract_program_fields"},
        messages=[
            {
                "role": "user",
                "content": f"Source URL: {url}\n\nPage text:\n{clean_text[:MAX_INPUT_CHARS]}",
            }
        ],
    )
    tool_use = next(block for block in response.content if block.type == "tool_use")
    return dict(tool_use.input)


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

    label_patterns = {
        "tuition_1st_year": r"Tuition[^:\n]*:\s*([^\n]+)",
        "application_fee": r"Application [Ff]ee[^:\n]*:\s*([^\n]+)",
        "duration": r"Duration[^:\n]*:\s*([^\n]+)",
        "success_rate": r"Success [Rr]ate[^:\n]*:\s*([^\n]+)",
    }
    for field, pattern in label_patterns.items():
        match = re.search(pattern, clean_text)
        if match:
            data[field] = match.group(1).strip()

    return data


def extract(html: str, url: str) -> dict:
    clean_text = clean_text_from_html(html)
    try:
        data = extract_via_llm(clean_text, url)
        data["_extraction_method"] = "llm"
        return data
    except Exception as exc:  # deliberate fallback boundary, not silent — logged below
        print(f"[extract] LLM extraction failed for {url} ({exc}); using heuristic fallback", file=sys.stderr)
        data = extract_via_heuristics(html, clean_text, url)
        data["_extraction_method"] = "heuristic"
        return data
