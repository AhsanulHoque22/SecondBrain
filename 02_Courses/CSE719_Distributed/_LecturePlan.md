# CSE 719 — Lecture-by-Lecture Study Plan & Question Mind Map
> [[_Topics]] · [[_TopicQuestionMap]] · [[wiki/_index]] · Built 2026-06-26 from slide audit + 2020/21/22 past papers.

**Exam: Wed 1 Jul 2026.** Format: answer **any 3 of 4 questions per section** (A & B), ~52.5–54 marks, 4 hr.
This file walks Lecture 1 → 10 serially. Each lecture lists its topics, the exact past-paper questions it answers, and a study slot. **Every one of the 76 question-parts across the 3 papers is accounted for** — either under a lecture or in the **Orphan Audit** at the bottom (questions with NO slide coverage).

> ⚠️ **Study by yield, not by lecture number.** Serial order is for *coverage*; the priority order is at the very bottom. Highest-yield lectures: **9 (DSM), 2 (Cloud), 10 (RPC+Concurrency)**.

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
**Slides + readings** (Unit 3, Unit 4, `Lecture-01.pdf`, `lecture-02.pdf`): providers (AWS/Azure/GCE), public vs private, IaaS/PaaS/SaaS, on-demand, deployment models, multi-tenancy, EUCALYPTUS.
**Status:** 🔲 NOT STUDIED — **highest cloud yield, do early.**

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q8a | Define cloud + pros/cons | ✅ slide |
| 2020 Q8b | E-commerce: cloud services + deployment models | ✅ slide (asked ALL 3 yrs) |
| 2021 Q3a | E-commerce cloud services + deployment | ✅ slide |
| 2021 Q4c | Phases in cloud architecture | ⚠️ partial (readings) |
| 2021 Q5a | On-demand functionality | ✅ slide |
| 2021 Q5b | What is a cloud + large-scale platforms | ✅ slide |
| 2021 Q5c | Cloud layers + cloud vs distributed | ✅ Unit 4 |
| 2021 Q5d | EUCALYPTUS + deployment models | ✅ slide (L2 + Unit 3) |
| 2022 Q1b | E-commerce cloud services + deployment | ✅ slide |
| 2022 Q1c | Multi-tenancy | ✅ readings (CMU/Unit 3) |
| 2022 Q2a | EC2 VMs vs physical machines — 3 benefits | ⚠️ partial (reason from slide) |
| 2022 Q1a | Define cloud **+ horizontal vs vertical scaling** | scaling part → **ORPHAN** |
| 2020 Q8c | Cloud for prognostic health management | **ORPHAN** (application reasoning) |

---

## Lecture 3 — MapReduce & Hadoop  · Topic #8 · yield 3/5
**Slides:** Map/Reduce model (Lisp roots), Hadoop, HDFS, fault tolerance via duplication, stragglers.

| Question | Asks | Coverage |
|---|---|---|
| 2021 Q7c | Types of MapReduce jobs | ✅ slide |
| 2022 Q4a | Two limitations on the Map function | ✅ slide |
| 2022 Q4b | Handling straggler tasks | ✅ slide |

---

## Lecture 4 — Failure Detection & Membership  · Topics #13/#14 · yield 2/5
**Slides:** why failure detectors, MTTF math, group membership service, heartbeating (all-to-all, gossip).

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q2b | Fault detection & recovery in distributed OS | ✅ slide |
| 2022 Q6b | Robustness of all-to-all heartbeating | ✅ slide |
| 2022 Q6d | Group membership protocol design | ✅ slide |

---

## Lecture 5 — Replication Control  · Topics #4/#6 · yield 4/5
**Slides:** replication (why: fault-tolerance, load balancing, availability — nines table), transactions on distributed servers, **two-phase commit**, one-copy serializability, FIFO/causal ordering.

| Question | Asks | Coverage |
|---|---|---|
| 2021 Q2c | 9 replicas + read/write quorum constraints | ✅ slide (+L7) |
| 2022 Q3a–c | ACID transactions under crashes (disk / memory+disk / log) | ✅ slide (2PC) |
| 2022 Q7a | Two-transaction schedule trace — issue? | ✅ slide (serializability) |
| 2021 Q7a | Round-robin load balancing | ⚠️ partial (replication LB) |

---

## Lecture 6 (Reading) — Networking & Routing  · yield 1/5
**Slides:** internet structure, routing, links/nodes, caching. **No past-paper question 2020–22 maps here.** SKIP unless time spare.

---

## Lecture 7 — Paxos  · Topic #9 · yield 3/5
**Slides:** consensus problem, validity/integrity/non-triviality, Paxos Phase 1/2, proposal numbers, majority/quorum intersection, safety + eventual liveness.

| Question | Asks | Coverage |
|---|---|---|
| 2021 Q2c | Quorum constraints (shared w/ L5) | ✅ slide |
| 2021 Q8c | Leader waits < majority — how it breaks Paxos | ✅ slide |
| 2022 Q2b | Paxos same proposal numbers — correct? counterexample (6 mk) | ✅ slide |

---

## Lecture 8 — ⛔ MISSING
No `Lecture-08` file exists in the folder (jumps 07 → 09). **Gap flagged.** No 2020–22 question is currently unmapped *because* of this — but if Dr. Atiqur's L8 covered a distinct topic, ask a classmate for it. Likely candidate from sequence: **Distributed File Systems** (which is the biggest orphan — see below).

---

## Lecture 9 — Distributed Shared Memory  · Topics #1/#4 · yield 5/5 ⭐⭐
**Slides:** DSM concept, DSM-over-message-passing (cache + page fault + multicast), **Invalidate** protocol (R/W states, owner), **Update** protocol, **false sharing**, consistency ladder (Linearizability→Sequential→Causal→PRAM/FIFO→Eventual→Release).
**Status:** ✅ wiki [[wiki/dsm]] done. Next: active recall.

