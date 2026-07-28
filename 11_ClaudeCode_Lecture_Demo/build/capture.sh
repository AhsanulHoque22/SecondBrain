#!/bin/bash
# Usage: capture.sh <step_script> <output_png> [hold_seconds]
SCRIPT="$1"
OUT="$2"
HOLD="${3:-5}"
konsole --fullscreen -e bash -c "bash '$SCRIPT'; sleep $HOLD" &
sleep 2.8
spectacle -b -n -o "$OUT"
echo "saved: $OUT"
