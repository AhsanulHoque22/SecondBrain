# CSE 719 Distributed & Cloud — Topic-Wise Question Map (2020–2024)
> [[_Topics]] · [[_LecturePlan]] · [[00_Dashboard]]

> Maps each exam topic to exact question numbers + content from past papers.
> Source PDF: `_Cloud prev_merged.pdf` (2020 + 2021 + 2022 + 2024 scanned).
> Last updated: 2026-06-29. **Lecture mapping + orphan audit:** see [[_LecturePlan]].

## Topic → Lecture source index
| Topic | Lecture | Slide-covered? |
|---|---|---|
| 1 DSM | L9 | ✅ (NRNMB strategies orphan) |
| 2 Cloud | L2 + Unit 3/4 readings | ✅ (virtualization subtopic; IaaS cost calc new) |
| 3 RPC | L10 | ✅ (RRA, callback/lightweight orphan) |
| 4 Consistency | L9 (+ L5) | ✅ (linearizability in L9 consistency ladder) |
| 5 DFS + AFS | — none — | 🔴 **ORPHAN — yield now 5/5 (asked all 4 yrs)** |
| 6 Concurrency/Transactions | L10 + L5 | ✅ |
| 7 Fundamentals | L1 | ✅ (coupling/transparencies textbook figs) |
| 8 MapReduce | L3 | ✅ — **yield jumped to 4/5 in 2024 (Q1 all 4 parts)** |
| 9 Paxos | L7 | ✅ — **yield now 4/5** |
| 10 DSO/Parallel-DB/Data-mining | — none — | 🔴 **ORPHAN (textbook)** |
| 11 SQL vs NoSQL | — none — | 🔴 ORPHAN |
| 12 Load balancing | L5 (partial) | ⚠️ |
| 13 Heartbeat/Membership | L4 | ✅ |
| 14 Fault detection | L4 | ✅ |
| 15 Multicast ordering | L5 / L9 partial | ⚠️ PARTIAL (new 2024) |
| 16 Chandy-Lamport snapshot | — none — | 🔴 **NEW ORPHAN (2024)** |
> ⛔ Missing lecture file: **Lecture-08** (07→09 gap) — likely DFS. See [[_LecturePlan]] Orphan Audit.
> Full per-lecture question mind map + coverage assertion: [[_LecturePlan]].

## PDF Navigation
| Paper Year | Code | Pages | Marks / Time |
|-----------|------|-------|--------------|
| 2020 | CSE-813 | pp. 1–2 | 52.5 / 4 hr |
| 2021 | CSE 813 | pp. 3–4 | 52.5 / 4 hr |
| 2022 | CSE 513 | pp. 5–6 | 54 / 4 hr |
| 2024 | CSE-813 | pp. 7–9 | 54 / 4 hr |

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
- **2024 Q4a** — Compare message passing vs DSM approaches (1.5)
- **2024 Q4b** — False sharing + minimize (1.5)
> ⭐ **False sharing appears ALL 4 years.** Memorize: definition + minimize (smaller block size / avoid co-locating unrelated vars on same page).

## 2. Cloud Computing — yield 5/5
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
- **2024 Q5a** — Two benefits and two drawbacks of cloud computing for enterprises (2.5)
- **2024 Q5b** — Fundamental concept of virtualization in cloud; 2 benefits to providers for resource management (2.5) ← **NEW subtopic: virtualization**
- **2024 Q6b** — IaaS vs PaaS trade-offs for e-commerce migration: dev speed, overhead, vendor lock-in, scalability (3)
- **2024 Q6c** — IaaS cost calculation: reserved instances (predictable) vs on-demand (variable workload), compute totals (3) ← **NEW question type: cost arithmetic**
> ⭐ E-commerce deployment-model question is verbatim 2020, 2021, 2022 — lock in IaaS/PaaS/SaaS + public/private/hybrid answer.
> 2024 shifts toward **IaaS vs PaaS analysis** and **virtualization** — study both.

