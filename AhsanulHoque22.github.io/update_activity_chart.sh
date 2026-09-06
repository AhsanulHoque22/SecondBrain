#!/usr/bin/env bash
# Refreshes the SERIES data in script.js's build-activity chart with real
# commit counts for the last 7 days. Not automatic (Livora's repo is
# private, so the chart can't safely live-fetch client-side) — run this
# manually before a deploy when you want the week's numbers current.
set -euo pipefail
cd "$(dirname "$0")"

VAULT_ROOT="$(git rev-parse --show-toplevel)"
LIVORA_REPO="AhsanulHoque22/Healthcare_WebApp"
PORTFOLIO_REPO="AhsanulHoque22/AhsanulHoque22.github.io"

livora=() secondbrain=() portfolio=()
for i in 6 5 4 3 2 1 0; do
  since=$(date -u -d "-$i days 00:00:00" +%Y-%m-%dT%H:%M:%SZ)
  until_=$(date -u -d "-$i days 23:59:59" +%Y-%m-%dT%H:%M:%SZ)

  livora+=("$(gh api -X GET "repos/$LIVORA_REPO/commits" -f since="$since" -f until="$until_" --jq 'length' 2>/dev/null || echo 0)")
  portfolio+=("$(gh api -X GET "repos/$PORTFOLIO_REPO/commits" -f since="$since" -f until="$until_" --jq 'length' 2>/dev/null || echo 0)")
  secondbrain+=("$(git -C "$VAULT_ROOT" log --since="$since" --until="$until_" --oneline -- . ':!AhsanulHoque22.github.io' | wc -l | tr -d ' ')")
done

join() { local IFS=', '; echo "$*"; }

python3 - "$(join "${livora[@]}")" "$(join "${secondbrain[@]}")" "$(join "${portfolio[@]}")" <<'EOF'
import re, sys, datetime
livora, secondbrain, portfolio = sys.argv[1:4]

today = datetime.date.today()
start = today - datetime.timedelta(days=6)
label = f"{start:%b %-d} - {today:%b %-d, %Y}"

with open('script.js') as f:
    content = f.read()

content = re.sub(
    r"commit counts \([^)]*\) pulled once",
    f"commit counts ({label}) pulled once",
    content, count=1,
)
content = re.sub(
    r"(\{ hex: '#c9a227', data: \[)[^\]]*(\] \},   /\* Livora \*/)",
    rf"\g<1>{livora}\g<2>", content, count=1,
)
content = re.sub(
    r"(\{ hex: '#57c2a8', data: \[)[^\]]*(\] \}, /\* Second Brain \*/)",
    rf"\g<1>{secondbrain}\g<2>", content, count=1,
)
content = re.sub(
    r"(\{ hex: '#c084e8', data: \[)[^\]]*(\] \}, /\* Portfolio \*/)",
    rf"\g<1>{portfolio}\g<2>", content, count=1,
)

with open('script.js', 'w') as f:
    f.write(content)

print(f"Updated: Livora=[{livora}] SecondBrain=[{secondbrain}] Portfolio=[{portfolio}]")
EOF
