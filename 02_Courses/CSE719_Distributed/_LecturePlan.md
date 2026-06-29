# CSE 719 — Lecture-by-Lecture Study Plan & Question Mind Map
> [[_Topics]] · [[_TopicQuestionMap]] · [[wiki/_index]] · Built 2026-06-26 from slide audit + 2020/21/22/24 past papers.

**Exam: Wed 1 Jul 2026.** Format: answer **any 3 of 4 questions per section** (A & B), ~52.5–54 marks, 4 hr.
This file walks Lecture 1 → 10 serially. Each lecture lists its topics, the exact past-paper questions it answers, and a study slot. **Every question-part across 4 papers is accounted for** — either under a lecture or in the **Orphan Audit** at the bottom.

> ⚠️ **Study by yield, not by lecture number.** Serial order is for *coverage*; the priority order is at the very bottom. Highest-yield lectures: **9 (DSM), 2 (Cloud), 10 (RPC+Concurrency), 3 (MapReduce — upgraded 2024)**.

---

## Lecture 1 — Distributed Systems: Introduction  · Topic #7 · yield 4/5
**Slides:** definition (Tanenbaum + working def), 9 design goals, hard issues (no global clock, failures, variable BW/latency, scale).
**Status:** ✅ wiki [[wiki/distributed-fundamentals]] + `Fundamentals_Solutions.pdf` done.

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q1a | Define distributed + cloud systems + examples | ✅ slide |
| 2020 Q1b | Tightly vs loosely coupled + figures | ⚠️ textbook fig (L2 mentions once) |
| 2020 Q1c | Distributed vs parallel processing | ⚠️ textbook |
| 2020 Q2a | Location/relocation/migration transparencies | ⚠️ textbook (L5 says "transparency" 4×) |
| 2020 Q2c | Design principles for performance | ✅ slide |
| 2021 Q1a | Define DS + real-time examples | ✅ slide |
| 2021 Q1b | Advantages/disadvantages of DS | ✅ slide |
| 2021 Q1c | Scalability + challenges | ✅ slide (+readings) |

---

## Lecture 2 — Introduction to Cloud Computing  · Topic #2 · yield 5/5 ⭐
**Slides + readings** (Unit 3, Unit 4, `Lecture-01.pdf`, `lecture-02.pdf`): providers (AWS/Azure/GCE), public vs private, IaaS/PaaS/SaaS, on-demand, deployment models, multi-tenancy, EUCALYPTUS, virtualization.

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q8a | Define cloud + pros/cons | ✅ slide |
| 2020 Q8b | E-commerce: cloud services + deployment models | ✅ slide (asked ALL 4 yrs) |
| 2021 Q3a | E-commerce cloud services + deployment | ✅ slide |
| 2021 Q4c | Phases in cloud architecture | ⚠️ partial (readings) |
| 2021 Q5a | On-demand functionality | ✅ slide |
| 2021 Q5b | What is a cloud + large-scale platforms | ✅ slide |
| 2021 Q5c | Cloud layers + cloud vs distributed | ✅ Unit 4 |
| 2021 Q5d | EUCALYPTUS + deployment models | ✅ slide (L2 + Unit 3) |
| 2022 Q1b | E-commerce cloud services + deployment | ✅ slide |
| 2022 Q1c | Multi-tenancy | ✅ readings (CMU/Unit 3) |
| 2022 Q2a | EC2 VMs vs physical machines — 3 benefits | ⚠️ partial (reason from slide) |
| 2022 Q1a | Define cloud + **horizontal vs vertical scaling** | scaling part → **ORPHAN** |
| 2020 Q8c | Cloud for prognostic health management | **ORPHAN** (application reasoning) |
| 2024 Q5a | Two benefits + two drawbacks of cloud for enterprises | ✅ slide |
| 2024 Q5b | Virtualization in cloud: concept + 2 benefits for resource management | ✅ slide (virtualization topic) |
| 2024 Q6b | IaaS vs PaaS trade-offs for e-commerce migration (dev speed, overhead, lock-in, scalability) | ✅ slide (IaaS/PaaS/SaaS) |
| 2024 Q6c | IaaS cost calculation: reserved instances (predictable workload) + on-demand (variable) | ⚠️ NEW — apply IaaS concepts arithmetically |

---

## Lecture 3 — MapReduce & Hadoop  · Topic #8 · yield 4/5 ⭐ (upgraded)
**Slides:** Map/Reduce model (Lisp roots), Hadoop, HDFS, fault tolerance via duplication, stragglers, GFS integration.

