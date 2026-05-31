#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────
# Claude CLI routing wrapper — API provider selection
#
# Default: Claude (Anthropic subscription via OAuth)
#
# Switch provider inline from Telegram:
#   /deepseek what's my plan?     → routes THIS message to DeepSeek
#   /claude explain this concept  → routes THIS message to Claude
#
# Or via file (for scripting / cron):
#   echo "deepseek" > scripts/data/model_override.txt
#   echo "claude"   > scripts/data/model_override.txt
#   (file is auto-deleted after being read)
# ──────────────────────────────────────────────────────────────────────────

REAL_CLAUDE="/home/ahsanul-hoque/.local/bin/claude"
VAULT="/home/ahsanul-hoque/Desktop/SecondBrain"
OVERRIDE_FILE="$VAULT/scripts/data/model_override.txt"

# ── detect inline /deepseek or /claude commands in the arguments ─────────
USE_DEEPSEEK=false
CLEANED_ARGS=()

for arg in "$@"; do
    case "$arg" in
        */deepseek*)
            USE_DEEPSEEK=true
            # Strip /deepseek from the argument (with optional trailing space)
            cleaned="${arg//\/deepseek /}"
            cleaned="${cleaned//\/deepseek/}"
            CLEANED_ARGS+=("$cleaned")
            ;;
        */claude*)
            USE_DEEPSEEK=false
            # Strip /claude from the argument (with optional trailing space)
            cleaned="${arg//\/claude /}"
            cleaned="${cleaned//\/claude/}"
            CLEANED_ARGS+=("$cleaned")
            ;;
        *)
            CLEANED_ARGS+=("$arg")
            ;;
    esac
done

# ── file-based override (takes precedence over inline command) ───────────
if [ -f "$OVERRIDE_FILE" ]; then
    OVERRIDE=$(tr -d '[:space:]' < "$OVERRIDE_FILE")
    rm "$OVERRIDE_FILE"
    case "$OVERRIDE" in
        deepseek) USE_DEEPSEEK=true ;;
        claude)   USE_DEEPSEEK=false ;;
    esac
fi

# ── execute ──────────────────────────────────────────────────────────────
if $USE_DEEPSEEK; then
    export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
    export ANTHROPIC_AUTH_TOKEN="sk-a8acfbddc39647798d6fd8a5f51a2f91"
    export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
    export ANTHROPIC_API_KEY="sk-a8acfbddc39647798d6fd8a5f51a2f91"
    exec "$REAL_CLAUDE" "${CLEANED_ARGS[@]}"
fi

# Default: Claude (Anthropic subscription via OAuth)
exec env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
     -u ANTHROPIC_MODEL -u ANTHROPIC_API_KEY \
     -u ANTHROPIC_DEFAULT_SONNET_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL \
     "$REAL_CLAUDE" "${CLEANED_ARGS[@]}"
