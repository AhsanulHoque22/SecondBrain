# CSE 713 — AI · Topic Tracker
> [[_Syllabus]] · [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold

| Topic | Status | Conf | Last Reviewed | Next Recall | Yield | Notes / weak spots |
|-------|:------:|:----:|:-------------:|:-----------:|:-----:|--------------------|
| Intelligent Agents + Environments (PAGE) | ✅ | 4 | 2026-06-01 | 2026-06-03 | 5/5 · 4–9 marks | Past paper practice done (2024/2022/2020 Q1) |
| Search: UCS, Greedy, A*, IDDFS — trace on graph | ✅ | 4 | 2026-06-01 | 2026-06-03 | 5/5 · 5–6 marks | BFS/DFS/UCS/IDDFS + Greedy/A* all done. Past paper practice pending. |
| Search: Problem Formulation (initial state, goal test, operators, path cost) | 🔁 | 4 | 2026-06-01 | 2026-06-03 | 5/5 · 2–3 marks | TSP, M&C, Water Jug, Robot Vacuum, Map Coloring, Monkey & Bananas — apply 4-part template cold |
| Alpha-Beta Pruning + Minimax | 📖 | — | 2026-06-02 | — | 5/5 · 4–5 marks | Slides done. Active recall pending — cannot mark ✅ until cold trace passes. |
| Forward + Backward Chaining + Rule-Based System | 🔲 | — | — | — | 5/5 · 6–9 marks | R1–R5 example is verbatim every year — memorise it |
| FOL + Resolution + Inference (Marcus/Pompeii) | 🔲 | — | — | — | 5/5 · 7–8 marks | Same facts set 2020–2022; 2023/2024 use FOL for robots/drones |
| ↳ PL Basics: satisfiability, validity, entailment, Modus Ponens | 🔲 | — | — | — | 4/5 · 2 marks | Sat/valid check 2021 Q4c; algorithm asked 2022 A-2a |
| ↳ Resolution in PL: clause form (4-step), refutation proof | 🔲 | — | — | — | 5/5 · 2–3 marks | Wumpus KB 2021 Q4d; 9-step algo asked every year |
| ↳ FOL Syntax: Terms, Predicates, Functions, ∀, ∃, Sentences | 🔲 | — | — | — | 5/5 · 1–2 marks | "FOL generalization of PL" asked in 2021 Q5a, 2017, 2016 |
| ↳ FOL Translation (car/drone/robot scenario) | 🔲 | — | — | — | 5/5 · 4–5 marks | 2023 Q4a (car), 2023 Q4b (drone) — declare predicates FIRST |
| ↳ Canonical Form Conversion (9-step algorithm) | 🔲 | — | — | — | 5/5 · 1.5–2.5 marks | Required in every resolution proof; asked directly in 2022/2016 |
| ↳ Resolution in FOL: Unification, Skolemization, refutation | 🔲 | — | — | — | 5/5 · 2–3 marks | Perfect Square 2021/2024; Marcus 2020/2022 — same proof each time |
| ↳ Knowledge Representation and Mapping (roles) | 🔲 | — | — | — | 3/5 · 1.5 marks | 2022 A-2c; 2016 Q3a — 5 roles: surrogate/ontological/inferential/expressivity/efficiency |
| ↳ Evidential Reasoning (ER): Dempster-Shafer, degree of belief | 🔲 | — | — | — | 3/5 · 2 marks | 2024 Q4a,b — Dempster's rule, Bel vs Pl, conflict factor K |
| STRIPS + Partial-Order Planning (Block World) | 🔲 | — | — | — | 5/5 · 8–9 marks | Sussman Anomaly appears 2020/2021 |
| Bayes' Theorem + Bayesian Networks | 🔲 | — | — | — | 5/5 · 4–9 marks | Numerical: compute P(E), posteriors, joint distribution |
| Hill Climbing + Simulated Annealing | 🔲 | — | — | — | 5/5 · 4 marks | 3 limitations of HC; SA as escape mechanism |
| Neural Networks + Learning | 🔲 | — | — | — | 5/5 · 7–9 marks | Section B; ANN vs biological; backprop |
| CSP (map coloring, cryptarithmetic) | 🔲 | — | — | — | 4/5 · 1–3 marks | Small marks; don't over-invest |
| Fuzzy Logic + Uncertainty | 🔲 | — | — | — | 4/5 · 2–3 marks | Short notes only needed |

## Column guide
- **Conf** — confidence 1–5 (1=shaky, 5=bulletproof). Update after every recall pass.
- **Last Reviewed** — date you last marked ✅ or completed a 🔁 pass (YYYY-MM-DD). Claude writes this.
- **Next Recall** — auto-computed by spaced_rep.py. Claude writes this after each update.

## Status rules
- ✅ only when you can explain it cold without notes AND solve a past-paper question on it.
- Re-reading ≠ ✅.
- When you complete a 🔁 recall pass → mark ✅ again and update Last Reviewed with today's date.
- High Yield + 🔲 status = today's target.
