# CSE 717 — InfoSec · Topic Tracker
> [[_Syllabus]] · [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold

> Ordered by **learning flow / lecture flow** (Lc#1 → Lc#11), not by yield. See `_Syllabus.md` for the 4-day plan and yield-based priority calls.
>
> ⚠️ **2026-06-13 major revision:** re-read all 5 past papers at 300dpi — first-pass OCR had significant errors. Added 2 NEW topics (#4 Hash Table Collision Resolution, #5 Game Theory — both confirmed in Lc#2/Lc#3 and both appear in 2023+2024). DES/Feistel (#13) and Digital Signature (#14) are CONFIRMED 5/5 years — reclassified from "insurance" to CRITICAL, cheat sheets required regardless of Lc coverage. Markov Chains (#6) upgraded from "1/5 unknown" to "2/5, both most recent years".

| # | Topic | Status | Conf | Last Reviewed | Next Recall | Yield | Notes / weak spots |
|---|-------|:------:|:----:|:-------------:|:-----------:|:-----:|--------------------|
| 1 | Classical Ciphers (Caesar, Playfair, Hill Cipher, Vigenère, OTP) | ✅ | — | 2026-06-13 | 2026-06-15 | 5/5 · 2–9 marks | Playfair matrix usually GIVEN in exam — practice encrypting sentences (with spaces). Wiki + solutions PDF done. Source: Lc#1 |
| ↳ Caesar Cipher (encrypt + decrypt, f(p)=(ap+b)mod26) | 🔲 | — | — | — | 5/5 every year | 2024 encrypt+decrypt; 2023 encrypt+decrypt; 2021 general-form program |
| ↳ Playfair Cipher (given-matrix encryption) | 🔲 | — | — | — | 3/5 (2020/21/23) · 2–4 marks | Matrix always GIVEN — drill digraph rules + spaces/duplicates handling |
| ↳ Hill Cipher (2×2 matrix encrypt/decrypt) | 🔲 | — | — | — | 0/5 in past papers, in Lc#1 | Not seen 2020-24 but worked examples in source — light pass only |
| ↳ Vigenère Cipher | 🔲 | — | — | — | 1/5 (2020) · 4.75 marks | Key "cse" on "explanation" — repeatable algorithm |
| ↳ One-Time Pad (OTP) — conceptual | 🔲 | — | — | — | 2/5 (2021/22) | "Perfect secrecy" argument + cryptanalysis conceptual answers |
| 2 | Security Fundamentals & Attacks (CIA, professions, steganography, SQLi, social eng, SWIFT, phishing, ransomware) | 📖 | — | 2026-06-13 | — | 4/5 · 2–9 marks | Fill-blank vocab Q1 style + attack short-notes. Lc#1 pp2-17 covers attack vectors; rest (CIA/professions/steganography/biometrics/SWIFT/backdoor-Trojan) NOT in any Lc — cheat sheet, like #13/#14. Wiki done. |
| ↳ Attack-vector short notes (DoS, DDoS, Phishing, SQLi, Ransomware, Rogue security software) | 🔲 | — | — | — | Lc#1 pp2-17, used 2023/2022/2021 | 6 definitions, exam asks "explain briefly" / "short note" |
| ↳ Security vocab cheat sheet (CIA-ish terms, risk eqn, professions, steganography, biometrics FAR/FRR, wireless threats, backdoor/logic bomb/Trojan, SWIFT, handshaking+digest, Shannon confusion/diffusion) | 🔲 | — | — | — | NOT in any Lc, 4/5 years | ~15 terms — no calculation, pure memorization |
| 3 | Symmetric vs Asymmetric / Block vs Stream Cipher | 📖 | — | 2026-06-13 | — | bundled into #2 most yrs, 7 marks in 2022, 4 in 2020 | NOT in any Lc material (Lc#1 pp25-28 & Lc#7 p12 are title-only slides) — cheat sheet like #13/#14. Wiki + solutions PDF done. |
| ↳ Essential ingredients of a symmetric cipher | 🔲 | — | — | — | 1/5 (2022) · 3 marks | plaintext, encryption algorithm, secret key, ciphertext, decryption algorithm |
| ↳ Block vs stream cipher comparison | 🔲 | — | — | — | 1/5 (2020) · 1 mark | one-line difference table |
| ↳ Classical Feistel cipher structure (diagram) | 🔲 | — | — | — | 1/5 (2020) · 3 marks | shared with DES cheat sheet #13 — same diagram |
| ↳ Public-key cryptosystem elements & key roles | 🔲 | — | — | — | 1/5 (2022) · 4 marks | 6 elements (plaintext/algo/keys/ciphertext) + public encrypts·verifies / private decrypts·signs |
| 4 | Hash Functions & Hash Table Collision Resolution (linear probing, double hashing) | 🔲 | — | — | — | 2/5 (2023+2024) · 3 marks | NEW topic — confirmed in Lc#2 w/ worked examples matching exam style exactly. Source: Lc#2 |
| 5 | Game Theory & Nash Equilibrium (payoff matrix, dominant strategy) | 🔲 | — | — | — | 2/5 (2023+2024) · 3–6 marks | NEW topic — confirmed in Lc#3 w/ worked examples. Source: Lc#3 |
| 6 | Markov Chains (steady-state probability, 2-state security model) | 🔲 | — | — | — | 2/5 (2023+2024) · 3–4 marks | UPGRADED — both most recent years ask 2-state Markov steady-state. Source: Lc#4A, Lc#4B |
| 7 | Number Theory & Modular Arithmetic (Euclidean, Fermat, Euler, CRT, Miller-Rabin, discrete log) | 🔲 | — | — | — | 5/5 · 5–9 marks | Foundation for RSA/DigSig. Recurring seed: 3^20x mod11, 7^1000 mod10/11. Source: Lc#5, Lc#6 |
| 8 | RSA (key gen + encrypt/decrypt numericals) | 🔲 | — | — | — | 5/5 · 5–16 marks | Every year, same numeric pipeline. "e=31,n=3599→find d" repeats verbatim 2020&2021. Source: Lc#6, Lc#7 |
| 9 | AES (S-box, GF(2^8), block diagram) | 🔲 | — | — | — | 4/5 · 4–6 marks | Block diagram recurs (2021/23/24); GF(2^8) S-box inverse (2022); ShiftRows trace (2024). Source: Lc#8 |
| 10 | Quantum Attacks & ECC (point arithmetic) | 🔲 | — | — | — | 1/5 (2024 only) · 3–5 marks | NEW numeric type — elliptic curve point-doubling 2P. Don't over-invest. Source: Lc#6, Lc#7 |
| 11 | IPsec (AH/ESP, transport/tunnel, RFC4301, architecture) | 🔲 | — | — | — | 3/5 · 2.25–9 marks | UPGRADED from 2/5 — 2024 confirmed. Same sub-Q cluster recurs (2020/21/24). Source: Lc#7 |
| 12 | Blockchain & Bitcoin (Merkle tree, PoW, ETH vs BTC) | 🔲 | — | — | — | 3/5 · 2.75–12 marks | NEW dedicated materials → expect high weight 2026. Source: Lc#11A, Lc#11B |
| 13 | DES/Feistel/S-box/Avalanche/3-DES (CHEAT SHEET) | 🔲 | — | — | — | 5/5 · 5–10 marks | ⚠️ CRITICAL, CONFIRMED EVERY YEAR — NOT insurance. NOT in any 2026 Lc material. 6 recurring sub-patterns (see map). ~45min cheat sheet |
| 14 | Digital Signature — generic model + properties + vulnerabilities (CHEAT SHEET) | 🔲 | — | — | — | 5/5 · 1–7 marks | ⚠️ CRITICAL, CONFIRMED EVERY YEAR — NOT insurance. Diagram + concepts, low prerequisite. ~30min cheat sheet |

## Column guide
- **Conf** — confidence 1–5 (1=shaky, 5=bulletproof). Update after every recall pass.
- **Last Reviewed** — date you last marked ✅ or completed a 🔁 pass (YYYY-MM-DD). Claude writes this.
- **Next Recall** — auto-computed by spaced_rep.py. Claude writes this after each update.

## Status rules
- ✅ only when you can explain it cold without notes AND solve a past-paper question on it.
- Re-reading ≠ ✅.
- When you complete a 🔁 recall pass → mark ✅ again and update Last Reviewed with today's date.
- High Yield + 🔲 status = today's target.
