# CSE 713 AI — Topic-Wise Question Map (2020–2024)
> [[_Topics]] · [[_Syllabus]] · [[00_Dashboard]]

> Maps each exam topic to exact question numbers + full question content from past papers.
> Source PDF: `AI Previous Year Questions(2024-2016).pdf`
> Last updated: 2026-06-01 (from scanned past papers)

## PDF Navigation
| Paper Year | Pages in PDF |
|-----------|-------------|
| 2024 | pp. 1–4 |
| 2023 | pp. 5–7 |
| 2022 | pp. 8–10 |
| 2021 | pp. 11–13 |
| 2020 | pp. 14–16 |

---

## ⚡ EXAM FORMAT (Critical)
- Full Marks: 54, Time: 4 Hours
- Answer **any 3 questions from each section** (Section A + Section B)
- 2024/2023/2021: Q1–Q4 Section A, Q5–Q8 Section B
- 2022: A-1 to A-4 (Sec A), B-1 to B-4 (Sec B) — different topic placement!

---

## SECTION A TOPICS

---

### Topic 1 — Intelligent Agents + Environments
**Source:** Ch01-02.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 7–9

#### 🔁 PATTERN (memorise this):
Every year Q1 has THREE parts:
1. **AI definition** + recent advancements OR connections among AI forms (1–2 marks)
2. **Turing Test** — evaluate a specific AI system (LLM/ChatGPT/Sophia) against Turing Test: how it corresponds + limitations (2.5–3 marks)
3. **Real-world agent scenario (BIG 4-mark question)** → always asks:
   - (i) Percepts / sensory inputs
   - (ii) Operating environment — characterize using PAGE/AI environment properties
   - (iii) Actions available
   - (iv) Performance measure / evaluation
   - (v) Most appropriate agent architecture + justification

#### Detailed Questions by Year:

**2024 — Q1 (9 marks)**
- a) Define AI. Point out a few advancements of AI recently. (1)
- b) Differentiate between AI and Machine Learning. (1.5)
- c) Evaluate the performance of Large Language Models (LLMs) in context of the Turing Test: (2.5)
  - i) How do LLMs exhibit human-like conversational abilities (fluency, contextual awareness, reasoning) that correspond with objectives of the Turing Test?
  - ii) Examine the constraints of LLMs (insufficient real-world grounding, hallucinations, no stable memory, long-horizon dialogue failure) — why these prevent reliably passing the Turing Test
- d) Investigate an **Autonomous Agricultural Field Robot** used in Bangladesh for monitoring crops, detecting pests, spraying fertilizer: (4)
  - i) Sensory inputs (percepts) used by this robot
  - ii) Characterize operating environment using standard AI environment properties
  - iii) Actions available during field operations
  - iv) How can performance be evaluated?
  - v) Which agent architecture is most appropriate for this robot, and why?

**2023 — Q1 (9 marks)**
- a) Define AI. How can connections among different forms of AI be clarified through generative traits, capabilities, and functional attributes? (2)
- b) Evaluate the performance of ChatGPT in context of the Turing Test: (3)
  - i) Ways ChatGPT corresponds to Turing Test goals regarding human-like conversation emulation
  - ii) Limitations of ChatGPT that would prevent it from passing the Turing Test in more complex/prolonged interactions
- c) Investigate the most recent Mars Rovers — **Curiosity (2012)** and **Perseverance (2021)**: (4)
  - i) Sensory inputs (percepts)
  - ii) Characterize operating environment
  - iii) Actions available
  - iv) How can performance be evaluated?
  - v) Most appropriate agent architecture + reasons

**2022 — A-1 (9 marks)** *(more theoretical — no scenario)*
- a) What function does an intelligent agent serve? (4)
- b) What primary component(s) will be used to evaluate the effectiveness of problem solving? (3)
- c) What does a utility-based agent do? (2)

**2021 — Q1 (9.75 marks)**
- a) Do you think humanoid **Sophia and Jarvis** possess features and signs of intelligence? Elaborate taking into account their behavior. (1.5)
- b) Suppose you design a machine to pass the Turing test. What capabilities must it have? (1)
- c) Describe how Simple Reflex agents differ from Goal Driven agents considering architecture. (1)
- d) Consider intelligent agent **"Amazon Echo"**: (2+2)
  - i) Write a PAGE (Percepts, Actions, Goals, Environments) description
  - ii) Characterize environment: accessible/inaccessible, deterministic/non-deterministic, episodic/non-episodic, static/dynamic, discrete/continuous