## 3. RPC (Remote Procedure Call) — yield 5/5
- **2020 Q3a** — Primary motivation for RPC + schematic diagram of RPC mechanism (1.5+3)
- **2020 Q3b** — What is a stub? How generated? Functionality & purpose (1.25+3)
- **2020 Q5a** — Communication protocol in RPC; steps of RRA protocol + figure
- **2020 Q5d** — Redefine RRA for concurrent access to multiple servers + figure (2.75)
- **2020 Q5c** — Define callback RPC and lightweight RPC (2)
- **2021 Q8a** — What is RPC? List design issues for RPC (2.75)
- **2022 Q8a** — What is RPC? List design issues for RPC (3)
- **2024 Q5c** — Marshalling/unmarshalling in RPC during invocation; evaluate communication paradigms (message-passing, RPC/RMI) on performance and reliability for time-sensitive apps (4)
> ⭐ "RPC design issues" verbatim 2021 & 2022. 2024 adds paradigm-comparison angle — know message-passing vs RPC trade-offs.

## 4. Consistency models — yield 5/5
- **2020 Q4a** — What is causal consistency? Example application best suited for it (1+2)
- **2020 Q4b** — Weak vs release consistency (shared with DSM) (2+1.5)
- **2021 Q2a** — Strong vs weak consistency; adv/disadv for video-upload site (3)
- **2021 Q2b** — Why strong consistency for law-enforcement video evidence (1.75)
- **2021 Q2c** — 9 replicas + quorums: constraints on read/write quorum sizes; worked example (4)
- **2022 Q4d** — Consistency + types (shared with DSM) (3)
- **2024 Q2b** — What is linearizability? Methods to ensure serializability (1.5)
> Quorum constraints (R+W>N, W>N/2) is the 2021 high-mark item. 2024 adds **linearizability** (top of L9 consistency ladder).

## 5. Distributed File Systems + AFS — yield 5/5 ⭐ (upgraded — asked ALL 4 years)
- **2020 Q7a** — Why is UNIX semantics hard to achieve in a DFS? (example) (2.5)
- **2020 Q7b** — General principles for designing DFS (4)
- **2020 Q7c** — How can the cache be validated? (2.25)
- **2021 Q3b** — UNIX semantics difficulty in DFS (2)
- **2021 Q6c** — DFS requirements / design issues (2)
- **2021 Q6d** — What is Andrew File System? File service architecture of AFS (2)
- **2022 Q6c** — Andrew File System + AFS architecture (2)
- **2024 Q3b** — How do you ensure security in DFS? Briefly remark on message ordering paradigms in distributed systems (3) ← **NEW: DFS security angle**
- **2024 Q4d** — What are venus and vice processes? How does AFS deal with risk of callback message loss? (3) ← **NEW: venus/vice + AFS callbacks**
> ⭐⭐ **DFS appears ALL 4 years. ZERO slide coverage — textbook only.** Venus/vice processes and AFS callbacks are new 2024 sub-topics. This is now the single biggest blind spot with highest yield.

## 6. Concurrency Control & Transactions — yield 5/5
- **2021 Q1d** — Marshalling/Unmarshalling + ACID properties (2)
- **2021 Q6a** — Concurrency control + deadlock + locking schemes (2.75)
- **2021 Q6b** — Timestamp ordering; validation phase vs update phase (2)
- **2022 Q3a–c** — ACID under crashes: (a) disk-per-txn, (b) memory+disk/50 txn, (c) memory+log file — shortcoming of each (3+3+3)
- **2022 Q6a** — Deadlock + locking schemes in concurrency control (3)
- **2022 Q7a** — Two-transaction schedule [r/w trace]: will it run cleanly? what issue? (4)
- **2022 Q7b** — Concurrency control; preventing isolation violation — ways (3)
- **2022 Q7c** — Deadlock detection in distributed systems; when do deadlocks occur (2)
- **2024 Q2a** — Define consensus algorithms; differentiate logical vs physical concurrency (1.5)
- **2024 Q2c** — What is atomic commit protocol? Explain two-phase commit for nested transactions (3)
- **2024 Q3c** — Purpose of wait-for-graph (WFG); give example; conditions a deadlock detection algorithm must satisfy (3) ← **NEW: WFG explicitly asked**
- **2024 Q6a** — How does concurrency in distributed systems differ fundamentally from centralized? Analyze partial failure + no global clock impact (3)
- **2024 Q8a** — What is ACID? Define each letter with one concise sentence (3)
- **2024 Q8b** — Deadlock scenario analysis (rowing crew / boitthas code) — will it deadlock? (3)
> Heavily weighted every year. 2024 adds **WFG**, **2PC for nested transactions**, and a **scenario-based deadlock** question.

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
> No dedicated 2022 or 2024 Q1 on fundamentals — 2024 Q1 is entirely MapReduce.

