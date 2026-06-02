#!/bin/bash
# Overnight Plan Rollover — runs at 11:30 PM via cron

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
TOMORROW=$(date -d 'tomorrow' '+%Y-%m-%d')
TOMORROW_WEEKDAY=$(date -d 'tomorrow' '+%A')
DAY_OF_WEEK=$(date '+%A')

export HOME=/home/ahsanul-hoque
export PATH="/home/ahsanul-hoque/.local/bin:/usr/local/bin:/usr/bin:/bin"

LOG="/tmp/secondbrain_rollover_$(date '+%Y%m%d').log"
echo "[$(date)] Overnight rollover starting" >> "$LOG"

# Run spaced repetition scheduler
echo "[$(date)] Running spaced rep" >> "$LOG"
python3 "$SCRIPT_DIR/spaced_rep.py" >> "$LOG" 2>&1
RECALL_DUE=$(cat "$SCRIPT_DIR/data/recall_due.md" 2>/dev/null || echo "None")

RESULT=$(cd "$VAULT_DIR" && claude -p --dangerously-skip-permissions \
  --allowedTools "Read,Write,Edit,Bash" \
  --no-session-persistence \
"Today is $TODAY. You are Ahsanul's autonomous study mentor running overnight.
Tomorrow is $TOMORROW_WEEKDAY $TOMORROW.

--- RECALL DUE TOMORROW ---
$RECALL_DUE
--- END ---

Read and execute these steps IN ORDER:

Step 1 — Read today's log (03_Daily_Logs/$TODAY.md).
Check 'End-of-day log'. If unfilled, note it and continue.

Step 2 — Update 02_Courses/[active course]/_Topics.md:
For every topic in 'Topics completed:' today: status → ✅, Last Reviewed → $TODAY, Next Recall → from recall data or +2 days.

Step 3 — Read scripts/data/carry_forward.json.
Add any incomplete topics from today. Remove topics completed today. Save.

Step 4 — Read 03_Daily_Logs/_Template.md. Build 03_Daily_Logs/$TOMORROW.md:
- Carry-forward topics first, then recall due, then next master plan topics.
- Paste recall due section from data above.
- Max 7 study blocks. Leave 'End-of-day log' blank.

Step 5 — Reset checkin state:
Write to scripts/data/checkin_state.json: {\"date\": \"$TOMORROW\", \"briefed\": [], \"checked\": [], \"responded\": []}

Step 6 — Update 00_Dashboard.md: topics done count, confidence average.

Step 7 — Write scripts/data/wiki_state.md with this EXACT structure:
# Study Brain — Compiled State
_Updated: $TODAY by overnight rollover_

## Active exam
[next upcoming exam: course, date, days from $TOMORROW, phase]

## Topics — [active course code]
[condensed table from _Topics.md: Topic | Status | Conf | Next Recall — no Notes column]

## Carry-forward
[list from carry_forward.json, or 'None']

## Recall due $TOMORROW
[paste from recall data above]

## Recent pattern (last 3 days)
[3-line summary: date | topics completed | energy — from today's log and wiki_state.md previous entries]

Step 8 — Send Telegram summary starting with:
🌙 *Overnight rollover — $TODAY*
- Topics ✅ today (if any)
- Carry-forward (if any)
- Recall due $TOMORROW
- Tomorrow's Block 1 topic
Under 10 lines." 2>> "$LOG")

if [ -n "$RESULT" ]; then
  bash "$SCRIPT_DIR/tg_send.sh" "$RESULT"
  echo "[$(date)] Rollover complete" >> "$LOG"
else
  bash "$SCRIPT_DIR/tg_send.sh" "⚠️ Overnight rollover failed — check /tmp/secondbrain_rollover_$(date '+%Y%m%d').log"
  echo "[$(date)] ERROR: empty output" >> "$LOG"
fi

# Sunday pattern analysis — Python only, no Claude call
if [ "$DAY_OF_WEEK" = "Sunday" ]; then
  echo "[$(date)] Running weekly pattern analysis" >> "$LOG"
  python3 "$SCRIPT_DIR/pattern_analysis.py" >> "$LOG" 2>&1
fi

cd "$VAULT_DIR"
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  git commit -m "auto: overnight rollover $TODAY" >> "$LOG" 2>&1
  echo "[$(date)] Git commit done" >> "$LOG"
fi
