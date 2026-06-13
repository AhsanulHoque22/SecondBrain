# Classical Ciphers
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Classical ciphers (Caesar, Playfair, Vigenère, Hill, OTP) are pre-modern substitution/transposition encryption schemes built on modular arithmetic over the 26-letter alphabet (A=0...Z=25); they form the foundation for discussing cryptanalysis, key management, and perfect secrecy.

## Key steps / algorithm
1. **Caesar:** $C=(P+k)\bmod 26$ (encrypt), $P=(C-k)\bmod 26$ (decrypt). General affine form $C=(aP+b)\bmod 26$.
2. **Playfair (encryption):** (1) strip spaces/punctuation, uppercase, merge I/J; (2) form digraphs — insert `X` between identical-letter pairs, pad odd trailing letter with `X`; (3) per digraph: same row → shift right (wrap), same column → shift down (wrap), else rectangle → swap columns within own row.
3. **Vigenère:** repeat keyword to message length, $C_i=(P_i+K_i)\bmod 26$.
4. **OTP:** $C_i=(P_i+K_i)\bmod 26$ with a truly random, message-length, single-use, secret key → Shannon perfect secrecy.
5. **Hill Cipher (2×2):** $C=(K\times P)\bmod 26$; decrypt with $K^{-1}\bmod 26$. (Lc#1 only, not in past papers.)

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q2(a,b) | Caesar encrypt "CRYPTO" shift 5; decrypt "ONXNG" with f(p)=(p+4)mod26 |
| 2023 | Q1(a) | Encrypt "See you at CSECU" with GIVEN 5×5 Playfair matrix |
| 2022 | Q2(b) | Conceptual: how cryptanalysis can work on Caesar and OTP |
| 2021 | A2(a,b), A4(iv) | OTP "perfect security" debate + difficulties; Playfair encrypt "See you at CSE department" (given matrix); write Caesar encrypt/decrypt program |
| 2020 | Q1(a,b) | Playfair encrypt "Must see you over CU playground. Coming now." (given matrix); Vigenère encrypt "explanation" key "cse" |

🔁 Repeats every year: SOME classical-cipher question, 2–9 marks. The SAME 5×5 Playfair matrix (M F H I/J K / U N O P Q / Z V W X Y / E L A R G / D S T B C) was given in 2020, 2021, AND 2023 — memorize it.

## Weak spots / common mistakes
- Forgetting to strip spaces before forming Playfair digraphs.
- Rectangle rule direction: each letter keeps its OWN row, takes the OTHER letter's column (not the reverse).
- Forgetting wrap-around on same-row/same-column shifts.
- Treating OTP's "perfect secrecy" as unconditional — it requires random+full-length+single-use+secret key; cryptanalysis only works when one of these is violated.
- Caesar decrypt: subtract the shift, don't re-add it.

## Related topics
[[wiki/security_fundamentals|Security Fundamentals & Attacks]] · [[wiki/symmetric_asymmetric|Symmetric/Asymmetric Ciphers]]