- e) What agent architecture is best for the **automated taxi driving** agent? Justify. (1.25)

**2020 — Q1** *(details from TopicQuestionMap notes — AI + agents, Mars Rover scenario)*

#### 🎯 What to master for this topic:
- **5 agent architectures**: Simple Reflex, Model-Based, Goal-Based, Utility-Based, Learning — when each is appropriate + justify
- **6 environment dimensions**: fully/partially observable · deterministic/stochastic · episodic/sequential · static/dynamic · discrete/continuous · single/multi-agent
- **PAGE model**: apply to ANY agent scenario (robot, drone, car, vacuum)
- **Turing Test**: what it measures + why LLMs fail in extended interactions (hallucinations, no memory, no grounding)
- **AI vs ML vs DL**: clear one-line differentiators

---

### Topic 2 — Search Algorithms (State Space Search)
**Source:** Chapter 3.pdf, Chapter 4.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 7–9

#### 🔁 PATTERN (memorise this):
Every year has a **graph trace question** (4.5–5 marks) + **problem formulation** (2–3 marks):
- Always given: cost table + h(n) table → draw graph → trace algorithms
- Algorithms tested: **UCS + Greedy + A*** (every year) + **IDDFS** (2024, 2023)
- At every step: show **which node is expanded** + **full fringe contents in sorted order**
- IDDFS: show depth limit per iteration + order of expansion

#### Detailed Questions by Year:

**2024 — Q2 (9 marks)**
- States: A, B, C, D, E, F, H, J, K, G (goal). All roads bidirectional.
- Given Table 1 (road connections + step costs) and Table 2 (heuristic estimates h(n) to G)
- Key graph: A→B(3), A→C(4), A→D(7), B→E(6), B→F(5), C→F(11), C→H(4), D→H(2), D→J(10), E→G(7), E→H(3), F→G(9), F→J(4), H→G(5), H→K(6), J→K(3), K→G(4)
- h(n): A=11, B=10, C=7, D=6, E=6, F=6, H=4, J=5, K=3, G=0
  - i) Draw state-space graph labelling all nodes and edge costs (1)
  - ii) Show search tree for: 1.UCS 2.Greedy Best-First h(n) 3.A* f(n)=g(n)+h(n) 4.IDDFS — at every step: node being expanded + fringe contents in order of selection. For IDDFS: depth limit per iteration. Ties broken alphabetically. (5)
- b) Give initial state, goal test, operators, path cost function for: (3)
  - i) **Robot Vacuum Cleaning** (Indoor, multi-room, static obstacles, minimize energy) — also comment: uninformed (BFS/UCS) or informed (A*)?
  - ii) **Water Jug Problem** (5L + 3L jugs, no markings, unlimited water, drain, goal: exactly 4L) — is state space finite or infinite?

**2023 — Q2 (9 marks)**
- a) Give initial state, goal test, operators, path cost for: (2)
  - i) **Travelling Salesman Problem (TSP)** — N cities, visit all exactly once, return to start, minimize tour
  - ii) **Missionaries & Cannibals** — 3M + 3C, 1 boat carries 2, M must never be outnumbered by C
- b) Search space given as table (State, Next, Cost) + h(n) table: (5)
  - States: A→B(4), A→C(1), B→D(3), B→E(8), C→C(0), C→D(2), C→F(6), D→C(2), D→E(4), E→G(2), F→G(8)
  - h(n): A=8, B=8, C=6, D=5, E=1, F=4, G=0
  - i) Draw state space (0.5)
  - ii) Trace UCS, Greedy search, A* showing node expanded + fringe at each step (4.5)
- c) Illustrate with example how **IDDFS** synthesizes benefits of BFS + DFS — optimality, completeness, linear space. Time complexity deteriorates vs both BFS+DFS. (2)

