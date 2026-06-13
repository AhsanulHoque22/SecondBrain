# CSE 717 InfoSec — Topic-Wise Question Map (2020–2024)
> [[_Topics]] · [[_Syllabus]] · [[00_Dashboard]]

> Source: `InformationSecurity Previous Year Questions(2024-2020).pdf` (scanned, read via image OCR 2026-06-13).
> Note: paper headers show mixed course codes (CSE-717 "Information Security" and CSE-718 "Cryptography and Network Security") across years — same syllabus lineage, questions are directly comparable.

## PDF Navigation
| Paper Year | Pages in PDF |
|-----------|-------------|
| 2024 | pp. 1–2 |
| 2023 | pp. 3–4 |
| 2022 | pp. 5–6 |
| 2021 | p. 7 |
| 2020 | pp. 8–9 |

---

### Topic 1 — Number Theory & Modular Arithmetic
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years

- **2024 Q2:** Use Fermat's theorem, find 3^203 mod 11; use Euler's theorem to find a number m between 0 and 9 such that m is congruent to 7^1000 modulo 10
- **2023 Q3:** Calculate 3^11 and 17 (Euler's theorem context); discrete log mod 11=3^x; finding multiplicative inverse mod p
- **2022 Q3:** Outline general algorithm for picking a prime number (Miller-Rabin); calculate 3^11 mod 17 = X; discrete logarithm
- **2021 Q3:** Extended Euclidean algorithm — find multiplicative inverse; Fermat's theorem — 3^203 mod 11; Euler's theorem — find number congruent to 9 mod 11; "find a between 0 and 9 such that a≡7^1000 mod 11"
- **2020 Group A Q2:** Chinese Remainder Theorem (x≡1 mod 3, x≡4 mod 5, x≡6 mod 7); Euler's theorem for finding distinct numbers for b^7 mod 7

**Pattern:** Same exact 3^203 mod 11 / 7^1000 mod 10 style number recurs across years (2021, 2024). CRT system-of-congruences (2020). Miller-Rabin primality test described in 2022/2023.

---

### Topic 2 — RSA Encryption/Decryption Numericals
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years (~4.75-5 marks every year)

- **2024 Q3(b):** RSA with M=3, p=13, q=7 — choose e<10, show steps; explain why Charlie (eavesdropper) cannot decrypt
- **2023 Q6(a):** RSA public-key cryptosystem, p=31, q=11 — perform key generation
- **2022 Q6(a):** RSA encryption/decryption, p=31, q=11, M=2 — full numeric pipeline
- **2021 Q5:** RSA encryption/decryption — given p, q, find n, φ(n), e, d, encrypt/decrypt M
- **2020 Q5(a):** RSA encryption — choose p,q, compute keys, encrypt/decrypt

**Pattern:** ALWAYS small primes (7,11,13,17,31 range). Practice: n=pq → φ(n)=(p-1)(q-1) → pick e coprime to φ(n) → d=e⁻¹ mod φ(n) → C=Mᵉ mod n → M=Cᵏ mod n. Memorize the algorithm cold — numbers change but steps don't.

---

### Topic 3 — Classical Ciphers (Playfair, Hill, OTP)
**Yield:** ⭐⭐⭐ 3/5 years (5–7.5 marks)

- **2024 Q1(a):** Alice using OTP-algorithm scheme with prime modulus P=47 (numeric scheme)
- **2021 Q2:** Solve using Playfair matrix (5x5 key matrix construction + encrypt/decrypt)
- **2020 Group A:** Playfair cipher — encrypt/decrypt with "CRYPTO" key; Vigenère cipher — encrypt message + explain "verification" using the key

**Pattern:** Playfair matrix construction (drop duplicate letters, fill remaining alphabet, I/J combined) appears 2020 & 2021. Hill Cipher is in Lc#1 with worked "HI" example — likely a substitute/addition for Playfair this year. Vigenère NOT in current Lc materials — if asked, fall back to general substitution-cipher logic (shift by repeating keyword).

---

### Topic 4 — AES / Advanced Encryption Standard
**Yield:** ⭐⭐⭐ 3/5 years (~4.75 marks)

- **2023 Q5(a):** Describe two operations (GF(2^8) inverse, AES S-box, multiplicative inverse in GF(2^8) for AES box)
- **2022 Q5(a):** Same — AES S-box operations via GF(2^8), digital signature process
- **2020 Group B Q6(a):** "Using RSA, encrypt message M=3" — adjacent to AES section; AES referenced as encryption standard topic

**Pattern:** GF(2^8) multiplicative inverse computation + S-box construction. Conceptual description more likely than full numeric AES round trace.

---

### Topic 5 — Security Fundamentals & Attack Vectors
**Yield:** ⭐⭐⭐ 3/5 years (4–9 marks)

- **2024 Q1:** "Ambiguity is security's enemy" — fill blanks (motivated to profit by stealing... = cybercrime; roles: penetration tester, cyber security auditor/analyst, data security analyst, network analyst, cyber security architect); what is steganography?
- **2023/2022 Q1:** Same fill-blank format — security terminology + professions + steganography
- **2022/2023 Q7:** SQL injection definition; social engineering; SWIFT banking network scenario — pentest a bank's SWIFT gateway, what would prove successful hack, what steps prevent damage; short notes on SQL injection and social engineering

**Pattern:** Fill-in-the-blank vocabulary question is GUARANTEED Q1 every year — memorize: security professions list, steganography definition, CIA triad terms. SWIFT/pentest scenario is a recurring essay-style Q7.

---

### Topic 6 — Symmetric/Asymmetric & Block/Stream Ciphers
**Yield:** ⭐⭐ 2/5 years (4 marks)

- **2023/2022 Q2:** Essential ingredients of a symmetric cipher; difference between block cipher and stream cipher; Caesar cryptanalysis (known-plaintext, brute force); one-time pad; roles/elements of public-key cryptosystem

**Pattern:** Definitional/comparison — low effort, high reliability if memorized as a table (symmetric ingredients: plaintext, key, encryption algo, ciphertext, decryption algo; block vs stream: fixed-size blocks vs bit/byte stream).

---

### Topic 7 — Blockchain & Bitcoin
**Yield:** ⭐⭐⭐⭐ NEW dedicated materials (Lc#11A/B just added) — 2/5 years historically, but expect 2026 emphasis (4.4-9 marks)

- **2023/2022 Q8:** Explain "same-origin policy" (web security) preferably using full blockchain example; how is data integrity checked in blockchain (Merkle tree depiction given — genesis block → block1→2→3→4, hash pointers, Merkle root); how do you distinguish Ethereum's currency (ETH) from Bitcoin?

**Pattern:** Merkle tree diagram-based question (given a partial tree, compute/verify hashes). ETH vs BTC conceptual comparison. Given Lc#11A (Blockchain) and Lc#11B (Bitcoin Mining) were JUST added as dedicated lecture materials, this topic likely gets a full Q8-style question in 2026 — HIGH PRIORITY.

---

### Topic 8 — IPsec
**Yield:** ⭐⭐ 2/5 years but 8.5–10 marks when it appears (cyclical, absent 2022-24)

- **2021 Q7:** Draw generic model of digital signature; find 8-bit word related to x³+x²+x; how would you test a number n=29 prime or not using Miller-Rabin; benefits of IPsec; differences between transport mode and tunnel mode; general services defined by RFC4301; application of IPsec; compare session state and connection state; explain architecture of IPsec
- **2020 Group B Q8:** Determine benefits of IPsec; general services by RFC4301; application & compare session/connection state; architecture of IPsec; transport vs tunnel mode

**Pattern:** Identical question set 2020 & 2021 (likely the SAME Q8 block reused). Last appeared 2021 — due for a comeback given cyclical pattern AND Lc#7 explicitly covers IPsec architecture/AH/ESP/key exchange.

---

## ⚠️ Insurance topics (in EVERY past paper, NOT found in 2026 Lc materials — verify Day 1)

### DES / Feistel Structure / S-box / Avalanche Effect
- **2023/2022 Q4:** Why include S-box concept in DES Data Encryption Standard; S-box representation DES, schematic 3-DES; cipher block/stream effects
- **2021 Q4:** DES round function, avalanche effect demo, classical Feistel cipher structure, block vs stream cipher differences
- **2020 Group B Q5:** Draw block diagram of 3-DES encryption; what does avalanche effect mean; properties of classical Feistel cipher structure; differences between block cipher and stream cipher

### Digital Signature (generic model + properties)
- **2024 Q7(b):** What properties should a digital signature scheme satisfy?
- **2022/2023 Q6(b):** Properties of digital signature
- **2021 Q7(a):** Draw generic model of digital signature process
- **2020 Group B Q6(b):** Sketch generic model of digital signature process

**If genuinely absent from Lc materials:** these are well-defined textbook topics (Feistel network 16-round structure, DES S-box purpose = nonlinearity, avalanche = 1-bit input change flips ~half output bits; digital signature generic model = sender hashes msg → encrypts hash with private key → receiver decrypts with public key → compares hash). A 1-page cheat sheet covers both — ~30 min investment for guaranteed 5-10 marks.

---

## Recurring numeric "seeds" worth memorizing
- `3^203 mod 11` and `7^1000 mod 10` (Fermat/Euler) — 2021 & 2024
- RSA with p,q ∈ {7,11,13,17,31} — every year
- Playfair key "CRYPTO"/"CSECU" style — 2020
