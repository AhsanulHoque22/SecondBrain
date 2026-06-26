# CSE 719 Distributed & Cloud — Topic-Wise Question Map (2020–2022)
> [[_Topics]] · [[00_Dashboard]]

> Maps each exam topic to exact question numbers + content from past papers.
> Source PDF: `_Cloud prev.pdf` (scanned). Only 3 years available — no 2023/2024 papers in the bundle.
> Last updated: 2026-06-26 (reset day).

## PDF Navigation
| Paper Year | Code | Pages | Marks / Time |
|-----------|------|-------|--------------|
| 2020 | CSE-813 | pp. 1–2 | 52.5 / 4 hr |
| 2021 | CSE 813 | pp. 3–4 | 52.5 / 4 hr |
| 2022 | CSE 513 | pp. 5–6 | 54 / 4 hr |

## ⚡ EXAM FORMAT (Critical)
- **Answer any 3 questions from each section** (Section A + Section B), separate scripts per section.
- 8 questions total (Q1–Q4 Sec A, Q5–Q8 Sec B). Figures in right margin = marks.

---

## 1. DSM (Distributed Shared Memory) — yield 5/5
- **2020 Q4b** — Differentiate weak vs release consistency; which for DSM design & why (2+1.5)
- **2020 Q4c** — Why does simple LRU fail as block replacement policy in DSM? (2.25)
- **2020 Q6a** — Draw schematic diagram of DSM (1.75)
- **2020 Q6b** — What is false sharing? How to minimize it? (1+2)
- **2020 Q6c** — Adv/disadv of NRNMB, NRMB, RMB, RNMB strategies in DSM design (4)
- **2021 Q3c** — False sharing + minimize (2)
- **2021 Q3d** — What is consistency? Types implementable with DSM (2)
- **2021 Q8b** — Define DSM; discuss with suitable illustrations (3.5)
- **2022 Q4c** — False sharing + minimize (2)
- **2022 Q4d** — Consistency + types implementable with DSM, define (3)
- **2022 Q8b** — Define DSM; implement DSM over a message-passing network (3)
- **2022 Q8c** — Compare Invalidate vs Update protocols; which preferable & why (3)
> ⭐ False sharing appears all 3 years. Memorize: definition + minimize (smaller block size / avoid co-locating unrelated vars).

## 2. Cloud Computing fundamentals — yield 5/5
- **2020 Q1a** — Define distributed and cloud systems + examples (2+1)
- **2020 Q8a** — Define cloud computing + pros/cons (2)
- **2020 Q8b** — E-commerce website: which cloud services + deployment models (4)
- **2020 Q8c** — Cloud aspects useful for prognostic health management apps (2.75)
- **2021 Q3a** — E-commerce website cloud services + deployment models (2.75)
- **2021 Q4c** — Phases involved in cloud architecture (1)
- **2021 Q5a** — On-demand functionality: what + how provided in cloud (1.75)
- **2021 Q5b** — What is a cloud? Platforms for large-scale cloud computing (1)
- **2021 Q5c** — Layers in cloud + working + diff cloud vs distributed (3)
- **2021 Q5d** — What is EUCALYPTUS? Why used? Deployment models (3)
- **2022 Q1a** — Define cloud computing; horizontal vs vertical scaling + scenarios (5)
- **2022 Q1b** — E-commerce website cloud services + deployment models (2)
- **2022 Q1c** — What is multi-tenancy? (2)
- **2022 Q2a** — EC2 VMs vs physical machines: 3 benefits to Amazon + motivation (3)
> ⭐ E-commerce deployment-model question is verbatim all 3 years. Lock in IaaS/PaaS/SaaS + public/private/hybrid answer.

## 3. RPC (Remote Procedure Call) — yield 5/5
- **2020 Q3a** — Primary motivation for RPC + schematic diagram of RPC mechanism (1.5+3)
- **2020 Q3b** — What is a stub? How generated? Functionality & purpose (1.25+3)
- **2020 Q5a** — Communication protocol in RPC; steps of RRA protocol + figure
- **2020 Q5d** — Redefine RRA for concurrent access to multiple servers + figure (2.75)
- **2020 Q5c** — Define callback RPC and lightweight RPC (2)
- **2021 Q8a** — What is RPC? List design issues for RPC (2.75)
- **2022 Q8a** — What is RPC? List design issues for RPC (3)
> ⭐ "RPC design issues" repeats verbatim 2021 & 2022. Schematic + stub heavy in 2020.

