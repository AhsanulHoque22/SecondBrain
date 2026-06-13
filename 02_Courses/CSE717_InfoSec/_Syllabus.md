# CSE 717 — Information Security · Syllabus (CONFIRMED from lecture materials + 2020–2024 past papers)
> [[_Topics]] · [[_TopicQuestionMap]] · [[00_Dashboard]]

> Built 2026-06-13 by Claude Code. **Revised same day** after re-reading all 5 past papers at 300dpi (first pass had significant OCR errors).
> Exam format: ~54 marks, 4 hours, Section A + Section B, answer 3 of 4 from each section.
> **Topics below are ordered by learning flow / lecture flow (Lc#1 → Lc#11)**, not by yield — yield stars (⭐) tell you how hard to push on each. Only **2.5 days** of core learning available (Sat 13 → Mon 15 AM) before 1.5 days pure revision. Ruthless 80/20 within each block.

---

## ⚠️ 2026-06-13 major correction
First-pass past-paper analysis was wrong in places. Re-read at 300dpi confirmed:
- **DES/Feistel/S-box/Avalanche (#13)** and **Digital Signature generic model (#14)** appear in **EVERY SINGLE YEAR 2020-2024** — these are NOT "insurance/maybe absent" topics, they are guaranteed marks. Neither is covered in the 2026 Lc materials, so both need a focused cheat sheet — but they are now CRITICAL, scheduled into TODAY.
- **Markov Chains (#6)** appears in BOTH 2023 and 2024 (2-state steady-state probability) — upgraded from "no precedent" to high-confidence repeat.
- **Game Theory/Nash Equilibrium (#5)** and **Hash Table Collision Resolution (#4)** are TWO NEW topics, both appearing in 2023+2024, and BOTH have matching worked examples in Lc#3 and Lc#2 respectively.
- **IPsec (#11)** upgraded from 2/5 to 3/5 (2024 confirmed).

---

## 1. Classical Ciphers
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years, 2–9 marks
**Source:** Lc#1 (Caesar, Playfair, Hill Cipher — pp.310-355)
**What to know:**
- Caesar Cipher: f(p)=(ap+b) mod 26 forms — both encrypt AND decrypt, brute-force feasibility
- Playfair Cipher: 5×5 matrix — in the exam the matrix is usually GIVEN, not built from a keyword. Practice encrypting full sentences (strip spaces, handle digraphs/duplicate letters with X filler)
- Vigenère Cipher: repeating-key shift (2020 — encrypt "explanation" key "cse")
- Hill Cipher: matrix-based encryption (2×2 matrix, mod 26) — in Lc#1 with worked "HI"/"CD" examples, not seen in past papers but a likely substitute for Playfair
- One-Time Pad (OTP): perfect secrecy concept, fundamental difficulties (2021 conceptual)
- **Past paper pattern:** EVERY year. 2024: Caesar encrypt+decrypt (3). 2023: Playfair given-matrix (4) + Caesar encrypt+decrypt (4). 2022: Caesar/OTP cryptanalysis. 2021: OTP conceptual (2.75) + Playfair given-matrix (2) + Caesar program (2). 2020: Playfair given-matrix (4) + Vigenère (4.75).

## 2. Security Fundamentals & Attack Vectors
**Yield:** ⭐⭐⭐⭐ 4/5 years, 2–9 marks
**Source:** Lc#1 (phishing, SQL injection, malware — pp.90-130), Lc#3 (Firewall)
**What to know:**
- CIA triad, security terminology (threat actor, asset, attack vector, confidentiality, authenticity, non-repudiation)
- Security professions: pentester, cybersecurity analyst/architect/auditor, network analyst, data security analyst
- Steganography vs cryptography
- Attack types: phishing, SQL injection, social engineering, malware, DoS/DDoS, ransomware (Clop/WannaCry), backdoor/logic bomb/Trojan horse
- Risk equation (threat × probability × loss), biometrics auth limitations, wireless threats
- SWIFT banking network pentest scenario (write-up style)
- **Past paper pattern:** 2024 (symmetric/asymmetric+ecommerce, handshaking/message-digest = 5). 2023 (phishing/DoS/SQLi/ransomware short-notes = 2). 2022 (fill-blank vocab+professions+steganography = 8, SQLi/social-eng/SWIFT = several marks). 2021 (risk equation+biometrics+wireless = 4.75, ransomware vs social-eng + backdoor/Trojan = 3.75).

## 3. Symmetric vs Asymmetric Crypto / Block vs Stream Ciphers
**Yield:** ⭐⭐⭐ usually bundled into #2, but 10 marks standalone in 2022
**Source:** Lc#1, Lc#7 (Symmetric crypto)
**What to know:**
- Ingredients of a symmetric cipher (plaintext, encryption algorithm, secret key, ciphertext, decryption algorithm)
- Block cipher vs stream cipher — definitions + differences
- Public-key cryptosystem roles/components
- Caesar cipher / OTP as cryptanalysis examples
- **Past paper pattern:** 2022 Q2 — symmetric cipher ingredients (3), block vs stream (3), Caesar/OTP cryptanalysis (2), public-key roles (2) = 10. 2020 — Feistel structure (3) + block vs stream (1).

## 4. Hash Functions & Hash Table Collision Resolution (NEW)
**Yield:** ⭐⭐⭐ 2/5 years (2023+2024, both most recent), 3 marks each + supports #12/#14
**Source:** Lc#2 (Hash Function — has WORKED EXAMPLES matching exam style exactly)
**What to know:**
- Hash function properties: deterministic, fixed-size output, avalanche, one-way, collision-resistant, pre-image/second-pre-image resistance
- **Collision resolution: linear probing AND double hashing** — practice inserting ~6 keys into a hash table of size m=10-13 by hand for BOTH methods
- **Past paper pattern:** 2024 double hashing insert [8,47,22,44,39,32] m=13, h1=k mod13, h2=7+(k mod7) (3). 2023 linear probing insert [21,8,13,44,28,33] m=13, h(k)=(k+2)mod m (3). 2023 hash function properties (2.5).

## 5. Game Theory & Nash Equilibrium (NEW)
**Yield:** ⭐⭐⭐ 2/5 years (2023+2024, both most recent), 3–6 marks
**Source:** Lc#3 (Game Theory — has worked Nash equilibrium examples)
**What to know:**
- Payoff matrix (2x2), best-response analysis, Nash equilibrium identification
- Dominant strategy (strict) — does either player have one?
- **Past paper pattern:** 2024 — Eve/Mallory PT vs ND payoff matrix, find Nash equilibria + dominant strategies (3). 2023 — "design a strategy to identify attackers using game theory" (3) + Alice/Bob ST#1/ST#2 payoff matrix, Nash equilibrium (3).

## 6. Markov Chains (UPGRADED)
**Yield:** ⭐⭐⭐⭐ 2/5 years (2023+2024, both most recent — strong recency signal), 3–4 marks
**Source:** Lc#4A (Markov Chain theory), Lc#4B (Markov Chain assignment/numericals)
**What to know:**
- Markov chain definition: states, transition probabilities, memoryless property
- **2-state steady-state probability**: set up transition matrix P, solve πP=π with Σπ=1
- Worked example: weather chain (Lc#4B) — map directly onto "Secure/Compromised" or "Secure/Insecure" security-state framing
- **Past paper pattern:** 2024 — Secure/Compromised system, Secure→Secure w.p.0.4, Compromised→Secure w.p.0.3, find steady-state + interpret (4). 2023 — Secure/insecure network, patch-cycle transitions, long-term behaviour (3).

## 7. Number Theory & Modular Arithmetic
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years, 5–9 marks — foundation for #8 and #14
**Source:** Lc#5 (Modular Arithmetic), Lc#6 (Modular Arithmetic + RSA + Euler/Fermat)
**What to know:**
- Modular arithmetic basics, Extended Euclidean Algorithm (GCD + multiplicative inverse)
- Fermat's Little Theorem: a^(p-1) ≡ 1 (mod p)
- Euler's Theorem + Euler's Totient function φ(n)
- Chinese Remainder Theorem (CRT) — solve system of congruences
- Discrete logarithm problem, cyclic groups
- Miller-Rabin primality test
- **Past paper pattern:** EVERY year, 5-9 marks. Recurring seed: `3^20x mod 11` and `7^1000 mod 10/11` (2020,2021,2023,2024). CRT (2020 & 2023). Extended Euclidean for mult. inverse (almost every year). Miller-Rabin + discrete log (2020-2022).

## 8. RSA — Key Generation + Encryption/Decryption Numericals
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years, 5–16 marks (largest single block some years)
**Source:** Lc#6 (RSA basics), Lc#7 (RSA + Quantum threat)
**What to know:**
- Key generation: choose p,q primes → n=pq, φ(n)=(p-1)(q-1), choose e, compute d=e⁻¹ mod φ(n)
- Encryption: C = M^e mod n; Decryption: M = C^d mod n
- **Always given small p,q (3,7,11,13,17,31,43,53,59,61 range) — drill the full pipeline cold**
- "Given e,n find d" variant repeats verbatim (2020&2021: e=31,n=3599)
- **Past paper pattern:** EVERY year — 2024 (encrypt+decrypt, 6), 2023 (encrypt+decrypt, 5), 2022 (full key-gen+encrypt+explain, 16!), 2021 (encrypt/decrypt + find d, 6.75), 2020 (encrypt/decrypt + find d, 8.75)

## 9. AES (Advanced Encryption Standard) (UPGRADED)
**Yield:** ⭐⭐⭐⭐ 4/5 years, 4–6 marks
**Source:** Lc#8 (AES, 14pg)
**What to know:**
- AES block diagram (rounds, key sizes 128/192/256, SubBytes/ShiftRows/MixColumns/AddRoundKey) — recurs as a "draw the diagram" question
- S-box and GF(2^8) arithmetic — multiplicative inverse computation
- ShiftRows transformation trace on a given state matrix
- **Past paper pattern:** 2024 (ShiftRows/MixColumns diffusion + perform ShiftRows = 4, block diagram = 2). 2023 (block diagram = 4). 2022 (S-box GF(2^8) inverse = 6). 2021 (block diagram = 4.75).

## 10. Quantum Attacks & ECC
**Yield:** ⭐⭐ 1/5 years (2024 only — NEW numeric type), 3–5 marks
**Source:** Lc#6 (ECC worked examples), Lc#7 (Quantum Attack, ECC, RSA threat)
**What to know:**
- Elliptic curve point arithmetic: given E: y²=x³+ax+b over F_p and point P, compute 2P (point doubling) — 2024 asked exactly this
- Why ECC/RSA are vulnerable to quantum attacks (Shor's algorithm) vs symmetric algorithms
- **Past paper pattern:** 2024 only — elliptic curve 2P computation (3) + quantum vulnerability conceptual (2). Don't over-invest beyond one worked point-doubling example.

## 11. IPsec (UPGRADED)
**Yield:** ⭐⭐⭐ 3/5 years, 2.25–9 marks
**Source:** Lc#7 (IPSec architecture, AH/ESP protocols, key exchange)
**What to know:**
- IPsec architecture: AH vs ESP, security associations
- Transport mode vs Tunnel mode, RFC 4301 services
- Session state vs connection state, application areas, benefits
- **Past paper pattern:** 2024 (architecture + security associations = 3). 2021 (application areas + session/connection state = 2.5, architecture = 2.5). 2020 (benefits+transport/tunnel = 2.25, RFC4301 = 2.25, application+session/connection = 2.25, architecture = 2) = 9 total. Same sub-Q cluster recurs.

## 12. Blockchain & Bitcoin
**Yield:** ⭐⭐⭐⭐ 3/5 years, 2.75–12 marks — dedicated 2026 materials → expect strong emphasis
**Source:** Lc#11A (Blockchain), Lc#11B (Bitcoin Mining)
**What to know:**
- Blockchain definition, block structure, immutability, Proof of Work
- Merkle tree — construction, root computation, integrity checking
- Bitcoin: mining, input/output scripts for signature validation
- Ethereum vs Bitcoin — key differences (ETH vs BTC)
- Hash functions role in blockchain security (links to #4)
- **Past paper pattern:** 2024 (PoW + hashing security = 3). 2022 (same-origin policy via blockchain = 4, Merkle tree diagram = 4, ETH vs BTC = 4 → 12 total). 2021 (blockchain-crypto relation + "what is bitcoin" = 4.75, input/output scripts = 4).

## 13. ⚠️ DES / Feistel Structure / S-box / Avalanche / 3-DES — CRITICAL, NOT INSURANCE
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years EVERY YEAR, 5–10 marks — NOT in any 2026 Lc material, cheat sheet required, scheduled TODAY
**What to know (cheat sheet, ~45min):**
- Classical Feistel cipher structure (16-round network) + properties
- 3-DES block diagram + simple encryption equation
- Avalanche effect (1-bit change → ~half output bits flip) + name the two families of DES attacks (differential & linear cryptanalysis)
- F-function components diagram in DES
- S-box purpose (nonlinearity) + S1-box table lookup for a given input byte (37 appeared in both 2020 & 2022)
- IP / IP⁻¹ permutation purpose and the decryption-reversal equation
- **Past paper pattern:** literally every year, cycling through these 6 sub-patterns. ~6-10 guaranteed marks for ~45min of focused memorization — best ROI on the entire syllabus.

## 14. ⚠️ Digital Signature — Generic Model + Properties — CRITICAL, NOT INSURANCE
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years EVERY YEAR, 1–7 marks — NOT in any 2026 Lc material, cheat sheet required, scheduled TODAY
**What to know (cheat sheet, ~30min):**
- Generic model diagram: sender hashes msg → encrypts hash with private key → receiver decrypts with public key → compares hashes (recurs as a draw/sketch question almost every year, 1-4.75 marks)
- Properties a digital signature scheme must satisfy
- Attack types that make digital signatures vulnerable
- RSA key-reuse safety question (2023): if private key leaks, is reusing the same n with new e/d safe? (No — must generate new modulus)
- **Past paper pattern:** every year — 2024 (concept+vulnerable attacks=6, diagram=1), 2023 (concept+vulnerable=6, key-reuse safety=1), 2022 (properties+requirements, signature-order), 2021 (diagram=2), 2020 (diagram=4.75).

---

## 4-Day Plan (Sat 13 → Tue 16) — 2.5 days core, 1.5 days revision, exam Wed 17

| Day | Topics (in learning-flow order) | Why this grouping |
|-----|--------|-----|
| **Sat 13 Jun (full day)** | #1 Classical Ciphers → #2 Security Fundamentals & Attacks → #3 Symmetric/Asymmetric (quick, bundled) → #4 Hash Functions & Collision Resolution → **#13 DES/Feistel cheat sheet → #14 Digital Signature cheat sheet** | Lc#1-2 cluster + the two CRITICAL no-source cheat sheets, scheduled early since they're standalone (no prerequisites) and now confirmed guaranteed — maximize safety margin. |
| **Sun 14 Jun (full day)** | #5 Game Theory → #6 Markov Chains → #7 Number Theory & Modular Arithmetic → #8 RSA | Lc#3-6 cluster: two NEW-but-quick topics (game theory, Markov) + the math/crypto core. #7 is the prerequisite for #8 and #14 — must land before RSA. |
| **Mon 15 Jun — AM only** | #9 AES → #10 Quantum/ECC → #11 IPsec → #12 Blockchain & Bitcoin | Lc#7/8/11 cluster. All diagram/conceptual + one ECC numeric — fits a condensed AM sweep. |
| **Mon 15 Jun PM → Tue 16 Jun (1.5 days revision)** | Timed past papers 2020, 2021, 2022, 2023, 2024 (one per sitting where possible) + active recall sweep across ALL 14 topics, notes closed + weak-spot repair | Per CLAUDE.md: last 2 days = this subject only, timed practice simulating 10:30 AM exam. |

**Note:** 14 topics in 2.5 days is tight, but #3 (bundled), #13, #14 (cheat sheets) are lower-depth, and #5/#6/#10 are each a single worked-example pattern. If Mon AM overflows, #10 (Quantum/ECC, 1/5 years) is the first to cut.

## Exam Structure Reminder
- ~54 marks, 4 hours, Section A (Q1-4) + Section B (Q5-8), answer 3 of 4 each
- Numeric problems (RSA, CRT/Fermat/Euler, Miller-Rabin, AES GF arithmetic, Markov steady-state, hash table insertion, Nash equilibrium, ECC point-doubling) carry the most reliable marks — prioritize being able to COMPUTE, not just define
