#!/usr/bin/env bash
# question_analysis.sh — Trigger "[Topic] question analysis and solution" workflow
# Usage: ./scripts/question_analysis.sh "FOL + Resolution"
#        Or from Telegram bot: automatically invoked when message matches pattern

set -euo pipefail

VAULT="/home/ahsanul-hoque/Desktop/SecondBrain"
COURSE_DIR="$VAULT/02_Courses/CSE713_AI"
PROTOCOL="$VAULT/scripts/data/protocols/question_analysis.md"
LOG="$VAULT/scripts/data/question_analysis.log"

TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
  echo "Usage: $0 \"Topic Name\""
  echo "Example: $0 \"FOL + Resolution\""
  exit 1
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
echo "[$TIMESTAMP] Question analysis triggered for: $TOPIC" | tee -a "$LOG"

# Map topic to slug for output file naming
slug_map() {
  local t="$1"
  case "$t" in
    *FOL*|*Resolution*|*Propositional*) echo "FOL_Resolution" ;;
    *Search*|*UCS*|*Greedy*|*A\**) echo "Search" ;;
    *Alpha*|*Beta*|*Minimax*) echo "AlphaBeta" ;;
    *Forward*|*Backward*|*Chain*|*Rule*) echo "RuleBased" ;;
    *STRIPS*|*Planning*|*POP*) echo "Planning" ;;
    *Bayes*|*Bayesian*|*Uncertainty*) echo "BayesNet" ;;
    *Neural*|*Learning*|*Backprop*) echo "NeuralNet" ;;
    *CSP*|*Constraint*) echo "CSP" ;;
    *Fuzzy*) echo "FuzzyLogic" ;;
    *Agent*) echo "Agents" ;;
    *Hill*|*Simulated*|*Anneal*) echo "LocalSearch" ;;
    *) echo "$(echo "$t" | tr ' +/' '_' | tr -d '()')" ;;
  esac
}

SLUG=$(slug_map "$TOPIC")
TEX_FILE="$COURSE_DIR/${SLUG}_Solutions.tex"
PDF_FILE="$COURSE_DIR/${SLUG}_Solutions.pdf"

echo "  Topic slug: $SLUG"
echo "  Output PDF: $PDF_FILE"

# If PDF already exists and tex file exists, offer to recompile
if [[ -f "$TEX_FILE" ]]; then
  echo "  [INFO] LaTeX file already exists: $TEX_FILE"
  echo "  [INFO] Recompiling PDF..."
  cd "$COURSE_DIR"
  pdflatex -interaction=nonstopmode "${SLUG}_Solutions.tex" > /dev/null 2>&1 && \
  pdflatex -interaction=nonstopmode "${SLUG}_Solutions.tex" > /dev/null 2>&1 && \
  echo "  [OK] PDF compiled: $PDF_FILE" || \
  echo "  [WARN] LaTeX compilation had errors — check ${SLUG}_Solutions.log"
  echo "[$TIMESTAMP] Recompiled PDF for: $TOPIC" >> "$LOG"
  exit 0
fi

# If no tex file, this script signals Claude Code to run the full protocol
PENDING_FILE="$VAULT/scripts/data/pending_analysis.txt"
cat > "$PENDING_FILE" <<EOF
TOPIC: $TOPIC
SLUG: $SLUG
TEX_FILE: $TEX_FILE
PDF_FILE: $PDF_FILE
PROTOCOL: $PROTOCOL
TIMESTAMP: $TIMESTAMP
STATUS: PENDING
EOF

echo ""
echo "========================================================"
echo "  QUESTION ANALYSIS REQUESTED"
echo "  Topic: $TOPIC"
echo "  Protocol: $PROTOCOL"
echo "  Claude Code will now:"
echo "    1. Read the source PDF slides (all pages)"
echo "    2. Extract all 2020-2024 past paper questions"
echo "    3. Update _Topics.md with sub-topics"
echo "    4. Update _TopicQuestionMap.md"
echo "    5. Generate LaTeX solutions (zero omissions)"
echo "    6. Compile PDF → ${SLUG}_Solutions.pdf"
echo "========================================================"
echo ""
echo "[$TIMESTAMP] Pending analysis created for: $TOPIC" >> "$LOG"

# Open protocol in case Claude is watching (Claude Code hook)
cat "$PROTOCOL"
