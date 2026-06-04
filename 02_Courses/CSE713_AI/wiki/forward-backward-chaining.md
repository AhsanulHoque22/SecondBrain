# Forward + Backward Chaining + Rule-Based System
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
A rule-based expert system fires IF-THEN rules against a working memory of facts (FC: data-driven forward; BC: goal-driven backward) to prove or derive a goal.

## Architecture
| Component | Role |
|---|---|
| Rule base | Set of IF-THEN rules (R1–R5) |
| Working memory | Known facts at any point |
| Inference engine | Applies rules; detects conflicts |

## The R1–R5 Example (verbatim every year)
```
R1: IF A AND C THEN E      Initial facts: A, B
R2: IF C AND D THEN F      Goal: Prove G
R3: IF B AND E THEN F
R4: IF B THEN C
R5: IF F THEN G
```

## Forward Chaining (FC) — data-driven
1. Start with known facts {A, B}
2. Find all rules whose LHS is satisfied → fire them → add conclusions to facts
3. Repeat until goal found or no new facts

**FC trace (memorise):**
- {A,B} → R4 fires (B→C) → {A,B,C}
- → R1 fires (A∧C→E) → {A,B,C,E}
- → R3 fires (B∧E→F) → {A,B,C,E,F}
- → R5 fires (F→G) → **G ✅** (R2 never fires — D not in KB)

## Backward Chaining (BC) — goal-driven
1. Start from goal G
2. Find rules that conclude G → need their preconditions
3. Recurse on each precondition until all are facts or derivable

**BC trace (memorise):**
- G ← R5 ← need F
- F ← R2? (need D — not in KB, fail) → R3 (need B✅ + E)
- E ← R1 ← need A✅ + C
- C ← R4 ← need B✅ → **C✅ → E✅ → F✅ → G✅**

## When to use FC vs BC
| Use FC when | Use BC when |
|---|---|
| Many goals possible; goal unknown | Specific goal known; want to check if provable |
| New facts arrive continuously | Many rules, few goals — avoid irrelevant firing |
| Forward inference is natural | Backward decomposition is cleaner |

## Conflict Resolution (when multiple rules fire at once)
1. **Recency** — fire the rule matching the most recently added facts
2. **Specificity** — fire the most specific rule (most conditions)
3. **Refractoriness** — don't re-fire a rule on the same facts

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | B-Q6 | FC/BC definition + factors + R1–R5 prove G + draw both trees |
| 2023 | B-Q6 | Same structure; conflict resolution (1 mark) |
| 2022 | B-3b,c | FC/BC definition + factors + R1–R5 trees |
| 2021 | B-Q6a | R1–R5 prove G using FC and BC with search trees |
| 2020 | A-Q4 | FC/BC with R1–R5, factors for choosing |
🔁 Repeats every year: R1–R5 rule set + draw FC propagation tree + BC backtracking tree

## Weak spots / common mistakes
- Drawing only the path sequence, not the actual tree diagram — trees earn the marks
- Forgetting R2 never fires (D is not in KB)
- BC tree: confusing AND nodes (all preconditions must hold) with OR nodes (alternative rules)

## Related topics
[[propositional-logic]] · [[fol-resolution]]
