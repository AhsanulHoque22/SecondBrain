# Question Analysis & Solution Protocol

**Trigger:** User says `"[Topic Name] question analysis and solution"` in terminal or Telegram.

**Scope:** Past papers 2020–2024 only.

---

## Steps to Execute

### Step 1 — Identify the Topic
- Match the topic name to an entry in `02_Courses/CSE713_AI/_Topics.md`
- Identify the source PDF (from the topic row's Notes or from `_Syllabus.md`)
- If a wiki page exists (`02_Courses/CSE713_AI/wiki/[topic].md`), use it — do NOT re-read the raw PDF

### Step 2 — Read the Source Slides (if no wiki page)
- Read the source PDF in chunks (max 20 pages per read, do all chunks in parallel)
- Extract all sub-topics, key definitions, algorithms, and examples

### Step 3 — Extract Past Paper Questions (2020–2024 only)
- Read `02_Courses/CSE713_AI/_TopicQuestionMap.md`
- Find ALL entries for this topic across 2020, 2021, 2022, 2023, 2024
- If the question map is incomplete for this topic, read the past papers PDF:
  - Pages 1–4: 2024
  - Pages 5–7: 2023
  - Pages 8–10: 2022
  - Pages 11–13: 2021
  - Pages 14–16: 2020
- Add any missing questions to `_TopicQuestionMap.md`

### Step 4 — Update _Topics.md
- Add any sub-topics found in the slides that are not already in `_Topics.md`
- Use the format: `| ↳ Sub-topic name | 🔲 | — | — | — | yield | notes |`

### Step 5 — Generate LaTeX Solutions
- Create `02_Courses/CSE713_AI/[TopicSlug]_Solutions.tex`
- Include EVERY question found in Step 3 — zero omissions
- Structure: one `\section{}` per year, `\subsection{}` per question part
- Use `qbox` (orange) for question text, `solbox` (blue) for solutions
- For math: use `\forall`, `\exists`, `\land`, `\lor`, `\neg`, `\rightarrow`, `\leftrightarrow`
- Include a Quick Summary section at the end with exam patterns

### Step 6 — Compile PDF
```bash
cd /home/ahsanul-hoque/Desktop/SecondBrain/02_Courses/CSE713_AI/
pdflatex -interaction=nonstopmode [TopicSlug]_Solutions.tex
pdflatex -interaction=nonstopmode [TopicSlug]_Solutions.tex  # run twice for TOC
```

### Step 7 — Wiki Ingest (if topic first reaches 📖 or ✅)
- Follow `wiki_ingest.md` protocol to create/update wiki page for this topic

### Step 8 — Git Commit
```bash
git add -A
git commit -m "study: [topic] question analysis + solutions PDF generated"
```

---

## Topic → Source PDF Mapping

| Topic | Source PDF |
|-------|-----------|
| FOL + Resolution + Inference | Propositional Logic.pdf |
| Forward + Backward Chaining + Rule-Based System | Rule-Based Systems.pdf |
| STRIPS + Partial-Order Planning | Planning.pdf, plan2.pdf |
| Bayes + Bayesian Networks | Reasoning with Uncertainty.pdf |
| Search Algorithms | Chapter 3.pdf, Chapter 4.pdf |
| Alpha-Beta Pruning + Minimax | Chapter 5.pdf |
| Neural Networks + Learning | original lecture note.pdf |
| CSP | 20_CSP.pdf |
| Fuzzy Logic | FuzzyLogic-14.pdf |
| Intelligent Agents | Ch01-02.pdf |

---

## Output File Naming Convention
`[TopicSlug]_Solutions.pdf` where TopicSlug is:
- `FOL_Resolution` → FOL + Resolution + Inference
- `Search` → Search Algorithms
- `AlphaBeta` → Alpha-Beta Pruning + Minimax
- `RuleBased` → Forward + Backward Chaining
- `Planning` → STRIPS + POP
- `BayesNet` → Bayes + Bayesian Networks
- `NeuralNet` → Neural Networks + Learning
- `CSP` → Constraint Satisfaction
- `FuzzyLogic` → Fuzzy Logic + Uncertainty
- `Agents` → Intelligent Agents
