#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────
# Claude CLI routing wrapper — API provider selection with auto-failover
#
# Default: Claude (Anthropic subscription via OAuth)
# Auto-failover: if Claude exits with an error, the NEXT call skips straight
#                to DeepSeek for 5 minutes, then retries Claude.
#
# Inline commands (type in Telegram message):
#   /deepseek what's my plan?     → force THIS message through DeepSeek
#   /claude how's the system?     → force THIS message through Claude
#
# File override (for scripting):
#   echo "deepseek" > scripts/data/model_override.txt
# ──────────────────────────────────────────────────────────────────────────

REAL_CLAUDE="/home/ahsanul-hoque/.local/bin/claude"
VAULT="/home/ahsanul-hoque/Desktop/SecondBrain"
OVERRIDE_FILE="$VAULT/scripts/data/model_override.txt"
STATUS_FILE="$VAULT/scripts/data/claude_status.txt"

# ── detect inline /deepseek or /claude commands ──────────────────────────
USE_DEEPSEEK=false
FORCE_CLAUDE=false
CLEANED_ARGS=()

for arg in "$@"; do
    case "$arg" in
        */deepseek*)
            USE_DEEPSEEK=true
            cleaned="${arg//\/deepseek /}"
            cleaned="${cleaned//\/deepseek/}"
            CLEANED_ARGS+=("$cleaned")
            ;;
        */claude*)
            FORCE_CLAUDE=true
            USE_DEEPSEEK=false
            cleaned="${arg//\/claude /}"
            cleaned="${cleaned//\/claude/}"
            CLEANED_ARGS+=("$cleaned")
            ;;
        *)
            CLEANED_ARGS+=("$arg")
            ;;
    esac
done

# ── file-based override (takes precedence over inline) ────────────────────
if [ -f "$OVERRIDE_FILE" ]; then
    OVERRIDE=$(tr -d '[:space:]' < "$OVERRIDE_FILE")
    rm "$OVERRIDE_FILE"
    case "$OVERRIDE" in
        deepseek) USE_DEEPSEEK=true; FORCE_CLAUDE=false ;;
        claude)   USE_DEEPSEEK=false; FORCE_CLAUDE=true ;;
    esac
fi

# ── auto-failover: skip Claude if it was recently down ────────────────────
# Unless user explicitly requested Claude via /claude or file override
if ! $FORCE_CLAUDE && ! $USE_DEEPSEEK; then
    if [ -f "$STATUS_FILE" ]; then
        LAST_DOWN=$(stat -c %Y "$STATUS_FILE" 2>/dev/null || echo 0)
        NOW=$(date +%s)
        if [ $((NOW - LAST_DOWN)) -lt 300 ]; then
            # Claude failed less than 5 min ago — use DeepSeek
            USE_DEEPSEEK=true
        else
            # Cooling period over — retry Claude, clear the flag
            rm -f "$STATUS_FILE"
        fi
    fi
fi

# ── helper: set DeepSeek environment ──────────────────────────────────────
setup_deepseek() {
    export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
    export ANTHROPIC_AUTH_TOKEN="sk-a8acfbddc39647798d6fd8a5f51a2f91"
    export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
    export ANTHROPIC_API_KEY="sk-a8acfbddc39647798d6fd8a5f51a2f91"
}

# ── helper: strip DeepSeek vars (use Claude OAuth) ────────────────────────
strip_deepseek() {
    unset ANTHROPIC_BASE_URL
    unset ANTHROPIC_AUTH_TOKEN
    unset ANTHROPIC_MODEL
    unset ANTHROPIC_API_KEY
    unset ANTHROPIC_DEFAULT_SONNET_MODEL
    unset ANTHROPIC_DEFAULT_OPUS_MODEL
}

# ── execute ──────────────────────────────────────────────────────────────

if $USE_DEEPSEEK; then
    # DeepSeek path — no failover needed, just run it
    setup_deepseek
    exec "$REAL_CLAUDE" "${CLEANED_ARGS[@]}"
fi

# ── Claude path with auto-failover ────────────────────────────────────────
# Run Claude as a child process so we can catch failures.
# stdin/stdout/stderr flow through transparently.
strip_deepseek
"$REAL_CLAUDE" "${CLEANED_ARGS[@]}"
CLAUDE_EXIT=$?

# Success — clear any stale down-flag and exit
if [ $CLAUDE_EXIT -eq 0 ]; then
    rm -f "$STATUS_FILE"
    exit 0
fi

# Claude failed (rate limit, quota, auth error, etc.)
# Mark as down so subsequent calls skip straight to DeepSeek
date '+%s' > "$STATUS_FILE"

# Retry this request with DeepSeek
setup_deepseek
exec "$REAL_CLAUDE" "${CLEANED_ARGS[@]}"
