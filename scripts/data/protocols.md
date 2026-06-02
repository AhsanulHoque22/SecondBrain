# Full Protocol Reference
> Load this file only when a protocol is triggered — never on session start.
> Referenced from CLAUDE.md triggers.

---

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

Step 6 — Git commit: `git commit -m "log: checkin [event_title] — [pct]% complete"`

**When a non-study check-in reply arrives (is_study = false):**
- Reply is "yes", "no", or "skip"
- Record in `completion_history.json`: `{date, event_title, type, completed: true/false, timestamp}`
- If "no": ask "Want to reschedule this? Reply with a time or say 'drop it'."
- Clear `pending_checkin.json`. No git commit needed.

**Pattern detection (Sundays only, in overnight rollover):**
Read `completion_history.json`. Detect: blocks avg pct < 70%, time-of-day patterns, 3-day streaks, trend.
```
📈 *Weekly pattern report*
Best block: [time] — avg [X]%
Weakest block: [time] — avg [X]%
Recommendation: [one concrete change]
```

---

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

### Step 6 — Git commit
```bash
git add -A && git commit -m "log: [DATE] — [N] topics done, energy [X]/5"
```

### Step 7 — Confirm via Telegram
```
✅ *Log updated — [DATE]*
Topics done: [list]
Next recall due: [topics or "none"]
Tomorrow's Block 1: [topic]
Energy today: [N]/5
```

---

## QUIZ MODE PROTOCOL

Triggered by: "Quiz me on [topic]" / "Test me on [topic]"

1. Read `02_Courses/[active course]/_TopicQuestionMap.md` for questions on that topic.
2. Select 3–5 questions, easiest first.
3. Send the FIRST question only. Wait for the answer.
4. On answer: grade ✅/⚠️/❌, give correct answer if wrong/partial, ask "Confidence? (1–5)"
5. Send next question. Repeat until done.
6. Final summary: score X/Y, weakest point. Update `_Topics.md` confidence. Run `python3 scripts/spaced_rep.py`

Rules: one question at a time; exam-style format matching `_TopicQuestionMap.md`.

---

## BLOCK STUDY GUIDE PROTOCOL

Triggered by: "starting block [N]" / "I'm starting block [N]" / "ready for block [N]"

### Step 1 — Identify topics
- Read `01_Master_Plan.md` → find block's topics
- Read `02_Courses/[active course]/_Syllabus.md` → full topic list
- Read `02_Courses/[active course]/_TopicQuestionMap.md` → past paper links

### Step 2 — Read and analyze source PDFs
- Read relevant PDF pages for every topic in the block
- For EVERY page: STUDY or SKIP with one-line reason
- Flag: worked examples, algorithm traces, comparison tables — exam gold

### Step 3 — Generate the study guide (this exact format)
```
## Block [N] Study Guide — [Topic Names]

| Pages | What's there | Why study it |
|-------|-------------|--------------|
| p.X-Y | [content]   | [exam relevance + past paper link] |

SKIP: p.A-B, p.C-D — [reason]

Past paper questions:
| Topic | Questions | What they ask |
|-------|-----------|---------------|
| [topic] | 20XX Q[N] | [trace/compare/prove/define] |

Block [N] plan ([time range]):
1. [topic] — p.X-Y — [N] min
...
[After each algorithm: "close PDF and trace on paper"]
```

### Step 4 — Link to exact past paper questions
Tell the user the exact exam format expected (e.g. "Show the fringe as a sorted list at every step").

Rule: guide fits one screen — tables and bullets only.

---

## ACTIVE RECALL PROTOCOL

Triggered by: "I finished the slides" / "give me active recall" / "ready for recall questions"

### Step 1 — Generate question set
1. Read studied source pages (from the block study guide)
2. Read past paper questions from `_TopicQuestionMap.md`
3. Generate 5-8 questions covering:
   - Key definitions (exam-style phrasing)
   - Algorithm tracing — HIGHEST YIELD ("Show the fringe at every step")
   - Comparison questions ("Compare A vs B: completeness, optimality, time, space — table")
   - Proof/explanation ("Prove that [algorithm] is [property]")
