#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Get all repos and count commits per day across all of them
python3 << 'PYEOF'
import subprocess
from datetime import datetime, timedelta

# Get all repos
result = subprocess.run(['gh', 'repo', 'list', 'AhsanulHoque22', '--limit', '100', '--jq', '.[].name'], 
                       capture_output=True, text=True)
repos = [r.strip() for r in result.stdout.strip().split('\n') if r.strip()]

print(f"Found {len(repos)} repos, fetching 7-day commit counts...")

# Count commits per repo across 7 days
repo_totals = {}
for repo in repos:
    total = 0
    for i in range(6, -1, -1):
        since = (datetime.utcnow() - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        until_ = (datetime.utcnow() - timedelta(days=i)).replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + 'Z'
        
        try:
            result = subprocess.run(['gh', 'api', f'repos/AhsanulHoque22/{repo}/commits', 
                                   '-f', f'since={since}', '-f', f'until={until_}', '--jq', 'length'],
                                  capture_output=True, text=True, timeout=5)
            count = int(result.stdout.strip()) if result.stdout.strip() else 0
            total += count
        except:
            pass
    
    repo_totals[repo] = total

# Get top 10 repos by commits
top_repos = sorted(repo_totals.items(), key=lambda x: x[1], reverse=True)[:10]
top_repo_names = [r[0] for r in top_repos]

print(f"Top repos: {', '.join([f'{r[0]}({r[1]})' for r in top_repos])}")

# Now get daily breakdowns for top repos
colors = ['#c9a227', '#57c2a8', '#c084e8', '#7dd9f5', '#f59b4e', '#d67ba8', '#a8d957', '#f57b7b', '#8ba8f5', '#f5b8a8']
days_data = {repo: [] for repo in top_repo_names}

for i in range(6, -1, -1):
    since = (datetime.utcnow() - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    until_ = (datetime.utcnow() - timedelta(days=i)).replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + 'Z'
    
    for repo in top_repo_names:
        try:
            result = subprocess.run(['gh', 'api', f'repos/AhsanulHoque22/{repo}/commits',
                                   '-f', f'since={since}', '-f', f'until={until_}', '--jq', 'length'],
                                  capture_output=True, text=True, timeout=5)
            count = int(result.stdout.strip()) if result.stdout.strip() else 0
        except:
            count = 0
        days_data[repo].append(count)

# Build SERIES string
series_lines = []
for idx, repo in enumerate(top_repo_names):
    color = colors[idx % len(colors)]
    data_str = ', '.join(str(c) for c in days_data[repo])
    series_lines.append(f"    {{ hex: '{color}', data: [{data_str}] }},   /* {repo} */")

today = datetime.utcnow().date()
start = today - timedelta(days=6)
label = f"{start.strftime('%b %-d')} - {today.strftime('%b %-d, %Y')}"

# Read script.js and update
with open('script.js', 'r') as f:
    content = f.read()

import re
# Update date comment
content = re.sub(
    r"commit counts \([^)]*\) pulled once",
    f"commit counts ({label}) pulled once",
    content, count=1
)

# Update SERIES array
new_series = "const SERIES = [\n" + '\n'.join(series_lines) + "\n  ];"
content = re.sub(
    r"const SERIES = \[.*?\];",
    new_series,
    content,
    flags=re.DOTALL,
    count=1
)

with open('script.js', 'w') as f:
    f.write(content)

print(f"✓ Updated script.js with {len(top_repo_names)} repos ({label})")
PYEOF
