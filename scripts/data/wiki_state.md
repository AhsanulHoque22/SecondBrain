# Study Brain — Compiled State
_Updated: 2026-06-13 by session (InfoSec unblocked)_

## Active exam
Course: CSE 717 — Information Security
Date: 2026-06-17 (Wednesday) | Days left from 2026-06-13: **4** | Phase: **UNBLOCKED — Day 1 of 2.5 core-learning days**. Materials arrived (11 lecture PDFs + 5-year past papers + Blockchain/Bitcoin). `_Syllabus.md`, `_Topics.md`, `_TopicQuestionMap.md` built and reordered by learning/lecture flow (Lc#1→Lc#11). Today's focus (Lc#1-3 cluster): Classical Ciphers → Security Fundamentals & Attacks → Symmetric/Asymmetric & Block/Stream → Hash Functions & Randomness. Sun (Lc#4-8 cluster): Markov Chains → Number Theory & Modular Arithmetic → RSA → AES. Mon AM (Lc#7/11 + insurance): Quantum/ECC → IPsec → Blockchain/Bitcoin → DES/Feistel + Digital Signature cheat sheets. Mon PM/Tue = 1.5 days pure revision + timed past papers. ⚠️ Open question: DES/Feistel/S-box and Digital Signature generic model appear in every past paper but weren't found via text search in 2026 materials — verify visually Day 1 (flagged in `_Syllabus.md`).

## Topics — CSE713 AI (exam complete — archived for retention recall)
| Topic | Status | Conf | Next Recall |
|---|:---:|:---:|---|
| Intelligent Agents + Environments (PAGE) | ✅ | 4 | 2026-06-05 ⚠️ overdue |
| Search: UCS, Greedy, A*, IDDFS — trace on graph | ✅ | 4 | 2026-06-05 ⚠️ overdue |
| Search: Problem Formulation | 🔁 | 4 | 2026-06-04 ⚠️ overdue |
| Alpha-Beta Pruning + Minimax | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| Forward + Backward Chaining | ✅ | 5 | 2026-06-06 ⚠️ overdue |
| ↳ PL Basics | ✅ | 5 | 2026-06-06 ⚠️ overdue |
| ↳ Resolution in PL | ✅ | 5 | 2026-06-06 ⚠️ overdue |
| FOL + Resolution + Inference | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| ↳ FOL Syntax | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| ↳ FOL Translation | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| ↳ Canonical Form Conversion (9-step) | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| ↳ Resolution in FOL | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| ↳ KR & Mapping roles | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| ↳ Evidential Reasoning (ER) | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| STRIPS + Partial-Order Planning | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| Hill Climbing + Simulated Annealing | ✅ | 5 | 2026-06-07 ⚠️ overdue |
| Bayes' Theorem + Bayesian Networks | ✅ | 3 | 2026-06-09 ⚠️ overdue |
| ↳ Uncertainty Concept (doorbell) | ✅ | 3 | 2026-06-09 ⚠️ overdue |
| ↳ Extended Bayes' Theorem | ✅ | 3 | 2026-06-09 ⚠️ overdue |
| ↳ BN Syntax, Semantics & Construction | 📖 | — | — |
| ↳ McCulloch-Pitts Neuron + Perceptron | ✅ | 3 | — |
| Neural Networks + Learning (main) | 📖 | — | 2026-06-09 ⚠️ overdue |
| ↳ Backpropagation (sigmoid fwd/bwd) | 📖 | — | — |
| ↳ Associative Memory + Hopfield | 📖 | — | — |
| ↳ ANN vs Biological + taxonomy | 📖 | — | — |
| ↳ NN Historical Evolution | 📖 | — | — |
| CSP (map coloring, cryptarithmetic) | 🔲 | — | — |
| Fuzzy Logic + Uncertainty | 📖 | — | — |

## Topics — CSE717 InfoSec (ordered by learning/lecture flow Lc#1→Lc#11)
| # | Topic | Status | Conf | Yield |
|---|---|:---:|:---:|---|
| 1 | Classical Ciphers (Caesar, Playfair, Hill Cipher, OTP) | 🔲 | — | 3/5 · 5–7.5 marks |
| 2 | Security Fundamentals & Attacks (CIA, professions, steganography, SQLi, SWIFT, firewall) | 🔲 | — | 3/5 · 4–9 marks |
| 3 | Symmetric/Asymmetric & Block/Stream Cipher | 🔲 | — | 2/5 · 4 marks |
| 4 | Hash Functions & Randomness | 🔲 | — | 1/5 · supporting |
| 5 | Markov Chains | 🔲 | — | 1/5 · new, unknown |
| 6 | Number Theory & Modular Arithmetic (Euclidean, Fermat, Euler, CRT, Miller-Rabin) | 🔲 | — | 5/5 · 5–8 marks |
| 7 | RSA (key gen + encrypt/decrypt numericals) | 🔲 | — | 5/5 · 4.75–5 marks |
| 8 | AES (S-box, GF(2^8)) | 🔲 | — | 3/5 · 4.75 marks |
| 9 | Quantum Attacks & ECC | 🔲 | — | 1/5 · new, unknown |
| 10 | IPsec (AH/ESP, transport/tunnel, RFC4301) | 🔲 | — | 2/5 · 8.5–10 marks, cyclical |
| 11 | Blockchain & Bitcoin (Merkle tree, ETH vs BTC) | 🔲 | — | 4/5 · NEW, expect high weight |
| 12 | ⚠️ DES/Feistel/S-box/Avalanche (insurance) | 🔲 | — | 5/5 historically — verify Day 1 |
| 13 | ⚠️ Digital Signature generic model (insurance) | 🔲 | — | 4/5 historically — verify Day 1 |

Full detail in `02_Courses/CSE717_InfoSec/_Topics.md` + `_Syllabus.md` + `_TopicQuestionMap.md`.

## Carry-forward
- None — InfoSec unblocked. Today's #1: Classical Ciphers → Security Fundamentals & Attacks → Symmetric/Asymmetric → Hash Functions (Blocks 1-4), then 10-min source check for DES/Digital Signature.

## Recall due 2026-06-12
- 🔁 Intelligent Agents + Environments (PAGE) `CSE713_AI` | conf 4/5
- 🔁 Search: UCS, Greedy, A*, IDDFS — trace on graph `CSE713_AI` | conf 4/5
- 🔁 Forward + Backward Chaining + Rule-Based System `CSE713_AI` | conf 5/5
- 🔁 ↳ PL Basics: satisfiability, validity, entailment, Modus Ponens `CSE713_AI` | conf 5/5
- 🔁 ↳ Resolution in PL: clause form (4-step), refutation proof `CSE713_AI` | conf 5/5
- 🔁 Alpha-Beta Pruning + Minimax `CSE713_AI` | conf 5/5
- 🔁 FOL + Resolution + Inference (Marcus/Pompeii) `CSE713_AI` | conf 5/5
- 🔁 Hill Climbing + Simulated Annealing `CSE713_AI` | conf 5/5
- 🔁 STRIPS + Partial-Order Planning (Block World) `CSE713_AI` | conf 5/5
- 🔁 ↳ Canonical Form Conversion (9-step algorithm) `CSE713_AI` | conf 5/5
- 🔁 ↳ Evidential Reasoning (ER): Dempster-Shafer, degree of belief `CSE713_AI` | conf 5/5
- 🔁 ↳ FOL Syntax: Terms, Predicates, Functions, ∀, ∃, Sentences `CSE713_AI` | conf 5/5
- 🔁 ↳ FOL Translation (car/drone/robot scenario) `CSE713_AI` | conf 5/5
- 🔁 ↳ Knowledge Representation and Mapping (roles) `CSE713_AI` | conf 5/5
- 🔁 ↳ Resolution in FOL: Unification, Skolemization, refutation `CSE713_AI` | conf 5/5
- 🔁 Bayes' Theorem + Bayesian Networks `CSE713_AI` | conf 3/5
- 🔁 ↳ Extended Bayes' Theorem `CSE713_AI` | conf 3/5
- 🔁 ↳ Uncertainty Concept (doorbell) `CSE713_AI` | conf 3/5
- 🔁 ↳ McCulloch-Pitts Neuron + Perceptron + Learning Rule `CSE713_AI` | conf 3/5

## Recent pattern (last 3 days)
- 2026-06-09: end-of-day log unfilled — no new completions logged
- 2026-06-10: 🎓 CSE 713 AI EXAM SAT (10:30 AM) | end-of-day log unfilled
- 2026-06-11: end-of-day log unfilled — no new completions logged, InfoSec setup still blocked, 19 AI recalls all still overdue
