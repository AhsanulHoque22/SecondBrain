#!/usr/bin/env python3
"""
Recall gaps tracker for SecondBrain active recall system.

Tracks topics that were missed during active recall questioning and
generates end-of-day revision reminders. Integrates with spaced_rep.py
to push weak topics into the recall schedule.

Usage:
  python3 recall_gaps.py add COURSE TOPIC "question_missed" [source_block]
  python3 recall_gaps.py list [--today-only]
  python3 recall_gaps.py mark-revised COURSE TOPIC
  python3 recall_gaps.py reminder    # print end-of-day reminder text
  python3 recall_gaps.py due-today   # machine-readable JSON for scripts
"""

import json
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

VAULT = Path(__file__).parent.parent
DATA_DIR = Path(__file__).parent / "data"
GAPS_FILE = DATA_DIR / "recall_gaps.json"


def load() -> dict:
    if GAPS_FILE.exists():
        return json.loads(GAPS_FILE.read_text())
    return {"gaps": [], "last_end_of_day_reminder": ""}


def save(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    GAPS_FILE.write_text(json.dumps(state, indent=2))


def add(course: str, topic: str, question_missed: str, source_block: str = "") -> dict:
    """Add a recall gap entry. Returns the created entry."""
    state = load()
    today = date.today().isoformat()

    entry = {
        "topic": topic,
        "course": course,
        "source_block": source_block,
        "date_identified": today,
        "question_missed": question_missed,
        "revised": False,
        "revision_date": None,
    }

    # Don't duplicate — if same topic+course exists and is unrevised, update it
    for gap in state["gaps"]:
        if (gap["topic"] == topic and gap["course"] == course
                and not gap["revised"]):
            gap["question_missed"] = question_missed
            gap["date_identified"] = today
            save(state)
            return gap

    state["gaps"].append(entry)
    save(state)
    return entry


def list_gaps(today_only: bool = False) -> list[dict]:
    """List all gaps, optionally filtered to today only."""
    state = load()
    if today_only:
        today = date.today().isoformat()
        return [g for g in state["gaps"]
                if g["date_identified"] == today and not g["revised"]]
    return state["gaps"]


def mark_revised(course: str, topic: str) -> Optional[dict]:
    """Mark a gap as revised. Returns the updated entry or None."""
    state = load()
    for gap in state["gaps"]:
        if (gap["topic"] == topic and gap["course"] == course
                and not gap["revised"]):
            gap["revised"] = True
            gap["revision_date"] = date.today().isoformat()
            save(state)
            return gap
    return None


def get_unrevised() -> list[dict]:
    """Return all unrevised gaps."""
    state = load()
    return [g for g in state["gaps"] if not g["revised"]]


def generate_reminder() -> str:
    """Generate end-of-day reminder text for unrevised gaps."""
    unrevised = get_unrevised()
    today = date.today().isoformat()

    if not unrevised:
        return ""

    # Group by course
    by_course: dict[str, list[dict]] = {}
    for gap in unrevised:
        by_course.setdefault(gap["course"], []).append(gap)

    lines = ["📝 *End-of-Day Recall Gaps — Revise These Tonight*\n"]
    for course, gaps in sorted(by_course.items()):
        course_short = course.replace("CSE713_", "AI — ").replace("CSE717_", "InfoSec — ").replace("CSE711_", "Compiler — ").replace("CSE719_", "Distributed — ").replace("CSE715_", "Graphics — ")
        lines.append(f"*{course_short}*")
        for gap in gaps:
            days_ago = (date.today() - datetime.strptime(gap["date_identified"], "%Y-%m-%d").date()).days
            ago_str = f" (from {days_ago}d ago)" if days_ago > 0 else " (today)"
            lines.append(f"  • {gap['topic']}{ago_str}")
            lines.append(f"    Missed: _{gap['question_missed']}_")
        lines.append("")

    lines.append("---")
    lines.append("Reply with: _'revised [topic name]'_ when done.")

    state = load()
    state["last_end_of_day_reminder"] = today
    save(state)

    return "\n".join(lines)


def due_today_json() -> str:
    """Print unrevised gaps as JSON for script consumption."""
    unrevised = get_unrevised()
    return json.dumps({"count": len(unrevised), "gaps": unrevised}, indent=2)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: recall_gaps.py <add|list|mark-revised|reminder|due-today> [args...]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "add":
        if len(sys.argv) < 5:
            print("Usage: recall_gaps.py add COURSE TOPIC QUESTION_MISSED [SOURCE_BLOCK]")
            sys.exit(1)
        course = sys.argv[2]
        topic = sys.argv[3]
        question = sys.argv[4]
        block = sys.argv[5] if len(sys.argv) > 5 else ""
        entry = add(course, topic, question, block)
        print(f"📝 Gap recorded: {topic} ({course})")

    elif action == "list":
        today_only = "--today-only" in sys.argv
        gaps = list_gaps(today_only=today_only)
        if not gaps:
            print("✅ No recall gaps tracked.")
        else:
            unrevised = [g for g in gaps if not g["revised"]]
            revised = [g for g in gaps if g["revised"]]
            if unrevised:
                print(f"🔴 {len(unrevised)} unrevised gap(s):")
                for g in unrevised:
                    print(f"  • {g['topic']} ({g['course']}) — {g['question_missed']}")
            if revised:
                print(f"✅ {len(revised)} revised gap(s).")

    elif action == "mark-revised":
        if len(sys.argv) < 4:
            print("Usage: recall_gaps.py mark-revised COURSE TOPIC")
            sys.exit(1)
        course = sys.argv[2]
        topic = sys.argv[3]
        result = mark_revised(course, topic)
        if result:
            print(f"✅ Marked revised: {topic} ({course})")
        else:
            print(f"⚠️  No unrevised gap found for: {topic} ({course})")

    elif action == "reminder":
        reminder = generate_reminder()
        if reminder:
            print(reminder)
        else:
            print("✅ All recall gaps revised. Nothing due.")

    elif action == "due-today":
        print(due_today_json())

    else:
        print(f"Unknown action: {action}")
        print("Usage: recall_gaps.py <add|list|mark-revised|reminder|due-today> [args...]")
        sys.exit(1)


if __name__ == "__main__":
    main()
