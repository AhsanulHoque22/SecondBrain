# Bayes' Theorem + Bayesian Networks

> [[_index]] · [[_Topics]] · [[_TopicQuestionMap]]

## Definition
A **Bayesian Network** is a directed acyclic graph (DAG) representing causal relationships between random variables, where each node has a conditional probability table (CPT) encoding the probability of that variable given its parents. Used to compute posterior beliefs under uncertainty.

---

## Core Formulas

| Formula | Name |
|---------|------|
| $P(H_i\|E) = \frac{P(E\|H_i) \cdot P(H_i)}{\sum_k P(E\|H_k)\cdot P(H_k)}$ | Extended Bayes' Theorem |
| $P(H\|E,e) = \frac{P(H\|E)\cdot P(e\|E,H)}{P(e\|E)}$ | Sequential update (new evidence) |
| $P(x_1,\ldots,x_n) = \prod_i P(x_i\|\text{Pa}(x_i))$ | BN joint factorization (chain rule) |
| $P(E) = \sum_i P(E\|H_i)\cdot P(H_i)$ | Total probability |

---

## Algorithm / Key Steps

**Extended Bayes (given evidence E, K hypotheses):**
1. Identify all hypotheses $H_1,\ldots,H_K$ and their priors $P(H_i)$
2. Get likelihoods $P(E|H_i)$ for each hypothesis
3. Compute $P(E) = \sum_k P(E|H_k)\cdot P(H_k)$ (total probability)
4. Compute each posterior: $P(H_i|E) = P(E|H_i)\cdot P(H_i) / P(E)$
5. Check: $\sum_i P(H_i|E) = 1$ ✓

**BN Joint Probability (given network):**
1. Write joint = product of $P(\text{node}|\text{parents})$ for every node
2. For root nodes (no parents): use prior probabilities
3. Substitute given values (T/F) for each variable
4. Multiply all factors

**BN Properties:**
- Root nodes → prior probability tables; all others → CPTs
- Markov condition: each node independent of non-descendants given its parents
- Polytree: BN with at most one undirected path between any two nodes (tractable inference)
- d-separation determines conditional independence between sets of nodes

---

## Exam Pattern (2020–2024)

| Year | Q# | Type | Key |
|------|----|------|-----|
| 2024 | Q7a | Extended Bayes (3 hypotheses) | P(E)=0.77; H1 most likely (45.45%) |
| 2024 | Q7b | Challenges in Bayesian decision theory | 5 challenges: prior elicitation, NP-hard inference, sensitivity, independence assumptions, data needs |
| 2024 | Q7c | Evolutionary method | GA: population, fitness, selection, crossover, mutation |
| 2023 | Q7a | Three Bayes calculations | Factory→0.4737; Medical→0.3311; Spam→0.667 |
| 2023 | Q7b | Alarm BN (F+E→A→X,Y) | P(F)=**0.4**, P(E)=**0.6** ← NOT 0.004/0.003 |
| 2022 | B-3d | Alarm BN (F+E→A→Yakin,Samin) | P(F)=0.004, P(E)=0.003 ← these are 2022 values |
| 2021 | Q7a | Uncertainty concept (doorbell) | Abductive/deductive both fail |
| 2021 | Q7b | Why deductive/abductive not sound | Incomplete model; affirming consequent |
| 2021 | Q7c | Meningitis Bayes | P(M\|S)=0.0002 (base rate matters!) |
| 2021 | Q8a | CPT count (Burglary→Alarm1,Alarm2) | CPT=5 params vs joint table=7 params |
| 2021 | Q8b | Burglary BN (B+E→A→J,M) | Standard 5-node network |
| 2020 | Q7a | Uncertainty concept (doorbell) | Same as 2021 Q7a |
| 2020 | Q7d | Extended Bayes — equations + semantics | Both forms; 5 application areas |
| 2020 | Q8a | BN syntax and semantics | N=(X,G,P); Markov condition; chain rule |
| 2020 | Q8c | Complex BN (B+E→A→R,C) | P(B)=0.02; P(A)≈0.02867; P(B\|A)≈0.628 |

**Recurring topology:** Two root causes → Alarm → Two callers. Appears in 2020, 2021, 2022, 2023, 2024.

---

## Key Numeric Results (memorise cold)

| Problem | Answer |
|---------|--------|
| 2024 Q7a: P(E) | 0.77 |
| 2024 Q7a: P(H1\|E) | 0.4545 (battery most likely) |
| 2023 Q7a(i) factory | 0.4737 |
| 2023 Q7a(ii) medical | 0.3311 |
| 2023 Q7a(iii) spam | 0.6667 = 2/3 |
| 2023 Q7b(i) alarm ¬F¬E | 0.001344 |
| 2023 Q7b(ii) alarm F¬E | 0.08064 |
| 2021/2020 meningitis | **0.0002** = 1/5000 |
| 2021 Q8a: CPT params | **5** (BN) vs **7** (joint table) |
| 2021 Q8b(ii) ¬B¬E | 6.28×10⁻⁴ |
| 2021 Q8b(iii) B¬E | 5.91×10⁻⁴ |
| 2022 B-3d(ii) ¬F¬E | 7.15×10⁻⁴ |
| 2022 B-3d(iii) F¬E | 2.70×10⁻³ |

---

## Uncertainty Concept (Doorbell Example)

**Two propositions:**
- Prop1: AtDoor(x) → Doorbell
- Prop2: Doorbell → Wake(Karim)

**Why reasoning fails:**
- **Abductive** (Was someone at door?): Prop1 has infinite possible antecedents → incomplete
- **Deductive** (Did Karim wake?): Prop2 is not a tautology → often true, not always

**Sources of uncertainty:** weak implications, imprecise language (often/rarely), incomplete knowledge, conflicting information, propagation of uncertainties.

---

## Extended Bayes — Two Forms

**Form 1 (multiple hypotheses):**
$$P(H_i|E) = \frac{P(E|H_i)\cdot P(H_i)}{\sum_{k=1}^{K} P(E|H_k)\cdot P(H_k)}$$

**Form 2 (sequential update):**
$$P(H|E,e) = \frac{P(H|E)\cdot P(e|E,H)}{P(e|E)}$$

**Application areas:** medical diagnosis, spam filtering, robot localization, weather forecasting, fault diagnosis.

---

## BN Inference Types (4 patterns)

| Type | Direction | Example |
|------|-----------|---------|
| Diagnostic | Effects → Causes | Given John calls, find P(Burglary) |
| Causal | Causes → Effects | Given Burglary, find P(John calls) |
| Inter-causal | Between causes | Given Alarm+Earthquake, find P(Burglary) |
| Mixed | Some causes + some effects | Given John calls + ¬Earthquake, find P(Alarm) |

---

## Weak Spots / Common Mistakes

- **2023 vs 2022 values:** 2023 uses P(F)=0.4, P(E)=0.6; 2022 uses P(F)=0.004, P(E)=0.003. Don't swap them.
- **Meningitis trap:** P(M|S)=0.0002 (answer), NOT P(S|M)=0.40 (given likelihood)
- **Joint factorization:** must include EVERY node in the chain — forget one and the answer is wrong
- **Posterior check:** $\sum_i P(H_i|E)$ must equal 1.0 after computation
- **Prior × Likelihood ≠ Posterior** without dividing by P(E)

---

## Related Topics

- [[propositional-logic]] — probabilistic reasoning extends classical logic
- [[forward-backward-chaining]] — rule-based vs probabilistic inference contrast
