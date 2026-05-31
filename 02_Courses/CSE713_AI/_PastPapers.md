# CSE 713 — AI · Past-Paper Analysis

## Papers analysed
- 2024 (4 pages, scanned)
- 2023 (3 pages, scanned)
- 2022 (3+ pages, scanned)
- 2021 (3 pages, scanned)
- 2020 (3+ pages, scanned)

## Exam structure
- Full marks: 54 · Duration: 4 hours
- Format: **Answer any 3 from Section A + any 3 from Section B** (~8 questions total, pick 6)
- Marks per question: typically 4–9 marks each

## Pattern table

| Topic | Appeared in (years) | Typical question type | Approx marks | Priority |
|-------|---------------------|-----------------------|:------------:|:--------:|
| Search algorithms (UCS, Greedy, A*, IDDFS) — trace on graph | 2020 2021 2022 2023 2024 | Trace algorithm step-by-step; show fringe at each step | 5–6 | ⭐⭐⭐ |
| Alpha-Beta Pruning + Minimax — apply to given game tree | 2020 2021 2022 2023 2024 | Apply α/β values at every node; show pruned branches | 4–5 | ⭐⭐⭐ |
| Forward + Backward Chaining, Rule-Based System (same R1–R5 example every year) | 2020 2021 2022 2023 2024 | Prove goal G; draw FC propagation tree + BC backtrack tree | 6–9 | ⭐⭐⭐ |
| Bayes' Theorem + Bayesian Networks (numerical computation) | 2020 2021 2022 2023 2024 | Compute P(E), posterior; full Bayesian network joint distribution | 4–9 | ⭐⭐⭐ |
| STRIPS + Partial-Order Planning, Block World / Sussman Anomaly | 2020 2021 2022 2023 2024 | Define action schema; develop POP plan; list causal links | 8–9 | ⭐⭐⭐ |
| FOL + Resolution + Inference (Marcus/Pompeii facts — identical across years) | 2020 2021 2022 2023 2024 | Translate to WFF; convert to clause form; prove by resolution | 7–8 | ⭐⭐⭐ |
| Intelligent Agents + Environments + Architecture (PAGE description) | 2020 2021 2022 2023 2024 | Define agent; PAGE description; characterise environment; best architecture | 4–9 | ⭐⭐ |
| Hill Climbing + Simulated Annealing (limitations; SA as solution) | 2020 2021 2022 2023 2024 | List limitations; explain SA; deterministic vs non-deterministic | 4 | ⭐⭐ |
| Neural Networks + Learning (Section B staple) | 2020 2021 2022 2023 2024 | Compare ANN/biological; inductive learning; forward/backprop | 7–9 | ⭐⭐ |
| CSP — map coloring, cryptarithmetic (SEND+MORE=MONEY) | 2020 2021 2022 2023 | Identify variables/domains/constraints; trace constraint propagation | 1–3 | ⭐ |
| Fuzzy Logic + Uncertainty | 2020 2021 2022 2023 2024 | Short notes | 2–3 | ⭐ |
| Evidential Reasoning (ER) | 2024 | Combined degree of belief | 2 | low |

## Key repeating patterns (memorise these)

### The R1–R5 rule base (appears verbatim 2020–2024)
```
R1: IF A and C THEN E    Initial facts: A, B (both true)
R2: IF C and D THEN F    Goal: Prove G
R3: IF B and E THEN F
R4: IF B THEN C
R5: IF F THEN G
```
FC path: B→C (R4), A∧C→E (R1), B∧E→F (R3), F→G (R5). **Know this cold.**

### The Marcus/Pompeii FOL set (appears verbatim 2020–2022)
Marcus was a man, a Pompeian, born 40 AD. All Pompeians died in 79 AD volcano.
No mortal lives >150 years. Prove "Marcus is not alive now" by resolution.

### The standard search-space graph
Same A→G graph with cost+heuristic table appears in 2020, 2022, 2023. Practice tracing UCS, Greedy, A* on it.

## Exam-day structure
- Total marks: 54 · Duration: 4h · Pick 3 from each of 2 sections = 6 questions
- Targeting 6×9 = 54 marks by doing the highest-yield 6 topics covers everything
