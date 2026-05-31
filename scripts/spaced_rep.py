#!/usr/bin/env python3
"""
Spaced repetition scheduler for SecondBrain.
- Reads _Topics.md files for all courses
- Tracks recall history in spaced_rep.json
- Computes due topics and writes recall_due.md
- Called by overnight_rollover.sh

Usage:
  python3 spaced_rep.py              # compute and write recall_due.md
  python3 spaced_rep.py done COURSE TOPIC [confidence]
  python3 spaced_rep.py recalled COURSE TOPIC [confidence]
"""

import json
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

VAULT       = Path(__file__).parent.parent
DATA_DIR    = Path(__file__).parent / "data"
STATE_FILE  = DATA_DIR / "spaced_rep.json"
DUE_FILE    = DATA_DIR / "recall_due.md"

# Days between review passes (Ebbinghaus simplified)
INTERVALS = [2, 4, 7, 14, 21]

def get_interval(recall_count: int) -> int:
    return INTERVALS[min(recall_count, len(INTERVALS) - 1)]

def load() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save(state: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))

def record(course: str, topic: str, confidence: int | None, today: datetime.date):
    """Mark a topic as done or recalled. Auto-computes next recall date."""
    state = load()
    state.setdefault(course, {})
    entry = state[course].get(topic)

    if entry is None:
        entry = {
            "first_done":    today.isoformat(),
            "recall_count":  0,
            "last_reviewed": today.isoformat(),
            "next_recall":   (today + timedelta(days=get_interval(0))).isoformat(),
            "confidence":    confidence or 3,
        }
    else:
        entry["recall_count"]  += 1
        entry["last_reviewed"]  = today.isoformat()
        entry["next_recall"]    = (today + timedelta(days=get_interval(entry["recall_count"]))).isoformat()
        if confidence is not None:
            entry["confidence"] = confidence

    state[course][topic] = entry
    save(state)
    return entry["next_recall"]

def sync_from_topics_md(today: datetime.date):
    """
    Read all _Topics.md files. If a topic is ✅ with a Last Reviewed date
    that isn't yet tracked, add it to state automatically.
    """
    state = load()
    changed = False

    for tf in VAULT.glob("02_Courses/**/_Topics.md"):
        course = tf.parent.name
        for line in tf.read_text().splitlines():
            if not line.startswith("|") or line.startswith("| Topic") or line.startswith("|---"):
                continue
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) < 5:
                continue
            topic_name   = re.sub(r'\*+', '', cols[0]).strip()
            status       = cols[1]
            confidence   = cols[2]
            last_reviewed = cols[3]
            # cols[4] = next_recall (we manage this ourselves)

            if "✅" not in status:
                continue
            if not last_reviewed or last_reviewed in ("-", "—", ""):
                continue

            try:
                rev_date = datetime.strptime(last_reviewed, "%Y-%m-%d").date()
            except ValueError:
                continue

            state.setdefault(course, {})
            if topic_name not in state[course]:
                conf_val = int(confidence) if confidence.isdigit() else 3
                state[course][topic_name] = {
                    "first_done":    rev_date.isoformat(),
                    "recall_count":  0,
                    "last_reviewed": rev_date.isoformat(),
                    "next_recall":   (rev_date + timedelta(days=get_interval(0))).isoformat(),
                    "confidence":    conf_val,
                }
                changed = True
            else:
                # Update confidence if changed in markdown
                if confidence.isdigit():
                    new_conf = int(confidence)
                    if state[course][topic_name].get("confidence") != new_conf:
                        state[course][topic_name]["confidence"] = new_conf
                        changed = True

    if changed:
        save(state)

def due_topics(target_date: datetime.date) -> list[dict]:
    """Return topics whose next_recall is on or before target_date."""
    state = load()
    due = []
    for course, topics in state.items():
        for name, data in topics.items():
            if "next_recall" not in data:
                continue
            nr = datetime.strptime(data["next_recall"], "%Y-%m-%d").date()
            if nr <= target_date:
                due.append({
                    "course":       course,
                    "topic":        name,
                    "next_recall":  nr,
                    "overdue":      (target_date - nr).days,
                    "recall_count": data.get("recall_count", 0),
                    "confidence":   data.get("confidence", "-"),
                })
    due.sort(key=lambda x: (-x["overdue"], x["confidence"] if isinstance(x["confidence"], int) else 5))
    return due

def write_due_file(today: datetime.date):
    today_due     = due_topics(today)
    tomorrow_due  = due_topics(today + timedelta(days=1))

    lines = [f"# Recall Schedule — {today.isoformat()}\n\n"]

    if today_due:
        lines.append(f"## Due Today ({len(today_due)} topics)\n")
        for t in today_due:
            flag = f" ⚠️ {t['overdue']}d overdue" if t["overdue"] > 0 else ""
            conf = f" | conf {t['confidence']}/5" if isinstance(t["confidence"], int) else ""
            lines.append(f"- 🔁 **{t['topic']}** `{t['course']}`{flag}{conf}\n")
    else:
        lines.append("## Due Today\nNone — all caught up ✅\n")

    lines.append("\n")

    if tomorrow_due:
        lines.append(f"## Due Tomorrow ({len(tomorrow_due)} topics)\n")
        for t in tomorrow_due:
            conf = f" | conf {t['confidence']}/5" if isinstance(t["confidence"], int) else ""
            lines.append(f"- 🔁 {t['topic']} `{t['course']}`{conf}\n")

    DUE_FILE.write_text("".join(lines))
    return today_due, tomorrow_due

def main():
    today = datetime.now().date()

    if len(sys.argv) >= 4:
        action  = sys.argv[1]   # "done" or "recalled"
        course  = sys.argv[2]
        topic   = sys.argv[3]
        conf    = int(sys.argv[4]) if len(sys.argv) > 4 else None

        if action in ("done", "recalled"):
            next_recall = record(course, topic, conf, today)
            print(f"✅ Recorded: {topic} ({course}) — next recall: {next_recall}")
            return

    # Default: sync from markdown, compute due, write file
    sync_from_topics_md(today)
    today_due, tomorrow_due = write_due_file(today)

    if today_due:
        print(f"🔁 {len(today_due)} topic(s) due for recall today:")
        for t in today_due:
            print(f"   • {t['topic']} ({t['course']})")
    else:
        print("✅ No recall topics due today.")

    if tomorrow_due:
        print(f"\n📅 {len(tomorrow_due)} topic(s) due tomorrow:")
        for t in tomorrow_due:
            print(f"   • {t['topic']} ({t['course']})")

if __name__ == "__main__":
    main()
