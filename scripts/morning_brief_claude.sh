#!/bin/bash
# Morning Briefing — runs at 4:15 AM via cron

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
WEEKDAY=$(date '+%A')

export HOME=/home/ahsanul-hoque
export PATH="/home/ahsanul-hoque/.local/bin:/usr/local/bin:/usr/bin:/bin"

LOG="/tmp/secondbrain_morning_$(date '+%Y%m%d').log"
echo "[$(date)] Morning brief starting" >> "$LOG"

BRIEF=$(cd "$VAULT_DIR" && claude -p --dangerously-skip-permissions \
  --allowedTools "Read" \
  --no-session-persistence \
"Today is $WEEKDAY $TODAY. Read scripts/data/wiki_state.md and 03_Daily_Logs/$TODAY.md.

Send this EXACT format — no extra text:

🌅 *Good morning, Ahsanul — $WEEKDAY $TODAY*

📍 *Where you stand:* [active exam, days left, phase — from wiki_state]

🎯 *Most important thing:* [highest-yield 🔲 topic or carry-forward item — 1 line]

⏰ *First block (5:10 AM):* [Block 1 from today's log — 1 line]

🔁 *Recall due today:* [from wiki_state recall section, or 'None']

Under 10 lines. No fluff." 2>> "$LOG")

if [ -n "$BRIEF" ]; then
  bash "$SCRIPT_DIR/tg_send.sh" "$BRIEF"
  echo "[$(date)] Brief sent" >> "$LOG"
else
  bash "$SCRIPT_DIR/tg_send.sh" "⚠️ Morning brief failed — check /tmp/secondbrain_morning_$(date '+%Y%m%d').log"
  echo "[$(date)] ERROR: empty output" >> "$LOG"
fi

cd "$VAULT_DIR"
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  git commit -m "auto: morning brief $TODAY" >> "$LOG" 2>&1
fi
