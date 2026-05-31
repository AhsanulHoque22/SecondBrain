#!/bin/bash
# Send a Telegram message to the user.
# Usage: bash tg_send.sh "message text"
# Reads credentials from scripts/.env

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/.env"

MSG="$1"
if [ -z "$MSG" ]; then
  echo "Usage: tg_send.sh <message>" >&2
  exit 1
fi

curl -s -X POST \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${ALLOWED_USERS}" \
  --data-urlencode "text=${MSG}" \
  --data-urlencode "parse_mode=Markdown" \
  > /dev/null
