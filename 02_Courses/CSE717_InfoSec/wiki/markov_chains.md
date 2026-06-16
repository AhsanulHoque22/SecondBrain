# Markov Chains — CSE 717 InfoSec

**Definition:** A Markov chain is a stochastic model where the probability of moving to the next state depends only on the current state (memoryless property). Described by a **transition matrix** $T$ where each row sums to 1.

---

## Core Algorithm — 5-Step Steady-State Solve

| Step | Action |
|------|--------|
| 1 | Build transition matrix $T$ (rows = from, columns = to; each row sums to 1) |
| 2 | Compute $T - I$ (subtract identity matrix) |
| 3 | Expand $[S \;\; C](T-I) = [0 \;\; 0]$ → extract one linear equation (both columns give same equation) |
| 4 | Apply normalization: $S + C = 1$ |
| 5 | Solve → state steady-state vector + interpret which state dominates |

**Key relation:** $VT = V \;\Leftrightarrow\; V(T-I) = 0$ with $\sum V_i = 1$

---

## Both Exam Questions Side-by-Side

| | 2024 Q1(c) [3 marks] | 2023 Q6(c) [4 marks] |
|--|----------------------|----------------------|
| States | Secure (S) / Compromised (C) | Secure (S) / Insecure (I) |
| S→S | 0.4 | 0.8 |
| other→S (recovery) | 0.3 | 0.6 |
| T matrix | $\begin{pmatrix}0.4&0.6\\0.3&0.7\end{pmatrix}$ | $\begin{pmatrix}0.8&0.2\\0.6&0.4\end{pmatrix}$ |
| Linear equation | $-0.6S + 0.3C = 0 \Rightarrow C = 2S$ | $-0.2S + 0.6I = 0 \Rightarrow S = 3I$ |
| Solution | $S = 1/3 \approx 0.333$, $C = 2/3 \approx 0.667$ | $S = 0.75$, $I = 0.25$ |
| Verdict | **Compromised** dominates | **Secure** dominates |

---

## Exam Pattern

- **2/5 years (2023 + 2024 — both most recent), 3–4 marks.** Strong recency signal.
- Always a **2-state security model** (Secure/Compromised or Secure/Insecure).
- Always asks: (1) find steady-state probabilities, (2) is system more secure or compromised long-run?
- Source: Lc#4A (theory + Sunny/Rainy weather worked example), Lc#4B (assignment numericals).

---

## Weak Spots / Common Mistakes

- **Row vs column:** rows = "from" state; each row must sum to 1. Don't transpose.
- **Missing probability:** if S→S = 0.4, then S→C = 0.6 automatically — fill it in before writing T.
- **Linear dependence:** the two column equations are always the same — drop one, use normalization as the second equation.
- **Always interpret:** just computing $\pi$ values isn't enough — state which outcome dominates and give the percentage.

---

## Related Topics

- [[hash_functions]] — hash properties (avalanche, collision-resistance) share "security state" framing
- [[game_theory]] — also appears in 2023 + 2024; both are "new" probability/game topics
- [[number_theory]] — no direct link, but both require careful algebra under exam pressure
