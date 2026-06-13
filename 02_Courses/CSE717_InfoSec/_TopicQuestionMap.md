# CSE 717 InfoSec — Topic-Wise Question Map (2020–2024)
> [[_Topics]] · [[_Syllabus]] · [[00_Dashboard]]

> Source: `InformationSecurity Previous Year Questions(2024-2020).pdf` (scanned, re-read via 300dpi image OCR 2026-06-13 — supersedes the first-pass read, which had several misreads).
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

### Topic 1 — Classical Ciphers (Caesar, Playfair, Hill, Vigenère, OTP)
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years (2–9 marks)

- **2024 Q2(a,b):** Encrypt "CRYPTO" with Caesar shift 5 (1.5); Caesar f(p)=(p+4)mod26, decrypt "ONXNG" (1.5)
- **2023 Q1(a):** Encrypt "See you at CSECU" using a GIVEN 5×5 Playfair matrix (4)
- **2022 Q2(b):** Cryptanalysis of Caesar cipher and one-time pad — how could it possibly work? (conceptual, part of 2(a,b,c)=3+3+4=10)
- **2021 A2(a):** "OTP offers complete security — agree?" + fundamental difficulties of OTP (2.75); **A2(b):** Encrypt "See you at CSE department" using GIVEN Playfair matrix (~2); **A4(iv):** Write a program to encrypt/decrypt using general Caesar cipher (2)
- **2020 Q1(a):** Encrypt "Must see you over CU playground. Coming now." using GIVEN Playfair matrix (4); **Q1(b):** Encrypt "explanation" with Vigenère cipher, key "cse" (4.75)

**⚠️ 2026-06-13 second correction:** the previously-listed "2023 Q7(a,b) Caesar f(p)=(p+12)mod26 on CSECU / decrypt CHATTOGRAM shift k=7" was a misattribution — those are Lc#1 SLIDE WORKED EXAMPLES, not a past-paper question. Removed from the 2023 row above.

**🎯 KEY FINDING — recurring Playfair matrix:** 2020, 2021, AND 2023 all give the EXACT SAME 5×5 matrix:
```
M F H I/J K
U N O P Q
Z V W X Y
E L A R G
D S T B C
```
Memorize this matrix cold — high chance it recurs again in 2026. If given, you only need the encryption procedure.

