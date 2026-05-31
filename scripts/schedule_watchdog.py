#!/usr/bin/env python3
"""
Runs every 5 minutes via cron (5 AM – 11 PM).
Checks today_schedule.json for:
  - Study blocks starting in ≤5 min  → send session briefing via Claude
  - Any event ending in last 5 min   → send check-in question
  - Behind by ≥2 study blocks        → send catch-up reminder
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# DeepSeek API routing — ensures watchdog uses DeepSeek regardless of cron env
os.environ.setdefault("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
os.environ.setdefault("ANTHROPIC_AUTH_TOKEN", "sk-a8acfbddc39647798d6fd8a5f51a2f91")
os.environ.setdefault("ANTHROPIC_MODEL", "deepseek-v4-pro[1m]")

VAULT      = Path(__file__).parent.parent
DATA       = Path(__file__).parent / "data"
SCHEDULE   = DATA / "today_schedule.json"
STATE      = DATA / "checkin_state.json"
PENDING    = DATA / "pending_checkin.json"
CARRY      = DATA / "carry_forward.json"
HISTORY    = DATA / "completion_history.json"
TG_SCRIPT  = Path(__file__).parent / "tg_send.sh"
TZ         = ZoneInfo("Asia/Dhaka")


# ── helpers ──────────────────────────────────────────────────────────────────

def load(path, default):
    try:
        return json.loads(path.read_text()) if path.exists() else default
    except Exception:
        return default

def save(path, data):
    DATA.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def tg(msg: str):
    subprocess.run(["bash", str(TG_SCRIPT), msg],
                   capture_output=True, timeout=10)

def run_claude(prompt: str, tools: str = "Read,Bash") -> str:
    r = subprocess.run(
        ["claude", "-p",
         "--dangerously-skip-permissions",
         "--allowedTools", tools,
         "--no-session-persistence",
         prompt],
        capture_output=True, text=True, cwd=str(VAULT), timeout=120
    )
    return r.stdout.strip()

def parse_dt(s: str) -> datetime:
    """Parse ISO datetime and make TZ-aware (Asia/Dhaka)."""
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return dt.astimezone(TZ)

def is_study(event: dict) -> bool:
    t = (event.get("title", "") + event.get("type", "")).lower()
    return event.get("type") == "study" or any(
        k in t for k in ["study", "block", "past paper", "recall", "revision"]
    )


# ── past paper analysis ──────────────────────────────────────────────────────

def analyze_past_papers(event: dict) -> None:
    """
    Reads the past-paper PDF for topics in this session.
    Updates _TopicQuestionMap.md with exact question wording.
    Runs BEFORE the briefing so the briefing can show real questions.
    """
    prompt = f"""You are preparing Ahsanul's past-paper analysis before his study session.

SESSION: {event['title']}
TOPICS IN THIS SESSION: {event.get('description', '')[:400]}

YOUR TASK — do these steps in order:

Step 1 — Find which course folder this session belongs to.
Run: find 02_Courses -name "_TopicQuestionMap.md"
Read the matching _TopicQuestionMap.md file.

Step 2 — Identify which topics from the session appear in the map.
For each matching topic:
  a. Note the question numbers and PDF page numbers listed in the map.
  b. Read those exact pages of the past-paper PDF (use the Read tool with the pages parameter).
     The PDF is in the same 02_Courses subfolder (filename contains "Previous Year" or "past" or "question").
  c. Extract the EXACT question text as it appears in the PDF — word for word.
     Include all sub-parts (i), (ii), (iii) etc.

Step 3 — Update _TopicQuestionMap.md.
For each topic's table, update the Notes column with the exact question wording you found.
Format: "Q: [exact question text truncated to 120 chars]"
Only update rows where the Notes are currently vague (e.g. just "PAGE model, environment classification").
Do NOT overwrite rows that already have exact question text.
Use Edit tool to make targeted updates — do not rewrite the whole file.

Step 4 — Output a compact summary for use in the briefing:
Format exactly like this (this will be inserted into the Telegram briefing):

PAST_PAPER_ANALYSIS_START
Topic: [Topic Name]
| Year | Q# | Exact question |
|------|-----|----------------|
| 2024 | A-Q1 | [exact wording, max 100 chars] |
| 2023 | A-Q1 | [exact wording, max 100 chars] |
| 2022 | A-Q1 | [exact wording, max 100 chars] |
🔁 Pattern: [one sentence — what aspect of this topic repeats every year]
PAST_PAPER_ANALYSIS_END

Repeat the block for each topic in the session.
If a topic has no past paper questions, write: "No direct questions found for [topic]."

Important: Read the actual PDF pages — do not guess or fabricate question text."""

    run_claude(prompt, tools="Read,Edit,Bash,LS")


# ── session briefing ─────────────────────────────────────────────────────────

def send_briefing(event: dict):
    # Step 1: analyze past papers and update the question map first
    analyze_past_papers(event)

    carry_data = load(CARRY, {"topics": []})
    carry_topics = carry_data.get("topics", [])

    carry_text = ""
    if carry_topics:
        lines = [f"- {t['topic']} ({t['remaining_pct']}% remaining, from {t['source_date']})"
                 for t in carry_topics]
        carry_text = "CARRY-FORWARD TOPICS (do these first):\n" + "\n".join(lines)

    start_dt = parse_dt(event["start_time"])
    end_dt   = parse_dt(event["end_time"])
    duration = event.get("duration_minutes") or int((end_dt - start_dt).seconds / 60)
    start_str = start_dt.strftime("%I:%M %p")

    prompt = f"""You are sending a pre-session briefing to Ahsanul on Telegram.

