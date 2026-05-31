# CSE 713 AI — 5-Day Study Plan (June 1–5, 2026)
## Exam: Wednesday June 10, 2026 at 10:30 AM · 54 marks · 4 hours

> **Exam format:** Answer any 3 from Section A + any 3 from Section B = 6 questions × 9 marks = 54.
> **Your 6 guaranteed wins:** Agents, Search, Alpha-Beta, FOL+Resolution, STRIPS+Planning, Bayes+BN.
> For past paper question numbers → open `_TopicQuestionMap.md`.

---

## Study Strategy

| Principle | How it's built into this plan |
|-----------|-------------------------------|
| **Past Papers After Every Topic** | Immediately after finishing a topic, you solve that topic's exam questions |
| **Active Recall** | Every study block ends with you explaining the concept aloud with notes closed |
| **Spaced Repetition** | Day 2 revisits Day 1 topics. Day 3 revisits Days 1–2. Day 4 revisits Days 2–3. Day 5 = full sweep |
| **Interleaving** | Each day mixes 2 different topics so your brain stays alert and distinguishes between them |
| **End-of-Day Brain Dump** | Every night's final block: blank page, write everything from memory, check gaps |
| **Timed Practice** | Afternoon blocks simulate exam pressure with actual past paper questions |

---

## Daily Template (same structure every day)

```
04:45  Wake up
04:45–05:00  Fajr prayer (15 min)
05:00–05:10  Morning prep — water, set up desk
05:10–06:40  Study Block 1 (90 min)          ← deep focus, most important
06:40–06:50  Phone scrolling / break (10 min)
06:50–07:20  Past paper practice — Topic 1 (30 min)
07:20–07:30  Short break (10 min)
07:30–09:00  Study Block 2 (90 min)
09:00–09:10  Break (10 min)
09:10–10:00  Study Block 3 (50 min)
10:00–10:30  Breakfast (30 min)
10:30–11:00  Past paper practice — Topic 2 (30 min)
11:00–11:25  Exercise — 25 min (warm-up 5 + light cardio 15 + cool-down 5)
11:25–11:55  Public speaking in English (30 min)
11:55–12:00  Break
12:00–13:00  Study Block 4 (60 min)           ← deeper consolidation / second topic
13:00–13:30  Girlfriend chat Part 1 (30 min)
13:30–13:45  Dhuhr prayer (15 min)
13:45–14:00  Phone scrolling (15 min)
14:00–14:30  Lunch (30 min)
14:30–16:30  Study Block 5 (120 min)          ← past paper deep practice, timed
16:30–17:00  Girlfriend chat Part 2 (30 min)
17:00–17:30  Break / phone scrolling (30 min)
17:30–17:45  Asr prayer (15 min)
17:45–18:30  Study Block 6 (45 min)           ← consolidation / spaced repetition
18:30–18:45  Phone scrolling / break (15 min)
18:45–19:00  Maghrib prayer (15 min)
19:00–19:30  Girlfriend chat Part 3 (30 min)
19:30–20:00  Dinner (30 min)
20:00–20:30  Study Block 7 — End-of-day review (30 min)
20:30–20:45  Isha prayer (15 min)
20:45–21:15  Girlfriend chat Part 4 (30 min)
21:15–21:30  Wind down — no screens, light stretch
21:30–21:45  Relax (no phone)
21:45        Sleep  →  wake 04:45 (7 hours)
```

**Total study per day: ~9 hours 5 minutes**
**Girlfriend chat total: 2 hours ✓**
**Exercise: 25 min (build stamina gradually — add 5 min every 2 days if energy allows)**
**Public speaking: 30 min ✓**

---

## Post-5-Day Revision Schedule (June 6–10)

| Date | Plan |
|------|------|
| June 6 (Sat) | Revise: Agents + Search + Alpha-Beta. Solve 2020 Section A under timed conditions |
| June 7 (Sun) | Revise: FC/BC + FOL + STRIPS + Bayes + Neural Networks |
| June 8 (Mon) | **PURE REVISION ONLY** — Timed past paper: 2021 full paper. No new content |
| June 9 (Tue) | **PURE REVISION ONLY** — Timed past paper: 2022 full paper. No new content |
| June 10 (Wed) | Light review of your revision sheets 7:00–10:00 AM. 10:30 AM: EXAM |

---

---

## DAY 1 — Monday June 1
### Topics: Intelligent Agents + Search Algorithms (Uninformed + Informed)
### Exam yield: ⭐⭐⭐ + ⭐⭐⭐

---

**05:10–06:40 · Study Block 1 — Intelligent Agents (90 min)**

Source: `Ch01-02.pdf`

Study in this order (close notes after each point and test yourself):
1. The 4 approaches to AI: think rationally, act rationally, think like human, act like human
2. Turing Test — what it measures, why LLMs pass some aspects but fail others
3. Intelligent agent definition — percepts, actions, goals, environment (PAGE model)
4. Environment types — fully/partially observable, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous, single/multi-agent
5. Agent architectures — simple reflex, model-based reflex, goal-based, utility-based, learning agent
6. Real-world examples — Mars Rover (Curiosity/Perseverance), Agricultural Robot in Bangladesh

Active recall check at 6:30 AM (10 min, notes closed):
- Name all 5 agent architectures
- Classify Mars Rover using PAGE
- What environment type is chess? (deterministic, fully observable, static, discrete, multi-agent)

---

