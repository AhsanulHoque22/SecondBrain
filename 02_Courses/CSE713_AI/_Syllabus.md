# CSE 713 — AI · Syllabus (CONFIRMED from lecture materials + past papers)
> [[_Topics]] · [[_TopicQuestionMap]] · [[00_Dashboard]]

> Updated 2026-05-29 by Claude Code after reading all PDFs + 5-year past paper analysis.
> Topics are ranked by exam yield. Study in this order.

---

## SECTION A TOPICS (Answer 3 of these in exam)

### TIER 1 — Must Know Cold (appeared 5/5 years, 5–9 marks each)

#### 1. Search Algorithms — State Space Search
**Source:** Lecture3_1_State_Space_Search.pdf, Chapter 3.pdf
**What to know:**
- State space representation: initial state, goal test, operators, path cost
- Uninformed: BFS, DFS, UCS (Uniform Cost Search), IDDFS
- Informed: Greedy Best-First Search, A* Search (f(n) = g(n) + h(n))
- Trace algorithms step-by-step on a given graph (show fringe at every step)
- Admissibility of heuristics
- Problem formulations: TSP, Water Jug, Missionaries & Cannibals, Robot Vacuum
- **Key exam graph:** A→G with step costs + h(n) table (2020, 2022, 2023, 2024)

#### 2. Alpha-Beta Pruning + Minimax
**Source:** Chapter 5.pdf
**What to know:**
- Minimax algorithm: MAX nodes (maximise), MIN nodes (minimise)
- Alpha-Beta Pruning: track α (MAX's best) and β (MIN's best) at every node
- Apply to a given game tree — show pruned branches
- Limitations of pure Minimax (exponential time, large trees)
- How Alpha-Beta addresses: time complexity, unnecessary node expansion
- Cutoffs: α-cutoff, β-cutoff, futility-cutoff
- "Waiting for Quiescence" concept
- **Key exam tree:** 3-level game tree (same structure 2020–2024)

#### 3. Forward + Backward Chaining + Rule-Based Systems
**Source:** Rule-Based Systems.pdf
**What to know:**
- Architecture of a rule-based expert system (rule base, database, inference engine)
- Forward Chaining (data-driven): propagate truth from facts to goal
- Backward Chaining (goal-driven): backtrack from goal to facts
- Factors determining which to use
- Conflict resolution: two approaches
- **THE R1–R5 RULE BASE (memorise — appears verbatim every year):**
  ```
  R1: IF A and C THEN E      Initial facts: A, B (both true)
  R2: IF C and D THEN F      Goal: Prove G
  R3: IF B and E THEN F
  R4: IF B THEN C
  R5: IF F THEN G
  FC path: B→C(R4), A∧C→E(R1), B∧E→F(R3), F→G(R5)
  ```
- Draw propagation tree (FC) and backtrack tree (BC) diagrammatically

#### 4. FOL + Resolution + Inference
**Source:** Propositional Logic.pdf (pp. 1-104), Chapter 4.pdf
**What to know:**
- **Why FOL?** PL limitation: can't express infinite-domain statements ("All dogs are faithful" needs one prop per dog); FOL adds variables, predicates, quantifiers (∀, ∃)
- FOL/Predicate Logic = generalisation of PL for infinite models ("All men are mortal", "Some birds can't fly")
- Predicates, quantifiers (∀, ∃), variables, constants; WFF construction
- Inference rules: Universal Elimination, Modus Ponens, Resolution
- **Clauses**: Literal = single proposition or its negation; Clause = disjunction of literals
- **4-step algorithm — Convert to Clausal Form (Disjunctive Normal Form)**:
  1. Eliminate implication signs (P→Q becomes ¬P ∨ Q)
  2. Eliminate double negation; reduce scope of ¬ using De Morgan's law
  3. Convert to Conjunctive Normal Form (CNF) using distributive and associative laws
  4. Extract the set of clauses
- **Resolution principle**: if (x∨s1) AND (¬x∨s2) → resolvent = (s1∨s2); x is "resolved upon"
- **Procedure for Resolution** (proof by refutation):
  1. Convert all premises to clausal form
  2. Negate the goal; convert to clausal form
  3. Combine all clauses into a set
  4. Iteratively apply resolution, adding resolvents to the set
  5. If null clause □ derived → contradiction → goal is TRUE (proved)
- **Practice example (quiz in slides)**: mammals drink milk; man is mortal; man is mammal; Tom is a man. Prove Tom drinks milk and Tom is mortal — by modus ponens AND by resolution
- **THE MARCUS/POMPEII SET (memorise — appears 2020–2022, robots/drones variant 2023–2024):**
  - Marcus was a man, Pompeian, born 40 AD
  - All Pompeians died in 79 AD volcano; no mortal lives >150 years
  - Prove: Marcus is not alive now (by resolution refutation)
- Forward chaining in FOL (2024: drone route finding with FOL predicates)

#### 5. Intelligent Agents + Environments
**Source:** Ch01-02.pdf
**What to know:**
- Define AI: 4 approaches (think rationally, act rationally, think like human, act like human)
- Turing Test: what it measures, LLM performance vs limitations
- Define intelligent agent: percepts, actions, goals, environment (PAGE)
- Environment types: fully/partially observable, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous, single/multi-agent
- Agent architectures: simple reflex, model-based reflex, goal-based, utility-based, learning
- Apply to real scenarios: Mars Rover (Curiosity, Perseverance), Agricultural Robot Bangladesh
- Recent AI advancements: LLMs, ChatGPT limitations