**Pattern:** EVERY year has a classical cipher question, 2-9 marks. Playfair matrix is usually GIVEN as the matrix above — practice using it to encrypt sentences with spaces (drop spaces, handle digraphs/duplicates, X filler). Caesar appears as both encrypt and decrypt with arbitrary f(p)=(ap+b)mod26 forms, and as a "write a program" question (2021). Vigenère (2020) and OTP conceptual (2021, 2022) both occurred — Hill Cipher (in Lc#1, worked "HI"/"CD" examples) has NOT appeared in 2020-2024 papers but is in source material as a likely substitute/addition.

---

### Topic 2 — Security Fundamentals & Attack Vectors
**Yield:** ⭐⭐⭐⭐ 4/5 years (2–9 marks) — re-verified 2026-06-13 via 300dpi re-read

- **2024 Q1(a):** Briefly describe symmetric and asymmetric cryptography with an example; point out why asymmetric cryptography is useful for e-commerce (3); **Q1(b):** What is handshaking? Briefly describe how message-digest works (2)
- **2023 Q2(c):** Explain briefly how to secure a network from: (i) Phishing attack (ii) Denial of service attack (iii) SQL injection attack (iv) Clop ransomware (2). *Related (not core):* Q2(b) digital certificates/CA/SSL secure web exchange (4); Q4(c) Shannon's two atomic operations in security [confusion & diffusion] (1)
- **2022 Q1 (whole question, 2+3+2+1=8):** (a) "Ambiguity is security" — why and how? (2); (b) Fill-in-the-blank security terms — "A ... (C) ... here is the existence of an individual motivated to profit by stealing an asset and selling it for cash" [threat actor/asset/attack vector] (3); (c) Write down key roles/responsibilities of: penetration tester, cyber security analyst, cyber security auditor, data security analyst, network analyst, cyber security architect (2); (d) What is steganography? (1). **Q7(b):** Write short notes on SQL injection and social engineering (~3); **Q7(c):** SWIFT banking-network pentest scenario — goal-setting + non-damaging steps for testing a bank's SWIFT gateway (~4)
- **2021 A-1(a):** Derive a risk equation depending on threat agent, probability of attack, and expected loss; draw a related model (4.75); **A-1(b):** How do physical and behavioural biometrics fail for authentication? How would you evaluate biometrics using standard criteria? (3); **A-1(c):** Remark on the threats in wireless security (1). **B-4(a):** How would you differentiate between ransomware and social engineering? (2); **B-4(d):** Describe backdoor, logic bomb, and Trojan horse (1.75)
- **2020:** not directly present as standalone — 2020 paper covers Playfair/Vigenère/CRT/discrete-log/Fermat/Euler/DES/RSA/digital signature/Miller-Rabin/IPsec only, nothing matching this topic's vocab/attack-type theme

**Pattern:** Fill-in-blank/short-note vocabulary (CIA-triad-adjacent terms, security professions, steganography, biometrics, wireless threats, backdoor/logic-bomb/Trojan, ransomware vs social engineering) is the dominant style — appears as a multi-part Q1 (2022) or scattered across A-1/B-4 (2021) or Q1/Q2(c) (2024/2023). SWIFT/pentest essay (2022) and Shannon's confusion/diffusion (2023) are one-off but plausible repeats. NONE of this is covered in any Lc material except the 6 attack types on Lc#1 pp.2-17 (Rogue security software, DoS, DDoS, Phishing, SQL Injection, Ransomware) — everything else is a cheat-sheet item like Topics 13/14.

---

### Topic 3 — Symmetric/Asymmetric & Block/Stream Ciphers
**Yield:** ⭐⭐⭐ bundled into Topic 2 most years, standalone big Q in 2022 (10 marks)

- **2024 Q1(a):** symmetric vs asymmetric crypto, why asymmetric for e-commerce (3) — overlaps Topic 2
- **2022 Q2:** essential ingredients of symmetric cipher (3), block vs stream cipher difference (3), Caesar/OTP cryptanalysis (2), public/private key roles (2) = 10
- **2020 Q5(b,c):** classical Feistel structure (3), block vs stream differences (1)

**Pattern:** Comparison-table material (symmetric ingredients; block vs stream; public/private key roles). Quick to memorize, moderate but recurring credit.

---

### Topic 4 — Hash Functions & Hash Table Collision Resolution (NEW — confirmed in Lc#2)
**Yield:** ⭐⭐⭐ 2/5 years (2023, 2024 — both most recent), 3 marks each, + supporting role for digital signatures/blockchain

- **2024 Section B Q7(c):** Hash table size m=13, double hashing — h1(k)=k mod 13, h2(k)=7+(k mod 7) — insert keys [8,47,22,44,39,32] in order (3)
- **2023 Section B Q8(c):** Hash table size m=13, open addressing, h(k)=(k+2) mod m, linear probing — insert keys [21,8,13,44,28,33] (3)
- **2023 Section B Q5(b):** Enumerate properties of a good hash function (2.5)
- Lc#2 has WORKED EXAMPLES of both linear probing and double hashing with the exact "insert into hash table of length m=10/11" framing — directly matches exam style.

**Pattern:** Both 2023 AND 2024 ask a hash-table insertion trace (linear probing or double hashing) — this is now a near-certain repeat. Practice both collision-resolution methods on a list of ~6 keys. Hash function properties (deterministic, fixed-size, avalanche, one-way, collision-resistant) support Topic 13/Blockchain too.

---

### Topic 5 — Game Theory & Nash Equilibrium (NEW — confirmed in Lc#3)
**Yield:** ⭐⭐⭐ 2/5 years (2023, 2024 — both most recent), 3-6 marks

- **2024 Section B Q7(a):** Eve/Mallory choosing PT vs ND training, given payoff matrix — find all Nash equilibria; does either player have a strictly dominant strategy? (3)
- **2023 Q4(b):** "Using game theory, design a strategy to identify attackers in a mobile social network" (3); **Section B Q8(a):** Alice/Bob ST#1/ST#2 payoff matrix (10,10 / 8,4 / 4,8 / 5,5) — find Nash equilibrium + dominant strategy (3)

**Pattern:** 2x2 payoff-matrix questions — find Nash equilibrium(s) by checking best responses, and identify dominant strategies. Lc#3 covers this with worked examples. Cheap, mechanical marks once the method is drilled.

---

### Topic 6 — Markov Chains (steady-state / long-run behaviour)
**Yield:** ⭐⭐⭐⭐ 2/5 years (2023, 2024 — both most recent, RECENCY signal), 3-4 marks

- **2024 Q1(c):** Secure(S)/Compromised(C) system — Secure→Secure w.p. 0.4 (else →Compromised), Compromised→Secure w.p. 0.3 (else stays Compromised). Find steady-state probabilities of S and C; is the system more likely secure or compromised long-run? (4)
- **2023 Section B Q6(c):** Secure/insecure network system with patch-cycle transition probabilities (80%/60% style) — determine long-term behaviour (3)

**Pattern:** Both questions are 2-state Markov chains (security/insecure) — set up the 2×2 transition matrix, solve πP=π with π1+π2=1 for steady state. Lc#4A/4B has the theory + a worked weather example — map that method directly onto the security-state framing. UPGRADED from "1/5 unknown" — this is now a confirmed 2-year-running, high-confidence repeat.

---

### Topic 7 — Number Theory & Modular Arithmetic
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years (5–9 marks) — foundation for RSA (Topic 8) and Digital Signature

- **2024 Q1(b,c):** Fermat/Euler theorem pair (2.5+2.5)
- **2023 Q1(b,c):** Fermat 3^302 mod 11 (2.5), Euler — find m∈[0,9] with m≡7^1000 mod 11 (2.5); **Q4(a):** State + apply CRT: X≡2(mod3), X≡4(mod5), X≡6(mod7) (5); **Section B Q7(b):** solve congruence 33X≡18(mod 280) (3)
- **2022 Q3:** Miller-Rabin primality algorithm (3), discrete log 11≡3^X mod17 explained via cyclic groups (3), Fermat 2^83 mod 5 (2), Euler — find X∈[0,9] with X≡5^1000 mod 10 (1)
- **2021 A3:** discrete log/cyclic group (2.75), ext. Euclidean — mult. inverse of 1234 mod 4321 (2), Fermat 3^301 mod 11 (2), Euler — find X∈[0,28] with X^45≡6 mod 35 (2)
- **2020 Q2:** CRT — X≡1 mod{3,4,5,7} (4.75), discrete log/cyclic groups + distinct remainders of b^x mod7 (2+2); **Q3:** ext. Euclidean — mult. inverse of 550 mod 1769 (4.75), Fermat 3^202 mod 11 + Euler 7^1000 mod 10 (2+2)

**Pattern:** HIGHEST-yield topic, confirmed every year, 6-9 marks. Recurring numeric "seeds": `3^20x mod 11` and `7^1000 mod 10/11` (Fermat/Euler combo — appears 2020,2021,2023,2024 in near-identical form). Extended Euclidean for multiplicative inverse appears almost every year. CRT appears 2020 & 2023. Miller-Rabin + discrete log/cyclic group appear 2020-2022.

---

### Topic 8 — RSA Encryption/Decryption Numericals
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years (5–16 marks every year — largest single-topic block some years)

- **2024 Q2(c):** Encrypt "DATA" via RSA, p=61,q=53,e=17 (3); **Q3(a):** decrypt ciphertext block c=17 with same p,q,e (3)
- **2023 Q7(c):** Encrypt "CU" via RSA, p=43,q=59 (3); **Q7(d):** decrypt with same p,q (2)
- **2022 Q6:** Encrypt M=3 via RSA, p=13,q=7, choose e<10, show steps; explain why eavesdropper (Charlie) can't decrypt without private key (3+3+2+8=16!)
- **2021 B2(a):** Encrypt+decrypt RSA, p=3,q=11,e=7,M=2 (2.75); **B2(b):** given e=31,n=3599, find private key d (2+2)
- **2020 Q6(a):** Encrypt+decrypt RSA, p=3,q=11,e=7,M=2 (4.75); **Q6(b):** given e=31,n=3599, find private key d (2+2)

**Pattern:** ALWAYS small primes (3,7,11,13,17,31,43,53,59,61 range). Drill the full pipeline cold: n=pq → φ(n)=(p-1)(q-1) → pick/verify e coprime to φ(n) → d=e⁻¹ mod φ(n) (extended Euclidean — links to Topic 7) → C=Mᵉ mod n → M=Cᵏ mod n. The "given e,n find d" variant (2020&2021, identical numbers e=31,n=3599) is a near-certain repeat style.

---

### Topic 9 — AES (Advanced Encryption Standard)
**Yield:** ⭐⭐⭐⭐ 4/5 years (4–6 marks)

- **2024 Q1(c):** ShiftRows+MixColumns diffusion explanation + perform ShiftRows on given state matrix (4); **Q3(d):** AES encryption block diagram (2)
- **2023 Q3(c):** AES encryption block diagram (4)
- **2022 Section B Q5:** AES S-box operation via GF(2^8), multiplicative inverse table, S-box({C4})=? (1.5+4.5)
- **2021 Section B Q1(a):** AES encryption block diagram (4.75)
- 2020: not found directly

**Pattern:** AES block diagram (rounds, SubBytes/ShiftRows/MixColumns/AddRoundKey) is a recurring "draw the diagram" question (2021,2023,2024). S-box/GF(2^8) inverse computation (2022) and ShiftRows trace (2024) are the numeric variants — practice both diagram + one GF(2^8) inverse lookup.

---

### Topic 10 — Quantum Attacks & ECC
**Yield:** ⭐⭐ 1/5 years (2024 only, NEW numeric type), 3-5 marks

- **2024 Q6(a):** Elliptic curve E: y²=x³+2x+3 over F₁₉, compute 2P for P=(3,6) (3) — point-doubling numeric!; **Q6(b):** Why ECC/RSA more vulnerable than symmetric algorithms to quantum attacks (2)

**Pattern:** Only 2024, but it's a genuine NUMERIC computation (point doubling on an elliptic curve mod p) — Lc#6 has worked ECC examples. Given only 1/5 years and the computation is moderately involved, treat as medium priority: learn the point-doubling formula and one worked example, don't over-invest.

---

### Topic 11 — IPsec
**Yield:** ⭐⭐⭐ 3/5 years (2.25–9 marks, cyclical)

- **2024 Section B Q5(c):** IPsec architecture + role of security associations (3)
- **2021 Section B Q4(b,c):** application areas + session vs connection state (2.5), architecture (2.5)
- **2020 Q8:** benefits + transport vs tunnel mode (2.25), RFC4301 services (2.25), application areas + session/connection state (2.25), architecture (2)

**Pattern:** Architecture diagram + transport vs tunnel mode + RFC4301 services + session vs connection state — same cluster of sub-questions recurs (2020,2021,2024). Higher yield than previously thought (was rated 2/5, now 3/5 with 2024 confirmed).

---

### Topic 12 — Blockchain & Bitcoin
**Yield:** ⭐⭐⭐⭐ 3/5 years (2.75–12 marks), dedicated 2026 materials (Lc#11A/B) → expect strong 2026 emphasis

- **2024 Q3(c):** Blockchain security via hashing + Proof of Work (3)
- **2022 Q8:** same-origin policy via blockchain example (4), Merkle tree data-integrity diagram (4), ETH vs BTC distinction (4) = 12
- **2021 Section B Q3:** blockchain-cryptography relation + "what is bitcoin" (2.75+2), bitcoin input/output script signature validation (4)

**Pattern:** Merkle tree diagram-based integrity question (2022) is the most detailed historical ask. Proof-of-Work + hashing security (2024) is simpler/conceptual. ETH vs BTC comparison recurs. Given NEW dedicated Lc#11A/11B materials, expect a full Q8-style question — HIGH PRIORITY, matches existing rating.

---

### Topic 13 — DES / Feistel Structure / S-box / Avalanche Effect / 3-DES
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years (5–10 marks) — ⚠️ NOT in any 2026 Lc material → CHEAT SHEET REQUIRED, but CONFIRMED GUARANTEED, not optional

- **2024 Q6(d):** avalanche effect + two families of attacks in DES (2)
- **2023 Q3(a,b):** 3-DES block diagram + DES encryption equation (3), avalanche effect + two attack families (2); **Section B Q5(a):** F-function in DES details (2.5)
- **2022 Q4:** why S-box in DES + S1-box value lookup for input 37 (2), 3-DES schematic + encryption equation (3), f-function component description (3)
- **2021 A4:** IP⁻¹ equation explanation (part of 4.75), 3-DES block diagram + equation (2.75), avalanche effect + two attack families (2)
- **2020 Q4(a):** IP/IP⁻¹ purpose + S1-box lookup for 37 (2+2.75), F-function details; **Q4(b):** IP⁻¹ decryption equation, finite fields in cryptography; **Section B Q5(a,b):** 3-DES block diagram+equation (2.75×2), avalanche+2 attack families, classical Feistel structure (3)

**Pattern:** EVERY SINGLE YEAR. Sub-questions cycle through: (1) 3-DES block diagram + encryption equation, (2) avalanche effect definition + name the two families of DES attacks (differential & linear cryptanalysis), (3) F-function components diagram, (4) S-box purpose / S1-box table lookup for a given input byte, (5) IP/IP⁻¹ permutation purpose, (6) classical Feistel structure properties. **Build a 1-2 page cheat sheet covering all 6 sub-patterns — this is ~6-10 guaranteed marks for ~45min of focused memorization.**

---

### Topic 14 — Digital Signature (generic model, properties, vulnerabilities)
**Yield:** ⭐⭐⭐⭐⭐ 5/5 years (1–7 marks) — partial Lc coverage (hash properties in Lc#2), generic-model diagram likely needs cheat sheet too

- **2024 Q2(a):** what is digital signature + attack types that make it vulnerable (3); **Section B Q2(c):** same theme (3); **Section B Q8(d):** draw generic model of digital signature (1)
- **2023 Q2(a):** what is digital signature + vulnerable attacks (3); **Section B Q5(c):** attack types vulnerable to digital signature (3); **Section B Q5(d):** RSA key-reuse safety after private-key leak (1)
- **2022 Section B Q5(b):** properties a digital signature should have + scheme requirements; **Q7(a):** order of signature vs confidentiality function + threats to direct digital signature
- **2021 Section B Q2(c):** draw generic model of digital signature (2)
- **2020 Q7(a):** draw generic model of digital signature process (4.75)

**Pattern:** EVERY SINGLE YEAR. Two recurring forms: (1) "draw/sketch the generic model of digital signature process" (sender hashes msg → encrypts hash with private key → receiver decrypts with public key → compares hashes) — 1-4.75 marks, pure diagram; (2) "what attacks make digital signatures vulnerable / what properties must they satisfy" — conceptual, 3 marks. **Combine with Topic 13 cheat sheet — both are guaranteed, diagram-heavy, low-prerequisite topics.**

---

## Recurring numeric "seeds" worth memorizing
- `3^20x mod 11` and `7^1000 mod 10/11` (Fermat/Euler combo) — 2020, 2021, 2023, 2024
- RSA with p,q ∈ {3,7,11,13,17,31,43,53,59,61} — every year; "e=31,n=3599→find d" repeats 2020&2021 verbatim
- S1-box lookup for input value 37 — 2020 & 2022 identical
- Hash table insertion (linear probing / double hashing) on a 6-key list, m=10-13 — 2023 & 2024
- 2x2 Nash equilibrium payoff matrix — 2023 (×2) & 2024
- Playfair matrix is usually GIVEN — practice encrypting full sentences (with spaces) against a provided 5×5 matrix
