# Second Brain System — Full Build Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** A self-updating, AI-powered second brain that runs your exams, startup, and life in parallel — anchored to prayer times, driven by Claude Code, accessible from your phone via Telegram.

**Architecture:** Obsidian vault (local markdown) + Claude Code (AI brain) + Telegram bot (mobile agent) + Gmail MCP (Google Classroom ingestion) + NotebookLM (per-course AI notebooks) + Google Drive (cloud backup + sharing).

**Tech Stack:** Python 3.12, Claude Code CLI, Obsidian, NotebookLM (web), Telegram Bot API, Gmail MCP (already connected), Google Calendar MCP (already connected)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR SECOND BRAIN                            │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  Obsidian Vault  ~/Desktop/SecondBrain/                 │  │
│   │                                                          │  │
│   │  00_Dashboard.md      ← live status, always open        │  │
│   │  01_Master_Plan.md    ← exam season map                 │  │
│   │  02_Courses/          ← 6 courses, past papers, topics  │  │
│   │  03_Daily_Logs/       ← one file per day                │  │
│   │  04_Livora/           ← startup + competitions          │  │
│   │  05_Skills/           ← public speaking + daily growth  │  │
│   │  06_Relationships/    ← relationship goals              │  │
│   │  07_Daily_Routine/    ← prayer-anchored schedule        │  │
│   │  scripts/             ← all automation                  │  │
│   └──────────────────────────────┬──────────────────────────┘  │
│                                  │                              │
│   ┌──────────────────────────────▼──────────────────────────┐  │
│   │  Claude Code (AI Brain)                                  │  │
│   │  Reads CLAUDE.md → becomes your personal mentor         │  │
│   │  Runs scripts/ automation on schedule                   │  │
│   │  Updates Dashboard, Daily Logs, Topics in real-time     │  │
│   └──────────────────────────────┬──────────────────────────┘  │
│                                  │                              │
│   ┌──────────┬───────────────────┼──────────┬───────────────┐  │
│   │ Telegram │   Gmail MCP       │  Google  │  NotebookLM   │  │
│   │   Bot    │ (Classroom fetch) │ Calendar │  (web, manual │  │
│   │ (mobile  │                   │  MCP     │   per course) │  │
│   │  agent)  │                   │          │               │  │
│   └──────────┴───────────────────┴──────────┴───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 0 — Obsidian Setup (15 min, do once)

- [ ] **Step 1: Open SecondBrain as Obsidian Vault**
  ```
  In Obsidian → Open folder as vault → select ~/Desktop/SecondBrain
  ```
  Install these community plugins (Settings → Community Plugins):
  - **Dataview** — live tables from your markdown
  - **Calendar** — visual daily log navigation
  - **Templater** — auto-apply log templates

- [ ] **Step 2: Set Graph View filters**
  In Graph View settings, exclude: `scripts/`, `_PastPapers.md`, `_Template.md`

- [ ] **Step 3: Pin to taskbar**
  Keep Obsidian and terminal (Claude Code) side-by-side on screen.

- [ ] **Step 4: Run Claude Code from vault root**
  ```bash
  cd ~/Desktop/SecondBrain
  claude
  ```
  Claude Code now reads CLAUDE.md automatically and becomes your mentor every session.

---

## Phase 1 — Telegram Bot (1 hour, do today)

**What this gives you:** Message Claude Code from your phone 24/7. Assign it tasks while you sleep. Get morning briefings sent to you. The bot has full access to your SecondBrain vault.

- [ ] **Step 1: Create your Telegram bot**
  ```
  1. Open Telegram → search @BotFather
  2. Send: /newbot
  3. Name it: Ahsanul Brain Bot  (or any name)
  4. Username: ahsanul_brain_bot  (must end in 'bot')
  5. Copy the API token — looks like: 7234567890:AAF_abc123...
  ```

- [ ] **Step 2: Get your Telegram user ID**
  ```
  1. Open Telegram → search @userinfobot
  2. Send /start
  3. Copy the number it gives you (your user ID)
  ```

