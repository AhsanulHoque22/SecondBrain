# CSE717 InfoSec Wiki Index
> [[_Topics]] · [[_TopicQuestionMap]] · [[00_Dashboard]]

## Topics
- [[wiki/classical_ciphers|Classical Ciphers]] — Caesar, Playfair, Vigenère, Hill, OTP; recurring Playfair matrix; 5/5 years.
- [[wiki/security_fundamentals|Security Fundamentals & Attack Vectors]] — CIA triad, attack short-notes (DoS/DDoS/phishing/SQLi/ransomware), security professions, steganography, biometrics; mostly no-source cheat sheet.
- [[wiki/symmetric_asymmetric|Symmetric/Asymmetric & Block/Stream Ciphers]] — symmetric cipher ingredients, block vs stream, Feistel structure, public-key cryptosystem elements & key roles; no-source cheat sheet.
- [[wiki/hash_functions|Hash Functions & Hash Table Collision Resolution]] — 6 hash function properties, linear probing, double hashing, quadratic probing; confirmed 2023+2024.
- [[wiki/des_feistel|DES/Feistel/S-box/Avalanche/3-DES]] — Feistel structure, IP/IP⁻¹, F-function, S1-box(37)=8, avalanche+attack families, 3-DES EDE; CRITICAL, 5/5 years.
- [[wiki/digital_signature|Digital Signature]] — generic model diagram, properties/requirements, attack→forgery types, sign-then-encrypt order, RSA key-leak forward secrecy; CRITICAL, 5/5 years.
- [[wiki/number_theory|Number Theory & Modular Arithmetic]] — GCD/Ext.Euclidean+mult.inverse, linear congruence, Fermat, Euler, CRT, Miller-Rabin, discrete log/cyclic groups; HIGHEST-YIELD, 5/5 years, 5–9 marks, foundation for RSA.
- [[wiki/rsa|RSA]] — 8-step key generation + encrypt/decrypt pipeline, square-and-multiply, "given e,n find d"; 5/5 years, 5–16 marks (largest single-topic block some years).
- [[wiki/aes|AES]] — 10-round structure (AddRoundKey, SubBytes/ShiftRows/MixColumns/AddRoundKey×9, final round drops MixColumns), GF(2^8) S-box + MixColumns; 4/5 years, 4–6 marks, block diagram near-certain.
- [[wiki/game_theory|Game Theory & Nash Equilibrium]] — 2×2 payoff matrix, 6-step underline method for NE, strictly dominant strategy; 2/5 years (2023+2024, both most recent), 3–6 marks.
- [[wiki/markov_chains|Markov Chains]] — 2-state security model (Secure/Compromised), transition matrix, steady-state via V(T−I)=0 + normalization; 2/5 years (2023+2024, both most recent), 3–4 marks.
- [[wiki/blockchain|Blockchain & Bitcoin]] — block header/hash chaining, Proof of Work, Merkle tree, bitcoin mining + input/output scripts; 2/5 years (2021+2024), 3–8.75 marks, NEW dedicated 2026 materials.
- [[wiki/quantum_ecc|Quantum Attacks & ECC]] — Shor's breaks RSA+ECC (polynomial), Grover's halves symmetric key strength (quadratic only); ECC point-doubling $2P$ formula; 1/5 years (2024 only), 5 marks.
- [[wiki/ipsec|IPsec]] — 7-component architecture (ESP=confidentiality, AH=auth+integrity, DOI, Key Management), Security Associations (one-way, 3-param), transport vs tunnel mode, RFC 4301 six services; 3/5 years (2020+2021+2024), 2.25–9 marks.
