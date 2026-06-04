# STRIPS + Partial-Order Planning

> **Source:** Planning.pdf (50 slides) + plan2.pdf (38 slides) · **Yield:** 5/5 · **Marks:** 8–9

## Definition (exam-style)
**STRIPS** is a planning framework where the world = set of positive ground literals; actions = (Preconditions, Add-list, Delete-list). **Closed World Assumption**: anything not stated is false. Solves the **Frame Problem**: only explicit effects change state.

**POP (Partial-Order Planning)**: searches in plan space, not state space. Plan = (A, O, L) — actions, ordering constraints, causal links. Uses **least commitment**: defer ordering until forced by a threat.

---

## STRIPS Action Schema

```
Action: Name(parameters)
  Preconditions: conjunction of positive function-free literals
  Add-effects:   propositions that become TRUE
  Delete-effects: propositions that become FALSE
```

**Block world operators** (memorise preconditions — asked verbatim 2022):

| Action | Preconditions | Add | Delete |
|--------|--------------|-----|--------|
| PICKUP(b) | ONTABLE(b), CLEAR(b), ARMEMPTY | HOLDING(b) | ONTABLE(b), CLEAR(b), ARMEMPTY |
| PUTDOWN(b) | HOLDING(b) | ONTABLE(b), CLEAR(b), ARMEMPTY | HOLDING(b) |
| UNSTACK(b,c) | ON(b,c), CLEAR(b), ARMEMPTY | HOLDING(b), CLEAR(c) | ON(b,c), CLEAR(b), ARMEMPTY |
| STACK(b,c) | HOLDING(b), CLEAR(c) | ON(b,c), ARMEMPTY, CLEAR(b) | HOLDING(b), CLEAR(c) |

---

## POP Algorithm (7 steps)

1. Let P be initial plan (A₀ ≺ A∞)
2. Pick a **flaw** f (open condition OR unsafe link)
3. Resolve flaw:
   - If open condition → choose action S that achieves it → add causal link
   - If unsafe link → choose **promotion** (Ac ≺ At) or **demotion** (At ≺ Ap)
4. Update P
5. Return NULL if no resolution exists
6. If no flaws remain → return P
7. Else go to 2

**A₀**: no preconditions; effects = initial state; must be FIRST  
**A∞**: no effects; preconditions = goal; must be LAST  
**Causal link**: Ap →(Q)→ Ac means Ap achieves condition Q for consumer Ac  
**Threat**: At threatens (Ap, Q, Ac) if At deletes Q AND could come between Ap and Ac  

---

## The Standard 4-Block World (2022, 2023, 2024 — verbatim)

```
Initial: ON(B,A), ONTABLE(A), ONTABLE(C), ONTABLE(D), ARMEMPTY, CLEAR(B), CLEAR(C), CLEAR(D)
Goal:    ON(C,A), ON(B,D), ONTABLE(A), ONTABLE(D)
```

**Total-order solution**: UNSTACK(B,A) → STACK(B,D) → PICKUP(C) → STACK(C,A)

**POP ordering**: A₀ ≺ S₁=UNSTACK(B,A) ≺ S₂=STACK(B,D) ≺ S₃=PICKUP(C) ≺ S₄=STACK(C,A) ≺ A∞

Key causal links: A₀→(ON(B,A))→S₁, S₁→(HOLDING(B))→S₂, S₂→(ARMEMPTY)→S₃, S₃→(HOLDING(C))→S₄, S₁→(CLEAR(A))→S₄

**No unresolved threats** in this plan.

---

## Sussman Anomaly (2021 — Sussman Anomaly)

```
Initial: ON(C,A), ONTABLE(A), ONTABLE(B), CLEAR(C), CLEAR(B)
Goal:    ON(A,B), ON(B,C)
```

Actions (no arm):
- **A3**: Move-C-from-A-to-Table: PRE={ON(C,A), CLEAR(C)} ADD={ONTABLE(C), CLEAR(A)} DEL={ON(C,A)}
- **A1**: Move-B-from-Table-to-C: PRE={ONTABLE(B), CLEAR(B), CLEAR(C)} ADD={ON(B,C)} DEL={ONTABLE(B), CLEAR(C)}
- **A2**: Move-A-from-Table-to-B: PRE={ONTABLE(A), CLEAR(A), CLEAR(B)} ADD={ON(A,B)} DEL={ONTABLE(A), CLEAR(B)}

**Two threats**:
1. A₂ deletes CLEAR(B) → threatens A₀→(CLEAR(B))→A₁ → **Promotion**: A₁ ≺ A₂
2. A₁ deletes CLEAR(C) → threatens A₀→(CLEAR(C))→A₃ → **Promotion**: A₃ ≺ A₁

**Final ordering**: A₀ ≺ A₃ ≺ A₁ ≺ A₂ ≺ A∞

---

## Exam Pattern (2020–2024)

| Year | Question | What was asked |
|------|----------|----------------|
| 2024 | B-Q5 | STRIPS + Household Robot schema + Block World POP (causal links, ordering, why POP avoids backtracking) |
| 2023 | B-Q5 | STRIPS + Air Cargo schema (LOAD/UNLOAD/FLY) + same Block World POP |
| 2022 | A-3 | Preconditions of UNSTACK/STACK/PICKUP/PUTDOWN + Block World goal-stack + Generative AI short note |
| 2021 | B-Q6b | Sussman Anomaly — POP with threat resolution |
| 2020 | B-Q6 | STRIPS + Block World (exact details not captured) |

**What to write for "STRIPS definition"** (1 mark):
> STRIPS represents actions as (Preconditions, Add-effects, Delete-effects). The world state is a set of positive literals. Only explicit effects change the state (solves Frame Problem).

**Why POP avoids backtracking** (always asked with 5-mark POP question):
> POP uses least commitment — defers action ordering until a causal link is threatened. When threat detected, resolve via promotion (Ac ≺ At) or demotion (At ≺ Ap) without restarting search. Total-order planners commit to a sequence upfront and backtrack when goals interfere.

---

## Weak Spots / Common Mistakes

- Forgetting ARMEMPTY in UNSTACK and PICKUP preconditions
- Forgetting CLEAR(b) in STACK add-effects (b is on top, nothing above it)
- In Sussman: confusing which action is the THREAT vs which is the CONSUMER (promotion = push consumer before threat)
- In POP: causal link direction is Ap → Ac (producer → consumer), not reversed
- Not stating CLEAR(B), CLEAR(C), CLEAR(D) in initial state derivation — exam expects you to infer these

---

## Related Topics
[[propositional-logic]] · [[forward-backward-chaining]]
