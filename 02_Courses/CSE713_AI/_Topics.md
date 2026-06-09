# CSE 713 — AI · Topic Tracker
> [[_Syllabus]] · [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold

| Topic | Status | Conf | Last Reviewed | Next Recall | Yield | Notes / weak spots |
|-------|:------:|:----:|:-------------:|:-----------:|:-----:|--------------------|
| Intelligent Agents + Environments (PAGE) | ✅ | 4 | 2026-06-01 | 2026-06-05 | 5/5 · 4–9 marks | Past paper practice done (2024/2022/2020 Q1) |
| Search: UCS, Greedy, A*, IDDFS — trace on graph | ✅ | 4 | 2026-06-01 | 2026-06-05 | 5/5 · 5–6 marks | BFS/DFS/UCS/IDDFS + Greedy/A* all done. Past paper practice pending. |
| Search: Problem Formulation (initial state, goal test, operators, path cost) | 🔁 | 4 | 2026-06-01 | 2026-06-04 | 5/5 · 2–3 marks | TSP, M&C, Water Jug, Robot Vacuum, Map Coloring, Monkey & Bananas — apply 4-part template cold |
| Alpha-Beta Pruning + Minimax | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 4–5 marks | Cold trace done. Past papers done. |
| Forward + Backward Chaining + Rule-Based System | ✅ | 5 | 2026-06-04 | 2026-06-06 | 5/5 · 6–9 marks | R1–R5 example is verbatim every year — memorise it |
| FOL + Resolution + Inference (Marcus/Pompeii) | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 7–8 marks | Marcus/Pompeii + FOL translation + 9-step CFC + resolution done. Past papers done. |
| ↳ PL Basics: satisfiability, validity, entailment, Modus Ponens | ✅ | 5 | 2026-06-04 | 2026-06-06 | 4/5 · 2 marks | Sat/valid check 2021 Q4c; algorithm asked 2022 A-2a |
| ↳ Resolution in PL: clause form (4-step), refutation proof | ✅ | 5 | 2026-06-04 | 2026-06-06 | 5/5 · 2–3 marks | Wumpus KB 2021 Q4d; 9-step algo asked every year |
| ↳ FOL Syntax: Terms, Predicates, Functions, ∀, ∃, Sentences | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 1–2 marks | "FOL generalization of PL" asked in 2021 Q5a, 2017, 2016 |
| ↳ FOL Translation (car/drone/robot scenario) | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 4–5 marks | 2023 Q4a (car), 2023 Q4b (drone) — declare predicates FIRST |
| ↳ Canonical Form Conversion (9-step algorithm) | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 1.5–2.5 marks | Required in every resolution proof; asked directly in 2022/2016 |
| ↳ Resolution in FOL: Unification, Skolemization, refutation | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 2–3 marks | Perfect Square 2021/2024; Marcus 2020/2022 — same proof each time |
| ↳ Knowledge Representation and Mapping (roles) | ✅ | 5 | 2026-06-05 | 2026-06-07 | 3/5 · 1.5 marks | 2022 A-2c; 2016 Q3a — 5 roles: surrogate/ontological/inferential/expressivity/efficiency |
| ↳ Evidential Reasoning (ER): Dempster-Shafer, degree of belief | ✅ | 5 | 2026-06-05 | 2026-06-07 | 3/5 · 2 marks | 2024 Q4a,b — Dempster's rule, Bel vs Pl, conflict factor K |
| STRIPS + Partial-Order Planning (Block World) | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 8–9 marks | Slides read, wiki + solutions PDF done. Sussman + 4-block POP fully solved. Past papers done 2020–2024. |
| Bayes' Theorem + Bayesian Networks | ✅ | — | 2026-06-06 | 2026-06-09 | 5/5 · 4–9 marks | Slides read. Extended Bayes, BN DAG+CPT+chain rule, 4 inference types, d-separation |
| ↳ Uncertainty Concept (doorbell) | ✅ | — | 2026-06-06 | — | 4/5 · 2–3 marks | 2020 Q7a, 2021 Q7a — abductive/deductive both fail; Prop1 incomplete, Prop2 not tautology |
| ↳ Extended Bayes' Theorem | ✅ | — | 2026-06-06 | — | 3/5 · 3 marks | 2020 Q7d — P(Hi\|E)=P(E\|Hi)P(Hi)/Σ P(E\|Hk)P(Hk); also sequential form; 5 application areas |
| ↳ BN Syntax, Semantics & Construction | 📖 | — | 2026-06-06 | — | 3/5 · 1–2 marks | 2020 Q8a — N=(X,G,P), DAG, chain rule: P(x1..xn)=ΠP(xi\|parents), Markov condition |
| Hill Climbing + Simulated Annealing | ✅ | 5 | 2026-06-05 | 2026-06-07 | 5/5 · 4 marks | 3 limitations of HC; SA as escape mechanism |
| Neural Networks + Learning | 📖 | — | 2026-06-07 | 2026-06-09 | 3/5 · 9 marks | Corrected yield (2024/2023/2022 only — 2021/2020 NOT asked, were Bayes-only). 5 new sources read in full: Banckpropogation, New Doc 2019, back propagation (Han&Kamber), NN Evolution, Lecture 13.2 ANN |
| ↳ McCulloch-Pitts Neuron + Perceptron + Learning Rule | ✅ | — | 2026-06-07 | — | 1/5 · within NN Q | a=Σ(wi·xi); Perceptron Training Rule Δi=η(t−o)xi; bias-as-input-unit trick; 2 worked examples (bright/dark pixel classifier) |
| ↳ Backpropagation Algorithm + Numerical (sigmoid fwd/bwd pass) | 📖 | — | 2026-06-07 | — | 1/5 · 6 marks (2023 Q8b) | Han&Kamber Example 9.1 is the canonical worked numerical — matches 2023's exact question style. Err_j=O_j(1−O_j)(T_j−O_j); Δw=l·Err_j·O_i |
| ↳ Associative Memory + Hopfield Networks | 📖 | — | 2026-06-07 | — | 1/5 · 3 marks (2023 Q8a) | Recall complete patterns from partial input; Hopfield energy E=−½Σwij·si·sj; Nobel 2024 (Hopfield+Hinton) |
| ↳ ANN vs Biological Network comparison + taxonomy | 📖 | — | 2026-06-07 | — | 2/5 · 3 marks | soma/dendrite/axon↔node/input/output mapping; feedforward vs recurrent; supervised/unsupervised/reinforcement |
| ↳ NN Historical Evolution (AI Winters → Transformers) | 📖 | — | 2026-06-07 | — | 0/5 · background only | MP(1943)→Rosenblatt(1958)→Minsky XOR(1969)→Hopfield(1982)→Hinton backprop(1986)→CNN/LSTM(1989-97)→AlexNet(2012)→Transformers(2017). Not directly examined — context for "what is learning/ANN" essays |
| CSP (map coloring, cryptarithmetic) | 🔲 | — | — | — | 4/5 · 1–3 marks | Small marks; don't over-invest |
| Fuzzy Logic + Uncertainty | 📖 | — | 2026-06-07 | — | 2/5 · 2–3 marks | Slides read, wiki + solutions PDF done. Only 2024/2022 ask it (short notes, inside NN Q). 2021/2020 corrected to "not asked". |

## Column guide
- **Conf** — confidence 1–5 (1=shaky, 5=bulletproof). Update after every recall pass.
- **Last Reviewed** — date you last marked ✅ or completed a 🔁 pass (YYYY-MM-DD). Claude writes this.
- **Next Recall** — auto-computed by spaced_rep.py. Claude writes this after each update.

## Status rules
- ✅ only when you can explain it cold without notes AND solve a past-paper question on it.
- Re-reading ≠ ✅.
- When you complete a 🔁 recall pass → mark ✅ again and update Last Reviewed with today's date.
- High Yield + 🔲 status = today's target.