## 4. Consistency models — yield 5/5
- **2020 Q4a** — What is causal consistency? Example application best suited for it (1+2)
- **2020 Q4b** — Weak vs release consistency (shared with DSM) (2+1.5)
- **2021 Q2a** — Strong vs weak consistency; adv/disadv for video-upload site (3)
- **2021 Q2b** — Why strong consistency for law-enforcement video evidence (1.75)
- **2021 Q2c** — 9 replicas + quorums: constraints on read/write quorum sizes; worked example (4)
- **2022 Q4d** — Consistency + types (shared with DSM) (3)
> Quorum constraints (R+W>N, W>N/2) is the 2021 high-mark item.

## 5. Distributed File Systems + AFS — yield 4/5
- **2020 Q7a** — Why is UNIX semantics hard to achieve in a DFS? (example) (2.5)
- **2020 Q7b** — General principles for designing DFS (4)
- **2020 Q7c** — How can the cache be validated? (2.25)
- **2021 Q3b** — UNIX semantics difficulty in DFS (2)
- **2021 Q6c** — DFS requirements / design issues (2)
- **2021 Q6d** — What is Andrew File System? File service architecture of AFS (2)
- **2022 Q6c** — Andrew File System + AFS architecture (2)
> AFS appears 2021 & 2022. UNIX-semantics difficulty appears 2020 & 2021.

## 6. Concurrency Control & Transactions — yield 4/5
- **2021 Q1d** — Marshalling/Unmarshalling + ACID properties (2)
- **2021 Q6a** — Concurrency control + deadlock + locking schemes (2.75)
- **2021 Q6b** — Timestamp ordering; validation phase vs update phase (2)
- **2022 Q3a–c** — Transaction processing w/ ACID under crashes: shortcomings of (a) disk-per-txn, (b) memory+disk every 50 txn, (c) memory + log file (3+3+3)
- **2022 Q6a** — Deadlock + locking schemes in concurrency control (3)
- **2022 Q7a** — Two-transaction schedule [r/w trace]: will it run cleanly? what issue? (4)
- **2022 Q7b** — Concurrency control; preventing isolation violation — ways (3)
- **2022 Q7c** — Deadlock detection in distributed systems; when do deadlocks occur (2)
> Heavily weighted in 2022. ACID + deadlock + locking recur.

## 7. Distributed System Fundamentals — yield 4/5
- **2020 Q1a** — Define distributed and cloud systems + examples (2+1)
- **2020 Q1b** — Tightly vs loosely coupled systems + figures (3.25)
- **2020 Q1c** — Why distributed computing better than parallel processing (2.5)
- **2020 Q2a** — Location vs relocation vs migration transparency + examples (3)
- **2020 Q2c** — Design principles for better performance in distributed system (3)
- **2021 Q1a** — Define distributed system + real-time examples (1.75)
- **2021 Q1b** — Adv of distributed computing over standalone + disadvantages (2.5)
- **2021 Q1c** — Define scalability + challenges in scalable distributed systems (2.5)
- **2021 Q1d** — Marshalling/Unmarshalling + ACID (shared) (2)
> Section-A opener both 2020 & 2021. Transparencies + scalability are reliable.

## 8. MapReduce — yield 3/5
- **2021 Q7c** — Various types of MapReduce jobs (2)
- **2022 Q4a** — Two limitations MapReduce places on the Map function (2)
- **2022 Q4b** — How MapReduce handles straggler tasks (2)

## 9. Paxos — yield 3/5
- **2021 Q8c** — Leader waits for < majority of acceptors before proceeding — how it breaks Paxos guarantees (2.5)
- **2022 Q2b** — Paxos w/ same proposal numbers + strict-smaller reject rule: correct? counterexample (6)
> 2022 version is 6 marks — high. Know the proposal-number / promise rules cold.

## 10. DSO + Parallel DB + Data Mining — yield 3/5
- **2021 Q4a** — Define DSO; how scalable parallel DB solves expensive real-world problem (4.25)
- **2021 Q4b** — Database apps finding hidden patterns: what patterns + extraction methods (3.50)
- **2022 Q5a** — DSO + scalable parallel database (4.5)
- **2022 Q5b** — Database hidden patterns + extraction methodologies (3.5)
- **2022 Q5c** — Show an example of a bitemporal relation (1)

## 11. SQL vs NoSQL — yield 2/5
- **2021 Q7b** — Briefly describe SQL and NoSQL databases + comparative analysis (4.75)

## 12. Load balancing — yield 2/5
- **2021 Q7a** — What is round-robin load balancing? (2)

## 13. Heartbeating + Group Membership — yield 2/5
- **2022 Q6b** — How to increase robustness of all-to-all heartbeating (2)
- **2022 Q6d** — How to design a group membership protocol (2)

## 14. Fault detection & recovery — yield 2/5
- **2020 Q2b** — Techniques for fault detection and recovery in distributed OS (2.75)
