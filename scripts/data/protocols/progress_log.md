## PROGRESS LOG PROTOCOL

Triggered by: "Update my log: did X, energy N, blocker Y" / "I finished [topic]" / "Log: topics done = X"

### Step 1 — Parse the message
Extract: topics completed/skipped, energy (1–5), blockers, confidence ratings.

### Step 2 — Update today's daily log
In `03_Daily_Logs/[TODAY].md`, fill 'End-of-day log':
- Did / Topics completed / Confidence updates / Energy (N/5) / Blockers / Slippage reason / Tomorrow's #1 thing
- Tick completed items: `- [ ]` → `- [x]`

### Step 3 — Update _Topics.md
For every completed topic:
1. Status → ✅
2. Last Reviewed → TODAY (YYYY-MM-DD)
3. Next Recall → today + 2 days (first completion) or spaced-rep intervals
4. Conf column → given rating or leave blank

For in-progress topics: status → 📖

### Step 4 — Run spaced rep and build tomorrow's log
```bash
python3 scripts/spaced_rep.py
```
Create/update `03_Daily_Logs/[TOMORROW].md`:
1. Copy _Template.md structure
2. Planned blocks: carry-forward first → recall due → new master plan topics
3. '🔁 Recall due today': paste from `scripts/data/recall_due.md`
4. Max 7 study blocks. Cut lowest-yield if overloaded.
5. Leave 'End-of-day log' blank.

### Step 5 — Update Dashboard
- Update 'High-yield done' count + 'Confidence /5' average in `00_Dashboard.md`

### Step 6 — Update wiki_state.md
- Update topics table (status, confidence, next recall)
- Update carry-forward section
- Update recent pattern (last 3 days)

### Step 7 — Git commit
```bash
git add -A && git commit -m "log: [DATE] — [N] topics done, energy [X]/5"
```

### Step 8 — Confirm via Telegram
```
✅ *Log updated — [DATE]*
Topics done: [list]
Next recall due: [topics or "none"]
Tomorrow's Block 1: [topic]
Energy today: [N]/5
```
