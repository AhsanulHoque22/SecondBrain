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

# Degree abbreviations that commonly open a program's <title>/og:title, e.g.
# "MSc in Statistical Science | Oxford University" — used by the heuristic
# fallback to backfill `level` when there's no JSON-LD to read it from.
DEGREE_LEVEL_PATTERN = re.compile(
    r"^(MSc|MPhil|MSt|MBA|MEng|MRes|LLM|PGCert|PGDip|PhD|DPhil|BSc|BEng|MA|BA)\b",
    re.IGNORECASE,
)

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
        level_match = DEGREE_LEVEL_PATTERN.match(data["program_name"])
        if level_match:
            data["level"] = level_match.group(1)

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
