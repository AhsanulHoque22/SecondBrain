# DES / Feistel Structure / S-box / Avalanche / 3-DES
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
DES is a 16-round **Feistel-structure** block cipher (64-bit blocks, 56-bit key). Each round splits the block into halves and applies a round function $F$ using a non-linear S-box substitution; **3-DES** chains DES three times (EDE) to extend the effective key length without breaking backward compatibility.

## Key steps / algorithm
**1. Classical Feistel structure** (one round):
$$L_i = R_{i-1}, \qquad R_i = L_{i-1} \oplus F(R_{i-1}, K_i)$$
Same algorithm decrypts — just apply subkeys $K_{16},\dots,K_1$ in reverse order.

**2. IP / IP⁻¹** — pure bit-reordering permutations before round 1 / after round 16 (on $R_{16}\|L_{16}$). **No cryptographic strength**, hardware convenience only.

**3. F-function (4 stages):** Expansion $E$ (32→48) → XOR with $K_i$ → S-box substitution $S_1$–$S_8$ (48→32, **only non-linear step**) → Permutation $P$ (32→32).

**4. S1-box lookup:** input $b_1b_2b_3b_4b_5b_6$ → row = $b_1b_6$, col = $b_2b_3b_4b_5$. For input **37** ($100101_2$): row=3, col=2 → $S_1(37) = \mathbf{8}$.

**5. Avalanche effect:** 1-bit input change → large unpredictable ciphertext change (~half the bits flip).

**6. Two DES attack families:** **Differential cryptanalysis** (Biham-Shamir) and **Linear cryptanalysis** (Matsui).

**7. 3-DES (EDE):** $C = E_{K_3}(D_{K_2}(E_{K_1}(P)))$. If $K_1=K_2=K_3$ → collapses to single DES (backward compatible). 2-key → ~112-bit security, 3-key → ~168-bit.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q6(d) | Avalanche effect + 2 attack families (2) |
| 2023 | Q3(a,b) + Section B Q5(a) | 3-DES diagram+equation, avalanche+attacks, F-function (5+2.5) |
| 2022 | Q4 | Why S-box + S1(37)=8, 3-DES schematic+equation, F-function components (8) |
| 2021 | A4 | IP⁻¹ equation, 3-DES diagram+equation, avalanche+attacks (9.5) |
| 2020 | Q4 + Section B Q5 | IP/IP⁻¹ + S1(37), IP⁻¹ decryption eqn + finite fields, 3-DES×2, avalanche+attacks, Feistel structure (9.5+8.25) |

🔁 5/5 years — guaranteed 5–10 marks, cycling through the 6 sub-patterns above.

## Weak spots / common mistakes
- Forgetting the **swap before IP⁻¹**: ciphertext = $IP^{-1}(R_{16}\|L_{16})$, not $L_{16}\|R_{16}$.
- Confusing EDE order — middle stage is **decrypt**, not encrypt (this is what gives backward compatibility when keys are equal).
- S1(37): row = outer bits ($b_1b_6$), column = inner 4 bits — easy to swap.

## Related topics
[[wiki/symmetric_asymmetric|Symmetric/Asymmetric & Block/Stream Ciphers]] (Feistel structure also asked there), [[wiki/hash_functions|Hash Functions]] (avalanche effect shared concept)
