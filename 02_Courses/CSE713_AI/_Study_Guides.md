# CSE 713 AI — Study Guides
> [[_Topics]] · [[_TopicQuestionMap]] · [[_Syllabus]] · [[00_Dashboard]]

Generated per block. Each guide maps slides → exam relevance. Saved for revision reference.

---

## Block 1 — Intelligent Agents + Environments (Ch01-02.pdf)
**Date:** 2026-06-01 | **Time:** 5:10–6:40

| Slide | Content | Why study it |
|-------|---------|-------------|
| 13-14 | AI definition + foundations | 2024 Q1a — "Define AI. Point out recent advancements." |
| 15-17 | Turing Test + Chinese Room argument | 2024 Q1c, 2023 Q1c — evaluate specific AI system vs Turing Test |
| 42-46 | Agent definition, PAGE model (Percepts, Actions, Goals, Environment) | Every year Q1 part (c) — identify percepts/actions/goals for a given agent |
| 49 | Performance measure, rationality | 2024 Q1c(iv) — "suggest appropriate performance measure" |
| 58-60 | PEAS table — worked examples (taxi driver, medical diagnosis, etc.) | Template for answering the 4-mark scenario question |
| 62-63 | 5 agent architectures overview | Foundation — you must know all 5 |
| 65-66 | Simple Reflex Agent — condition-action rules | 2024 Q1c(v) — "most appropriate architecture + justification" |
| 67-69 | Model-Based Reflex Agent — internal state | 2023 Q1c(v) |
| 70-72 | Goal-Based Agent — search + planning | 2022 Q1c(v) |
| 73-75 | Utility-Based Agent — utility function | 2021 Q1c(v) |
| 76-77 | 6 environment types (fully/partially observable, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous, single/multi-agent) | Every year — characterize the environment |
| 83-84 | Characteristics table (all environment types summarized) | Memorize this table |
| 86 | Chapter summary | Quick reference |

**SKIP:** 1-12 (preface/TOC), 18-39 (AI history), 50-57 (detailed agent theory), 61,64,68,72,75 (pseudocode), 78-82, 85, 87

**Past paper links:** 2024 Q1 (9 marks), 2023 Q1 (9 marks), 2022 A-1 (9 marks), 2021 Q1 (9 marks), 2020 Q1 (9 marks)

---

## Block 2 — BFS, DFS, UCS, IDDFS (Chapter 3.pdf)
**Date:** 2026-06-01 | **Time:** 7:30–9:00

| Slide | Content | Why study it |
|-------|---------|-------------|
| 46-48 | Search strategy intro + evaluation criteria (completeness, optimality, time, space) | How every algorithm is judged. Exam asks "compare completeness + optimality." |
| 49-52 | Uninformed/blind search definition | Foundation — these use NO domain knowledge beyond problem definition |
| 53-55 | BFS — expand shallowest first, QUEUE, step-by-step algorithm | 2024 Q2, 2023 Q2, 2020 Q2. Fringe = queue (FIFO) |
| 56 | BFS pseudocode (fringe-based loop) | Memorize the loop structure — same template for all algorithms |
| 61-63 | BFS trace — CLOSED list + backpointers + search tree | Shows exactly what the exam asks: node expansion order + fringe |
| 64 | UCS — expand lowest g(n), priority queue | 2024 Q2, 2021 Q2. Fringe sorted by path cost |
| 69-70 | UCS trace — node expansion table with costs | Exam format: show fringe sorted by g(n) at each step |
| 71-72 | DFS — expand deepest first, LIFO/stack | 2022 Q2, 2020 Q2. Fringe = stack |
| 76 | DFS pseudocode (ENQUEUE-ATFRONT) | Implementation detail — same template, different queueing |
| 78 | When DFS is preferred | Direct comparison question material |
| 81 | Depth-Limited Search — DFS with depth cutoff | Pre-requisite for IDDFS |
| 83-85 | DFID/IDDFS — iterative deepening, complexity proof (O(b^d), 78% overhead at b=4) | 2024 Q2, 2023 Q2. Know the complexity formula + when to use |
| 91 | "When to use what" — all 4 algorithms compared | Direct exam answer: BFS (shallow solutions), DFS (many solutions), UCS (varying costs), IDDFS (limited space) |
| 93 | Comparing Search Strategies — full table | Memorize this table: completeness, optimality, time, space for every algorithm |

**SKIP:** 1-45 (problem formulation, Romania, 8-puzzle — not directly tested), 57-60, 65-68, 73-75, 77, 79-80, 82, 86-90 (diagram-only pages), 92 (bidirectional search — not in past papers), 94-100 (review/wrap-up)

**Past paper links:** 2024 Q2, 2023 Q2, 2022 B-4, 2021 Q2, 2020 Q2 — all ask "show node expanded + fringe contents at every step"

---

## Block 3 — Greedy Best-First + A* (Chapter 3.pdf)
**Date:** 2026-06-01 | **Time:** 9:10–10:00

| Slide | Content | Why study it |
|-------|---------|-------------|
| 89 | "Heuristic search" intro + "BEST FIRST SEARCH" algorithm family | Foundation — what makes a search "informed" |
| 90 | BFS (uninformed) vs Best-First (informed) side-by-side | Exam comparison question material |
| 91 | "Heuristic Function" — h(n) definition | Core definition: h(n) = estimated cheapest cost from n to goal |
| 92 | Example — Romanian map with straight-line distances as heuristic | Classic AIMA example, shows how h(n) works in practice |
| 93 | Greedy Best-First — algorithm + first example | Expands lowest h(n) first. Fringe = priority queue by h(n) |
| 94 | Greedy Best-First — continued trace | See how Greedy can be suboptimal (chooses h=0 wrong path) |
| 95 | Greedy Best-First — properties (complete? optimal? time/space) | Memorize: NOT optimal, NOT complete (can loop), O(b^m) |
| 96 | A* Search — f(n)=g(n)+h(n), algorithm | HIGHEST YIELD. Every year has an A* tracing question. |
| 97 | A* — worked example with graph tracing step by step | Shows fringe sorted by f(n), node expansion order |
| 98 | A* — admissibility proof + optimality conditions | 2023 Q2: "Define admissible heuristic." Must know: h(n) ≤ h*(n) |
| 99 | Comparison table: Greedy vs A* (completeness, optimality, time, space) | Direct exam answer format |
| 100 | Summary / Chapter wrap-up | Final reference |

**SKIP:** 84-88 (uninformed search wrap-up — already covered in Block 2)

**Past paper links:** 2024 Q2, 2023 Q2, 2022 B-4, 2021 Q2, 2020 Q2 — "trace Greedy + A*, show fringe sorted at every step"