**2022 — B-4 (search appears in Section B here!)** (9 marks)
- a) Steepest-Ascent Hill Climbing algorithm. Problems HC may reach. How to deal. (2)
- b) Search space given as table + h(n): (3)
  - States: A→B(4), A→C(1), B→D(3), B→E(8), C→C(0), C→D(2), C→F(6), D→C(2), D→E(4), E→G(2), F→G(8)
  - h(n): A=8, B=8, C=6, D=5, E=1, F=4, G=0
  - i) Draw state space
  - ii) Trace **Uniform cost, Greedy search, A\*** (A→G)
- c) Heuristic function? Block world problem (9-block stack) — show HC fails with local heuristic, works with global heuristic. (1)
- d) CSP: Trace **SEND+MORE=MONEY** cryptarithmetic. (3)

**2021 — Q2 (9 marks)**
- a) What is the state space search problem? (0.75)
- b) Give initial state, goal test, successor function, cost function + working principle of basic search algorithm for: (3)
  - i) **Map Coloring** (4 colors, no adjacent regions same color)
  - ii) **Monkey & Bananas** (3-ft monkey, 8-ft ceiling, 3-ft crates, get bananas)
- c) Search space (Figure 1 — S as start, G as goal, graph with arc costs and h* values): (3+2)
  - i) Assume start=S, goal=G. Trace **Depth First Iterative Deepening, Greedy, A\*** — at each step show node expanded + fringe. Report eventual algorithm + solution cost.
  - h(n): S=9, A=9, B=4, C=5, D=∞, E=∞, G=0

**2020 — Q2** *(Search + Hill Climbing combined — see Topic 9)*

#### 🎯 What to master for this topic:
- **UCS**: expand lowest g(n). Fringe = priority queue ordered by path cost.
- **Greedy**: expand lowest h(n). Fringe = priority queue ordered by h(n).
- **A\***: expand lowest f(n)=g(n)+h(n). Fringe = priority queue ordered by f(n).
- **IDDFS**: DFS with depth_limit=0,1,2,... until goal found. Show each iteration.
- **Fringe format at every step** (exam marks): `[node(cost), node(cost), ...]` sorted
- **Admissibility**: h(n) ≤ h*(n) — A* is optimal if heuristic is admissible
- **Problem formulations** — know for: Water Jug, TSP, M&C, Robot Vacuum, Map Coloring, Monkey+Bananas

---

### Topic 3 — Alpha-Beta Pruning + Minimax
**Source:** Chapter 5.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 4–5

#### 🔁 PATTERN:
- Always given a **game tree with leaf values** → apply Alpha-Beta pruning
- Must show: α and β values at every MAX and MIN node as they update + which branches pruned + final Min-Max value returned to root
- Also asks: why Min-Max is inefficient / 2 limitations

#### Detailed Questions by Year:

**2024 — Q3a (5 marks)**
- Game tree: Root A (MAX), children B, C, D (MIN), their children E,F,G,H,I,J,K (MAX), leaf values: L(7),M(5),N(4),O(-5),P(2),Q(3),R(0),S(-2),T(6),U(2),V(5),W(8),X(9),Y(0)
  - i) Explain why Min-Max becomes inefficient for large game trees. Discuss at least 2 limitations of pure Min-Max.
  - ii) Apply Alpha-Beta Pruning — show α and β at every MAX/MIN node as updated, which branches pruned, final Min-Max value to root.
  - iii) Using your analysis, explain how Alpha-Beta addresses limitations in terms of: 1.time complexity 2.unnecessary node expansion 3.improved decision-making under resource limits

**2023 — Q3b (4 marks)**
- Same game tree structure (A→B,C,D→E,F,G,H,I,J,K→leaves: 7,5,4,-5,2,3,0,-2,6,2,5,8,9,0)
- By analyzing this game tree, illustrate how alpha-beta pruning minimizes time complexity of Min-Max by applying concept of pruning.

**2022 — A-4 (partial)**
- b) Describe the minimax search procedure. (4)
- c) Explain with figures: i) α-cutoff ii) β-cutoff iii) Futility-cutoff (2)
- d) What is "Waiting for Quiescence"? (1)

**2021 — Q3d (4 marks)**
- Different game tree (3 levels, leaf values: 0,5,-3,3 and 3,-2,3)
- Explain how Alpha-Beta pruning improves game playing using this example.

#### 🎯 What to master:
- Minimax algorithm + why O(b^m) is a problem
- Alpha-Beta pruning: α = best MAX seen on path to root, β = best MIN seen on path to root
- Prune: at MIN node if value ≤ α; at MAX node if value ≥ β
- Always track α/β at every node as they update left-to-right
- 2024 tree is the HARDEST — practice it fully