- [ ] **Step 3: Install the bot**
  ```bash
  pip3 install "git+https://github.com/RichardAtCT/claude-code-telegram@v1.3.0"
  ```

- [ ] **Step 4: Configure it**
  ```bash
  cd ~/Desktop/SecondBrain/scripts
  cp telegram_bot.env.example telegram_bot.env
  # Edit telegram_bot.env:
  # TELEGRAM_BOT_TOKEN=your_token_here
  # TELEGRAM_BOT_USERNAME=ahsanul_brain_bot
  # APPROVED_DIRECTORY=/home/ahsanul-hoque/Desktop/SecondBrain
  # ALLOWED_USERS=your_user_id_here
  ```

- [ ] **Step 5: Run the bot**
  ```bash
  bash ~/Desktop/SecondBrain/scripts/start_telegram_bot.sh
  ```
  Then message your bot on Telegram. It will respond with full Claude Code capabilities.

- [ ] **Step 6: Make it start on boot (optional)**
  ```bash
  bash ~/Desktop/SecondBrain/scripts/install_bot_service.sh
  ```

**What to message the bot:**
- `"What's my plan for today?"` — reads Dashboard + daily log
- `"I finished search algorithms. Mark it done."` — updates _Topics.md
- `"Build the login page for Livora while I sleep"` — assigns SaaS task
- `"Give me 5 practice questions on Bayes' theorem"` — instant quiz
- `"Update my daily log: I studied FOL for 90 mins, energy 4/5"` — logs progress

---

## Phase 2 — Gmail → Google Classroom Connector (30 min)

**What this gives you:** Automatically pulls all Google Classroom materials, deadlines, and announcements from your Gmail into the SecondBrain vault.

- [ ] **Step 1: Run the classroom fetcher (Gmail MCP is already connected)**
  ```bash
  cd ~/Desktop/SecondBrain
  python3 scripts/classroom_fetch.py
  ```
  This reads your Gmail for Google Classroom emails and creates structured notes in each course folder.

- [ ] **Step 2: Check the output**
  Each course folder gets a `_ClassroomNotes.md` file with all extracted materials.

- [ ] **Step 3: Schedule daily auto-fetch**
  The `morning_briefing.sh` script runs this automatically every morning.

---

## Phase 3 — NotebookLM Per-Course Setup (30 min)

**What NotebookLM gives you:** Upload all your PDFs + past papers → get an AI that answers questions ONLY from your course material. Generates study guides, practice questions, and audio overviews you can listen to while walking.

- [ ] **Step 1: Go to notebooklm.google.com**

- [ ] **Step 2: Create one notebook per course**
  ```
  Notebook 1: CSE 713 — Artificial Intelligence
  Notebook 2: CSE 717 — Information Security
  Notebook 3: CSE 711 — Compiler
  Notebook 4: CSE 719 — Distributed & Cloud
  Notebook 5: CSE 715 — Computer Graphics
  ```

- [ ] **Step 3: Upload sources per course (run this first to see what to upload)**
  ```bash
  python3 ~/Desktop/SecondBrain/scripts/notebooklm_prep.sh
  ```
  Output: per-course upload lists in each `02_Courses/*/NotebookLM_Sources.md`

- [ ] **Step 4: Upload to NotebookLM for the active course (AI now)**
  Upload to CSE 713 notebook:
  - All PDFs in `02_Courses/CSE713_AI/`
  - Paste the past paper images/text
  - Paste `_Syllabus.md` and `_PastPapers.md`

- [ ] **Step 5: Use NotebookLM for daily study**
  Prompts to use in NotebookLM:
  - `"Generate 10 exam-style questions on search algorithms"`
  - `"Explain A* search like I'm preparing for the exam"`
  - `"What are all the topics from the past papers that I haven't covered yet?"`
  - `"Create an audio overview of Bayesian networks"` → listen while eating/commuting

---

## Phase 4 — Google Drive Course Folders (1 hour, Day 2)

