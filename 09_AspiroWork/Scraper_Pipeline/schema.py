"""Canonical program schema — one output row per program, 19 columns
covering identity, cost, dates, and requirements, including
tuition_currency (split out of the raw tuition string by cleaner.py) and
last_verified_date (stamped at write time).

Repeatable sections (Intakes, Prerequisites, Must Requirements, Tags) are
flattened into one semicolon-separated cell per column rather than kept as
nested structures, so the output stays a flat, spreadsheet-friendly CSV.
"""

FIELDNAMES = [
    "program_image_url",
    "university_name",
    "level",
    "program_name",
    "destination",
    "location",
    "campus_city",
    "tuition_1st_year",
    "tuition_currency",
    "application_fee",
    "duration",
    "success_rate",
    "intake_terms",
    "deadlines",
    "prerequisites",
    "must_requirements",
    "tags",
    "source_url",
    "last_verified_date",
]

# A row missing any of these gets skipped rather than written half-empty.
REQUIRED_FIELDS = ["university_name", "level", "program_name"]

# Fields the extractor should populate before the cleaner normalizes them.
# prerequisites / must_requirements are lists of {"title": ..., "description": ...}
# tags are lists of {"name": ..., "category": ..., "details": ...}
# intake_terms / deadlines are parallel lists of strings.
EXTRACTED_KEYS = [
    "program_image_url",
    "university_name",
    "level",
    "program_name",
    "destination",
    "location",
    "campus_city",
    "tuition_1st_year",
    "application_fee",
    "duration",
    "success_rate",
    "intake_terms",
    "deadlines",
    "prerequisites",
    "must_requirements",
    "tags",
]
