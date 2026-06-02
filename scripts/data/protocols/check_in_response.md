## CHECK-IN RESPONSE PROTOCOL

A check-in is pending whenever `scripts/data/pending_checkin.json` is non-empty.

**Detect a check-in reply when:**
- `pending_checkin.json` exists and is non-empty
- AND the user's message is a short reply: a number (0–100), "yes", "no", "skip", or "done"

**When a study check-in reply arrives (is_study = true):**

Parse replies in ANY of these forms:
- `done` or `100` → 100% complete, no carry-forward
- `70%` or `70` → ~70% complete, estimate incomplete topics from session plan
- `done except A* search` → 100% complete but one named topic incomplete
- `done except A* search and past papers` → multiple named incomplete topics
- `only did agents` or `only did agents and search` → named completed topics, rest incomplete
- `70%, couldn't finish past papers` → percentage + named incomplete topic
- `couldn't do anything` or `0` → 0% complete

Priority order for determining incomplete topics:
1. Explicit topic names mentioned as incomplete — use EXACTLY as stated.
2. Explicit topic names mentioned as completed — mark everything else as incomplete.
3. Percentage only — estimate which topics from the END of the session plan were not reached.

Step 1 — Record completion:
- Extract pct (100/"done", 0/"couldn't do anything", explicit %, or estimate)
- Read `completion_history.json`
- Append: `{date, event_title, type: "study", pct_complete, incomplete_topics: [...], completed_topics: [...], timestamp}`
- Save `completion_history.json`

Step 2 — Update carry_forward.json:
- Read `scripts/data/carry_forward.json`
- For each incomplete topic add: `{"topic": "...", "source_date": "...", "source_event": "...", "remaining_pct": 100}`
- UPDATE existing entries (don't duplicate). Remove topics completed today.
- Save `carry_forward.json`

Step 3 — Adjust tomorrow's schedule if significantly behind:
If carry_forward topics > 2 OR 3rd day in a row with pct < 70%:
- Read tomorrow's daily log
- Reduce one non-study block by 30 min (priority: break > phone > girlfriend chat > exercise)
- Add carry-forward topics to earliest available study block
- Note: "⚠️ Schedule adjusted: reduced [block] by 30 min to accommodate carry-forward"

Step 4 — Send confirmation:
```
📊 *Logged: [event_title]*
Completion: [pct]%
[If < 100%]: Carrying forward: [topic list]
[If adjustment]: ⚡ Tomorrow's schedule adjusted — reduced [block] by 30 min
[If 100%]: 🎯 Full session complete.
```

Step 5 — Clear pending check-in: write `{}` to `scripts/data/pending_checkin.json`

Step 6 — Update wiki_state.md carry-forward section with new state.

Step 7 — Git commit: `git commit -m "log: checkin [event_title] — [pct]% complete"`

**When a non-study check-in reply arrives (is_study = false):**
- Reply is "yes", "no", or "skip"
- Record in `completion_history.json`: `{date, event_title, type, completed: true/false, timestamp}`
- If "no": ask "Want to reschedule this? Reply with a time or say 'drop it'."
- Clear `pending_checkin.json`. No git commit needed.
