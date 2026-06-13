# CSE 717 — InfoSec · Topic Tracker
> [[_Syllabus]] · [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold

| Topic | Status | Conf | Last Reviewed | Next Recall | Yield | Notes / weak spots |
|-------|:------:|:----:|:-------------:|:-----------:|:-----:|--------------------|
| Number Theory & Modular Arithmetic (Euclidean, Fermat, Euler, CRT, Miller-Rabin) | 🔲 | — | — | — | 5/5 · 5–8 marks | Foundation for RSA/digital sig. Source: Lc#5, Lc#6 |
| RSA (key gen + encrypt/decrypt numericals) | 🔲 | — | — | — | 5/5 · 4.75–5 marks | Every year, same numeric pipeline. Source: Lc#6, Lc#7 |
| Classical Ciphers (Caesar, Playfair, Hill Cipher, OTP) | 🔲 | — | — | — | 3/5 · 5–7.5 marks | Vigenère unclear in materials — check Lc#1 visually. Source: Lc#1 |
| AES (S-box, GF(2^8), structure) | 🔲 | — | — | — | 3/5 · 4.75 marks | Source: Lc#8 |
| Security Fundamentals & Attacks (CIA, professions, steganography, SQLi, social eng, SWIFT) | 🔲 | — | — | — | 3/5 · 4–9 marks | Source: Lc#1, Lc#3 |
| Symmetric vs Asymmetric / Block vs Stream Cipher | 🔲 | — | — | — | 2/5 · 4 marks | Source: Lc#1, Lc#7 |
| Blockchain & Bitcoin (Merkle tree, mining, ETH vs BTC) | 🔲 | — | — | — | 4/5 · 4.4–9 marks | NEW dedicated materials → expect high weight. Source: Lc#11A, Lc#11B |
| IPsec (AH/ESP, transport/tunnel, RFC4301) | 🔲 | — | — | — | 2/5 · 8.5–10 marks | Cyclical — absent 2022-24, big marks when it appears. Source: Lc#7 |
| Hash Functions & Randomness (SHA, avalanche effect) | 🔲 | — | — | — | 1/5 · supporting | No direct past Q — supports Blockchain/DigSig. Source: Lc#2, Lc#9, Lc#10 |
| Markov Chains (transition probabilities, weather example) | 🔲 | — | — | — | 1/5 · unknown, new | No past-paper precedent. Source: Lc#4A, Lc#4B |
| Quantum Attacks & ECC | 🔲 | — | — | — | 1/5 · unknown, new | No past-paper precedent. Source: Lc#7 |
| ⚠️ DES/Feistel/S-box/Avalanche (insurance) | 🔲 | — | — | — | 5/5 historically · 5-7 marks | NOT FOUND in any 2026 Lc material — verify Day 1, else use cheat sheet |
| ⚠️ Digital Signature (generic model) (insurance) | 🔲 | — | — | — | 4/5 historically · 2-4.75 marks | NOT FOUND in any 2026 Lc material — verify Day 1, else use cheat sheet |

## Column guide
- **Conf** — confidence 1–5 (1=shaky, 5=bulletproof). Update after every recall pass.
- **Last Reviewed** — date you last marked ✅ or completed a 🔁 pass (YYYY-MM-DD). Claude writes this.
- **Next Recall** — auto-computed by spaced_rep.py. Claude writes this after each update.

## Status rules
- ✅ only when you can explain it cold without notes AND solve a past-paper question on it.
- Re-reading ≠ ✅.
- When you complete a 🔁 recall pass → mark ✅ again and update Last Reviewed with today's date.
- High Yield + 🔲 status = today's target.