---

### Topic 4 — Forward + Backward Chaining + Rule-Based Systems
**Source:** Rule-Based Systems.pdf · **Yield:** ⭐⭐ 3/5 years in Sec A, 5/5 years in Sec B

#### 🔁 PATTERN — THE R1–R5 EXAMPLE APPEARS VERBATIM EVERY YEAR:
```
R1: IF A AND C THEN E      Initial facts: A, B (both true)
R2: IF C AND D THEN F      Goal: Prove hypothesis G
R3: IF B AND E THEN F
R4: IF B THEN C
R5: IF F THEN G
```
- Must: prove G using FC AND BC, show sequence of rule firings, draw FC propagation tree + BC backtracking tree

#### Detailed Questions by Year:

**2024 — Q6 (Section B)**
- a) Define FC and BC. What factors determine whether to use FC vs BC? (2)
- b) What is conflict resolution? Discuss 2 approaches. (1.5)
- c) R1-R5 system above. Prove G using FC and BC. Show rule firing sequence + draw search tree for FC (propagation of truth) and BC (backtracking of goals). (5.5)

**2023 — Q6 (Section B)**
- Same structure: FC/BC definition + factors (2), conflict resolution (1), R1-R5 prove G (6)
- Note: 2023 Q4b also has FOL + Forward Chaining for drone delivery scenario

**2022 — B-3 + B-3c**
- b) Define FC and BC. Factors for choosing. (1.5)
- c) R1-R5 same example — prove G using FC and BC with search trees. (2... + more)

**2021 — Q6a**
- R1-R5 same example — prove G using FC and BC with search trees.

**2020 — Q4**
- FC/BC with R1-R5, factors for choosing FC vs BC

#### 🎯 What to master:
- FC algorithm: data-driven, start from facts, fire rules that match, add conclusions to KB
- BC algorithm: goal-driven, start from goal, find rules that can prove it, recurse on preconditions
- R1-R5 trace: memorize the exact firing sequence for both FC and BC
  - FC: Facts={A,B} → R4 fires (B→C) → {A,B,C} → R1 fires (A,C→E) → {A,B,C,E} → R3 fires (B,E→F) → {A,B,C,E,F} → R5 fires (F→G) ✅
  - BC: Goal=G → R5: need F → R2: need C,D (fail, D not in KB) → R3: need B,E → B✅, need E → R1: need A,C → A✅, C? → R4: need B → B✅ → C✅ → E✅ → F✅ → G✅
- Conflict resolution: 3 approaches (recency, specificity, refractoriness)

---

### Topic 9 — Hill Climbing + Simulated Annealing
**Source:** Chapter 4.pdf (Local Search) · **Yield:** ⭐⭐ 3/5 years

| Year | Section | Q# | Notes |
|------|---------|-----|-------|
| 2024 | A | Q4b | HC deterministic/non-deterministic; 3 HC limitations for drone route; SA explanation |
| 2023 | A | Q3a | Deterministic vs non-deterministic; HC limitations; SA for drone route |
| 2022 | B | B-4a | Steepest-Ascent HC algorithm; problems HC reaches; solutions |
| 2021 | A | Q3a | Steepest-Ascent HC; problems; solutions |
| 2020 | A | Q2 (partial) | Combined with search algorithms |

#### 🎯 What to master:
- **3 HC limitations**: local maxima, ridges, plateaux
- SA: escape local maxima by accepting worse solutions with probability e^(ΔE/T), T decreases over time
- HC is deterministic; SA is non-deterministic (probabilistic acceptance)

---

### Topic 10 — CSP (Constraint Satisfaction Problems)
**Source:** 20_CSP.pdf · **Yield:** ⭐ (appears in parts)

| Year | Section | Q# | Notes |
|------|---------|-----|-------|
| 2024 | A | Q4 (part) | Short note within HC/SA/Fuzzy/CSP combined question |
| 2023 | A | Q3c | Map coloring CSP — identify variables, domains, constraints |
| 2022 | B | B-4d | SEND+MORE=MONEY cryptarithmetic CSP trace |
| 2021 | A | Q3c | Map coloring CSP — variables, domains, constraints |
| 2020 | B | B-Q8 (part) | Combined with Neural Networks |