**06:50–07:20 · Past Paper Practice — Agents (30 min)**

Open `AI Previous Year Questions(2024-2016).pdf`.
→ See `_TopicQuestionMap.md` → Topic: Intelligent Agents

Attempt in this order (10 min each for 3 questions, then check):
1. **2024: A-Q1** (p.1) — PAGE model, environment classification
2. **2022: A-Q1** (p.8) — Agent types, environment types
3. **2020: A-Q1** (p.14) — AI + agents, scenario application

After attempting: check your answers against your notes. Mark gaps with a red pen — those gaps are your targets.

---

**07:30–09:00 · Study Block 2 — Uninformed Search (90 min)**

Source: `Chapter 3.pdf`

1. State space representation: initial state, goal test, operators/actions, path cost
2. Problem formulations — work through each one explicitly:
   - Water Jug Problem
   - Missionaries & Cannibals
   - Robot Vacuum
   - TSP (brief)
3. BFS — trace on a sample graph. Show the fringe (frontier) at every step.
4. DFS — trace same graph. Show what gets popped and what gets expanded.
5. UCS (Uniform Cost Search) — trace on a weighted graph. Sort frontier by cumulative cost g(n).
6. IDDFS (Iterative Deepening DFS) — trace depth=1, depth=2, depth=3. Why it combines DFS space efficiency with BFS completeness.

Mentor tip: The exam always gives you a specific graph with labelled step costs. Practice showing the fringe as a sorted list at each expansion. That is what earns marks.

---

**09:10–10:00 · Study Block 3 — Informed Search (50 min)**

Source: `Chapter 4.pdf` (first section only — stop before local search)

1. Greedy Best-First Search — uses h(n) only. Fast but incomplete (can miss optimal).
2. A* Search — f(n) = g(n) + h(n). Combines path cost + heuristic.
   - g(n) = cost from start to n
   - h(n) = estimated cost from n to goal
   - f(n) = total estimated cost
3. Admissibility of heuristics — a heuristic is admissible if h(n) ≤ h*(n) (never overestimates)
4. The key exam graph — memorise or practice: A→G directed graph with step costs AND h(n) table at each node. This exact graph appears in 2020, 2022, 2023, 2024.

---

**10:30–11:00 · Past Paper Practice — Search (30 min)**

→ See `_TopicQuestionMap.md` → Topic: Search Algorithms

1. **2024: A-Q2** (p.2) — Trace UCS / Greedy / A* (show fringe at each step)
2. **2023: A-Q2** (p.5) — A* / UCS / IDDFS trace

Technique: For each search, draw the fringe as a list in the margin. Expand the best node. Cross off expanded nodes. This is what full marks looks like.

---

**11:00–11:25 · Exercise**

5 min walk + 15 min light cardio (jogging in place, jumping jacks, or yoga sun salutations) + 5 min stretching.
Your brain consolidates learning during movement — this is not wasted time.

---

**11:25–11:55 · Public Speaking in English (30 min)**

Today's topic: Explain A* Search aloud as if teaching a classmate.
- Start with the problem: "We have a graph where each edge has a cost..."
- Explain f(n) = g(n) + h(n) in plain words
- Walk through one example step by step in English
- Time yourself. Aim for clear, confident sentences. Don't translate in your head — think in English.

---

**12:00–13:00 · Study Block 4 — A* Deep Practice + Problem Formulations (60 min)**

1. Trace A* on a fresh graph (different from the one in the slides) — create your own
2. Revisit the key exam graph with h(n) table from the slides — trace UCS, Greedy, A* all three
3. Active recall: explain the difference between UCS and A* in one sentence
4. Review all problem formulations: Water Jug, Missionaries, Robot Vacuum — what are the states, operators, goal tests?

---

**14:30–16:30 · Study Block 5 — Full Search Past Paper Practice (120 min)**

This is your simulation block. Set a timer. Treat each question like it is the actual exam.

1. **2021: A-Q2** (p.11) — 30 min, timed
2. **2020: A-Q2** (p.14) — 30 min, timed
3. **2021: A-Q1 + 2023: A-Q1** — Agents questions (30 min)
4. **2024: A-Q1** — Agents hardest variant (20 min)
5. Review all attempts. What did you miss? Rewrite the missed parts cleanly (10 min)

---

**17:45–18:30 · Study Block 6 — Active Recall + Spaced Repetition (45 min)**

Close all notes. Blank page. Write down:
- All 5 agent architectures with a one-line definition each
- All 4 uninformed search algorithms with time and space complexity
- The A* formula and what each variable means
- One problem formulation from memory (your choice)

Then open notes and check. Red-circle any gap. That gap is tomorrow morning's first task.

---

**20:00–20:30 · Study Block 7 — Day 1 Comprehensive Review (30 min)**

Do a mental walk-through of everything studied today:
1. Agents: can you name all environment types without looking?
2. Search: can you trace UCS on a 5-node graph without notes?
3. A*: can you write the f(n) formula and explain admissibility?

Write 5 flashcard questions on a piece of paper (not phone) for spaced repetition tomorrow:
- "What is the difference between BFS and UCS?"
- "Define admissible heuristic"
- "Name all 5 agent architectures"
- "What does PAGE stand for?"
- "When does A* guarantee an optimal solution?"

---

---

## DAY 2 — Tuesday June 2
### Topics: Minimax + Alpha-Beta Pruning + Hill Climbing + Simulated Annealing
### Exam yield: ⭐⭐⭐ + ⭐⭐