| Question | Asks | Coverage |
|---|---|---|
| 2021 Q7c | Types of MapReduce jobs | ✅ slide |
| 2022 Q4a | Two limitations on the Map function | ✅ slide |
| 2022 Q4b | Handling straggler tasks | ✅ slide |
| 2024 Q1a | HPC fault tolerance technique in message-passing programs | ✅ slide (checkpointing / duplication) |
| 2024 Q1b | MapReduce advantage over MPI for failure handling + recovery | ✅ slide |
| 2024 Q1c | GFS exposes block replica locations via API — what MapReduce optimization does this enable? | ✅ slide (locality optimization) |
| 2024 Q1d | Two important limitations MapReduce places on Map function | ✅ slide (same as 2022 Q4a) |

> ⭐ 2024 Q1 is **entirely MapReduce** (all 4 parts). Know: checkpointing for fault tolerance, straggler re-execution, data-locality via GFS, Map constraints (deterministic, no side effects, idempotent).

---

## Lecture 4 — Failure Detection & Membership  · Topics #13/#14 · yield 3/5 (upgraded)
**Slides:** why failure detectors, MTTF math, group membership service, heartbeating (all-to-all, gossip), asynchronous network model.

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q2b | Fault detection & recovery in distributed OS | ✅ slide |
| 2022 Q6b | Robustness of all-to-all heartbeating | ✅ slide |
| 2022 Q6d | Group membership protocol design | ✅ slide |
| 2024 Q2d | Primary goal of failure detection; why perfect/instant detection is impossible in async networks | ✅ slide (FLP impossibility / async model) |
| 2024 Q3a | Server carrying client requests: why can't it bound response time? What should it do? | ✅ slide (async network; timeout-based approach) |

---

## Lecture 5 — Replication Control  · Topics #4/#6 · yield 4/5
**Slides:** replication (why: fault-tolerance, load balancing, availability — nines table), transactions on distributed servers, **two-phase commit**, one-copy serializability, FIFO/causal ordering.

| Question | Asks | Coverage |
|---|---|---|
| 2021 Q2c | 9 replicas + read/write quorum constraints | ✅ slide (+L7) |
| 2022 Q3a–c | ACID transactions under crashes (disk / memory+disk / log) | ✅ slide (2PC) |
| 2022 Q7a | Two-transaction schedule trace — issue? | ✅ slide (serializability) |
| 2021 Q7a | Round-robin load balancing | ⚠️ partial (replication LB) |
| 2024 Q2c | Atomic commit protocol; two-phase commit for **nested transactions** | ✅ slide (2PC) |
| 2024 Q4c | Different types of ordering of multicast messages in overlapping groups | ⚠️ partial (FIFO/causal in L5; total order not explicit) |
| 2024 Q7c | Primary-backup vs Paxos for 3 scenarios | ✅ slide (replication + L7 Paxos) |

---

## Lecture 6 (Reading) — Networking & Routing  · yield 1/5
**Slides:** internet structure, routing, links/nodes, caching. **No past-paper question 2020–24 maps here.** SKIP unless time spare.

---

## Lecture 7 — Paxos  · Topic #9 · yield 4/5 ⭐ (upgraded)
**Slides:** consensus problem, validity/integrity/non-triviality, Paxos Phase 1/2, proposal numbers, majority/quorum intersection, safety + eventual liveness, f-failure tolerance math.

| Question | Asks | Coverage |
|---|---|---|
| 2021 Q2c | Quorum constraints (shared w/ L5) | ✅ slide |
| 2021 Q8c | Leader waits < majority — how it breaks Paxos | ✅ slide |
| 2022 Q2b | Paxos same proposal numbers — correct? counterexample (6 mk) | ✅ slide |
| 2024 Q2a | Define consensus algorithms (+ logical vs physical concurrency) | ✅ slide (consensus part) |
| 2024 Q7a | Why Paxos cannot tolerate f failures with less than 2f + 1 nodes | ✅ slide |
| 2024 Q7b | Leader waits < majority before proceeding — breaks Paxos (same as 2021 Q8c) | ✅ slide |
| 2024 Q7c | Primary-backup vs Paxos for 3 scenarios (stock lock server / doc movies / login server) | ✅ slide |

> ⭐ "Leader < majority" repeats 2021 & 2024. 2024 also adds: **f-failure math (2f+1)** and **primary-backup decision** — both must be cold-memorised.

---

## Lecture 8 — ⛔ MISSING
No `Lecture-08` file was found (07→09 gap). Now confirmed as **DFS/AFS** based on 4-year question pattern. No 2020–24 slide question maps here. Questions from 2020 Q7, 2021 Q3b/6c/6d, 2022 Q6c, 2024 Q3b/4d all go to **Orphan #1 (DFS)** below.

