# Session Protocol Checklist
> ⚠️ This file is the persistent source of truth for session protocols.
> Claude MUST read and execute this at the START of every session.
> Created: 2026-06-01

## 🔴 AT SESSION START (mandatory — do not skip)

### 1. Read Dashboard + Today's Log
- Read `00_Dashboard.md`
- Read `03_Daily_Logs/[TODAY].md`
- Read `scripts/data/carry_forward.json`

### 2. Compute Slippage
- Compare yesterday's planned vs. done
- If something slipped → re-plan (move to today/tomorrow, cut lowest-yield if overloaded)

### 3. Brief the User (3 lines)
- Where they stand
- Single most important thing right now
- First 90-minute block

### 4. Question Analysis (for every topic being studied today)
- Read `02_Courses/[active course]/_TopicQuestionMap.md`
- For each topic in today's blocks: link to specific past paper questions
- Tell the user exactly what the exam asks and what format the answer should take

### 5. Source PDF Study Guide (for each study block)
- Read the relevant PDF pages
- Give precise page numbers: what to STUDY, what to SKIP
- Link each topic to its past paper questions

---

## 🟡 BLOCK WORKFLOW (the full study cycle for each block)

### Phase 1 — Block Start: Study Guide Generation

**Trigger:** User says "starting block [N]" or "I'm starting block [N]"

**Execute:**
1. Read the relevant source PDF pages for that block
2. Read `_TopicQuestionMap.md` for the active course
3. Analyze page by page — identify what to STUDY vs what to SKIP
4. Generate a study guide with:
   - Precise page numbers for each topic
   - What's on each page and why it matters
   - Direct links to past paper questions (year + Q number + what they ask)
   - A timed study plan for the block (e.g. "p.46-48 BFS — 20 min")
   - SKIP list (pages to skip and why)
5. Format exactly like the reference study guide (tables + concise bullets)

### Phase 2 — Active Recall (after slides)

**Trigger:** User says "I finished the slides" or "give me active recall"

**Execute:**
1. Read the source pages that were studied
2. Read past paper questions for those topics from `_TopicQuestionMap.md`
3. Generate 5-8 active recall questions covering:
   - Key definitions (exam-style)
   - Algorithm tracing (show fringe at each step — highest yield)
   - Comparison questions (e.g. "Compare BFS vs DFS — completeness, optimality, time, space")
   - Proof/explanation questions (e.g. "Prove that A* with an admissible heuristic is optimal")
4. Send ALL questions at once, numbered
5. User hand-writes answers and uploads images to Telegram
6. Evaluate each answer when images arrive:
   - ✅ Correct — no action needed
   - ⚠️ Partial — note gap, give correct answer briefly
   - ❌ Wrong — record gap, give correct answer
7. After evaluation, ask confidence (1-5) on each weak topic
8. Record gaps: `python3 scripts/recall_gaps.py add COURSE "topic" "question missed" "Block N"`
9. Update `_Topics.md` confidence for topics tested

### Phase 3 — Past Paper Practice

**Trigger:** User says "ready for past papers" or after active recall complete

**Execute:**
1. Select relevant past paper questions from `_TopicQuestionMap.md`
2. User attempts under timed conditions
3. Grade and provide model answer for anything missed
4. Update `_Topics.md` confidence
5. Block is now COMPLETE ✅

---

## 🟡 AFTER EACH STUDY BLOCK / CALENDAR EVENT (mandatory)

### 1. Update `_Topics.md`
- Change status to ✅ for completed topics
- Write TODAY's date in 'Last Reviewed' column
- Write confidence in 'Conf' column (ask user if not provided)

### 2. Update Daily Log
- Tick completed items: `- [ ]` → `- [x]`
- Fill in completed topics section

### 3. Update Dashboard
- Update 'High-yield done' count
- Update confidence average

### 4. Git Commit
```
git add -A
git commit -m "study: [topic] done — conf [X]/5"
```

---

## 🔵 AT END OF SESSION / DAY (mandatory)

### 1. End-of-Day Log
- Fill 'End-of-day log' section in `03_Daily_Logs/[TODAY].md`
- Did, Topics completed, Confidence updates, Energy/focus, Blockers, Slippage reason, Tomorrow's #1 thing

### 2. Update `_Topics.md` for ALL completed topics
- Status, Last Reviewed, Next Recall, Confidence

### 3. Run Spaced Repetition
```bash
python3 scripts/spaced_rep.py
```

### 4. Create Tomorrow's Daily Log
- Copy template structure
- Carry forward incomplete tasks first
- Add next topics from `01_Master_Plan.md`
- Paste recall-due topics from `scripts/data/recall_due.md`

### 5. Recall Gaps Reminder
- Run: `python3 scripts/recall_gaps.py reminder`
- If there are unrevised gaps, send the reminder via Telegram
- Add unrevised gaps to tomorrow's Block 1 (highest priority)

### 6. Update Dashboard
- Update all counts and confidence averages

### 7. Git Commit
```
git add -A
git commit -m "log: [DATE] — [N] topics done, energy [X]/5"
```

---

## 🟢 DAILY ROUTINE RULES

1. **Google Calendar is the ONLY source of truth for daily plans.**
   - Never use the overnight rollover script for scheduling.
   - Always read Google Calendar events for today before presenting any plan.

2. **Exam season constraints:**
   - Livora: 2 hours/day max
   - Public speaking: 1 hour/day
   - Last 2 days before exam = that subject only

3. **Study technique enforcement:**
   - Past-papers first → identify patterns before studying
   - Active recall over re-reading
   - 80/20: high-yield topics front-loaded
   - Timed practice in last 2 days
