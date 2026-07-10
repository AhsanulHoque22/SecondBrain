"""Canonical program schema — matches Appendix A (Program Entry Schema) plus
tuition_currency and last_verified_date, added because they were flagged as
the two cheapest, highest-leverage gaps in the CSVs already in
`09_AspiroWork/Data Collection/`.

Repeatable sections in Appendix A (Intakes, Prerequisites, Must Requirements,
Tags) are flattened into one semicolon-separated cell per column, matching
the convention already used in the existing scraped CSVs.
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

# Starred (*) fields in Appendix A.
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
