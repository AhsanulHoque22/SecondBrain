"""Generates a day schedule from constraints.json.

v2 strategy (fixed): place fixed blocks first, then walk flexible tasks
HIGHEST PRIORITY FIRST, and for each one scan forward from the cursor to
find the next gap that is actually free for its full duration — skipping
over (and past) any fixed block that would otherwise be clipped. This is
the fix for v1's bug: a naive scheduler that placed tasks in file order
with no look-ahead, so several tasks landed on top of prayer times.

Usage: python3 schedule.py > schedule_v2.json
"""
import json

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def to_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def load_constraints():
    with open("constraints.json") as f:
        return json.load(f)


def next_free_slot(cursor, duration, fixed, day_end):
    """Return the earliest start >= cursor where [start, start+duration)
    doesn't overlap any fixed block, pushing past any block in the way."""
    while True:
        end = cursor + duration
        if end > day_end:
            raise ValueError("ran out of day — task doesn't fit")
        collision = next((fb for fb in fixed
                           if to_minutes(fb["start"]) < end and cursor < to_minutes(fb["end"])), None)
        if not collision:
            return cursor
        cursor = to_minutes(collision["end"])


def generate(constraints):
    fixed = sorted(constraints["fixed_blocks"], key=lambda b: to_minutes(b["start"]))
    day_start = to_minutes(constraints["day_window"]["start"])
    day_end = to_minutes(constraints["day_window"]["end"])

    blocks = [dict(b) for b in fixed]
    cursor = day_start

    ordered_tasks = sorted(
        constraints["flexible_tasks"],
        key=lambda t: PRIORITY_RANK.get(t["priority"], 9),
    )

    for task in ordered_tasks:
        start = next_free_slot(cursor, task["duration_min"], fixed, day_end)
        end = start + task["duration_min"]
        blocks.append({"name": task["name"], "start": to_hhmm(start), "end": to_hhmm(end)})
        cursor = end

    blocks.sort(key=lambda b: to_minutes(b["start"]))
    return {"date": constraints["date"], "blocks": blocks}


if __name__ == "__main__":
    print(json.dumps(generate(load_constraints()), indent=2))
