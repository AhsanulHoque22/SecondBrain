#!/bin/bash
# Overnight Livora Task — runs at 2:00 AM via cron
# Reads the task you assigned before sleeping, executes it, reports back.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TASK_FILE="$SCRIPT_DIR/data/overnight_task.txt"
RESULT_FILE="$SCRIPT_DIR/data/overnight_result.txt"
TODAY=$(date '+%Y-%m-%d')

export HOME=/home/ahsanul-hoque
export PATH="/home/ahsanul-hoque/.local/bin:/usr/local/bin:/usr/bin:/bin"

LOG="/tmp/secondbrain_livora_$(date '+%Y%m%d').log"
echo "[$(date)] Overnight Livora task starting" >> "$LOG"

# Check if a task was assigned
if [ ! -f "$TASK_FILE" ] || [ ! -s "$TASK_FILE" ]; then
  echo "[$(date)] No overnight task found — skipping" >> "$LOG"
  exit 0
fi

TASK=$(cat "$TASK_FILE")
echo "[$(date)] Task: $TASK" >> "$LOG"

# Notify start
bash "$SCRIPT_DIR/tg_send.sh" "🤖 *Overnight Livora task starting (2 AM)*
Task: $TASK"

# Execute
RESULT=$(cd "$VAULT_DIR" && claude -p --dangerously-skip-permissions \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep,LS" \
  --no-session-persistence \
"Today is $TODAY. You are executing an overnight Livora (startup SaaS) task for Ahsanul.

THE TASK: $TASK

Context:
- Livora files are in 04_Livora/
- Read 04_Livora/README.md first to understand current state
- Work only in 04_Livora/ — do not touch study files
- Time budget: 2 hours of work equivalent
- Quality over speed — commit clean, working code

When done:
1. Write a summary of what you built/changed to $RESULT_FILE
2. Update 04_Livora/README.md with what was accomplished and what tomorrow's task should be
3. Return a short Telegram-ready summary starting with: ✅ *Livora task complete*" 2>> "$LOG")

# Clear the task file so it doesn't re-run tomorrow
> "$TASK_FILE"

if [ -n "$RESULT" ]; then
  bash "$SCRIPT_DIR/tg_send.sh" "$RESULT"
  echo "[$(date)] Livora task complete, result sent to Telegram" >> "$LOG"
else
  bash "$SCRIPT_DIR/tg_send.sh" "⚠️ Livora overnight task failed — check /tmp/secondbrain_livora_$(date '+%Y%m%d').log"
  echo "[$(date)] ERROR: Claude returned empty output" >> "$LOG"
fi

# Git commit — capture all Livora changes
cd "$VAULT_DIR"
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  git commit -m "livora: overnight task $TODAY" >> "$LOG" 2>&1
  echo "[$(date)] Git commit done" >> "$LOG"
fi