---

**05:00–05:10 · Morning — Day 1 Gap Recall (before Block 1)**

Look at yesterday's red-circled gaps (from Block 6 last night). Fix them first. 10 minutes max.

---

**05:10–06:40 · Study Block 1 — Minimax Algorithm (90 min)**

Source: `Chapter 5.pdf`

1. Game tree concept: two players, MAX (you) and MIN (opponent)
2. Minimax algorithm: at MAX nodes → pick the child with highest value. At MIN nodes → pick child with lowest value.
3. Terminal nodes have utility values (given in the problem)
4. Trace a 3-level game tree step by step:
   - Level 0: MAX node (root)
   - Level 1: MIN nodes
   - Level 2: MAX nodes
   - Level 3: terminal nodes (leaf values)
5. Propagate values bottom-up

Limitations of pure Minimax:
- Exponential time: O(b^m) where b = branching factor, m = depth
- For chess: b≈35, m≈100 → completely infeasible

---

**06:50–07:20 · Past Paper Practice — Minimax (30 min)**

→ See `_TopicQuestionMap.md` → Topic: Alpha-Beta Pruning

1. **2020: A-Q3** (p.14) — trace game tree, show values at each node
2. **2021: A-Q3** (p.11) — full Minimax trace

Do not skip writing the α and β values. You will lose marks if you only show the final answer without showing the propagation.

---

**07:30–09:00 · Study Block 2 — Alpha-Beta Pruning (90 min)**

Source: `Chapter 5.pdf`