---

### Topic 11 — Fuzzy Logic + Uncertainty
**Source:** FuzzyLogic-14.pdf · **Yield:** ⭐ (appears in parts)

| Year | Section | Q# | Notes |
|------|---------|-----|-------|
| 2024 | A | Q4 (part) | Short note within Q4 |
| 2022 | B | B-1d | Short note: Fuzzy logic + Uncertainty |
| 2021 | B | combined | Part of Neural Networks question |
| 2020 | B | combined | Part of Neural Networks question |

---

## SECTION B TOPICS

---

### Topic 5 — FOL + Resolution + Inference
**Source:** Propositional Logic.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 7–9

#### 🔁 PATTERN:
Two sub-types appear alternately:
- **Type A (Marcus/Pompeii)**: Translate facts to FOL → backward reasoning → clause form → resolution proof
- **Type B (Self-driving car / Drone / Robot)**: Define actions/predicates in FOL → forward chaining

**Marcus/Pompeii facts (memorize):**
```
F1: Marcus was a man.          F6: No mortal lives longer than 150 years.
F2: Marcus was a Pompeian.     F7: It is now 2023.
F3: Marcus was born in 40 AD.  F8: Alive means not dead.
F4: All men are mortal.        F9: If someone dies, he is dead at all later times.
F5: All Pompeians died when    Goal: Prove Marcus is NOT alive now.
    volcano erupted in 79 AD.
```

#### Detailed Questions by Year:

**2024 — Q4a (5 marks) — FOL (Self-driving car)**
- Define in FOL: i) car moves to reachable destination with no obstacles ii) proceeds through intersection if traffic light green + no pedestrians iii) stops if obstacle on road iv) reduces speed in school zone during active hours v) changes lanes only if adjacent lane clear + car moving

**2024 — Q4b (4 marks) — FOL + Forward Chaining (Drone delivery)**
- Drone at L0, R1:L0→L1, R2:L1→L2 (obstacle), R3:L2→Lp
- Define predicates, knowledge base, rules in FOL, then use forward chaining to determine if drone reaches destination

**2023 — Q4a (5 marks) — FOL (Self-driving car, same as 2024 Q4a)**
**2023 — Q4b (4 marks) — FOL + Forward Chaining (Drone, same scenario)**

**2022 — A-2 (FOL appears in Section A!)**
- a) What is resolution? Write algorithm for conversion of wff in predicate logic to clause form. (2.5)
- b) Marcus/Pompeii facts F1-F9:
  - i) Translate to wff in predicate logic (1)
  - ii) Answer "Is Marcus alive now?" using backward reasoning (1)
  - iii) Convert formula to clause form (1)
  - iv) Prove Marcus is not alive now using resolution (2)
- c) Knowledge Representation and Mapping roles (1.5)

**2021 — Q4d (3.5 marks) — KB Resolution**
- Given KB: R1:~P1,1 / R2:B1,1↔(P2,1∨P1,2) / R3:B2,1↔(P1,1∨P2,2∨P3,1) / R4:~B1,1 / R5:B2,1
- Show that P1,2 is false using resolution

**2021 — Q5b (7.75 marks) — Perfect Squares FOL**
- Same sentences as 2024 Q4c:
  - i) Perfect square divisible by prime P → also divisible by P²
  - ii) Every perfect square divisible by some prime
  - iii) 36 is a perfect square
  - iv) Does there exist prime q such that q² divides 36?
- Translate to FOL → clause form → resolution proof

---

### Topic 6 — STRIPS + Partial-Order Planning
**Source:** Planning.pdf, plan2.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 4–9

#### 🔁 PATTERN:
- Always: **Block World problem** (same start/goal state across years!)
- Sometimes: STRIPS definition + Action Schema first, then Block World
- 2024/2023/2022: POP (Partial-Order Planning) with causal links + ordering constraints

**The Block World (appears verbatim 2024, 2023, 2022, 2021, 2020):**
```
Start: ON(B,A), ONTABLE(A), ONTABLE(C), ONTABLE(D), ARMEMPTY
Goal:  ON(C,A), ON(B,D), ONTABLE(A), ONTABLE(D)
```

#### Detailed Questions by Year:

**2024 — Q5 (9 marks)**
- a) What is STRIPS? How are actions represented using STRIPS action schema? Develop a planning problem using STRIPS defining one action (Household Robot: cleaning a room, turning on appliances, fetching objects) with Preconditions, Add-effects, Delete-effects. (4)
- b) Block World problem (above). Using POP: 1.Construct minimal POP plan 2.List all causal links and ordering constraints 3.Explain how POP avoids backtracking vs total-order planning. (5)

**2023 — Q5 (9 marks)**
- a) What is STRIPS? Action Schema of STRIPS? Devise planning problem for **Air Cargo Transport** (load/unload cargo, fly planes). (4)
- b) Block World (same). Solve using partial order planning. (5)

**2022 — A-3 (9 marks)**
- a) Preconditions of UNSTACK(A,B), STACK(A,B), PICKUP(A), PUTDOWN(A). (2)
- b) Block World (same). Solve using goal stack planning/partial order planning/STRIPS. (5)
- c) Short notes on Generative AI. (2)

**2021 — Q6b (4 marks)**
- Block World = **Sussman Anomaly**: Start: C on A, B on table, A on table. Goal: A on B, B on C.
- Develop effective and complete plan using POP/STRIPS addressing threats to causal links and open conditions.

---

### Topic 7 — Bayes' Theorem + Bayesian Networks
**Source:** Reasoning with Uncertainty.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 4–9

#### 🔁 PATTERN:
- Always either: Bayes' Theorem calculation problems OR full Bayesian Network
- Bayesian Network: given topology + CPTs → compute joint probabilities

#### Detailed Questions by Year:

**2024 — Q7a (4 marks) — Robot Vacuum Bayesian Network**
- Robot vacuum stops (Evidence E). Hypotheses: H1=Battery low, H2=Dust full, H3=Motor overheated
- P(H1)=0.5, P(H2)=0.3, P(H3)=0.2
- P(E|H1)=0.7, P(E|H2)=0.8, P(E|H3)=0.9
- 1.Compute P(E) 2.Calculate P(H1|E), P(H2|E), P(H3|E) 3.Identify most likely cause 4.Justify

**2023 — Q7 (9 marks) — Multiple Bayes problems + Alarm Network**
- a) Three Bayes problems: (3)
  - i) Factory: 60% Machine A, 40% Machine B. Defect: 3% A, 5% B. Product found defective — P(Machine A)?
  - ii) Medical test: 98% accurate, 1% population has disease. Test positive — P(has disease)?
  - iii) Spam filter: prior spam=20%. P(word "offer"|spam)=80%, P(word "offer"|not spam)=10%. Calculate P(spam|contains "offer").
- b) Alarm Bayesian Network (Fire+Earthquake→Alarm→YakinCalls,SaminCalls): (6)
  - P(F)=0.004, P(E)=0.003, P(A|F,E)={TT:0.05,TF:0.94,FT:0.29,FF:0.001}
  - P(Y|A)={T:0.90,F:0.05}, P(S|A)={T:0.80,F:0.01}
  - i) Express joint distribution P(F,E,A,Y,S)
  - ii) P(alarm sounded, no fire, no earthquake, both Y and S call)
  - iii) P(alarm sounded, fire occurred, no earthquake, both Y and S call)

**2022 — B-3d (3 marks) — Alarm Network (different values)**
- B,E,A,Y,S = Burglary,Earthquake,Alarm,YakinCalls,SaminCalls
- P(F)=0.004, P(E)=0.003 [same topology as 2023]
- P(A|T,T)=0.05 [different from 2023 - check 0.94,0.29,0.001]

**2021 — Q7 (9 marks)**
- a) Concept of uncertainty: "doorbell rang at 12'0 clock in midnight, was someone there?" (2.75)
- b) Why deductive and adductive reasoning are not sound — source of uncertainty. (2.5)
- c) Bayes Theorem: Doctor knows meningitis causes stiff neck 40% of time. P(meningitis)=1/50000, P(stiff neck)=1/25. Find P(meningitis|stiff neck). (3.5)

