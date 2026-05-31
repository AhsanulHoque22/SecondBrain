#!/usr/bin/env python3
"""
Google Classroom Fetcher
Uses the Gmail MCP (already connected) via Claude Code to extract
Google Classroom materials and announcements into the SecondBrain vault.

Run from vault root:
  python3 scripts/classroom_fetch.py

What it does:
- Searches Gmail for Google Classroom notification emails
- Extracts material titles, links, deadlines
- Creates/updates _ClassroomNotes.md in each course folder
"""

import subprocess
import json
import re
import os
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).parent.parent
COURSES_DIR = VAULT / "02_Courses"

# Map Google Classroom course names → our local folders
COURSE_MAP = {
    "713": "CSE713_AI",
    "717": "CSE717_InfoSec",
    "711": "CSE711_Compiler",
    "719": "CSE719_Distributed",
    "715": "CSE715_Graphics",
    "700": "CSE700_Thesis",
    "artificial intelligence": "CSE713_AI",
    "information security": "CSE717_InfoSec",
    "compiler": "CSE711_Compiler",
    "distributed": "CSE719_Distributed",
    "graphics": "CSE715_Graphics",
    "thesis": "CSE700_Thesis",
}

def get_course_folder(subject_line: str) -> str | None:
    subject_lower = subject_line.lower()
    for keyword, folder in COURSE_MAP.items():
        if keyword.lower() in subject_lower:
            return folder
    return None

def parse_classroom_email(subject: str, body: str, date: str) -> dict:
    """Extract structured info from a Classroom email."""
    entry = {
        "date": date,
        "subject": subject,
        "type": "announcement",
        "body_preview": body[:500] if body else "",
    }
    if any(w in subject.lower() for w in ["assignment", "due", "submit"]):
        entry["type"] = "assignment"
    elif any(w in subject.lower() for w in ["material", "posted", "resource"]):
        entry["type"] = "material"
    elif any(w in subject.lower() for w in ["quiz", "test", "exam"]):
        entry["type"] = "quiz"
    return entry

def write_classroom_notes(folder_name: str, entries: list):
    course_dir = COURSES_DIR / folder_name
    course_dir.mkdir(exist_ok=True)
    output_file = course_dir / "_ClassroomNotes.md"

    lines = [
        f"# Google Classroom Notes — {folder_name}",
        f"\n> Last fetched: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "\n---\n",
    ]

    assignments = [e for e in entries if e["type"] == "assignment"]
    materials = [e for e in entries if e["type"] == "material"]
    announcements = [e for e in entries if e["type"] == "announcement"]

    if assignments:
        lines.append("## Assignments / Deadlines\n")
        for e in sorted(assignments, key=lambda x: x["date"], reverse=True):
            lines.append(f"- **{e['date']}** — {e['subject']}")
            if e["body_preview"]:
                lines.append(f"  > {e['body_preview'][:200]}")
        lines.append("")

    if materials:
        lines.append("## Posted Materials\n")
        for e in sorted(materials, key=lambda x: x["date"], reverse=True):
            lines.append(f"- **{e['date']}** — {e['subject']}")
        lines.append("")

    if announcements:
        lines.append("## Announcements\n")
        for e in sorted(announcements, key=lambda x: x["date"], reverse=True):
            lines.append(f"- **{e['date']}** — {e['subject']}")
            if e["body_preview"]:
                lines.append(f"  > {e['body_preview'][:200]}")
        lines.append("")

    output_file.write_text("\n".join(lines))
    return output_file

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Google Classroom Fetcher")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print("NOTE: This script uses Claude Code's Gmail MCP.")
    print("Run it from inside a Claude Code session for full automation,")
    print("or use it as a reference for what to search in Gmail manually.")
    print("")
    print("Gmail searches to run manually (copy-paste to Gmail search):")
    print("")
    searches = [
        ("CSE 713 AI", 'from:classroom.google.com "CSE 713" OR "Artificial Intelligence"'),
        ("CSE 717 InfoSec", 'from:classroom.google.com "CSE 717" OR "Information Security"'),
        ("CSE 711 Compiler", 'from:classroom.google.com "CSE 711" OR "Compiler"'),
        ("CSE 719 Distributed", 'from:classroom.google.com "CSE 719" OR "Distributed"'),
        ("CSE 715 Graphics", 'from:classroom.google.com "CSE 715" OR "Graphics"'),
    ]
    for name, query in searches:
        print(f"  {name}:")
        print(f"    {query}")
        print()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Claude Code will do this automatically when you say:")
    print('  "Fetch my Google Classroom materials and update the vault"')
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()
