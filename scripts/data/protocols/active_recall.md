## ACTIVE RECALL PROTOCOL

Triggered by: "I finished the slides" / "give me active recall" / "ready for recall questions"

### Step 1 — Generate question set
1. Read `02_Courses/[active course]/wiki/[topic-slug].md` (wiki page for studied topic)
2. Read past paper questions from `_TopicQuestionMap.md`
3. Generate 5–8 questions covering:
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

### Step 6 — Update wiki page weak spots
For any ❌/⚠️ gaps: add or update the "Weak spots / common mistakes" section of `wiki/[topic-slug].md`.

### Step 7 — Summary
```
📝 *Active Recall Complete — Block [N]*
Score: [X]/[Y] correct
⚠️ Gaps recorded: [list]
Ready for past paper practice?
```

### Step 8 — Git commit
```bash
git add -A && git commit -m "study: active recall Block [N] — [X]/[Y] correct"
```