**2021 — Q8a (3.5 marks) — Burglary Alarm Network**
- B,E,A,J,M = Burglary,Earthquake,Alarm,JohnCalls,MaryCalls
- P(B)=0.001, P(E)=0.002
- P(A|B,E)={TT:0.95,TF:0.94,FT:0.29,FF:0.001}
- P(J|A)={T:0.90,F:0.05}, P(M|A)={T:0.70,F:0.01}
- i) Express P(B,E,A,J,M) joint distribution
- ii) P(alarm sounds, no burglary, no earthquake, both Mary and John call)
- iii) P(alarm sounds, burglary, no earthquake, both Mary and John call)

---

### Topic 8 — Neural Networks + Machine Learning
**Source:** original lecture note.pdf · **Yield:** ⭐⭐⭐ 5/5 years · **Marks:** 7–9

#### 🔁 PATTERN:
- Always: ANN architecture + comparison with biological networks
- Sometimes: backpropagation numerical (sigmoid, weight update)
- Short notes: Fuzzy Logic + Uncertainty often combined here

#### Detailed Questions by Year:

**2024 — Q8 (9 marks)**
- a) What is learning? Describe inductive learning method with example. (3)
- b) Compare artificial and biological networks. What aspects of biological networks are not mimicked by artificial ones? What aspects are similar? (3)
- c) Short notes: i) Fuzzy logic ii) Uncertainty (3)

**2023 — Q8 (9 marks)**
- a) What is associative memory? Is it your belief that neural networks are fundamentally rooted in associative memory? Explain considering structure and principles of multilayer neural network architecture. (3)
- b) Sigmoid activation function scenario: neurons use sigmoid, perform forward pass + backward pass, update weights. True output y=0.6, learning rate=0.8. Network given with weights W13=0.1, W14=0.4, W23=0.8, W24=0.6, W35=0.3, W45=0.9. x1=0.35, x2=0.9. Execute additional forward pass. (6)

**2022 — B-1 (9 marks)**
- a) What is ANN? Compare artificial and biological networks — aspects not mimicked + similar. (3)
- b) What is learning? Describe inductive learning with example. (2)
- c) Supervised, unsupervised, reinforcement learning. (2)
- d) Short notes: Fuzzy Logic + Uncertainty. (2)

**2021 — Q8 (9 marks) — NN + Burglary Alarm Bayesian Network**
- See Bayesian Network details under Topic 7.

---

## Quick Lookup Table

| Topic | 2020 | 2021 | 2022 | 2023 | 2024 |
|-------|------|------|------|------|------|
| Intelligent Agents | A-Q1 | A-Q1 | A-1 | A-Q1 | A-Q1 |
| Search Algorithms | A-Q2(pt) | A-Q2 | B-4 | A-Q2 | A-Q2 |
| Alpha-Beta Pruning | A-Q3 | A-Q3d | A-4b | A-Q3b | A-Q3 |
| FC/BC + Rule-Based | A-Q4 | B-Q6a | B-3c | B-Q6 | B-Q6 |
| Hill Climbing + SA | A-Q2(pt) | A-Q3a | B-4a | A-Q3a | A-Q4b |
| CSP | — | A-Q3c | B-4d | A-Q3c | A-Q4(pt) |
| Fuzzy Logic | B-Q8(pt) | combined | B-1d | — | B-Q8(pt) |
| FOL + Resolution | B-Q5 | B-Q5 | A-2 | A-Q4 | A-Q4 |
| STRIPS + Planning | B-Q6 | B-Q6b | A-3 | B-Q5 | B-Q5 |
| Bayes + BN | B-Q7 | B-Q7,8 | B-3d | B-Q7 | B-Q7 |
| Neural Networks | B-Q8 | B-Q8 | B-1,2 | B-Q8 | B-Q8 |

---

## ⚠️ Critical Exam Notes

1. **Section A Q1 = Intelligent Agents** — guaranteed 9 marks, never skipped. Learn PAGE cold.
2. **Section A Q2 = Search** — guaranteed 5 marks from graph trace. Practice the fringe format.
3. **R1–R5 example appears verbatim every year** — memorize FC and BC traces.
4. **Block World appears verbatim every year** — same start/goal state.
5. **Bayesian Network topology repeats** — Fire/Earthquake/Alarm/Calls is the template.
6. **IDDFS added in 2024/2023** — new pattern, will likely repeat.
7. **2022 is structured differently** — FOL in Section A, Search in Section B. Know your topics not your section.
