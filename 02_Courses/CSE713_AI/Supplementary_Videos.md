# CSE 713 AI — Supplementary Videos for Missing Topics
> [[02_Courses/CSE713_AI/_Topics|AI Topics]] · [[02_Courses/CSE713_AI/_TopicQuestionMap|Question Map]] · [[00_Dashboard]]

> Videos covering gaps not in the main FOL/Resolution playlist.
> Main playlist: `https://youtube.com/playlist?list=PLcGpEOlyH5z9t6ufvNzzeqMSJENObQdvs`
> Last updated: 2026-06-03

---

## Watch Order (Priority → Low)

| Priority | Topic | Videos | Exam Marks |
|:---:|-------|--------|:---:|
| 🔴 | [[#Rule-Based Systems]] | #1, #2 | 6–9 marks |
| 🔴 | [[#FOL Syntax Terms Predicates Quantifiers]] | #3, #4 | 1–2 marks |
| 🟡 | [[#Horn Sentences + Skolemization]] | #5, #6 | 1.5 marks |
| 🟡 | [[#FOL Translation Practical Scenarios]] | #7, #8 | 4–5 marks |
| 🟢 | [[#Knowledge Representation and Mapping]] | #9 | 1.5 marks |
| 🟢 | [[#Evidential Reasoning Dempster-Shafer]] | #10 | 2 marks |

---

## Rule-Based Systems

> **Highest priority — completely missing from main playlist. Verbatim every year (6–9 marks).**
> After watching: do one cold trace of R1–R5 from memory using `RuleBased_Solutions.pdf`.

**Video 1** — Architecture + FC/BC with rule examples
[Artificial Intelligence | Lecture 15: Rule Based Expert Systems - Forward and Backward Chaining](https://www.youtube.com/watch?v=MZwHQVnXAjE)
- Rule base, working memory, inference engine architecture
- FC trace with rule firing sequence
- BC trace with goal-driven backtracking

**Video 2** — FC vs BC + Conflict Resolution
[3.9 Types of Rule Based System | Forward Chaining & Backward Chaining | Artificial Intelligence](https://www.youtube.com/watch?v=jHfaVoKQPhs)
- When to use FC vs BC (data-driven vs goal-driven)
- Conflict resolution: recency, specificity, refractoriness

---

## FOL Syntax: Terms, Predicates, Quantifiers

> The main playlist jumps straight to WFFs — these fill the theory gap.

**Video 3** — Full FOL intro: terms, constants, variables, predicates, ∀, ∃
[L56: First Order Logic (FOL) | Predicate Logic Introduction | Quantifiers in Predicate Logic | AI](https://www.youtube.com/watch?v=Q_15qjqX-RE)
- Constants vs variables vs functions
- Predicate syntax: unary (property), binary (relation), zero-arg (proposition)
- Universal and existential quantifier usage

**Video 4** — Predicate types, quantifier scope, bound/free variables
[Concept of Predicates — First Order Logic (GATE)](https://www.youtube.com/watch?v=RwrgXAGnoHs)
- Universal quantifier: `∀x dog(x) → faithful(x)`
- Existential quantifier: `∃x planet(x) ∧ haslife(x)`
- Duality: `∀x ¬P(x) ≡ ¬∃x P(x)`

---

## Horn Sentences + Skolemization

> Critical for understanding *why* the 9-step CFC works. Covers steps 6–7 of canonical form.

**Video 5** — Horn clauses: what they are and why they matter
[Horn Clause in Artificial Intelligence with Example](https://www.youtube.com/watch?v=htidfFH7nUs)
- Horn clause = atomic sentence OR implication with conjunction of atoms on left, single atom on right
- Why FC/BC work only on Horn clauses
- `Perfect_sq(36)` and `∀x,y PerfSq(x) ∧ Prime(y) ∧ Divides(y,x) → Divides(square(y),x)` as examples

**Video 6** — Skolemization: constant vs function rule
[Skolemization in Artificial Intelligence | Skolemization Explained](https://www.youtube.com/watch?v=kiRbcnTWpzc)
- `∃y` outside any `∀` → Skolem **constant** (e.g., `p`)
- `∀x ∃y` → Skolem **function** (e.g., `g(x)`)
- The `g(36)` trick used in Perfect Square resolution proof

---

## FOL Translation: Practical Scenarios

> 2023 Q4a (self-driving car, 5 marks) is pure FOL translation — no video in main playlist covers this type.

**Video 7** — Encoding real-world sentences as FOL predicates
[Predicate Logic in Artificial Intelligence | First Order Predicate Logic FOL | Knowledge Representation](https://www.youtube.com/watch?v=cOXT86_KZGI)
- Declare predicates before writing sentences (exam requirement)
- Translate natural language → `∀x ∀d Car(x) ∧ Reachable(x,d) ∧ ¬Obstacle(d) → Moves(x,d)`

**Video 8** — ∀/∃ with domain examples (agents, robots, scenarios)
[FOL using Quantifiers | Examples | Artificial Intelligence | Bhanu Priya](https://www.youtube.com/watch?v=x5GfV8ORetQ)
- Multiple real-world FOL encoding examples
- Practice for 2023-style FOL definition questions

---

## Knowledge Representation and Mapping

> 2022 A-2c asks: "What are the roles of KR?" — 1.5 marks. One short video is enough.

**Video 9** — All 5 roles of KR in intelligent systems
[Knowledge Representation in AI | Role | Challenges | Core Methods](https://www.youtube.com/watch?v=6wzGEWKzPRo)
- **5 roles to memorise:** Surrogate · Ontological commitment · Inferential foundation · Medium of expression · Efficient computation
- Challenges: representational adequacy, inferential adequacy, efficiency

---

## Evidential Reasoning: Dempster-Shafer

> 2024 Q4a,b — only 2 marks total. Watch Video 10 only; skip 11–12 if pressed for time.

**Video 10** ⭐ *Best single video* — Bel, Pl, combination rule
[Dempster-Shafer Theory of Evidential Reasoning | Artificial Intelligence | Intelligent Systems](https://www.youtube.com/watch?v=sjbxhpnrecA)
- Basic probability assignment (mass function)
- `Bel(H)` = committed belief, `Pl(H)` = plausibility upper bound
- Dempster's rule: `m₁⊕m₂(A) = Σ_{B∩C=A} m₁(B)·m₂(C) / (1−K)`
- Conflict factor `K` = sum of masses for disjoint sets

**Video 11** — Theory part A (if more depth needed)
[3A — Dempster Shafer Theory of Evidential Reasoning](https://www.youtube.com/watch?v=ANv6-HK2Tus)

**Video 12** — Theory part B with examples
[3B — Dempster-Shafer Theory of Evidential Reasoning](https://www.youtube.com/watch?v=k55c4it6UHU)

---

## What the Main Playlist Already Covers (Don't Rewatch)

| Topic | Videos in Main Playlist |
|-------|------------------------|
| Modus Ponens / Inference Rules in PL | #1–5 |
| Model Checking (Truth Table) | #6 |
| CNF Conversion (PL + FOL) | #7–8, #19–21 |
| Resolution in PL (refutation) | #9–10 |
| Forward + Backward Chaining in PL | #11–12 |
| Wumpus World | #13–14 |
| WFF in Predicate Logic / Marcus examples | #15–18 |
| Unification in FOL | #22–23 |
| Resolution in FOL (complete proofs) | #24–26 |
| FC + BC in FOL | #27–28 |

---

## Related Files
- [[02_Courses/CSE713_AI/FOL_Resolution_Solutions|FOL & Resolution Past Paper Solutions PDF]]
- [[02_Courses/CSE713_AI/RuleBased_Solutions|Rule-Based Systems Solutions PDF]]
- [[02_Courses/CSE713_AI/_TopicQuestionMap|Past Paper Question Map]]