SESSION DETAILS:
Title: {event['title']}
Start: {start_str}
Duration: {duration} minutes
Description: {event.get('description', '')[:600]}

{carry_text}

Instructions:
1. Read scripts/data/carry_forward.json for any additional carry-forward topics.
2. Run: find 02_Courses -type f   to list all available source materials.
3. Read the _TopicQuestionMap.md for this course — it has just been updated with exact past paper questions.
4. For each topic, identify which source file(s) from 02_Courses/ are relevant.
5. Combine carry-forward topics with topics from the session description.
6. Distribute ALL topics across the {duration}-minute session with realistic timestamps starting at {start_str}.
7. Put carry-forward topics first. Reserve last 10 minutes for active recall.

Output a Telegram message in this EXACT format (use Markdown):
📚 *{event['title']}*
🕐 {start_str} · {duration} min

*Session plan:*
`HH:MM` Topic 1 — X min
`HH:MM` Topic 2 — X min
`HH:MM` Active recall — 10 min

*Sources:*
📄 Topic 1 → `filename.pdf`
📄 Topic 2 → `filename.pdf`

*Past paper questions for today's topics:*
📝 [Topic Name] — appears [N]/5 years
  • 2024 A-Q1: [exact question, max 80 chars]
  • 2023 A-Q1: [exact question, max 80 chars]
  • 🔁 Pattern: [what repeats every year — one line]

*Carry-forward:* [list or "None"]
*Goal:* [one sentence — what does success look like?]

Rules:
- Only list source files that actually exist in 02_Courses/. Do not invent filenames.
- Use the exact question text from the updated _TopicQuestionMap.md.
- Be realistic. Never schedule more content than fits in {duration} minutes."""

    result = run_claude(prompt, tools="Read,LS,Bash")
    if result:
        tg(result)


# ── check-in questions ────────────────────────────────────────────────────────

def send_checkin(event: dict):
    title = event.get("title", "that task")

    if is_study(event):
        msg = (
            f"📊 *Check-in: {title}*\n\n"
            f"How did it go? Reply in any format:\n\n"
            f"• `done` — finished everything\n"
            f"• `70%` — roughly how much you covered\n"
            f"• `done except A* search` — what you didn't finish\n"
            f"• `only did agents and search` — what you did finish\n"
            f"• `70%, couldn't finish past papers` — both\n\n"
            f"_(reply `skip` to skip)_"
        )
    else:
        msg = (
            f"✅ *Quick check: {title}*\n\n"
            f"Did you complete this? Reply `yes` or `no`"
        )

    pending = {
        "event_id":    event.get("id", ""),
        "event_title": title,
        "is_study":    is_study(event),
        "start_time":  event["start_time"],
        "end_time":    event["end_time"],
        "description": event.get("description", "")[:600],
        "asked_at":    datetime.now(TZ).isoformat(),
    }
    save(PENDING, pending)
    tg(msg)


# ── behind-schedule detector ──────────────────────────────────────────────────

def check_if_behind(state: dict, schedule: dict, now: datetime):
    """If 2+ study events ended without a check-in response, send a nudge."""
    events = schedule.get("events", [])
    missed = 0
    for ev in events:
        end = parse_dt(ev["end_time"])
        if end < now and is_study(ev):
            ev_id = ev.get("id", ev.get("title"))
            if ev_id not in state.get("responded", []):
                missed += 1

    if missed >= 2 and not state.get("nudge_sent_at"):
        behind_msg = (
            f"⚠️ *Heads up — you're behind*\n\n"
            f"{missed} study block(s) ended without a check-in.\n"
            f"Reply to the last check-in, or tell me:\n"
            f"`Update log: [what you did, energy X/5]`\n\n"
            f"I'll adjust tomorrow's plan around what's left over."
        )
        tg(behind_msg)
        state["nudge_sent_at"] = datetime.now(TZ).isoformat()


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    now = datetime.now(TZ)

    # Only run 5 AM – 11 PM
    if now.hour < 5 or now.hour >= 23:
        return

    schedule = load(SCHEDULE, {})
    if not schedule or "events" not in schedule:
        return

    today_str = now.strftime("%Y-%m-%d")
    state = load(STATE, {})

    # Reset state on new day
    if state.get("date") != today_str:
        state = {"date": today_str, "briefed": [], "checked": [], "responded": []}

    events = schedule.get("events", [])
    window = timedelta(minutes=5)

    for event in events:
        ev_id  = event.get("id") or event.get("title", "")
        start  = parse_dt(event["start_time"])
        end    = parse_dt(event["end_time"])

        # ── briefing: study block starts within next 5 min ──────────────────
        time_to_start = (start - now).total_seconds()
        if 0 < time_to_start <= 300 and ev_id not in state["briefed"]:
            if is_study(event):
                send_briefing(event)
            state["briefed"].append(ev_id)

        # ── check-in: event ended in last 5 min ─────────────────────────────
        time_since_end = (now - end).total_seconds()
        if 0 < time_since_end <= 300 and ev_id not in state["checked"]:
            # Skip check-ins for very short events (<5 min) and breaks
            if event.get("duration_minutes", 999) >= 10 and event.get("type") not in ("break",):
                send_checkin(event)
            state["checked"].append(ev_id)

    # ── behind-schedule nudge ────────────────────────────────────────────────
    check_if_behind(state, schedule, now)

    save(STATE, state)


if __name__ == "__main__":
    main()
