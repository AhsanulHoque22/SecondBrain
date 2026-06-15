# Game Theory & Nash Equilibrium
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
**Game theory** models the payoffs of two players' strategy choices via a **payoff matrix**; a **Nash Equilibrium (NE)** is a strategy combination where neither player can improve their own payoff by unilaterally switching, given the other's choice — a game can have 0, 1, or multiple NEs.

## Key steps / algorithm
**The 6-step "underline" method (Lc#3) to find ALL NEs in a 2×2 matrix:**
1. Pretend you are the row player (P1).
2. Fix the column player's (P2's) action (look down one column).
3. Find P1's best (highest) payoff in that column → underline it.
4. Repeat for P2's other action (other column).
5. Switch roles: for each row (P1's action fixed), find P2's best payoff across that row → underline it.
6. **Any cell with BOTH numbers underlined = a Nash Equilibrium.**

**Dominant strategy check:** for each player, compare their payoffs for a fixed strategy across ALL of the opponent's actions. If one strategy is strictly better in *every* case → that's a **strictly dominant strategy**.

**Worked example (Lc#3):** $\begin{array}{c|cc} & C & D \\\hline A & 10,2 & 8,3 \\ B & 12,4 & 10,1 \end{array}$ → unique NE $=(B,C)=(12,4)$; P1's dominant strategy = B (12>10 in both columns).

**Coordination games can have TWO NEs** — e.g. 2024 Eve/Mallory (both prefer matching, but disagree which): NE₁=(PT,PT)=(4,3), NE₂=(ND,ND)=(3,4).

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Section B Q7(a) | Eve/Mallory PT vs ND payoff matrix → find ALL NEs (two: (PT,PT) and (ND,ND)) + neither player has a strictly dominant strategy (3) |
| 2023 | Section B Q8(a) | Alice/Bob ST#1 vs ST#2 payoff matrix → unique NE=(ST#1,ST#1)=(10,10); BOTH players have ST#1 as strictly dominant (3) |
| 2023 | Q4(b) | "Design a strategy to identify attackers in a mobile social network" — server/node game, surveillance trade-off, Nash equilibrium balances security vs. service quality (3) |
| 2020–2022 | — | No Game Theory question found — NEW topic for 2023+2024 |

🔁 2/5 years, both MOST RECENT (2023, 2024) — strong recency signal for 2026.

## Weak spots / common mistakes
- Stopping after finding ONE NE — coordination games (2024-style) can have **two**.
- Confusing "best response" with "dominant strategy" — dominant means best regardless of opponent's choice; best-response is conditional on a specific opponent action.
- For the "design a strategy" conceptual question (2023 Q4(b)), don't just define NE — describe the **server vs. node model** (actions: nothing/packet/surveillance vs. forward/ignore/damage) and the **security-vs-service trade-off**.
- Always draw the matrix with underlines shown — it's the method proof.

## Related topics
[[wiki/markov_chains|Markov Chains]] — both are "small mathematical model" topics newly emphasized in 2023/2024 papers; similar low-investment, high-mechanical-marks profile.
