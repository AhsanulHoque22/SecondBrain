# AES — Advanced Encryption Standard
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
**AES** is a symmetric block cipher operating on a $4\times4$ byte **state matrix** (128-bit block, filled column-major); AES-128 runs **10 rounds**, each (except the last) consisting of SubBytes, ShiftRows, MixColumns, AddRoundKey, with an initial AddRoundKey before round 1 and MixColumns dropped in the final round.

## Key steps / algorithm
**AES-128 structure (Lc#8 p5):**
1. **AddRoundKey($K_0$)** — XOR plaintext state with initial round key.
2. **Rounds 1–9** (identical): SubBytes → ShiftRows → MixColumns → AddRoundKey($K_i$).
3. **Round 10 (final)**: SubBytes → ShiftRows → AddRoundKey($K_{10}$) — **no MixColumns**.

**The 4 operations:**
- **SubBytes**: S-box substitution — split byte into (row=high nibble, col=low nibble), look up table. Example: `EA → 87`.
- **ShiftRows**: cyclic LEFT shift per row — Row 0: none, Row 1: left-1, Row 2: left-2, Row 3: left-3.
- **MixColumns**: multiply each column by fixed matrix $\begin{bmatrix}02&03&01&01\\01&02&03&01\\01&01&02&03\\03&01&01&02\end{bmatrix}$ in GF($2^8$).
  - GF($2^8$) rules: $01\times x=x$; $02\times x$ = left-shift, XOR `1B` if MSB overflow; $03\times x=(02\times x)\oplus x$.
- **AddRoundKey**: bitwise XOR state with round-key matrix.

**Plaintext → state matrix**: ASCII→hex per character, fill $4\times4$ matrix column-major (top-to-bottom, then next column).

**S-box via GF($2^8$) inverse + affine transform** (when inverse table is given instead of S-box table): $S(x)=\text{Affine}(\text{inv}(x))$, where $b'_i = b_i \oplus b_{(i+4)\bmod8} \oplus b_{(i+5)\bmod8} \oplus b_{(i+6)\bmod8} \oplus b_{(i+7)\bmod8} \oplus c_i$, $c=\texttt{63}$. Example: $\text{inv}(\texttt{C2})=\texttt{2F} \to S(\texttt{C2})=\texttt{25}$.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q3(a),(c) | Explain ShiftRows+MixColumns diffusion + perform ShiftRows on given state matrix (4); draw AES block diagram (2) |
| 2023 | Q3(c) | Draw AES encryption block diagram (4) |
| 2022 | Section B Q5 | $A_i=(11000010)_2=$`C2`hex; via GF($2^8$) inverse table + affine transform, $S(\texttt{C2})=\texttt{25}$ (1.5+4.5) |
| 2021 | Section B Q1(a) | Draw AES encryption block diagram (4.75) |
| 2020 | — | No AES question found |

🔁 4/5 years, 4–6 marks. **Block diagram is the highest-probability question** (2021/23/24) — memorize the exact 10-round structure.

## Weak spots / common mistakes
- Forgetting **Round 10 drops MixColumns** — this is the #1 diagram mistake.
- ShiftRows shifts are **cyclic LEFT**, amount = row index (0,1,2,3) — confusing with right shifts or column shifts.
- MixColumns $02\times x$: only XOR with `1B` if the **MSB before shifting was 1** (overflow check).
- When the exam gives the GF($2^8$) **multiplicative inverse table** (not the S-box table directly), the affine transform step is still required — don't stop at the inverse value.
- Plaintext-to-matrix fill order is **column-major**, not row-major.

## Related topics
[[wiki/des_feistel|DES/Feistel/S-box/Avalanche/3-DES]] — both ciphers use substitution tables and diffusion/avalanche concepts; AES's MixColumns+ShiftRows is the modern analogue of DES's permutation+S-box diffusion.