4. Send ALL questions at once, numbered.

### Step 2 — Wait for handwritten answers (images via Telegram)

### Step 3 — Evaluate each answer
- ✅ Correct — no action
- ⚠️ Partial — "Almost. Missing: [correction]." Record gap.
- ❌ Wrong — "Not quite. Correct: [correction]." Record gap.
- For each ⚠️/❌: ask "Confidence on [topic]? (1–5)"

### Step 4 — Record gaps
```bash
python3 scripts/recall_gaps.py add [COURSE] "[topic]" "[question missed]" "Block [N]"
```

### Step 5 — Update confidence
- Update `_Topics.md` confidence for all tested topics
- Run `python3 scripts/spaced_rep.py`

### Step 6 — Summary
```
📝 *Active Recall Complete — Block [N]*
Score: [X]/[Y] correct
⚠️ Gaps recorded: [list]
Ready for past paper practice?
```

### Step 7 — Git commit
```bash
git add -A && git commit -m "study: active recall Block [N] — [X]/[Y] correct"
```

---

## RECALL GAPS TRACKING PROTOCOL

Data store: `scripts/data/recall_gaps.json`
Fields per gap: topic, course, source_block, date_identified, question_missed, revised (bool), revision_date

Adding a gap (after active recall):
```bash
python3 scripts/recall_gaps.py add COURSE "topic" "question missed" "Block N"
```

Marking revised — triggered by "revised [topic]" or "done revising [topic]":
```bash
python3 scripts/recall_gaps.py mark-revised COURSE "topic"
python3 scripts/spaced_rep.py recalled COURSE "topic" [confidence]
```

End-of-day reminder (part of 🔵 end-of-session):
```bash
python3 scripts/recall_gaps.py reminder
```
If unrevised gaps: send Telegram reminder + add to tomorrow's Block 1.
For gaps older than 2 days: escalate to Block 1 AND morning reminder.

Listing: `python3 scripts/recall_gaps.py list` / `list --today-only`

---

## CONFIDENCE UPDATE PROTOCOL

Triggered by: "Confidence on [topic]: [1-5]" / after any quiz

1. Find topic in `_Topics.md` (fuzzy match OK)
2. Update 'Conf' column
3. Run `python3 scripts/spaced_rep.py`
4. If confidence ≤ 2: add topic to tomorrow's Block 1
5. Confirm: "Updated confidence for [topic]: [N]/5"

Scale: 1=barely remember | 2=blank in exam | 3=explain but detail errors | 4=cold explain + past papers | 5=bulletproof

---

## OBSIDIAN WIKILINK PROTOCOL

Every markdown file must have ≥1 `[[wikilink]]`.

Navigation line (line 2, after title):
```
> [[00_Dashboard]] · [[relevant_file]] · [[another_relevant_file]]
```

Standard links by file type:
- Daily logs → `[[00_Dashboard]]` + `[[active course _Topics]]` + `[[01_Master_Plan]]`
- Course _Topics.md → `[[_Syllabus]]` + `[[_TopicQuestionMap]]` + `[[00_Dashboard]]`
- Course _Syllabus.md → `[[_Topics]]` + `[[_TopicQuestionMap]]`
- Any new topic note → link to course file + `[[_Topics]]`

Course wikilinks: AI=`[[02_Courses/CSE713_AI/_Topics|AI]]`, InfoSec=`[[02_Courses/CSE717_InfoSec/README|InfoSec]]`, Compiler=`[[02_Courses/CSE711_Compiler/README|Compiler]]`, Distributed=`[[02_Courses/CSE719_Distributed/README|Distributed]]`, Graphics=`[[02_Courses/CSE715_Graphics/README|Graphics]]`

In daily logs: always `[[link]]` every topic name to its course file.
