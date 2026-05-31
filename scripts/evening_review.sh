#!/bin/bash
# Evening Review Prompt
# Run at 21:30 or triggered manually
# Prints the daily log template to fill in

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date '+%Y-%m-%d')
LOG_FILE="$VAULT_DIR/03_Daily_Logs/$TODAY.md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Evening Review — $TODAY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$LOG_FILE" ]; then
    echo "Planned items for today:"
    grep "^\- \[" "$LOG_FILE"
    echo ""
    echo "Now open Claude Code and say:"
    echo ""
    echo '  "Update today'\''s log. I did: [list what you did].'
    echo '   Energy: [1-5]. Blockers: [what got in the way].'
    echo '   Roll the plan forward and write tomorrow'\''s log."'
    echo ""
    echo "Or message your Telegram bot the same thing."
else
    echo "No log file for today. Run Claude Code to create it."
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Also: assign overnight Livora task to Telegram bot before sleeping."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
