# Security Fundamentals & Attack Vectors
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
A grab-bag topic covering core security vocabulary (CIA triad, risk equation, security roles), common attack types (DoS/DDoS, phishing, SQL injection, ransomware, social engineering, backdoors), and authentication/network basics (biometrics, wireless threats, handshaking, SWIFT) — mostly short-note / fill-in-the-blank style questions.

## Key steps / algorithm — definitions to memorize
**Covered by Lc#1 (pp.2–17, read):**
1. **Rogue security software:** fake "your PC has a virus" pop-ups that trick users into installing real malware or paying for a fake fix.
2. **DoS attack:** one machine floods a server with traffic until it can't serve legitimate users.
3. **DDoS attack:** same as DoS but from many compromised machines (a **botnet**) — much harder to block/trace since traffic comes from many IPs.
4. **Phishing:** a form of **social engineering** — fake emails/messages trick victims into revealing credentials or installing malware.
5. **SQL Injection:** malicious SQL in input fields exploits app vulnerabilities to read/modify/destroy database data, bypass auth, or void transactions.
6. **Ransomware (Clop/WannaCry):** malware that encrypts files/networks and demands payment; Clop disables Windows Defender/Security Essentials first, then spreads network-wide (e.g. Maastricht University incident).

**⚠️ NOT in any Lc material — pure cheat-sheet, general security knowledge:**
7. **CIA triad:** Confidentiality (no unauthorized disclosure), Integrity (no unauthorized modification), Availability (authorized users can access when needed).
8. **Risk equation:** Risk = Threat × Vulnerability × Impact (asset value). A **threat agent** exploits a **vulnerability** in an **asset** via an **attack vector**.
9. **Security professions:** Penetration Tester (simulates attacks), Cybersecurity Analyst (monitors/responds to incidents), Security Architect (designs secure systems), Security Auditor (checks compliance), Data Security Analyst (protects data assets), Network Security Analyst (secures network infra).
10. **Steganography:** hiding the *existence* of a message (e.g. inside an image/audio file) — vs. cryptography, which hides the *content* of a known message.
11. **Biometric authentication failure modes:** False Accept Rate (FAR — impostor accepted), False Reject Rate (FRR — genuine user rejected); evaluation criteria: accuracy, speed, uniqueness, permanence, user acceptance.
12. **Wireless network threats:** rogue access points, eavesdropping/sniffing, evil twin, deauthentication attacks, WEP/weak-encryption cracking.
13. **Malware short-notes:** **Backdoor** — hidden access bypassing normal auth; **Logic bomb** — malicious code triggered by a condition/date; **Trojan horse** — malware disguised as legitimate software (no self-replication, unlike a virus).
14. **Handshaking + message digest (2024 Q1b):** handshaking = initial negotiation establishing a secure session (algorithms, keys); message digest = fixed-size hash of a message used to verify integrity.
15. **SWIFT pentest scenario:** goal-setting (define scope/objectives without disrupting live banking ops), then non-damaging steps: reconnaissance, vulnerability scanning, controlled exploitation with rollback plans, reporting — emphasize "do no harm to production."

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q1(a,b) | Symmetric vs asymmetric + why asymmetric for e-commerce (3); handshaking + message digest (2) |
| 2023 | Q2(c), Q2(b)*, Q4(c)* | Secure network from phishing/DoS/SQLi/Clop ransomware (2); *digital certs/CA/SSL (4); *Shannon's confusion & diffusion (1) |
| 2022 | Q1 (8), Q7(b,c) | Q1: ambiguity=security(2)+fill-blank threat-actor terms(3)+security professions roles(2)+steganography(1). Q7(b): SQLi+social-eng notes (~3). Q7(c): SWIFT gateway pentest scenario (~4) |
| 2021 | A-1(a,b,c) 8.75, B-4(a,d) 3.75 | A1: risk equation+model(4.75), biometrics FAR/FRR+criteria(3), wireless threats(1). B4: ransomware vs social engineering(2), backdoor/logic bomb/Trojan(1.75) |
| 2020 | — | not standalone |

🔁 Repeats every year in some form: 2-4 marks of "define/short-note this attack type" (rotates through phishing, DoS/DDoS, SQLi, ransomware, social engineering, backdoor/Trojan). Fill-in-blank vocab (threat-actor chain, professions, steganography) and the risk-equation model recur most years. Full solutions: `SecurityFundamentals_Solutions.pdf`.

## Weak spots / common mistakes
- Confusing **steganography** (hides existence) with **cryptography** (hides content) — they're complementary, not the same.
- DoS = one machine; DDoS = botnet of many machines — always state the distinction.
- Phishing IS a social-engineering technique (not separate) — say so explicitly for "differences" questions.
- Backdoor vs Trojan vs logic bomb: backdoor = persistent hidden access; Trojan = disguise as legit software; logic bomb = condition-triggered payload. Don't conflate.
- For SWIFT/pentest essays: always mention authorization/scope + "no damage to production" — graders look for this explicitly.

## Related topics
[[wiki/classical_ciphers|Classical Ciphers]] · [[wiki/symmetric_asymmetric|Symmetric/Asymmetric Ciphers]]
