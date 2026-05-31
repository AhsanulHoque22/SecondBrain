#!/bin/bash
# Start the Second Brain Telegram Bot
# Usage: bash scripts/start_telegram_bot.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

# Check .env exists
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$SCRIPT_DIR/telegram_bot.env" ]; then
        ENV_FILE="$SCRIPT_DIR/telegram_bot.env"
    else
        echo "ERROR: No .env file found."
        echo "Copy the template and fill it in:"
        echo "  cp $SCRIPT_DIR/telegram_bot.env.example $SCRIPT_DIR/.env"
        echo "  nano $SCRIPT_DIR/.env"
        exit 1
    fi
fi

# Check token is filled in
if grep -q "YOUR_TOKEN_HERE" "$ENV_FILE"; then
    echo "ERROR: Fill in your bot token in $ENV_FILE first."
    exit 1
fi

if grep -q "YOUR_USER_ID_HERE" "$ENV_FILE"; then
    echo "ERROR: Fill in your Telegram user ID in $ENV_FILE first."
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Starting Second Brain Telegram Bot"
echo "  Vault: $(grep APPROVED_DIRECTORY "$ENV_FILE" | cut -d= -f2)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Message your bot on Telegram to test."
echo "  Press Ctrl+C to stop."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run from scripts dir so .env is found automatically
cd "$SCRIPT_DIR"
export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)
claude-telegram-bot
