#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────
# Claude CLI routing wrapper — API provider selection
#
# Routing:
#   - Claude (DEFAULT): all tasks use Anthropic subscription via OAuth
#   - DeepSeek: only when explicitly requested via model_override.txt
#
# Manual override:
#   echo "deepseek" > scripts/data/model_override.txt  → use DeepSeek
#   echo "claude"   > scripts/data/model_override.txt  → use Claude
#   The file is auto-deleted after being read.
# ──────────────────────────────────────────────────────────────────────────

REAL_CLAUDE="/home/ahsanul-hoque/.local/bin/claude"
VAULT="/home/ahsanul-hoque/Desktop/SecondBrain"
OVERRIDE_FILE="$VAULT/scripts/data/model_override.txt"

# ── check for manual override ────────────────────────────────────────────
if [ -f "$OVERRIDE_FILE" ]; then
    OVERRIDE=$(tr -d '[:space:]' < "$OVERRIDE_FILE")
    rm "$OVERRIDE_FILE"

    if [ "$OVERRIDE" = "deepseek" ]; then
        export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
        export ANTHROPIC_AUTH_TOKEN="sk-a8acfbddc39647798d6fd8a5f51a2f91"
        export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
        export ANTHROPIC_API_KEY="sk-a8acfbddc39647798d6fd8a5f51a2f91"
        exec "$REAL_CLAUDE" "$@"
    fi
    # "claude" or anything else → fall through to default
fi

# ── default: Claude (Anthropic subscription via OAuth) ────────────────────
# Strip any DeepSeek vars that might have leaked from the environment
exec env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
     -u ANTHROPIC_MODEL -u ANTHROPIC_API_KEY \
     -u ANTHROPIC_DEFAULT_SONNET_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL \
     "$REAL_CLAUDE" "$@"