1. Core idea: avoid exploring branches that cannot change the final decision
2. Track α at MAX nodes (MAX's best so far on this path) and β at MIN nodes (MIN's best so far)
3. **α-cutoff:** at a MIN node, if the value found ≤ α of the parent MAX node → prune (don't explore more children of this MIN node)
4. **β-cutoff:** at a MAX node, if the value found ≥ β of the parent MIN node → prune
5. Apply to the SAME game tree from Block 1 — show which branches get pruned and why

Key invariant to memorise:
- α starts at -∞, β starts at +∞
- α increases (MAX pushes it up), β decreases (MIN pushes it down)
- Prune when α ≥ β

Additional concepts:
- Futility cutoff: if a node's value is so poor that no further improvement is possible
- Quiescence search: don't cut off at positions with large swings in evaluation (wait for stable position)

---

**09:10–10:00 · Study Block 3 — Alpha-Beta Practice Problems (50 min)**

Take the game tree from the 2022 or 2023 exam paper. Solve it completely:
1. Assign leaf values
2. Apply Minimax (write values at every node)
3. Apply Alpha-Beta (show α, β at every node, cross out pruned branches)

Repeat with a fresh tree you draw yourself (4 leaves, 2-level tree). Can you apply Alpha-Beta without looking at notes?

---

**10:30–11:00 · Past Paper Practice — Alpha-Beta (30 min)**

→ `_TopicQuestionMap.md` → Topic: Alpha-Beta Pruning

1. **2022: A-Q3** (p.8) — full Alpha-Beta with pruning
2. **2023: A-Q3** (p.5) — Minimax + Alpha-Beta

---

**11:00–11:25 · Exercise**

Same as Day 1. Today: try to go slightly longer on the cardio section if energy allows.

---

**11:25–11:55 · Public Speaking in English (30 min)**

Today's topic: Explain Alpha-Beta pruning aloud.
- "Alpha-Beta pruning is an optimisation of Minimax..."
- Walk through why a branch gets pruned — explain the α/β logic in plain English
- Then explain what Hill Climbing is (preview of afternoon content)

---

**12:00–13:00 · Study Block 4 — Hill Climbing + Simulated Annealing (60 min)**

Source: `Chapter 4.pdf` (Local Search section)

**Hill Climbing:**
1. Start at a random state
2. Move to the best neighbouring state if it is better than current
3. Stop when no better neighbour exists

**3 problems with Hill Climbing:**
1. **Local maxima** — stuck at a peak that is not the global peak
2. **Plateaux** — flat region with no clear direction of improvement
3. **Ridges** — narrow peak that search cannot navigate correctly

**Simulated Annealing (SA):**
1. Like HC, but sometimes accepts worse moves with probability e^(ΔE/T)
2. T = temperature (starts high → decreases over time)
3. At high T: many random moves (explores widely)
4. At low T: mostly greedy (like HC, but near the global optimum)
5. SA solves all 3 HC problems via probabilistic acceptance of worse states

Application: drone route optimisation (2024 paper), robot navigation (2023 paper)

---

**14:30–16:30 · Study Block 5 — Full Game Tree + HC/SA Past Papers (120 min)**

Part 1 (60 min): Alpha-Beta deep practice
- **2024: A-Q3** (p.2) — timed 30 min, then check
- **2021: A-Q3** (p.11) — timed 30 min, then check

Part 2 (40 min): Hill Climbing + SA questions
- **2023: A-Q4** (p.7) — HC limitations + SA + drone application
- **2024: A-Q4** (p.3) — HC + SA + short notes on Fuzzy/CSP

Part 3 (20 min): Active recall
- Draw a game tree from memory and apply both Minimax and Alpha-Beta without looking at notes

---

**17:45–18:30 · Study Block 6 — Spaced Repetition: Day 1 Topics (45 min)**

Review your Day 1 flashcard questions. Answer each one aloud.
- Agent architectures? (name and define all 5)
- A* formula? (write it and trace UCS vs A* in one sentence)
- What is PAGE?
- What is admissible heuristic?

Then answer these new questions from Day 2:
- What are the 3 problems with Hill Climbing?
- What does α represent? What does β represent?
- When do you prune in Alpha-Beta?

---

**20:00–20:30 · Study Block 7 — Days 1+2 Comprehensive Review (30 min)**

Blank page. Write everything you know about today's two topics (Alpha-Beta, HC/SA) without notes.
Compare against notes. Red-circle gaps. Set 5 new flashcard questions for Day 3 morning.

---

---

## DAY 3 — Wednesday June 3
### Topics: Forward/Backward Chaining + Rule-Based Systems + CSP
### Exam yield: ⭐⭐⭐ + ⭐

---

**05:00–05:10 · Morning — Day 1+2 Gap Recall**

Answer all 10 flashcard questions from Days 1+2. 1 minute per question. Mark any failures.

---

**05:10–06:40 · Study Block 1 — Rule-Based Systems + Forward Chaining (90 min)**

Source: `Rule-Based Systems.pdf`

**Architecture of a rule-based expert system:**
- Rule base (IF-THEN rules)
- Working memory / database (known facts)
- Inference engine (applies rules to facts)

**The R1–R5 Rule Base — MEMORISE THIS. It appears verbatim every year.**
```
R1: IF A and C  THEN E
R2: IF C and D  THEN F
R3: IF B and E  THEN F
R4: IF B        THEN C
R5: IF F        THEN G

Initial facts: A = TRUE, B = TRUE
Goal: Prove G
```

**Forward Chaining (FC) — data-driven:**
Start from facts, fire rules, derive new facts, repeat until goal is reached.

FC trace for R1–R5:
1. Facts: {A, B}
2. R4 fires (B is true) → add C. Facts: {A, B, C}
3. R1 fires (A and C are true) → add E. Facts: {A, B, C, E}
4. R3 fires (B and E are true) → add F. Facts: {A, B, C, E, F}
5. R5 fires (F is true) → add G. Facts: {A, B, C, E, F, G}
6. G is proved. DONE.

**Conflict resolution:** When multiple rules can fire at the same time (conflict set), use one of these strategies:
1. Fire the most specific rule (fewest matching conditions)
2. Fire the most recently added rule (recency)

---

**06:50–07:20 · Past Paper Practice — FC (30 min)**

→ `_TopicQuestionMap.md` → Topic: FC/BC + Rule-Based

1. Draw the FC propagation tree for R1–R5 from memory (no notes)
2. Check against the trace above
3. **2020: A-Q4** (p.15) — FC/BC with R1–R5, full answer

---

**07:30–09:00 · Study Block 2 — Backward Chaining Algorithm (90 min)**

Source: `Rule-Based Systems.pdf`

**Backward Chaining (BC) — goal-driven:**
Start from goal, find rules that can prove it, work backwards to find facts needed.

BC trace for R1–R5 (Goal: G):
1. To prove G → need R5 → need F
2. To prove F → try R2 (need C and D) or R3 (need B and E)
3. D is not in facts. R2 fails.
4. Try R3: need B and E. B is in facts. Need E.
5. To prove E → R1 → need A and C. A is in facts. Need C.
6. To prove C → R4 → need B. B is in facts. C proved.
7. E proved. F proved. G proved. DONE.

Draw this as a backtrack tree (AND-OR tree):
- OR nodes: alternative rules to prove a goal
- AND nodes: all conditions of a rule must be met

**When to use FC vs BC:**
- Use FC when: you have facts and want to see what can be derived; many possible goals
- Use BC when: you have a specific goal and want to check if it follows from facts; few goals, many rules

---

**09:10–10:00 · Study Block 3 — BC Problems + Factors (50 min)**

1. Draw BC tree for R1–R5 from memory — full diagram with AND/OR structure
2. Compare FC tree vs BC tree side by side
3. Factors determining which to use: number of rules, number of goals, known facts, system type

Mentor tip: In the exam, you will always be given R1–R5 or a very similar rule set. You will draw both trees. The trees are the answer — no need to explain the algorithm in prose.

---

**10:30–11:00 · Past Paper Practice — FC/BC (30 min)**

1. **2021: A-Q4** (p.12) — FC/BC with R1–R5, conflict resolution
2. **2022: A-Q4** (p.9) — FC/BC trees

Attempt both. Then check: did you draw the tree correctly? Are all nodes labelled?

---

**11:00–11:25 · Exercise**

Day 3 exercise: if energy is better, try 5 min walk + 20 min cardio. You are building stamina.

---

**11:25–11:55 · Public Speaking in English (30 min)**

Today's topic: Explain the difference between Forward and Backward Chaining in English.
Then record yourself on your phone for 1 minute. Listen back. Was it clear?

---

**12:00–13:00 · Study Block 4 — CSP: Constraint Satisfaction Problems (60 min)**

Source: `20_CSP.pdf`

This is a lower-yield topic (Tier 2) — learn it for short notes and bonus questions.

1. Definition: Variables + Domains + Constraints
   - Variables: the things to assign values to
   - Domain: set of possible values for each variable
   - Constraint: restriction on allowed combinations

2. Map Coloring problem:
   - Variables: regions (WA, NT, Q, NSW, V, SA, T)
   - Domain: {red, green, blue}
   - Constraints: adjacent regions cannot share the same color

3. Cryptarithmetic: SEND + MORE = MONEY
   - Each letter is a unique digit (0–9)
   - This is a classic CSP — all you need to know is the problem setup and that it's solved by constraint propagation + backtracking

4. Constraint propagation: eliminate values from domains using constraints before searching
5. Backtracking: assign a value, check constraints, backtrack if violated

---

**14:30–16:30 · Study Block 5 — FC/BC Deep Practice + Timed Past Papers (120 min)**

Part 1 (60 min): Draw FC and BC trees for R1–R5 completely from memory — timed 20 min each
- FC tree: 20 min
- BC tree: 20 min
- Check against your notes: 10 min, mark errors, redraw the wrong part

Part 2 (40 min): Past papers timed
- **2020: A-Q4** (p.15) — full answer, 20 min
- **2022: A-Q4** (p.9) — full answer, 20 min

Part 3 (20 min): Spaced repetition
- Revisit Day 1 and Day 2 weakest topics from your red-circled gaps

---

**17:45–18:30 · Study Block 6 — Spaced Repetition: Days 1+2 (45 min)**

Quick-fire questions (1 min each):
- Trace UCS on a 4-node graph from memory
- What are the α-cutoff and β-cutoff conditions in Alpha-Beta?
- What is the HC plateau problem and how does SA solve it?
- Name all 5 agent architectures
- Draw the A* formula and explain each variable

Then add: what is FC? What is BC? When do you use which?

---

**20:00–20:30 · Study Block 7 — Day 1-3 Comprehensive Review (30 min)**

Blank page. From memory, in any order:
- R1-R5 rule base (write out all 5 rules and initial facts)
- FC path (which rules fire in order)
- BC tree (which goals does BC explore)
- One Alpha-Beta cutoff rule
- One search algorithm trace

Set 5 new flashcard questions for tomorrow morning.

---

---

## DAY 4 — Thursday June 4
### Topics: FOL + Resolution + STRIPS + Partial-Order Planning
### Exam yield: ⭐⭐⭐ + ⭐⭐⭐ — HEAVIEST DAY

---

**05:00–05:10 · Morning — Days 1-3 Gap Recall**

Answer all flashcard questions from Days 1-3. Maximum 10 minutes.

---

**05:10–06:40 · Study Block 1 — Propositional Logic Limitations → FOL (90 min)**

Source: `Propositional Logic.pdf` (pp. 1–50)

**Why FOL?** (this is the most common exam opener)

Propositional Logic (PL) limitation: PL can only express facts about specific, named things.
- PL: you need a separate proposition for "Dog1 is faithful", "Dog2 is faithful", "Dog3 is faithful"...
- For infinite or large domains this is impossible
- FOL adds variables, predicates, and quantifiers to express general statements

**First-Order Logic / Predicate Logic:**
- "All men are mortal" → ∀x: Man(x) → Mortal(x)
- "Some birds can't fly" → ∃x: Bird(x) ∧ ¬CanFly(x)
- "Socrates is a man" → Man(Socrates)

**FOL components:**
- Constants: specific named objects (Socrates, Tom, Marcus)
- Variables: x, y, z — range over objects in the domain
- Predicates: properties and relations (Man(x), Loves(x,y))
- Quantifiers: ∀ (for all), ∃ (there exists)
- Connectives: ∧, ∨, ¬, →
- Well-Formed Formulas (WFF): syntactically valid FOL sentences

**Inference rules:**
- Universal Elimination: from ∀x P(x) and constant c → P(c)
- Modus Ponens: from P and P→Q → Q
- Resolution: see Block 2

---

**06:50–07:20 · Past Paper Practice — FOL Sentences (30 min)**

Practice converting English sentences to FOL:
1. "All Pompeians were Romans" → ∀x: Pompeian(x) → Roman(x)
2. "Marcus was born in 40 AD" → BornIn(Marcus, 40AD)
3. "No Pompeian survived the volcano" → ∀x: Pompeian(x) → DiedIn79(x)
4. Write your own 3 sentences in English, convert to FOL, then back to English

Also attempt: **2024: B-Q5** (p.4) — skim only (don't solve yet, just understand the problem structure)

---

**07:30–09:00 · Study Block 2 — Resolution + Clausal Form (90 min)**

Source: `Propositional Logic.pdf` (pp. 50-104)

**4-Step Algorithm: Convert any formula to Clausal Form (CNF)**

Step 1: Eliminate implication signs
- P→Q becomes ¬P ∨ Q

Step 2: Eliminate double negation; move ¬ inward using De Morgan's laws
- ¬(P ∧ Q) becomes ¬P ∨ ¬Q
- ¬(P ∨ Q) becomes ¬P ∧ ¬Q
- ¬¬P becomes P

Step 3: Convert to Conjunctive Normal Form (CNF) using distributive law
- (P ∨ (Q ∧ R)) becomes (P ∨ Q) ∧ (P ∨ R)

Step 4: Extract the set of clauses
- Each conjunct becomes a separate clause
- A clause is a disjunction of literals

**Resolution Principle:**
Given two clauses containing complementary literals:
- (x ∨ s1) AND (¬x ∨ s2) → resolvent = (s1 ∨ s2)
- x is the "resolved-upon" literal

Example:
- (A ∨ B) AND (¬A ∨ C) → (B ∨ C)

**Proof by Refutation (5-step procedure):**
1. Convert all premises to clausal form
2. Negate the goal; convert to clausal form
3. Combine all clauses into a set
4. Iteratively apply resolution, adding resolvents to the set
5. If □ (null/empty clause) is derived → contradiction → original goal is TRUE (proved)

---

**09:10–10:00 · Study Block 3 — Marcus/Pompeii Proof (50 min)**

**THE MARCUS/POMPEII PROBLEM — memorise this entire proof:**

Given:
1. Marcus was a man → Man(Marcus)
2. Marcus was a Pompeian → Pompeian(Marcus)
3. Marcus was born in 40 AD → Born(Marcus, 40AD)
4. All Pompeians died in the eruption of 79 AD → ∀x: Pompeian(x) → Died(x, 79AD)
5. No mortal lives more than 150 years → ∀x∀t: Mortal(x) ∧ Born(x,t) ∧ (Now-t > 150) → ¬Alive(x)
6. All men are mortal → ∀x: Man(x) → Mortal(x)

Goal: Prove Marcus is NOT alive now → ¬Alive(Marcus)

Proof by resolution refutation:
- Assume Alive(Marcus) [negation of goal]
- Apply premises step by step using resolution
- Derive □ (contradiction)

Write this proof out in full — the Marcus/Pompeii refutation appears verbatim in 2020, 2021 papers and as a variant in 2022, 2023.

---

**10:30–11:00 · Past Paper Practice — FOL + Resolution (30 min)**

→ `_TopicQuestionMap.md` → Topic: FOL + Resolution

1. **2020: B-Q5** (p.16) — Marcus/Pompeii verbatim — solve in 30 min, timed
2. Check: did you get the null clause? Did you show every step?

---

**11:00–11:25 · Exercise**

Day 4: same 25 min routine. Your stamina is building — notice if you feel more energised.

---

**11:25–11:55 · Public Speaking in English (30 min)**

Today: Explain what Resolution is and walk through one resolution step.
"Given two clauses, if one contains a literal and the other contains its negation, we can cancel them out and combine the rest..."

---

**12:00–13:00 · Study Block 4 — STRIPS: Action Schemas + Block World (60 min)**

Source: `Planning.pdf`

**STRIPS Actions — each action has:**
- **Preconditions:** what must be true before the action can execute
- **Add effects (ADD list):** what becomes true after the action
- **Delete effects (DEL list):** what becomes false after the action

**The 4 Block World Operators:**

PICKUP(A):
- Pre: ONTABLE(A) ∧ CLEAR(A) ∧ ARMEMPTY
- Add: HOLDING(A)
- Del: ONTABLE(A), CLEAR(A), ARMEMPTY

PUTDOWN(A):
- Pre: HOLDING(A)
- Add: ONTABLE(A), CLEAR(A), ARMEMPTY
- Del: HOLDING(A)

UNSTACK(A, B) — pick up A from on top of B:
- Pre: ON(A,B) ∧ CLEAR(A) ∧ ARMEMPTY
- Add: HOLDING(A), CLEAR(B)
- Del: ON(A,B), CLEAR(A), ARMEMPTY

STACK(A, B) — put A on top of B:
- Pre: HOLDING(A) ∧ CLEAR(B)
- Add: ON(A,B), CLEAR(A), ARMEMPTY
- Del: HOLDING(A), CLEAR(B)

**THE BLOCK WORLD PROBLEM — appears every year:**
```
Start: ON(B,A), ONTABLE(A), ONTABLE(C), ONTABLE(D), ARMEMPTY
Goal:  ON(C,A), ON(B,D), ONTABLE(A), ONTABLE(D)
```

Plan:
1. UNSTACK(B, A) → B in hand, A clear
2. PUTDOWN(B) → B on table
3. PICKUP(C) → C in hand
4. STACK(C, A) → C on A ✓
5. PICKUP(B) → B in hand
6. STACK(B, D) → B on D ✓

---

**14:30–16:30 · Study Block 5 — FOL + STRIPS Deep Practice (120 min)**

Part 1 (50 min): FOL/Resolution past papers
- **2021: B-Q5** (p.13) — Marcus/Pompeii variant — timed
- **2022: B-Q5** (p.10) — clausal form conversion + resolution

Part 2 (50 min): STRIPS past papers
- **2020: B-Q6** (p.16) — Block World: trace full action sequence, verify preconditions
- **2021: B-Q6** (p.13) — Sussman Anomaly (see Block 6 for theory)

Part 3 (20 min): Active recall
- Write the R1–R5 FC path from memory
- Draw one resolution proof from memory

---

**17:45–18:30 · Study Block 6 — POP + Sussman Anomaly (45 min)**

Source: `plan2.pdf`

**Partial-Order Planning (POP):**
- A minimal plan — only add ordering constraints when needed
- Uses causal links: an action A achieves condition p for action B → A →(p) B
- Ordering constraints: A must come before B
- POP avoids the Sussman Anomaly that plagues total-order planners

**Sussman Anomaly:**
```
Start: ON(A,B), ONTABLE(B), ONTABLE(C)
Goal:  ON(A,B), ON(B,C)
```
Total-order planning gets stuck — any order of subgoals achieves one but undoes the other.
POP resolves this by finding a non-linear ordering.

After this block: attempt **2023: B-Q6** (Air Cargo) and **2024: B-Q6** (Household Robot) — 20 min each

---

**20:00–20:30 · Study Block 7 — Days 1-4 Comprehensive Review (30 min)**

Blank page. In 30 minutes, write:
1. R1-R5 rule base and FC path
2. The 4-step clausal form algorithm
3. UNSTACK and STACK preconditions from memory
4. Block World start and goal state
5. α/β pruning cutoff condition

Set 5 final flashcard questions for Day 5 morning.

---

---

## DAY 5 — Friday June 5
### Topics: Bayes' Theorem + Bayesian Networks + Neural Networks + Fuzzy + Final Review
### Exam yield: ⭐⭐⭐ + ⭐⭐⭐ + ⭐

---

**05:00–05:10 · Morning — All Flashcard Questions**

Answer all flashcard questions accumulated over Days 1-4. This is your spaced repetition check.

---

**05:10–06:40 · Study Block 1 — Bayes' Theorem (90 min)**

Source: `Reasoning with Uncertainty.pdf`

**Bayes' Theorem:**
```
P(H|E) = P(E|H) · P(H) / P(E)
```
- P(H|E): probability of hypothesis H given evidence E (posterior)
- P(E|H): probability of seeing evidence E given H is true (likelihood)
- P(H): prior probability of H
- P(E): probability of evidence (total probability)

**Computing P(E) — total probability theorem:**
```
P(E) = Σ P(E|Hi) · P(Hi)    (sum over all hypotheses Hi)
```

**Example — Robot Vacuum (2024):**
- H1: Battery low, H2: Dust bin full, H3: Motor overheated
- Given evidence (robot stopped), compute P(Hi|E) for each Hi
- Steps:
  1. Write out P(E|Hi) for each hypothesis
  2. Write prior P(Hi) for each
  3. Compute P(E) = Σ P(E|Hi)·P(Hi)
  4. Compute P(Hi|E) = P(E|Hi)·P(Hi) / P(E)
  5. Compare posteriors → highest is most likely hypothesis

---

**06:50–07:20 · Past Paper Practice — Bayes (30 min)**

→ `_TopicQuestionMap.md` → Topic: Bayes + Bayesian Networks

1. **2020: B-Q7** (p.16) — Bayes' theorem calculation, posteriors
2. **2021: B-Q7** (p.13) — posterior probability computation

---

**07:30–09:00 · Study Block 2 — Bayesian Networks (90 min)**

Source: `Reasoning with Uncertainty.pdf`

**Bayesian Network structure:**
- Directed Acyclic Graph (DAG)
- Each node: random variable
- Each edge: conditional dependence
- Each node: Conditional Probability Table (CPT)

**The Alarm Network (appears 2022-2024):**
```
Fire → Alarm → Mr. X calls
Earthquake → Alarm → Mr. Y calls
```
- P(Alarm | Fire, Earthquake) — CPT for Alarm node
- P(X_calls | Alarm) — CPT for X calls node
- P(Y_calls | Alarm) — CPT for Y calls node

**Joint distribution:**
P(A, B, C) = P(A) · P(B|A) · P(C|B) — product of conditionals following the network structure

**Computing a specific probability:**
e.g., P(alarm sounds but no fire, no earthquake, and both call)
= P(Alarm=T | Fire=F, Earthquake=F) × P(X=T | Alarm=T) × P(Y=T | Alarm=T)
× P(Fire=F) × P(Earthquake=F)

**Evidential Reasoning (ER):**
- High-level attribute inferred via lower-level attributes
- Combined degree of belief aggregates multiple evidence sources

---

**09:10–10:00 · Study Block 3 — Bayesian Networks Practice (50 min)**

1. Sketch the Alarm Network from memory (30 min)
2. Compute one joint probability from the CPTs
3. Attempt **2022: B-Q7** (p.10) — Alarm Network full question

---

**10:30–11:00 · Past Paper Practice — Bayesian Networks (30 min)**

1. **2023: B-Q7** (p.7) — Bayes + Evidential Reasoning
2. **2024: B-Q7** (p.4) — Robot Vacuum Bayesian Network

---

**11:00–11:25 · Exercise**

Day 5 — final exam is June 10. Your body needs to stay in good shape. Do the full 25 min routine.

---

**11:25–11:55 · Public Speaking in English (30 min)**

Today: explain Bayes' theorem and then explain what a Bayesian Network is.
"Given some evidence, we update our belief about a hypothesis using Bayes' theorem..."
Record yourself for 90 seconds. Listen back. You want to sound confident and clear.

---

**12:00–13:00 · Study Block 4 — Neural Networks: Architecture + Learning (60 min)**

Source: `original lecture note.pdf` (Neural Computing: The Basics)

**Biological vs Artificial Neural Networks:**

| Biological | Artificial |
|-----------|-----------|
| Neuron | Processing Element (PE) |
| Dendrites (receives signals) | Input connections |
| Axon (sends output) | Output connection |
| Synapse (connection strength) | Weight (W) |
| Cell body (sums inputs) | Weighted sum + activation function |

**ANN Architecture:**
- Input layer: receives input features
- Hidden layer(s): intermediate computation
- Output layer: produces final output

**Feedforward** — signals flow one direction (input → hidden → output)
**Recurrent** — connections can go backwards (memory)

**Activation Functions:**
- Sigmoid: Y = 1 / (1 + e^(-V)) — maps any value to (0,1)
- Threshold: Y = 1 if V ≥ θ, else 0

**Learning Rule (Delta Rule):**
```
Delta = Z - Y          (Z = true output, Y = computed output)
W_new = W_old + α × Delta × X    (α = learning rate, X = input)
```

**Learning rate α:**
- Too high → oscillates, diverges
- Too low → very slow convergence
- Typical range: 0.01 to 0.5

**Supervised vs Unsupervised:**
- Supervised: labelled training data (input → known output)
- Unsupervised: no labels; network discovers patterns

---

**14:30–16:30 · Study Block 5 — Backprop + Neural Networks + Fuzzy Sweep (120 min)**

**Part 1 — Backpropagation (40 min):**

Source: `original lecture note.pdf`

- Error for output layer: E = ½ Σ(Z - Y)²
- Error propagated backward through all layers
- Each weight updated proportional to its contribution to the error
- The gradient of error with respect to each weight drives the update

Numerical example (2023 style):
Given: sigmoid activation, input X, weights W, true output Z
1. Forward pass: compute V = Σ(Wi × Xi), then Y = sigmoid(V)
2. Compute error: Delta = Z - Y
3. Update weights: Wi_new = Wi_old + α × Delta × Xi

**Part 2 — Competitive Learning Networks (20 min):**
- Unsupervised — neurons compete to respond to an input
- Winner takes all: only the closest neuron updates its weights
- Used in clustering tasks

**Part 3 — Fuzzy Logic brief (20 min):**

Source: `FuzzyLogic-14.pdf`

- Classical (crisp) logic: TRUE or FALSE (1 or 0)
- Fuzzy logic: degrees of truth — a value can be partially true (e.g., 0.7)
- Membership function: maps a value to its degree of membership in a set
  - e.g., temperature 28°C might be 0.3 "cool" and 0.6 "warm"
- Used for imprecise reasoning — control systems, medical diagnosis

**Part 4 — Neural Networks Past Papers (40 min):**
- **2020: B-Q8** (p.16) — Neural Networks + Fuzzy short note
- **2021: B-Q8** (p.13) — ANN architecture, learning
- **2024: B-Q8** (p.4) — backprop numerical + sigmoid activation

---

**17:45–18:30 · Study Block 6 — Full Sweep: All 11 Topics (45 min)**

This is your comprehensive review. For each topic, write one key thing from memory:

| # | Topic | Your one-line recall |
|---|-------|---------------------|
| 1 | Intelligent Agents | PAGE = ? |
| 2 | Search Algorithms | f(n) = ? |
| 3 | Alpha-Beta Pruning | α-cutoff condition = ? |
| 4 | FC/BC | R1–R5 FC path = ? |
| 5 | FOL + Resolution | 4-step algorithm step 1 = ? |
| 6 | STRIPS + Planning | UNSTACK precondition = ? |
| 7 | Bayes + BN | Bayes formula = ? |
| 8 | Neural Networks | Delta rule formula = ? |
| 9 | Hill Climbing + SA | 3 HC problems = ? |
| 10 | CSP | Variables + Domains + ? |
| 11 | Fuzzy Logic | Crisp vs Fuzzy = ? |

Check your answers. Red-circle any gap. That gap is your revision target for June 6–7.

---

**20:00–20:30 · Study Block 7 — Final Active Recall + Exam Strategy (30 min)**

**Exam strategy (confirm this in your head):**

Section A — answer 3 of 4:
- Q1 = Intelligent Agents (easy marks, always answer this)
- Q2 = Search Algorithms (trace step by step = full marks)
- Q3 = Alpha-Beta Pruning (trace + prune = full marks)
- Q4 = FC/BC or HC/SA — answer whichever you know better

Section B — answer 3 of 4:
- Q5 = FOL + Resolution (Marcus/Pompeii proof = full marks)
- Q6 = STRIPS + Planning (Block World trace = full marks)
- Q7 = Bayes + Bayesian Networks (calculations = full marks)
- Q8 = Neural Networks (ANN + delta rule = full marks)

All 8 are within your reach. You have mastered all 8.

**Final active recall:**
- Write R1-R5 from memory
- Write Bayes' theorem formula
- Write the Block World start state and first 3 plan steps
- Write f(n) = g(n) + h(n) and explain each term

---

---

## Mentor Notes

**On stamina:** You said you are low on stamina. The 25-min exercise slot is intentional — short enough to not drain you, long enough to build up over 5 days. By Day 5, if you feel your energy improving, extend to 30 min. During the exam preparation period, 7 hours of sleep is non-negotiable. Do not sacrifice it for extra study.

**On overwhelm:** If a topic is not clicking after 30 minutes, skip to the past paper for that topic first. Seeing the actual exam question often makes the concept click faster than re-reading slides. Then go back and fill the gap.

**On girlfriend chat:** The 4 × 30 min slots are real time, not "maybe" time. Log off fully. This recharges you mentally. Undivided attention for 30 min is better than distracted presence for 2 hours.

**On public speaking:** Use these sessions to think in English, not translate. If you explain a concept clearly in English, you understand it fully. If you fumble, that is your study gap.

**On exercise:** Low stamina is fixed by consistent light movement, not by skipping it. Even 15 minutes of walking counts on bad-energy days. The goal is daily habit, not performance.

**What earns marks in this exam:**
- In search questions: showing the fringe at every step
- In Alpha-Beta: writing α and β values at every node, crossing pruned branches
- In FC/BC: drawing the tree diagram (not just writing the path)
- In FOL: showing each resolution step — not just the final answer
- In Bayes: showing P(E) calculation before posteriors — markers look for the intermediate step
- In STRIPS: writing out preconditions for each action

You have 5 days. That is exactly the right amount of time for this exam. Trust the schedule.