---

## Lecture 9 — Distributed Shared Memory  · Topics #1/#4 · yield 5/5 ⭐⭐
**Slides:** DSM concept, DSM-over-message-passing (cache + page fault + multicast), **Invalidate** protocol (R/W states, owner), **Update** protocol, **false sharing**, consistency ladder (Linearizability→Sequential→Causal→PRAM/FIFO→Eventual→Release).
**Status:** ✅ wiki [[wiki/dsm]] done.

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q4a | Causal consistency + example | ✅ slide |
| 2020 Q4b | Weak vs release consistency (DSM) | ✅ slide |
| 2020 Q6a | DSM schematic diagram | ✅ slide |
| 2020 Q6b | False sharing + minimize | ✅ slide (ALL 4 yrs) |
| 2021 Q2a | Strong vs weak consistency (video site) | ✅ slide |
| 2021 Q2b | Strong consistency for law-enforcement | ✅ slide |
| 2021 Q3c | False sharing + minimize | ✅ slide |
| 2021 Q3d | Consistency + types in DSM | ✅ slide |
| 2021 Q8b | Define DSM + illustrations | ✅ slide |
| 2022 Q4c | False sharing + minimize | ✅ slide |
| 2022 Q4d | Consistency + types in DSM | ✅ slide |
| 2022 Q8b | DSM over message-passing network | ✅ slide |
| 2022 Q8c | Invalidate vs Update protocols | ✅ slide |
| 2024 Q4a | Compare message passing vs DSM approaches | ✅ slide |
| 2024 Q4b | False sharing + minimize | ✅ slide |
| 2024 Q2b | What is linearizability? Methods to ensure serializability | ✅ slide (top of consistency ladder) |
| 2020 Q4c | Why LRU fails for DSM block replacement | ⚠️ **partial** — textbook |
| 2020 Q6c | NRNMB/NRMB/RMB/RNMB strategies | **ORPHAN** — textbook |

---

## Lecture 10 — RPC & Concurrency Control  · Topics #3/#6 · yield 5/5 ⭐⭐
**Slides:** RPC (Birrell & Nelson), LPC vs RPC, stub, marshalling, **call semantics** (at-least-once / at-most-once / maybe / exactly-once), concurrency control, **deadlock** (detection, locking, timestamp, WFG), ACID.

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q3a | RPC motivation + schematic | ✅ slide |
| 2020 Q3b | Stub: what / how generated / purpose | ✅ slide |
| 2021 Q1d | Marshalling/Unmarshalling + ACID | ✅ slide |
| 2021 Q6a | Concurrency control + deadlock + locking | ✅ slide |
| 2021 Q6b | Timestamp ordering; validation vs update phase | ⚠️ partial (timestamp ✅, optimistic phases textbook) |
| 2021 Q8a | RPC + design issues | ✅ slide |
| 2022 Q3a–c | ACID transactions under crashes (shared w/ L5) | ✅ slide |
| 2022 Q6a | Deadlock + locking in concurrency control | ✅ slide |
| 2022 Q7b | Concurrency control; preventing isolation violation | ✅ slide |
| 2022 Q7c | Deadlock detection in distributed systems | ✅ slide |
| 2022 Q8a | RPC + design issues | ✅ slide |
| 2024 Q2a | Logical vs physical concurrency (+ consensus def) | ✅ slide |
| 2024 Q3c | Wait-for-graph (WFG) purpose + example + deadlock detection conditions | ✅ slide |
| 2024 Q5c | Marshalling/unmarshalling in RPC; communication paradigm comparison for time-sensitive apps | ✅ slide |
| 2024 Q6a | Concurrency distributed vs centralized; partial failure + no global clock impact | ✅ slide |
| 2024 Q8a | ACID — define each letter (3 mk) | ✅ slide |
| 2024 Q8b | Deadlock scenario analysis (rowing crew / boitthas code) — will it deadlock? | ✅ slide (deadlock conditions) |
| 2020 Q5a | RPC comm protocol; **RRA protocol** steps | **ORPHAN** — RRA textbook |
| 2020 Q5d | RRA for concurrent multi-server access | **ORPHAN** — textbook |
| 2020 Q5c | Callback RPC + lightweight RPC | **ORPHAN** — textbook |

---

# 🔴 Orphan Audit — questions with NO slide coverage (study from textbook)
Ranked by exam risk. Updated for 2024.

