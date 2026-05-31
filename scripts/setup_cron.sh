#!/bin/bash
# Sets up all cron jobs for Second Brain automation.
# Run once: bash scripts/setup_cron.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Setting up Second Brain cron jobs..."

# Make all scripts executable
chmod +x "$SCRIPT_DIR"/*.sh

# Ensure data dir exists
mkdir -p "$SCRIPT_DIR/data"
touch "$SCRIPT_DIR/data/overnight_task.txt"
touch "$SCRIPT_DIR/data/overnight_result.txt"

# Define cron entries
CRON_MORNING="15 4 * * * bash $SCRIPT_DIR/morning_brief_claude.sh"
CRON_EVENING="10 21 * * * bash $SCRIPT_DIR/evening_reminder.sh"
CRON_ROLLOVER="30 23 * * * bash $SCRIPT_DIR/overnight_rollover.sh"
CRON_LIVORA="0 2 * * * bash $SCRIPT_DIR/overnight_livora.sh"

# Install cron jobs (remove old entries first to avoid duplicates)
(crontab -l 2>/dev/null \
  | grep -v "morning_brief_claude\|evening_reminder\|overnight_rollover\|overnight_livora\|morning_briefing\|evening_review"
  echo "$CRON_MORNING"
  echo "$CRON_EVENING"
  echo "$CRON_ROLLOVER"
  echo "$CRON_LIVORA"
) | crontab -

echo ""
echo "Cron jobs installed:"
echo "  4:15 AM  — Morning briefing (Claude reads vault → Telegram)"
echo "  9:10 PM  — Evening reminder (nudge to fill daily log)"
echo " 11:30 PM  — Overnight rollover (Claude rolls plan forward → Telegram)"
echo "  2:00 AM  — Livora overnight task (runs task from overnight_task.txt)"
echo ""
echo "Overnight task file: $SCRIPT_DIR/data/overnight_task.txt"
echo "Before sleeping, tell the Telegram bot:"
echo "  \"Tonight's Livora task: [describe what to build]\""
echo ""
echo "View cron jobs: crontab -l"
echo "View logs:      ls /tmp/secondbrain_*.log"
