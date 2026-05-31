#!/bin/bash
# Morning Briefing — runs at 4:15 AM via cron
# Claude reads the vault, generates a personalized brief, sends to Telegram.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
WEEKDAY=$(date '+%A')

export HOME=/home/ahsanul-hoque
export PATH="/home/ahsanul-hoque/.local/bin:/usr/local/bin:/usr/bin:/bin"

# DeepSeek API routing
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-a8acfbddc39647798d6fd8a5f51a2f91"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"

LOG="/tmp/secondbrain_morning_$(date '+%Y%m%d').log"

echo "[$(date)] Morning brief starting" >> "$LOG"

BRIEF=$(cd "$VAULT_DIR" && claude -p --dangerously-skip-permissions \
  --allowedTools "Read,Bash" \
  --no-session-persistence \
"Today is $WEEKDAY $TODAY. You are Ahsanul's study mentor.

Read these files:
- 00_Dashboard.md
- 03_Daily_Logs/$TODAY.md (if it exists)
- 02_Courses/CSE713_AI/_Topics.md (or the active course _Topics.md)

Then send him a morning briefing via Telegram in this EXACT format — no extra text, just this:

🌅 *Good morning, Ahsanul — $WEEKDAY $TODAY*

📍 *Where you stand:* [days to next exam, course name, current phase — 1 line]

🎯 *Most important thing right now:* [single most urgent action — 1 line]

⏰ *First block (5:10 AM):* [exact topic + what to do in it — 1–2 lines]

🔁 *Spaced recall today (10 min each):*
[list only topics with 🔁 status from _Topics.md, or write 'None' if none]

Keep the whole message under 15 lines. Be direct. No fluff." 2>> "$LOG")

if [ -n "$BRIEF" ]; then
  bash "$SCRIPT_DIR/tg_send.sh" "$BRIEF"
  echo "[$(date)] Brief sent to Telegram" >> "$LOG"
else
  bash "$SCRIPT_DIR/tg_send.sh" "⚠️ Morning brief failed — check /tmp/secondbrain_morning_$(date '+%Y%m%d').log"
  echo "[$(date)] ERROR: Claude returned empty output" >> "$LOG"
fi

# Git commit — if rollover wrote tomorrow's log, capture it
cd "$VAULT_DIR"
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  git commit -m "auto: morning brief $TODAY" >> "$LOG" 2>&1
  echo "[$(date)] Git commit done" >> "$LOG"
fi