| Question | Asks | Coverage |
|---|---|---|
| 2020 Q4a | Causal consistency + example | ✅ slide |
| 2020 Q4b | Weak vs release consistency (DSM) | ✅ slide |
| 2020 Q6a | DSM schematic diagram | ✅ slide |
| 2020 Q6b | False sharing + minimize | ✅ slide (ALL 3 yrs) |
| 2021 Q2a | Strong vs weak consistency (video site) | ✅ slide |
| 2021 Q2b | Strong consistency for law-enforcement | ✅ slide |
| 2021 Q3c | False sharing + minimize | ✅ slide |
| 2021 Q3d | Consistency + types in DSM | ✅ slide |
| 2021 Q8b | Define DSM + illustrations | ✅ slide |
| 2022 Q4c | False sharing + minimize | ✅ slide |
| 2022 Q4d | Consistency + types in DSM | ✅ slide |
| 2022 Q8b | DSM over message-passing network | ✅ slide |
| 2022 Q8c | Invalidate vs Update protocols | ✅ slide |
| 2020 Q4c | Why LRU fails for DSM block replacement | ⚠️ **partial** — textbook |
| 2020 Q6c | NRNMB/NRMB/RMB/RNMB strategies | **ORPHAN** — textbook |

---

## Lecture 10 — RPC & Concurrency Control  · Topics #3/#6 · yield 5/5 ⭐⭐
**Slides:** RPC (Birrell & Nelson), LPC vs RPC, stub, marshalling, **call semantics** (at-least-once / at-most-once / maybe / exactly-once), concurrency control, **deadlock** (detection, locking, timestamp), ACID.

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
| 2020 Q5a | RPC comm protocol; **RRA protocol** steps | **ORPHAN** — RRA textbook |
| 2020 Q5d | RRA for concurrent multi-server access | **ORPHAN** — textbook |
| 2020 Q5c | Callback RPC + lightweight RPC | **ORPHAN** — textbook |

---

# 🔴 Orphan Audit — questions with NO slide coverage (study from textbook)
These are real past-paper questions whose content is in **no lecture deck or reading PDF**. Do not let the slides fool you into thinking you're covered. Ranked by exam risk.

| # | Orphan topic | Questions | Yrs | Risk | Where to study |
|---|---|---|:---:|:---:|---|
| 1 | **Distributed File Systems + Andrew File System (AFS)** | 2020 Q7a/b/c, 2021 Q3b/6c/6d, 2022 Q6c | 3/3 | 🔴 HIGH (yield 4/5, **7 parts**, zero slides) | Tanenbaum Ch on DFS; Sinha Ch 9. UNIX semantics, DFS design principles, cache validation, AFS file-service architecture. **Possibly the missing Lecture-08.** |
| 2 | **DSO + Scalable Parallel DB + Data-mining patterns** | 2021 Q4a/4b, 2022 Q5a/5b | 2/3 | 🟠 MED (yield 3/5, 4 parts) | Distributed System Overhead; parallel DB; hidden-pattern extraction (classification/clustering/association). |
| 3 | **Callback & Lightweight RPC** | 2020 Q5c | 1 | 🟠 MED | Sinha RPC chapter. |
| 4 | **RRA protocol (Request/Reply/Ack) + concurrent variant** | 2020 Q5a, Q5d | 1 | 🟠 MED | Sinha RPC communication protocols. |
| 5 | **NRNMB / NRMB / RMB / RNMB DSM strategies** | 2020 Q6c | 1 | 🟠 MED | Sinha Ch 5 (DSM block replication). |
| 6 | **Horizontal vs Vertical scaling** | 2022 Q1a | 1 | 🟢 LOW (concept is simple) | Any cloud text — scale-out vs scale-up. |
| 7 | **SQL vs NoSQL comparison** | 2021 Q7b | 1 | 🟢 LOW | General DB knowledge (4.75 mk though). |
| 8 | **Prognostic health management (cloud application)** | 2020 Q8c | 1 | 🟢 LOW | Reason from cloud benefits (scalability, big-data analytics). |
| 9 | **Bitemporal relation** | 2022 Q5c | 1 | 🟢 LOW (1 mk) | Valid-time + transaction-time DB. |

**Headline finding:** the **DFS/AFS cluster (orphan #1)** is the single biggest blind spot — a 4/5-yield topic asked every year with **no slides at all**. Treat it as a must-study textbook topic, and it is the most likely identity of the missing Lecture-08.

---

# ✅ Coverage assertion
- **76 question-parts** total across 2020 (23) + 2021 (28) + 2022 (25).
- **Mapped to a lecture:** 57 parts (✅ or ⚠️ partial).
- **Orphan (textbook):** 19 parts across 9 topics (listed above).
- **Unaccounted: 0.** Every part is either under a lecture or in the orphan audit.

# 🎯 Recommended study ORDER (by yield, 4 days left)
1. **L9 DSM** (✅ wiki done → active recall) — 5/5
2. **L2 Cloud** (+ Unit 3/4 readings) — 5/5
3. **L10 RPC + Concurrency** — 5/5
4. **Orphan #1 DFS/AFS** (textbook) — 4/5, *highest-risk gap*
5. **L5 Replication/Transactions** — 4/5
6. **L1 Fundamentals** (✅ done → revise) — 4/5
7. **L7 Paxos** · **L3 MapReduce** · **L4 Failure/Membership** — 2–3/5
8. Tail orphans (#2–9) — skim in final pass.
