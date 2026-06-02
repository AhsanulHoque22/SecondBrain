#!/usr/bin/env python3
"""
Weekly pattern analysis — runs every Sunday inside overnight_rollover.sh.
Reads completion_history.json, computes stats, sends Telegram report.
No Claude call needed — pure arithmetic.
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "data", "completion_history.json")
TG_SEND = os.path.join(SCRIPT_DIR, "tg_send.sh")

def load_history():
    with open(HISTORY_FILE) as f:
        return json.load(f).get("entries", [])

def last_n_days(entries, n=7):
    cutoff = (datetime.now() - timedelta(days=n)).date()
    results = []
    for e in entries:
        try:
            d = datetime.fromisoformat(e["timestamp"]).date()
            if d >= cutoff:
                results.append(e)
        except Exception:
            pass
    return results

def hour_bucket(ts):
    """Return AM/PM block label from ISO timestamp."""
    try:
        h = datetime.fromisoformat(ts).hour
        if h < 8:
            return "Early morning (before 8 AM)"
        elif h < 12:
            return "Morning (8–12)"
        elif h < 15:
            return "Early afternoon (12–3 PM)"
        elif h < 18:
            return "Late afternoon (3–6 PM)"
        else:
            return "Evening (6 PM+)"
    except Exception:
        return "Unknown"

def detect_streak(entries):
    """Find any block type missed 3+ days in a row (study only)."""
    by_date = defaultdict(list)
    for e in entries:
        if e.get("type") != "study":
            continue
        d = datetime.fromisoformat(e["timestamp"]).date()
        by_date[d].append(e)

    sorted_dates = sorted(by_date.keys())
    if len(sorted_dates) < 3:
        return None

    streak_count = 1
    for i in range(1, len(sorted_dates)):
        gap = (sorted_dates[i] - sorted_dates[i-1]).days
        if gap == 1:
            streak_count += 1
        else:
            streak_count = 1

    return streak_count if streak_count >= 3 else None

def main():
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        entries = load_history()
    except Exception as e:
        msg = f"⚠️ Pattern analysis failed: {e}"
        subprocess.run(["bash", TG_SEND, msg])
        return

    recent = last_n_days(entries, 7)
    study = [e for e in recent if e.get("type") == "study"]

    if not study:
        msg = (f"📈 *Weekly pattern report — {today}*\n"
               "No study sessions recorded in the last 7 days.")
        subprocess.run(["bash", TG_SEND, msg])
        return

    # Average pct per time bucket
    bucket_pcts = defaultdict(list)
    for e in study:
        pct = e.get("pct_complete", 0)
        bucket = hour_bucket(e.get("timestamp", ""))
        bucket_pcts[bucket].append(pct)

    bucket_avgs = {b: sum(v)/len(v) for b, v in bucket_pcts.items()}
    best_bucket = max(bucket_avgs, key=bucket_avgs.get)
    worst_bucket = min(bucket_avgs, key=bucket_avgs.get)

    # Overall trend (first half vs second half of the week)
    half = len(study) // 2 or 1
    first_avg = sum(e.get("pct_complete", 0) for e in study[:half]) / half
    second_avg = sum(e.get("pct_complete", 0) for e in study[half:]) / max(len(study) - half, 1)

    if second_avg > first_avg + 10:
        trend = "improving ↑"
    elif second_avg < first_avg - 10:
        trend = "declining ↓"
    else:
        trend = "stable →"

    overall_avg = sum(e.get("pct_complete", 0) for e in study) / len(study)

    # Recommendation
    if bucket_avgs.get(worst_bucket, 100) < 70:
        rec = f"Consider moving a lighter topic to {worst_bucket.split('(')[0].strip()} — or protect it from interruptions."
    elif overall_avg < 70:
        rec = "Overall completion below 70% — cut one block per day and go deeper on fewer topics."
    else:
        rec = "Solid week. Keep the current pacing."

    streak = detect_streak(recent)
    streak_note = f"\n⚠️ {streak}-day study streak — keep going!" if streak and streak >= 3 else ""

    msg = (
        f"📈 *Weekly pattern report — {today}*\n"
        f"Sessions: {len(study)} | Avg completion: {overall_avg:.0f}%\n"
        f"Best block: {best_bucket} — avg {bucket_avgs[best_bucket]:.0f}%\n"
        f"Weakest block: {worst_bucket} — avg {bucket_avgs[worst_bucket]:.0f}%\n"
        f"Trend: {trend}{streak_note}\n"
        f"Recommendation: {rec}"
    )

    subprocess.run(["bash", TG_SEND, msg])

if __name__ == "__main__":
    main()
