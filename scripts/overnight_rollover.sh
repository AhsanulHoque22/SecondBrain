#!/bin/bash
# Overnight Plan Rollover — runs at 11:30 PM via cron
# Claude checks if today's log was filled, rolls plan forward, writes tomorrow's log.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
TOMORROW=$(date -d 'tomorrow' '+%Y-%m-%d')
TOMORROW_WEEKDAY=$(date -d 'tomorrow' '+%A')

export HOME=/home/ahsanul-hoque
export PATH="/home/ahsanul-hoque/.local/bin:/usr/local/bin:/usr/bin:/bin"

LOG="/tmp/secondbrain_rollover_$(date '+%Y%m%d').log"
echo "[$(date)] Overnight rollover starting" >> "$LOG"

# Step 1: Run spaced repetition scheduler
echo "[$(date)] Running spaced rep scheduler" >> "$LOG"
python3 "$SCRIPT_DIR/spaced_rep.py" >> "$LOG" 2>&1
RECALL_DUE=$(cat "$SCRIPT_DIR/data/recall_due.md" 2>/dev/null || echo "No recall data")

RESULT=$(cd "$VAULT_DIR" && claude -p --dangerously-skip-permissions \
  --allowedTools "Read,Write,Edit,Bash" \
  --no-session-persistence \
"Today is $TODAY. You are Ahsanul's autonomous study mentor running overnight.

TASK: Roll the plan forward for tomorrow ($TOMORROW_WEEKDAY $TOMORROW).

--- SPACED REPETITION DATA ---
$RECALL_DUE
--- END SPACED REP DATA ---

Step 1 — Read today's log:
Read 03_Daily_Logs/$TODAY.md.
Check the 'End-of-day log' section. If 'Did:' and 'Energy/focus' are filled in, proceed.
If the log is empty or unfilled, write the rollover report noting the log was not filled.

Step 2 — Update all relevant files:
a) Read 02_Courses/[active course]/_Topics.md.
   For every topic listed under 'Topics completed:' in today's log:
   - Change status to ✅
   - Write today's date ($TODAY) in the 'Last Reviewed' column
   - Write the computed next recall date in 'Next Recall' (use the spaced rep data above, or +2 days if not listed)
   - Update Confidence column if a rating was given
b) Update 00_Dashboard.md status board (topics mapped, high-yield done, confidence).
c) Read 01_Master_Plan.md to find what comes next.
d) Read 03_Daily_Logs/_Template.md for the log format.

Step 3 — Build tomorrow's log (03_Daily_Logs/$TOMORROW.md):
Create the file using the template. Fill in:
- 'Planned blocks' section: carry forward any INCOMPLETE tasks from today first (highest priority), then add next topics from master plan
- '🔁 Recall due today' section: paste the due topics from the spaced rep data above
- Leave 'End-of-day log' blank (Ahsanul fills this tomorrow night)
- Make the plan realistic — do not schedule more than 7 blocks

Step 4 — Report summary:
Format as a Telegram message starting with:
🌙 *Overnight rollover — $TODAY*

Include:
- Topics marked ✅ today (if any)
- Recall topics scheduled for tomorrow
- Tomorrow's Block 1 topic (the most important thing)

Keep under 10 lines." 2>> "$LOG")

if [ -n "$RESULT" ]; then
  bash "$SCRIPT_DIR/tg_send.sh" "$RESULT"
  echo "[$(date)] Rollover complete, result sent to Telegram" >> "$LOG"
else
  bash "$SCRIPT_DIR/tg_send.sh" "⚠️ Overnight rollover failed — check /tmp/secondbrain_rollover_$(date '+%Y%m%d').log"
  echo "[$(date)] ERROR: Claude returned empty output" >> "$LOG"
fi

# Git commit — capture everything done overnight
cd "$VAULT_DIR"
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  git commit -m "auto: overnight rollover $TODAY" >> "$LOG" 2>&1
  echo "[$(date)] Git commit done" >> "$LOG"
fi
