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

RESULT=$(cd "$VAULT_DIR" && claude -p --dangerously-skip-permissions \
  --allowedTools "Read,Write,Edit,Bash" \
  --no-session-persistence \
"Today is $TODAY. You are Ahsanul's autonomous study mentor running overnight.

TASK: Roll the plan forward for tomorrow ($TOMORROW_WEEKDAY $TOMORROW).

Step 1 — Check today's log:
Read 03_Daily_Logs/$TODAY.md.
If the log has real content (planned vs done, energy level filled in), proceed to Step 2.
If the log is empty or just a template, skip to Step 3.

Step 2 — Update and roll forward:
a) In 02_Courses/[active course]/_Topics.md, mark any topics listed as done today as ✅ (from not done to done).
b) Read 01_Master_Plan.md to understand tomorrow's planned content.
c) Read 00_Dashboard.md to understand current phase and progress.
d) Create or update 03_Daily_Logs/$TOMORROW.md with a realistic plan for tomorrow based on what was completed today and what remains. Follow the existing log template structure.
e) Update 00_Dashboard.md status board if any topics were completed.

Step 3 — Report:
Write a 3-line summary of what you did (or that the log was empty).
Format the summary to send as a Telegram message starting with:
🌙 *Overnight rollover — $TODAY complete*

Keep the message under 8 lines." 2>> "$LOG")

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
