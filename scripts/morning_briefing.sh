#!/bin/bash
# Morning Briefing Script
# Run manually or via cron at 6 AM
# Reads Dashboard + today's log and prints a 3-line brief
# If Telegram bot is running, sends the brief to your phone

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
WEEKDAY=$(date '+%A')
DAYS_TO_EXAM=""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Good morning — $WEEKDAY, $TODAY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Calculate days to next exam (AI exam Jun 10)
EXAM_DATE="2026-06-10"
DAYS_LEFT=$(( ($(date -d "$EXAM_DATE" +%s) - $(date +%s)) / 86400 ))
if [ $DAYS_LEFT -ge 0 ]; then
    echo "  Next exam: AI (CSE 713) — $DAYS_LEFT days away"
else
    # Check next exam
    echo "  AI exam passed. Check Dashboard for next exam."
fi
echo ""

# Show today's log if it exists
LOG_FILE="$VAULT_DIR/03_Daily_Logs/$TODAY.md"
if [ -f "$LOG_FILE" ]; then
    echo "TODAY'S PLAN:"
    grep "^\- \[" "$LOG_FILE" | head -8
else
    echo "  No log for today yet. Create: 03_Daily_Logs/$TODAY.md"
fi
echo ""

# Show topics needing recall (🔁 status in _Topics.md)
TOPICS_FILE="$VAULT_DIR/02_Courses/CSE713_AI/_Topics.md"
if [ -f "$TOPICS_FILE" ]; then
    RECALL_TOPICS=$(grep "🔁" "$TOPICS_FILE" | awk -F'|' '{print $2}' | sed 's/^ *//;s/ *$//')
    if [ -n "$RECALL_TOPICS" ]; then
        echo "NEEDS RECALL (10 min each):"
        echo "$RECALL_TOPICS" | while read -r topic; do
            echo "  → $topic"
        done
        echo ""
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Start Claude Code: cd ~/Desktop/SecondBrain && claude"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