| # | Orphan topic | Questions | Yrs | Risk | Where to study |
|---|---|---|:---:|:---:|---|
| 1 | **Distributed File Systems + Andrew File System (AFS)** | 2020 Q7a/b/c, 2021 Q3b/6c/6d, 2022 Q6c, **2024 Q3b/4d** | **4/4** | 🔴🔴 CRITICAL (yield 5/5, **ALL 4 years**, **11 parts total**) | Tanenbaum Ch on DFS; Sinha Ch 9. UNIX semantics, design principles, cache validation, AFS architecture, **venus/vice processes**, **AFS callback mechanism**. Almost certainly the missing Lecture-08. |
| 2 | **DSO + Scalable Parallel DB + Data-mining patterns** | 2021 Q4a/4b, 2022 Q5a/5b | 2/4 | 🟠 MED (yield 3/5, 4 parts, absent 2024) | Distributed System Overhead; parallel DB; hidden-pattern extraction (classification/clustering/association). |
| 3 | **Chandy-Lamport Global Snapshot** | **2024 Q8c** | **1/4** | 🟠 MED — NEW 2024 (3 mk) | Tanenbaum on global state; requires FIFO channels; n-process snapshot does NOT guarantee n−1 empty channels. |
| 4 | **Multicast message ordering (FIFO/Causal/Total)** | **2024 Q4c** | **1/4** | 🟠 MED — NEW 2024 (3 mk) | Tanenbaum Ch on communication. FIFO: messages from same sender in order. Causal: causally related in order. Total: all agree on order. |
| 5 | **Callback & Lightweight RPC** | 2020 Q5c | 1/4 | 🟠 MED | Sinha RPC chapter. |
| 6 | **RRA protocol (Request/Reply/Ack) + concurrent variant** | 2020 Q5a, Q5d | 1/4 | 🟠 MED | Sinha RPC communication protocols. |
| 7 | **NRNMB / NRMB / RMB / RNMB DSM strategies** | 2020 Q6c | 1/4 | 🟠 MED | Sinha Ch 5 (DSM block replication). |
| 8 | **Horizontal vs Vertical scaling** | 2022 Q1a | 1/4 | 🟢 LOW (concept is simple) | Scale-out vs scale-up. |
| 9 | **SQL vs NoSQL comparison** | 2021 Q7b | 1/4 | 🟢 LOW | General DB knowledge (4.75 mk though). |
| 10 | **Prognostic health management (cloud application)** | 2020 Q8c | 1/4 | 🟢 LOW | Reason from cloud benefits (scalability, big-data analytics). |
| 11 | **Bitemporal relation** | 2022 Q5c | 1/4 | 🟢 LOW (1 mk) | Valid-time + transaction-time DB. |

**Headline finding:** The **DFS/AFS cluster (orphan #1)** is now asked in **ALL 4 years** — the single highest-yield and highest-risk blind spot. Two new sub-topics from 2024: venus/vice processes and AFS callback loss handling. The **Chandy-Lamport snapshot (orphan #3)** is new in 2024 and high-value (3 mk).

---

# ✅ Coverage assertion (updated for 4 papers)
- Papers: **2020** (23 parts) + **2021** (28 parts) + **2022** (25 parts) + **2024** (~26 parts) ≈ **102 total question-parts**
- **Mapped to a lecture:** ~76 parts (✅ or ⚠️ partial)
- **Orphan (textbook):** ~26 parts across 11 topics (listed above)
- **Unaccounted: 0.** Every part is either under a lecture or in the orphan audit.

# 🎯 Recommended study ORDER (by yield, 2 days left)
1. **L9 DSM** (✅ wiki done → active recall + false sharing drill) — 5/5
2. **Orphan #1 DFS/AFS** (textbook) — **5/5, ALL 4 YEARS**, venus/vice + AFS callbacks new
3. **L10 RPC + Concurrency** (WFG + ACID + deadlock scenario + 2PC) — 5/5
4. **L2 Cloud** (virtualization + IaaS vs PaaS analysis + cost calc) — 5/5
5. **L3 MapReduce** (checkpointing, straggler, locality, Map constraints) — 4/5, 2024 Q1 all 4 parts
6. **L7 Paxos** (f-failure math, leader<majority, primary-backup vs Paxos) — 4/5
7. **L5 Replication/Transactions** (2PC for nested transactions, quorum) — 4/5
8. **L1 Fundamentals** (✅ done → revise) — 4/5
9. **L4 Failure Detection** (async impossibility + bounded time) — 3/5
10. Orphan #3 Chandy-Lamport + Orphan #4 Multicast ordering — skim
11. Tail orphans (#5–11) — final pass only
