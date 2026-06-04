# Propositional Logic + Resolution in PL
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Propositional Logic (PL) is a formal system where atomic sentences are combined with connectives (¬ ∧ ∨ → ↔) to form well-formed formulas, and truth is determined by model assignment.

## Key concepts
| Term | Meaning |
|---|---|
| **Satisfiable** | At least one assignment of T/F makes it true |
| **Valid (tautology)** | True under ALL assignments |
| **Contradictory** | False under ALL assignments |
| **Entailment** KB ⊨ α | Every model of KB is also a model of α |

## Inference rules
- **Modus Ponens:** P, P→Q ⊢ Q
- **Modus Tollens:** ¬Q, P→Q ⊢ ¬P
- **Resolution:** (P∨Q) ∧ (¬P∨R) → (Q∨R)

## 4-Step Clause Form Conversion (PL only)
1. Eliminate ↔: A↔B → (A→B)∧(B→A)
2. Eliminate →: A→B → ¬A∨B
3. Push ¬ inward (De Morgan): ¬(A∧B)→¬A∨¬B; ¬(A∨B)→¬A∧¬B; ¬¬A→A
4. Distribute ∨ over ∧ (CNF): A∨(B∧C) → (A∨B)∧(A∨C); split conjuncts into separate clauses

## Resolution Refutation (proof by contradiction)
1. Convert all KB sentences to clause form
2. Negate the goal; convert to clause form
3. Combine into clause set
4. Repeatedly apply resolution — add resolvents to set
5. Derive □ (empty clause) → contradiction → goal is **proved**

## Wumpus World Example (2021 Q4a, Q4d)
```
KB: R1: ¬P₁,₁
    R2: B₁,₁ ↔ (P₂,₁ ∨ P₁,₂)
    R4: ¬B₁,₁
```
2-step proof that P₁,₂ is false:
1. P₁,₂ + (¬P₁,₂ ∨ B₁,₁) → B₁,₁
2. B₁,₁ + ¬B₁,₁ → □ ✅

## Satisfiability check example (2021 Q4c)
`(P∨Q) ∧ (P∨¬Q) ∨ P`
→ Simplifies to P
→ **Satisfiable** (true when P=T, false when P=F)

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2021 | A-Q4a | Wumpus KB: infer safe cells using PL inference |
| 2021 | A-Q4b | Proof vs theorem — one-line distinction |
| 2021 | A-Q4c | Is (P∨Q)∧(P∨¬Q)∨P satisfiable/contradictory/valid? |
| 2021 | A-Q4d | Show P₁,₂ is false using resolution (2-step) |
| 2022 | A-2a | Write the wff→clause form algorithm (9-step) |
🔁 Repeats: Wumpus-style KB + resolution proof; satisfiability check on a formula

## Weak spots / common mistakes
- Stopping at CNF without splitting into individual clauses
- Proof vs theorem: **theorem** is a sentence provable from KB; **proof** is the derivation sequence
- 9-step CFC (asked in 2022): the full FOL version has extra steps (Skolemize, standardize, prenex) — don't confuse with the 4-step PL version

## Related topics
[[forward-backward-chaining]] · [[fol-resolution]]