## 8. MapReduce — yield 4/5 ⭐ (upgraded from 3/5)
- **2021 Q7c** — Various types of MapReduce jobs (2)
- **2022 Q4a** — Two limitations MapReduce places on the Map function (2)
- **2022 Q4b** — How MapReduce handles straggler tasks (2)
- **2024 Q1a** — HPC fault tolerance technique (using message passing) (2.5)
- **2024 Q1b** — MapReduce advantage over MPI for failure handling and recovery (2)
- **2024 Q1c** — GFS exposes block replica locations via API — what important MapReduce optimization does this enable? (2.5)
- **2024 Q1d** — Two important limitations MapReduce places on Map function (same as 2022 Q4a) (2)
> ⭐ 2024 dedicates ALL of Q1 (Section A) to MapReduce — treat it as a core topic now. Know: fault tolerance (checkpointing), straggler handling, locality optimization via GFS, Map function constraints (deterministic + no side effects).

## 9. Paxos — yield 4/5 ⭐ (upgraded from 3/5)
- **2021 Q8c** — Leader waits for < majority of acceptors before proceeding — how it breaks Paxos guarantees (2.5)
- **2022 Q2b** — Paxos w/ same proposal numbers + strict-smaller reject rule: correct? counterexample (6)
- **2024 Q2a** — Define consensus algorithms (shared w/ concurrency) (1.5)
- **2024 Q7a** — Why Paxos cannot tolerate f failures with less than 2f + 1 nodes (3)
- **2024 Q7b** — Leader waits < majority before proceeding — how it breaks Paxos (same as 2021 Q8c) (3)
- **2024 Q7c** — For 3 scenarios, choose primary-backup or Paxos and justify: (i) stock exchange lock server, (ii) documentary movie storage, (iii) login server (3)
> ⭐ "Leader < majority" question repeats 2021 & 2024. 2024 adds: **Paxos fault-tolerance math** (2f+1 nodes) and **primary-backup vs Paxos decision** — both must be known cold.

## 10. DSO + Parallel DB + Data Mining — yield 3/5
- **2021 Q4a** — Define DSO; how scalable parallel DB solves expensive real-world problem (4.25)
- **2021 Q4b** — Database apps finding hidden patterns: what patterns + extraction methods (3.50)
- **2022 Q5a** — DSO + scalable parallel database (4.5)
- **2022 Q5b** — Database hidden patterns + extraction methodologies (3.5)
- **2022 Q5c** — Show an example of a bitemporal relation (1)
> 2024 does not include DSO questions. Still textbook-only.

## 11. SQL vs NoSQL — yield 2/5
- **2021 Q7b** — Briefly describe SQL and NoSQL databases + comparative analysis (4.75)

## 12. Load balancing — yield 2/5
- **2021 Q7a** — What is round-robin load balancing? (2)

## 13. Heartbeating + Group Membership — yield 2/5
- **2022 Q6b** — How to increase robustness of all-to-all heartbeating (2)
- **2022 Q6d** — How to design a group membership protocol (2)

## 14. Fault Detection & Recovery — yield 3/5 (upgraded from 2/5)
- **2020 Q2b** — Techniques for fault detection and recovery in distributed OS (2.75)
- **2024 Q2d** — Primary goal of failure detection; why perfect/instant detection is practically impossible in asynchronous networks (3)
- **2024 Q3a** — Server carrying client requests: why can't it bound response time? What should it do to execute within bounded time? (3)
> 2024 adds two failure-detection questions. Know: FLP impossibility, asynchronous network model, timeout trade-offs.

## 15. Multicast Message Ordering — yield 2/5 (NEW topic, 2024)
- **2024 Q4c** — Briefly explain the different types of ordering of multicast messages in overlapping groups (3)
> ⚠️ FIFO / Causal / Total (atomic) ordering. Partially covered in L5/L9. Know all three definitions + why they matter for overlapping groups.

## 16. Chandy-Lamport Global Snapshot — yield 1/5 (NEW ORPHAN, 2024)
- **2024 Q8c** — (i) Does Chandy-Lamport work correctly for non-FIFO channels? (ii) In n-process system, will snapshot always show ≥ n−1 empty channels? Take a position and justify (3)
> 🔴 **ORPHAN — no slides.** Answer: (i) FALSE — algorithm requires FIFO channels. (ii) FALSE — not necessarily n−1 empty. Study from textbook (Tanenbaum Ch on global state / Lamport clocks).