---

## SECTION B TOPICS (Answer 3 of these in exam)

### TIER 1 — Must Know Cold (appeared 5/5 years, 7–9 marks each)

#### 6. STRIPS + Partial-Order Planning (Block World)
**Source:** Planning.pdf, plan2.pdf
**What to know:**
- What is STRIPS? Action schema: preconditions, add-effects, delete-effects
- Operators: UNSTACK(A,B), STACK(A,B), PICKUP(A), PUTDOWN(A) — preconditions of each
- Partial-Order Planning (POP): minimal plan, causal links, ordering constraints
- Goal Stack Planning
- How POP avoids backtracking vs total-order planning
- Sussman Anomaly (2020, 2021)
- **THE BLOCK WORLD PROBLEM (same every year):**
  ```
  Start: ON(B,A), ONTABLE(A), ONTABLE(C), ONTABLE(D), ARMEMPTY
  Goal:  ON(C,A), ON(B,D), ONTABLE(A), ONTABLE(D)
  ```
- Air Cargo Transport domain (2023 variant)
- Household Robot domain (2024 variant)

#### 7. Bayes' Theorem + Bayesian Networks
**Source:** Reasoning with Uncertainty.pdf
**What to know:**
- Bayes' Theorem: P(H|E) = P(E|H)·P(H) / P(E)
- Computing total probability P(E) = Σ P(E|Hi)·P(Hi)
- Posterior probabilities: compute and compare to identify most likely hypothesis
- Bayesian Networks: topology, Conditional Probability Tables (CPTs)
- Joint distribution expressed as product of conditionals
- Challenges in Bayesian decision theory
- Evidential Reasoning (ER): high-level attribute via lower-level attributes, combined degree of belief
- **THE ALARM NETWORK (same 2022–2024):**
  - Fire, Earthquake → Alarm → Mr. X calls, Mr. Y calls
  - Compute: P(alarm sounds but no fire/earthquake and both call)
- **ROBOT VACUUM (2024):**
  - H1: Battery low, H2: Dust full, H3: Motor overheated
  - Compute P(E), posteriors, identify most likely cause

#### 8. Neural Networks + Machine Learning
**Source:** original lecture note.pdf (Neural Computing: The Basics)
**What to know:**
- What is Machine Learning? Methods: neural computing, statistical, inductive, genetic algorithms
- ANN vs Biological Neural Networks: similarities and differences
  - Biological: Neurons, Dendrites (inputs), Axon (output), Synapses (weights)
  - ANN: Processing Elements, connections, weights, activation function
- ANN Architecture: input layer, hidden layer(s), output layer
- Feedforward vs Recurrent architectures
- Transfer (Activation) Functions: Sigmoid (Y = 1/(1+e^-V)), Threshold
- ANN Learning: adjust weights → compute output → compare → update
  - Delta = Z - Y (error); W(final) = W(initial) + α × Delta × X
  - Learning rate α: too high → diverge, too low → slow
- Supervised vs Unsupervised Learning
- **Back Propagation:** error propagated backward through layers; E = ½Σ(Z-Y)²
- Inductive learning method with example
- Benefits and Limitations of Neural Networks
- Competitive Learning Networks (2022 questions)
- **BACKPROP NUMERICAL (2023):** sigmoid activation, given weights and true output, update weights

### TIER 2 — Know Well (4/5 years, 1–4 marks)

#### 9. Hill Climbing + Simulated Annealing
**Source:** Chapter 4.pdf (Local Search)
**What to know:**
- Hill Climbing: deterministic, greedy local improvement
- 3 limitations: local maxima, plateaux, ridges
- Simulated Annealing: non-deterministic, escape from local optima via probabilistic acceptance
- SA as solution to HC limitations
- Application: drone route optimization (2024), robot navigation (2023)

#### 10. CSP — Constraint Satisfaction Problems
**Source:** 20_CSP.pdf
**What to know:**
- Variables, domains, constraints
- Map coloring problem (4-color theorem)
- Cryptarithmetic: SEND+MORE=MONEY
- Constraint propagation, backtracking
- Small marks — don't over-invest

#### 11. Fuzzy Logic + Uncertainty
**Source:** FuzzyLogic-14.pdf, Lec2012-3-159741-FuzzyLogic-v.2.pdf
**What to know:**
- Short notes only: what is fuzzy logic, membership functions, contrast with crisp logic
- What is uncertainty in AI? Sources and handling
- Evolutionary method / Genetic Algorithms: what, example

---

## Topic Priority for 5-Day Study Plan

| Day | Topics | Exam yield |
|-----|--------|-----------|
| Day 1 (Jun 1) | Agents + Search Algorithms | ⭐⭐⭐ + ⭐⭐⭐ |
| Day 2 (Jun 2) | Alpha-Beta Pruning + Hill Climbing/SA | ⭐⭐⭐ + ⭐⭐ |
| Day 3 (Jun 3) | Forward/Backward Chaining + Rule-Based | ⭐⭐⭐ |
| Day 4 (Jun 4) | FOL/Resolution + STRIPS/Planning | ⭐⭐⭐ + ⭐⭐⭐ |
| Day 5 (Jun 5) | Bayes/BN + Neural Networks + CSP/Fuzzy | ⭐⭐⭐ + ⭐⭐⭐ + ⭐ |

## Exam Structure Reminder
- Full marks: 54 · Duration: 4 hours
- Format: Answer any 3 from Section A + any 3 from Section B
- Targeting 6 × 9 marks = 54 → perfect score possible by mastering 6 core topics
