#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────
# Claude CLI routing wrapper — task-based API provider selection
#
# Routes claude calls to either DeepSeek (default) or Anthropic (Claude
# subscription) based on task complexity. The bot's SDK invokes this
# wrapper instead of calling `claude` directly.
#
# Routing rules:
#   - DeepSeek (default): most tasks — study briefings, daily logs,
#     Livora coding, quick questions, file ops, past paper extraction
#   - Claude: complex mentoring, strategic planning, weekly pattern
#     analysis — tasks where nuanced judgment matters most
#
# Manual override (touch a file before sending a Telegram message):
#   echo "claude" > scripts/data/model_override.txt   → force Claude
#   echo "deepseek" > scripts/data/model_override.txt → force DeepSeek
#   rm scripts/data/model_override.txt                → back to auto
# ──────────────────────────────────────────────────────────────────────────

REAL_CLAUDE="/home/ahsanul-hoque/.local/bin/claude"
VAULT="/home/ahsanul-hoque/Desktop/SecondBrain"

# ── manual override via temp file ────────────────────────────────────────
OVERRIDE_FILE="$VAULT/scripts/data/model_override.txt"
if [ -f "$OVERRIDE_FILE" ]; then
    OVERRIDE=$(cat "$OVERRIDE_FILE" | tr -d '[:space:]')
    rm "$OVERRIDE_FILE"
    case "$OVERRIDE" in
        claude)
            exec env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
                 -u ANTHROPIC_MODEL -u ANTHROPIC_API_KEY \
                 -u ANTHROPIC_DEFAULT_SONNET_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL \
                 "$REAL_CLAUDE" "$@"
            ;;
        deepseek|*)
            exec "$REAL_CLAUDE" "$@"
            ;;
    esac
fi

# ── automatic routing: inspect prompt for complexity markers ─────────────
# Combine all args into a single string for pattern matching
COMBINED="$*"

# Tasks that benefit from Claude's nuanced reasoning:
# - Strategic system planning / architecture
# - Weekly pattern analysis (multi-week trends, subtle correlations)
# - Complex mentoring decisions (schedule restructuring, risk assessment)
# - Deep research with adversarial verification
if echo "$COMBINED" | grep -qiE \
    "(strategic.*plan|system.*architect|weekly.*pattern|pattern.*analys"\
"|deep.*research|adversarial.*verif|complex.*mentoring|schedule.*restructur"\
"|risk.*assess|master.*plan)"; then
    # Route to Anthropic subscription (Claude) by stripping DeepSeek vars
    exec env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
         -u ANTHROPIC_MODEL -u ANTHROPIC_API_KEY \
         -u ANTHROPIC_DEFAULT_SONNET_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL \
         "$REAL_CLAUDE" "$@"
fi

# ── default: DeepSeek API ─────────────────────────────────────────────────
exec "$REAL_CLAUDE" "$@"
