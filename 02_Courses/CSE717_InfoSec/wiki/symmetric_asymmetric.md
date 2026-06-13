# Symmetric vs Asymmetric & Block vs Stream Ciphers
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Comparison/definition topic covering the building blocks of cryptosystems: the 5 essential ingredients of a symmetric cipher, the block-vs-stream cipher distinction, the classical Feistel network structure, and the 6 elements + key roles of a public-key cryptosystem. No-source cheat sheet — like Topics #13/#14, not covered by any Lc material.

## Key steps / algorithm
1. **Symmetric cipher — 5 ingredients:** plaintext, encryption algorithm, secret key, ciphertext, decryption algorithm.
2. **Block vs stream cipher:** block = encrypts fixed-size chunks at once (DES/AES); stream = encrypts bit/byte-by-byte via XOR with a keystream (RC4).
3. **Feistel structure (1 round):** $L_i = R_{i-1}$, $R_i = L_{i-1} \oplus F(R_{i-1}, K_i)$. Decryption = same structure, subkeys reversed. Shared with DES (#13).
4. **Public-key cryptosystem — 6 elements:** plaintext, encryption algorithm, public key, private key, ciphertext, decryption algorithm.
5. **Key roles:** public key encrypts/verifies (shared openly); private key decrypts/signs (kept secret). Memory aid: "public locks, private unlocks."

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q1(a) | Symmetric vs asymmetric + why asymmetric for e-commerce (3) — bundled with Topic 2, solved there |
| 2023/2021 | — | not standalone |
| 2022 | Q2(a), Q2(c) | Essential ingredients of symmetric cipher (3); public-key cryptosystem elements (2) + key roles (2) = 7 |
| 2020 | Q5(b,c) | Classical Feistel structure diagram (3); block vs stream cipher difference (1) |

🔁 Appears most years bundled into Topic 2 (symmetric vs asymmetric, ~3 marks); standalone definition/diagram cluster (7 marks) in 2022, smaller cluster (4 marks) in 2020. Full solutions: `SymmetricAsymmetric_Solutions.pdf`.

## Weak spots / common mistakes
- Don't confuse "essential ingredients of a symmetric cipher" (5 items, generic) with "elements of a public-key cryptosystem" (6 items, includes both key types) — different lists, often confused under exam pressure.
- Feistel structure diagram is shared with DES (#13) — learn it once, reuse for both.
- Block vs stream: the 1-mark version just needs ONE sentence — don't over-write.
- "Roles of public/private key" ≠ "elements of cryptosystem" — these are two separate 2-mark sub-answers in 2022 Q2(c).

## Related topics
[[wiki/classical_ciphers|Classical Ciphers]] · [[wiki/security_fundamentals|Security Fundamentals & Attacks]]
