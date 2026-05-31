#!/bin/bash
# Evening Reminder — runs at 9:10 PM via cron (just before wind-down)
# Sends a Telegram nudge to fill the daily log before sleeping.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TODAY=$(date '+%Y-%m-%d')

bash "$SCRIPT_DIR/tg_send.sh" "📝 *Daily log time — $TODAY*

Before you sleep, tell me:
1. What you did today (topics covered)
2. Energy level (1–5)
3. Any blockers

Also: if you have a Livora task for tonight, say:
*\"Tonight's Livora task: [what to build/write]\"*

I'll roll the plan forward and write tomorrow's log while you sleep."
