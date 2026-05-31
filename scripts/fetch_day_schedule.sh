#!/bin/bash
# Runs at 5:00 AM — fetches today's Google Calendar events, saves as JSON.
# schedule_watchdog.py reads this file all day.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
TODAY_END=$(date -d 'tomorrow' '+%Y-%m-%d')

export HOME=/home/ahsanul-hoque
export PATH="/home/ahsanul-hoque/.local/bin:/usr/local/bin:/usr/bin:/bin"

LOG="/tmp/secondbrain_schedule_$(date '+%Y%m%d').log"
echo "[$(date)] Fetching day schedule for $TODAY" >> "$LOG"

cd "$VAULT_DIR"

claude -p --dangerously-skip-permissions \
  --allowedTools "mcp__claude_ai_Google_Calendar__list_events,Write,Bash" \
  --no-session-persistence \
"Today is $TODAY. Fetch ALL Google Calendar events for today ($TODAY, timezone Asia/Dhaka).

Then write them to scripts/data/today_schedule.json in this EXACT JSON format:
{
  \"date\": \"$TODAY\",
  \"fetched_at\": \"[current ISO time]\",
  \"events\": [
    {
      \"id\": \"[google event id]\",
      \"title\": \"[event title]\",
      \"start_time\": \"[ISO datetime with timezone]\",
      \"end_time\": \"[ISO datetime with timezone]\",
      \"duration_minutes\": [integer],
      \"type\": \"[study|prayer|meal|relationship|exercise|livora|break|other]\",
      \"description\": \"[first 500 chars of description or empty string]\"
    }
  ]
}

Type classification rules:
- study: any event with 'Study', 'Block', 'AI Study', 'Past Paper' in title
- prayer: Fajr, Dhuhr, Asr, Maghrib, Isha
- meal: Breakfast, Lunch, Dinner
- relationship: Girlfriend
- exercise: Exercise
- livora: Livora
- break: Break, Wind down, Phone
- other: everything else

Write the file, then output exactly: SCHEDULE_SAVED" 2>> "$LOG"

if grep -q "SCHEDULE_SAVED" "$LOG" 2>/dev/null || [ -f "$SCRIPT_DIR/data/today_schedule.json" ]; then
  EVENT_COUNT=$(python3 -c "import json; d=json.load(open('$SCRIPT_DIR/data/today_schedule.json')); print(len(d['events']))" 2>/dev/null || echo "?")
  bash "$SCRIPT_DIR/tg_send.sh" "📅 *Schedule loaded for $TODAY* — $EVENT_COUNT events. I'll check in with you after each one."
  echo "[$(date)] Schedule saved with $EVENT_COUNT events" >> "$LOG"
else
  echo "[$(date)] ERROR: Schedule file not created" >> "$LOG"
  bash "$SCRIPT_DIR/tg_send.sh" "⚠️ Could not load today's schedule from Google Calendar. Check /tmp/secondbrain_schedule_$(date '+%Y%m%d').log"
fi
