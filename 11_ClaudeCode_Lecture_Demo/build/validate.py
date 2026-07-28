"""Validates a generated schedule against constraints.json.

Checks:
  1. No two blocks overlap in time.
  2. Every fixed block from constraints.json is present, unchanged.
  3. Tasks with a 'must_be_before' deadline are scheduled before it.
  4. Tasks with an 'hard_cap_min' are not scheduled longer than that cap.

Usage: python3 validate.py schedule_v1.json
"""
import json
import sys


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def load(path):
    with open(path) as f:
        return json.load(f)


def check_overlaps(blocks):
    conflicts = []
    spans = [(b["name"], to_minutes(b["start"]), to_minutes(b["end"])) for b in blocks]
    spans.sort(key=lambda s: s[1])
    for i in range(len(spans) - 1):
        name_a, _, end_a = spans[i]
        name_b, start_b, _ = spans[i + 1]
        if start_b < end_a:
            conflicts.append(f"'{name_b}' ({spans[i+1][1]}) overlaps '{name_a}' (ends {end_a}) by {end_a - start_b} min")
    return conflicts


def check_fixed_present(schedule_blocks, fixed_blocks):
    missing = []
    by_name = {b["name"]: b for b in schedule_blocks}
    for fb in fixed_blocks:
        sb = by_name.get(fb["name"])
        if sb is None:
            missing.append(f"fixed block '{fb['name']}' is missing from the schedule")
        elif sb["start"] != fb["start"] or sb["end"] != fb["end"]:
            missing.append(f"fixed block '{fb['name']}' was moved (expected {fb['start']}-{fb['end']}, got {sb['start']}-{sb['end']})")
    return missing


def check_deadlines(schedule_blocks, flexible_tasks):
    violations = []
    by_name = {b["name"]: b for b in schedule_blocks}
    for t in flexible_tasks:
        deadline = t.get("must_be_before")
        if not deadline:
            continue
        sb = by_name.get(t["name"])
        if sb and to_minutes(sb["end"]) > to_minutes(deadline):
            violations.append(f"'{t['name']}' ends at {sb['end']}, after its {deadline} deadline")
    return violations


def check_hard_caps(schedule_blocks, flexible_tasks):
    violations = []
    by_name = {b["name"]: b for b in schedule_blocks}
    for t in flexible_tasks:
        cap = t.get("hard_cap_min")
        if not cap:
            continue
        sb = by_name.get(t["name"])
        if sb:
            duration = to_minutes(sb["end"]) - to_minutes(sb["start"])
            if duration > cap:
                violations.append(f"'{t['name']}' scheduled for {duration} min, exceeds hard cap of {cap} min")
    return violations


def main():
    schedule_path = sys.argv[1]
    constraints = load("constraints.json")
    schedule = load(schedule_path)

    blocks = schedule["blocks"]
    problems = []
    problems += check_overlaps(blocks)
    problems += check_fixed_present(blocks, constraints["fixed_blocks"])
    problems += check_deadlines(blocks, constraints["flexible_tasks"])
    problems += check_hard_caps(blocks, constraints["flexible_tasks"])

    print(f"Validating {schedule_path} against constraints.json ...\n")
    if problems:
        print(f"FAILED — {len(problems)} problem(s) found:\n")
        for p in problems:
            print(f"  x {p}")
        sys.exit(1)
    else:
        print("PASSED — all fixed blocks intact, no overlaps, no deadline or cap violations.")
        sys.exit(0)


if __name__ == "__main__":
    main()
