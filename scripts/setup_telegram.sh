#!/bin/bash
# Telegram Bot Setup Script
# Run this AFTER you have your bot token from @BotFather and your Telegram user ID

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$SCRIPT_DIR/telegram_bot.env"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Second Brain — Telegram Bot Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python
if ! python3 --version &>/dev/null; then
    echo "ERROR: Python 3 not found. Install it first."
    exit 1
fi

# Install the bot
echo "Installing claude-code-telegram..."
pip3 install "git+https://github.com/RichardAtCT/claude-code-telegram@v1.3.0" --quiet
echo "✓ Installed"

# Create env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    cat > "$ENV_FILE" << 'ENVFILE'
# Telegram Bot Configuration
# Fill in all fields before running start_telegram_bot.sh

# Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Your bot's username (without @)
TELEGRAM_BOT_USERNAME=your_bot_username_here

# Your Telegram user ID (get from @userinfobot)
ALLOWED_USERS=YOUR_TELEGRAM_USER_ID_HERE

# Directory the bot has access to (your SecondBrain vault)
APPROVED_DIRECTORY=/home/ahsanul-hoque/Desktop/SecondBrain
ENVFILE
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "NEXT STEPS:"
    echo ""
    echo "1. Open Telegram → @BotFather → /newbot"
    echo "   Copy the API token"
    echo ""
    echo "2. Open Telegram → @userinfobot → /start"
    echo "   Copy your user ID number"
    echo ""
    echo "3. Edit this file with your credentials:"
    echo "   $ENV_FILE"
    echo ""
    echo "4. Run: bash $SCRIPT_DIR/start_telegram_bot.sh"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "✓ Config file already exists: $ENV_FILE"
    echo "  Edit it if you need to change credentials."
fi