- [ ] **Step 1: Run the Drive setup script**
  ```bash
  python3 ~/Desktop/SecondBrain/scripts/create_drive_folders.py
  ```
  Creates this structure in your Google Drive:
  ```
  My Drive/
  └── CSE Exam Season 2026/
      ├── CSE713_AI/
      │   ├── Lecture Materials/
      │   ├── Past Papers/
      │   └── My Notes/
      ├── CSE717_InfoSec/
      ├── CSE711_Compiler/
      ├── CSE719_Distributed/
      ├── CSE715_Graphics/
      └── CSE700_Thesis/
  ```

- [ ] **Step 2: Upload your AI materials to Drive**
  Drag all PDFs from `02_Courses/CSE713_AI/` to Google Drive → shareable from anywhere.

---

## Phase 5 — Background Study Agent (Day 2, 30 min)

**What this gives you:** Claude Code wakes up every morning at 6 AM, reads your plan, checks what's overdue, updates the Dashboard, and sends you a Telegram message with today's briefing.

- [ ] **Step 1: Set up morning briefing cron**
  ```bash
  bash ~/Desktop/SecondBrain/scripts/setup_cron.sh
  ```
  This adds:
  - **6:00 AM daily** — morning briefing (Telegram message with today's plan)
  - **10:30 PM daily** — evening review prompt (reminds you to fill daily log)
  - **Every 2 days** — spaced repetition reminder (topics that need recall)

---

## Daily Routine Template (Prayer-Anchored)

> Adjust times to your actual prayer schedule. These are approximate for Chittagong, June 2026.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MORNING — Peak Focus Window
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
04:10  Fajr prayer (anchor)
04:30  📱 Check Telegram bot morning briefing
       Read: Today's #1 topic + yesterday's slippage
04:45  ━━ DEEP WORK BLOCK 1 (90 min) ━━
       Hardest topic of the day — your brain is freshest
       Method: Teach it, don't read it (Feynman)
06:15  Break: movement, water, breakfast (30 min)
06:45  ━━ DEEP WORK BLOCK 2 (90 min) ━━
       Second topic or practice problems from yesterday
08:15  Break (15 min)
08:30  ━━ DEEP WORK BLOCK 3 (60 min) ━━
       Past-paper practice / algorithm tracing
09:30  Personal time / chores / morning tasks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MIDDAY — Secondary Focus + Startup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12:00  Dhuhr prayer (anchor)
12:15  ━━ LIVORA BLOCK (2h MAX) ━━
       Startup SaaS work — use Telegram bot to assign
       overnight tasks so work continues while you sleep
       Competition prep goes here too
14:15  Light review / NotebookLM audio / reading notes
       (no heavy encoding — this is passive time)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AFTERNOON — Active Recall
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15:45  Asr prayer (anchor)
16:00  ━━ DEEP WORK BLOCK 4 (75 min) ━━
       Active recall of today's topics (close notes, explain)
       Spaced repetition: 10-min recall pass on day-2-ago topics
17:15  ━━ RELATIONSHIP BLOCK (30 min) ━━
       One quality connection: call/message family or close friend
       Not scrolling — intentional contact
17:45  Wind down, prepare for Maghrib

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENING — Skills + Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
18:45  Maghrib prayer (anchor)
19:00  ━━ PUBLIC SPEAKING BLOCK (60 min) ━━
       Record yourself explaining today's study topic out loud.
       This is TRIPLE-PURPOSE: speaking + Feynman recall + viva prep.
       Structure: 10 warm-up → 20 recorded talk → 20 review → 10 impromptu
20:00  Dinner / personal time

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIGHT — Consolidation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20:15  Isha prayer (anchor)
20:30  ━━ EVENING BLOCK (60 min) ━━
       Light active recall (no new content at night)
       Review revision sheets, not full notes
21:30  ━━ DAILY LOG + PLANNING (30 min) ━━
       Fill today's log: planned vs done, energy, blockers
       Tell Claude Code / Telegram bot: what you did today
       Claude updates Dashboard + rolls plan forward
       Assign overnight Livora tasks to Telegram bot
22:00  Sleep prep — phone away, no screens after this
22:30  SLEEP (target: 6 hours minimum, 7 ideal)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Study Techniques (in priority order)

### 1. Past-Paper First (ALWAYS)
Before learning a topic, look at how it was asked in 3 past papers. You're studying toward the question, not the textbook.

### 2. Active Recall (not re-reading)
After any topic: close everything. Write down everything you remember. Then check. The effort of retrieval is what builds memory. Re-reading feels good but does almost nothing.

### 3. Feynman Technique (for hard topics)
Explain the topic out loud like you're teaching a confused student. Where you stumble = what you don't actually know. Fix that gap specifically.

### 4. Spaced Repetition (built into the plan)
Every topic gets a 10-min recall pass every 2–3 days. Update `_Topics.md` status. The system reminds you.

### 5. Interleaving (Week 2+ per subject)
Don't do 3h of A* then 3h of Bayes. Mix topics within a session: 45 min search → 45 min Bayes → 45 min planning. Harder but builds deeper retrieval.

### 6. Timed Simulation (last 2 days only)
Simulate exam conditions exactly: 10:30 AM start, no phone, no notes, 4h. This trains your brain for the actual test.

### 7. NotebookLM Audio Override
Upload materials → generate "Audio Overview" → listen while eating, walking, showering. Passive encoding during dead time. 30 min/day of dead time covered = 3h extra per week.

---

## Learning Resources by Topic (AI — CSE 713)

| Topic | Best Free Resource |
|-------|-------------------|
| Search algorithms (A*, UCS) | 3Blue1Brown-style: CS50 AI Week 0 on YouTube |
| Alpha-Beta Pruning | Sebastian Lague "Algorithms Explained" on YouTube |
| Bayesian Networks | Khan Academy Probability + AIMA Chapter 13 PDF |
| FOL + Resolution | AIMA Chapter 7-9 (already have the PDF in vault) |
| STRIPS + Planning | AIMA Chapter 10 PDF |
| Neural Networks | 3Blue1Brown Neural Networks series (4 videos, 1h total) |
| CSP | CS50 AI Week 3 on YouTube |

AIMA = `Artificial_Intelligence_A_Modern_Approac.pdf` — already in your vault.

---

## NotebookLM Study Workflow (per course)

```
Upload sources → Generate Study Guide → Ask practice questions → Audio Overview

Upload:
  ├── Textbook chapters (AIMA chapters relevant to your topics)
  ├── All lecture PDFs in the course folder
  ├── Past papers (paste as text or upload scans)
  └── Your _Syllabus.md

Prompts that work:
  "Give me 15 exam-style questions from the 2024 paper topics"
  "Explain A* search step by step with the 2024 graph"
  "What are all the numerical problems I should practice?"
  "Create a 1-page cheat sheet for this course"
  "Generate an Audio Overview focusing on search algorithms"
```

---

## Livora / SaaS Parallel Strategy

**The constraint:** 2h/day during exams. Not negotiable. But these 2h can be highly leveraged.

### Using the Telegram Bot for Overnight SaaS Work
Every night at 21:30, assign tasks to your Telegram bot before sleeping:
```
"Tonight's Livora task: Build the user authentication flow for Livora. 
 Files to create: src/auth/login.py, src/auth/register.py.
 Follow the existing patterns in src/.
 Leave a summary in 04_Livora/SaaS_Build_Log.md when done."
```
Wake up to working code. Review in your morning 30-min personal time.

### The 2h Daily Livora Block Structure
```
00:00 - 00:15  Review what the bot built overnight (or yesterday's work)
00:15 - 00:30  Plan today's 2h: one concrete deliverable
00:30 - 01:30  Deep build (1 feature, 1 fix, 1 design decision)
01:30 - 02:00  Test + commit + assign tomorrow's overnight task to bot
```

### Competition Prep
Enter all competitions in `04_Livora/README.md` with dates immediately. Rule: if a competition is within 5 days of an exam, all prep must be front-loaded before that window.

---

## Relationship Quality Strategy

**The exam-season constraint:** you're heads-down, but isolation compounds stress. Budget 30 min/day for meaningful connection — this is not optional, it protects your mental performance.

### Daily (30 min, post-Asr)
- One intentional message or call (not scroll-reply): family member, close friend, or study partner
- Ask a real question. Listen. Don't multitask during it.

### Weekly (60 min, fits in a lighter Livora day)
- One deeper conversation: a friend you haven't properly talked to in a week
- Or: a collaborative study session (teaching someone = Feynman technique + relationship)

### Study accountability partner
- Find one person doing exam season too
- Daily 2-min check-in: "I'm doing ___ today. You?" 
- End of day: "Done / not done. Why."
- This turns isolation into shared momentum.

---

## Skill Development (Exam Season)

During exams, limit skill dev to what directly serves your goals:

| Skill | How | Time | ROI |
|-------|-----|------|-----|
| Public speaking | 1h/day post-Maghrib (already scheduled) | 7h/week | Thesis viva + startup pitches |
| AI/ML coding | Livora SaaS work teaches this naturally | In 2h Livora | Startup |
| Communication writing | Daily log + study notes | 0 extra | Everything |

**Do NOT add new skill tracks during exam season.** Public speaking is enough.

---

## The Weekly Engine (reuse for exams 2–5)

```
DAY 0 (Wed afternoon, post-exam):
  - 30 min: debrief the exam just done (what surprised you → learn it for viva)
  - 60 min: load next subject — syllabus, past papers, rank topics by yield
  - Ask Claude Code: "Analyze [course] past papers and give me the priority list"
  
DAY 1–4 (Thu–Sun): Core learning
  - Each day: 1–2 topics from the priority list
  - End each day with active recall + update _Topics.md
  
DAY 5 (Mon): First full past paper, timed
  - 10:30 AM start, exam conditions
  - Afternoon: identify weak areas
  
DAY 6 (Tue): Repair weak areas + revision
  - Focus ONLY on what the past paper exposed
  - Build 1-page cheat sheet (writing it = active recall)
  
DAY 7 (Wed 10:30 AM): EXAM
```

---

## Real-Time Plan Adjustment Protocol

When you log a failure or unexpected result, Claude Code immediately:
1. Re-reads `01_Master_Plan.md` and today's daily log
2. Identifies what slipped
3. Cuts the lowest-yield item to make room
4. Updates Dashboard, daily log, and Master Plan
5. Tells you the new next action in 3 lines

**Never guilt. Always next action.**

Trigger this anytime by saying (in Claude Code or Telegram):
```
"I didn't finish [topic] today. It's now 8 PM. What do I do?"
```

---

## How All the Tools Connect

```
MORNING FLOW:
  6 AM → cron → morning_briefing.sh → reads Dashboard + daily log
       → sends Telegram message: "Today's plan + yesterday's gap"

STUDY FLOW:
  You study → explain topic to Claude Code (Feynman test)
            → Claude asks you 3 questions
            → You answer → Claude marks topic ✅ or 🔁 in _Topics.md

EVENING FLOW:
  21:30 → You tell Telegram bot: "Done: [topics]. Energy: 4/5. Blocker: [X]"
        → Claude updates 03_Daily_Logs/today.md
        → Updates 00_Dashboard.md status board
        → Rolls tomorrow's plan
        → You assign overnight Livora task to bot

SLEEP FLOW:
  22:30 → You sleep
        → Telegram bot runs assigned SaaS tasks
        → Results in 04_Livora/SaaS_Build_Log.md when you wake up

SPACED REP FLOW:
  Every 2 days → cron → checks _Topics.md for 🔁 items
               → Sends Telegram: "10-min recall: search algorithms"
```

---

## Build Checklist (execute in order)

- [ ] **Phase 0 (15 min):** Open SecondBrain in Obsidian, install 3 plugins
- [ ] **Phase 1 (1 hour):** Set up Telegram bot → test with one message
- [ ] **Phase 2 (30 min):** Run classroom_fetch.py → review extracted notes
- [ ] **Phase 3 (30 min):** Set up NotebookLM notebook for AI, upload sources
- [ ] **Phase 4 (1 hour, Day 2):** Create Google Drive folder structure
- [ ] **Phase 5 (30 min, Day 2):** Set up morning briefing cron

**Total setup time: ~3.5 hours, spread across 2 days**
**After that: system runs itself. You just study.**
