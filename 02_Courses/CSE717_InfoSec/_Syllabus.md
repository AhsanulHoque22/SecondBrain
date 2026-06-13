# CSE 717 — Information Security · Syllabus (CONFIRMED from lecture materials + 2020–2024 past papers)
> [[_Topics]] · [[_TopicQuestionMap]] · [[00_Dashboard]]

> Built 2026-06-13 by Claude Code after scanning all 13 lecture PDFs (Lc#1–#11B) + 5-year past paper analysis (image-OCR read, since PDF is scanned).
> Exam format: ~54 marks, 4 hours, Section A + Section B, answer 3 of 4 from each section.
> **Topics below are ordered by learning flow / lecture flow (Lc#1 → Lc#11)**, not by yield — yield stars (⭐) tell you how hard to push on each. Only **2.5 days** of core learning available (Sat 13 → Mon 15 AM) before 1.5 days pure revision. Ruthless 80/20 within each block.

---

## ⚠️ Source gap — flag for Day 1
Past papers ask **DES/Feistel structure/S-box/avalanche effect** and **Digital Signature (generic model)** and **Diffie-Hellman key exchange** in **every single year 2020–2024**, often worth 5–10 marks combined — but these terms do **not appear in any of the 13 uploaded lecture PDFs** (Lc#1–#11B). Either:
- They're in diagram-only slides pdftotext can't read (check visually on Day 1), or
- The 2026 syllabus dropped them in favor of AES/ECC/Quantum/Blockchain (new topics with dedicated materials #6,7,8,11A,11B).
**Action:** Open Lc#1 (59pg), Lc#7 (Quantum, 22pg), Lc#8 (AES,14pg) visually for 10 min on Day 1 to confirm. If truly absent, treat DES/DigSig/DH as low priority (not in this year's materials) but keep a 1-page cheat sheet ready as insurance since they're historically guaranteed.

---

## 1. Classical Ciphers
**Yield:** ⭐⭐⭐ 3/5 years, 5–7.5 marks
**Source:** Lc#1 (Caesar, Playfair, Hill Cipher — pp.310-355)
**What to know:**
- Caesar Cipher: shift cipher, brute-force attack feasibility
- Playfair Cipher: 5×5 key matrix construction + encrypt/decrypt
- Hill Cipher: matrix-based encryption (2×2 matrix, mod 26)
- One-Time Pad (OTP): perfect secrecy concept
- Substitution vs Transposition ciphers
- **Past paper pattern:** 2024 Q1 (OTP-based scheme, P=47), 2021 Q2 (Hill/Playfair matrix encrypt/decrypt), 2020 Group A (Playfair + Vigenère encrypt/decrypt — note: Vigenère not in current Lc materials, check Lc#1 visually)

## 2. Security Fundamentals & Attack Vectors
**Yield:** ⭐⭐⭐ 3/5 years, 4–9 marks
**Source:** Lc#1 (phishing, SQL injection, malware — pp.90-130), Lc#3 (Firewall)
**What to know:**
- CIA triad, security terminology (confidentiality, authenticity, non-repudiation)
- Security professions: pentester, cybersecurity analyst, cybersecurity architect, network analyst, data security analyst
- Steganography vs cryptography
- Attack types: phishing, SQL injection, social engineering, malware, DoS
- Firewall basics, intrusion detection
- SWIFT banking network scenario (pentest write-up style)
- **Past paper pattern:** 2024 Q1 (security terms fill-blank + steganography), 2022/2023 Q1 (same fill-blank pattern), 2022/2023 Q7 (SQL injection, social engineering, SWIFT pentest scenario — write short notes)

## 3. Symmetric vs Asymmetric Crypto / Block vs Stream Ciphers
**Yield:** ⭐⭐ 2/5 years, 4 marks
**Source:** Lc#1, Lc#7 (Symmetric crypto)
**What to know:**
- Ingredients of a symmetric cipher (plaintext, encryption algorithm, secret key, ciphertext, decryption algorithm)
- Block cipher vs stream cipher — definitions + differences
- Public-key cryptosystem roles/components
- Caesar cipher / OTP as cryptanalysis examples
- **Past paper pattern:** 2022/2023 Q2 — symmetric cipher ingredients, block vs stream, Caesar/OTP cryptanalysis, public-key roles

## 4. Hash Functions & Randomness
**Yield:** ⭐ supporting role only
**Source:** Lc#2 (Hash Function), Lc#9 (Basic Data Statistics), Lc#10 (Randomness, SHA)
**What to know:**
- Hash function properties: deterministic, fixed-size output, avalanche effect (small input change → large output change), one-way
- SHA family basics
- Randomness/PRNG concepts, basic statistics (mean/variance — likely supporting Markov chain topic)
- **Past paper pattern:** No direct historical question, but hash functions underpin Blockchain Q8 (Merkle tree) and Digital Signatures — study as supporting concept, don't over-invest standalone.

## 5. Markov Chains
**Yield:** ⭐ unknown, new
**Source:** Lc#4A (Markov Chain theory), Lc#4B (Markov Chain assignment/numericals)
**What to know:**
- Markov chain definition: states, transition probabilities, memoryless property
- Compute multi-step transition probabilities (matrix power)
- Worked example: sunny/rainy weather chain
- **Past paper pattern:** None found 2020–2024. Likely a NEW addition (probability/cryptanalysis foundation). Low priority unless time permits — but if tested, it's a "free" numeric question type (practice the 1 worked example in Lc#4B).

## 6. Number Theory & Modular Arithmetic
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years, 5–8 marks — foundation for #7, #8, #13
**Source:** Lc#5 (Modular Arithmetic), Lc#6 (Modular Arithmetic + RSA + Euler/Fermat)
**What to know:**
- Modular arithmetic basics: mod operations, properties
- Euclidean Algorithm + Extended Euclidean Algorithm (find GCD, multiplicative inverse)
- Fermat's Little Theorem: a^(p-1) ≡ 1 (mod p)
- Euler's Theorem + Euler's Totient function φ(n)
- Chinese Remainder Theorem (CRT) — solve system of congruences
- Discrete logarithm problem
- Miller-Rabin primality test (determine if n is prime, witness selection)
- Multiplicative inverse mod n (find x such that a·x ≡ 1 mod n)
- **Past paper pattern:** 2024 Q2 (CRT modulus 47, prime check), 2023/2022 Q3 (Miller-Rabin, discrete log, Euler's totient), 2021 Q3 (Euclidean alg, Fermat, CRT discrete log), 2020 Q2 (CRT, Euler totient, discrete log, multiplicative inverse)

## 7. RSA — Key Generation + Encryption/Decryption Numericals
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years, 4.75–5 marks
**Source:** Lc#6 (RSA basics), Lc#7 (RSA + Quantum threat)
**What to know:**
- Key generation: choose p,q primes → n=pq, φ(n)=(p-1)(q-1), choose e, compute d=e⁻¹ mod φ(n)
- Encryption: C = M^e mod n; Decryption: M = C^d mod n
- **Always given small p,q (e.g., p=13,q=7 or similar) — practice the full numeric pipeline**
- **Past paper pattern:** EVERY year — 2024 Q3(b), 2023 Q6(a), 2022 Q6(a), 2021 Q5, 2020 Q5(a) — all numeric RSA encrypt/decrypt with given p,q,e,M

## 8. AES (Advanced Encryption Standard)
**Yield:** ⭐⭐⭐ 3/5 years, 4.75 marks
**Source:** Lc#8 (AES, 14pg)
**What to know:**
- AES structure overview (rounds, key sizes 128/192/256)
- S-box and GF(2^8) (Galois Field) arithmetic — multiplicative/additive inverse in GF(2^8)
- SubBytes, ShiftRows, MixColumns, AddRoundKey (at least conceptually)
- **Past paper pattern:** 2022/2023 Q5 — describe AES operations using S-box, GF(2^8) inverse computation; 2020 Group B mentions "advanced encryption standard" AES encryption

## 9. Quantum Attacks & ECC
**Yield:** ⭐ unknown, new
**Source:** Lc#7 (Quantum Attack, ECC, RSA threat)
**What to know:**
- Why quantum computing threatens RSA/ECC (Shor's algorithm — factor large numbers / discrete log fast)
- Elliptic Curve Cryptography (ECC) basics — what it is, why smaller keys than RSA
- Post-quantum crypto motivation
- **Past paper pattern:** None found 2020–2024 — NEW topic. Likely short-note/conceptual question only (1-2 marks). Don't over-invest.

## 10. IPsec
**Yield:** ⭐⭐ 2/5 years but 8.5–10 marks when it appears, cyclical
**Source:** Lc#7 (IPSec architecture, AH/ESP protocols, key exchange)
**What to know:**
- IPsec architecture: AH (Authentication Header) vs ESP (Encapsulating Security Payload)
- Transport mode vs Tunnel mode
- RFC 4301
- Benefits of IPsec, applications
- **Past paper pattern:** 2021 Q7 (benefits, transport/tunnel difference, RFC4301, application/architecture — 8.5 marks), 2020 Group B Q8 (transport/tunnel mode, RFC4301, architecture — high marks). NOT in 2022/2023/2024 — cyclical, may return.

## 11. Blockchain & Bitcoin (NEW — dedicated materials, likely high-weight this year)
**Yield:** ⭐⭐⭐⭐ 2/5 years historically, but expect 2026 emphasis (4.4–9 marks)
**Source:** Lc#11A (Blockchain), Lc#11B (Bitcoin Mining)
**What to know:**
- Blockchain definition, block structure, immutability/tamper-resistance
- Merkle tree — construction, root computation, integrity checking
- Bitcoin: decentralized P2P payment, mining process, consensus
- Ethereum vs Bitcoin — key differences (ETH vs BTC)
- Hash functions role in blockchain (SHA)
- **Past paper pattern:** 2022/2023 Q8 — same-origin policy + blockchain schematic, data integrity via Merkle tree, Ethereum vs Bitcoin distinction. Given dedicated #11A/#11B materials were JUST added, expect this to be tested directly this year.

## 12. ⚠️ DES / Feistel Structure / S-box / Avalanche Effect (insurance)
**Yield:** 5/5 years historically, 5–7 marks — NOT FOUND in 2026 materials, verify Day 1
**What to know if needed:**
- Feistel network 16-round structure
- DES S-box purpose = nonlinearity
- Avalanche effect = 1-bit input change flips ~half output bits
- 3-DES block diagram, block vs stream cipher differences
- **Past paper pattern:** 2023/2022 Q4, 2021 Q4, 2020 Group B Q5 — every year

## 13. ⚠️ Digital Signature — Generic Model (insurance)
**Yield:** 4/5 years historically, 2–4.75 marks — NOT FOUND in 2026 materials, verify Day 1
**What to know if needed:**
- Generic model: sender hashes msg → encrypts hash with private key → receiver decrypts with public key → compares hash
- Properties a digital signature scheme must satisfy
- **Past paper pattern:** 2024 Q7(b), 2022/2023 Q6(b), 2021 Q7(a), 2020 Group B Q6(b) — every year

---

## 4-Day Plan (Sat 13 → Tue 16) — 2.5 days core, 1.5 days revision, exam Wed 17

| Day | Topics (in learning-flow order) | Why this grouping |
|-----|--------|-----|
| **Sat 13 Jun (full day)** | #1 Classical Ciphers → #2 Security Fundamentals & Attacks → #3 Symmetric/Asymmetric & Block/Stream → #4 Hash Functions & Randomness | Lc#1-3 cluster: security context + intro crypto, lowest prerequisite load — good warm-up day. |
| **Sun 14 Jun (full day)** | #5 Markov Chains → #6 Number Theory & Modular Arithmetic → #7 RSA → #8 AES | Lc#4-8 cluster: the math/crypto core. #6 is the prerequisite for #7 and #13 — must land before RSA. |
| **Mon 15 Jun — AM only** | #9 Quantum Attacks & ECC → #10 IPsec → #11 Blockchain & Bitcoin → #12 DES/Feistel insurance → #13 Digital Signature insurance | Lc#7/11 cluster + insurance cheat sheets. All conceptual/short-note style — fits a condensed AM sweep. |
| **Mon 15 Jun PM → Tue 16 Jun (1.5 days revision)** | Timed past papers 2020, 2021, 2022, 2023, 2024 (one per sitting where possible) + active recall sweep across ALL 13 topics, notes closed + weak-spot repair | Per CLAUDE.md: last 2 days = this subject only, timed practice simulating 10:30 AM exam. |

**Note:** This compresses what the AI exam got 5 days for into 2.5. If Mon AM overflows, IPsec and Blockchain (#10, #11) are non-negotiable (high marks); Quantum/ECC (#9) is the first to cut (no past-paper precedent, 1-2 marks at most).

## Exam Structure Reminder
- ~54 marks, 4 hours, Section A (Q1-4) + Section B (Q5-8), answer 3 of 4 each
- Numeric problems (RSA, CRT, Miller-Rabin, AES GF arithmetic) carry the most reliable marks — prioritize being able to COMPUTE, not just define
