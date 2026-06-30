# CSE 719 — Distributed & Cloud Computing · Topic Tracker
> [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold
Built 2026-06-26 from 3-year past-paper analysis (2020 / 2021 / 2022, Univ. of Chittagong, CSE 513/813).
**Exam: Wed 1 Jul 2026, 10:30 AM.** Format: ~52.5–54 marks, 4 hours, **answer any 3 of 4 from each Section (A & B)**.

---

## 🎯 Ranked by yield (study top-down)

| # | Topic | Status | Conf | Last Rev | Yield | Recurs | Notes / weak spots |
|---|-------|:------:|:----:|:--------:|:-----:|:------:|--------------------|
| 1 | **DSM (Distributed Shared Memory)** | 📖 | — | 2026-06-30 | 5/5 · 9–12 mk | 2020·21·22·24 | Wiki updated. Solutions: DSM_Consistency_Solutions.pdf. False sharing, Invalidate/Update, NRNMB strategies, LRU-fail, all covered. |
| 2 | **Cloud Computing fundamentals** | 📖 | — | 2026-06-30 | 5/5 · 8–12 mk | 2020·21·22 | Wiki ingested (→ [[wiki/cloud-computing]]). Solutions: Cloud_Solutions.pdf (all 17 Q 2020–24). E-commerce scenario asked ALL 3 years. + definition, deployment vs service models, horizontal/vertical scaling, multi-tenancy, EUCALYPTUS, layers, on-demand, pros/cons. |
| 3 | **RPC (Remote Procedure Call)** | 📖 | — | 2026-06-30 | 5/5 · 6–9 mk | 2020·21·22·24 | Wiki ingested (→ [[wiki/rpc-concurrency]]). Solutions: RPC_Concurrency_Solutions.pdf. Design issues, stub, RRA, callback/lightweight RPC, marshalling, paradigm comparison. |
| 4 | **Consistency models** | 📖 | — | 2026-06-30 | 5/5 · 5–9 mk | 2020·21·22·24 | Wiki ingested (→ [[wiki/consistency-models]]). Causal/release/weak/sequential/linearizability; quorum rules + 9-replica example; scenarios. Solutions: DSM_Consistency_Solutions.pdf. |
| 5 | **Distributed File Systems + AFS** | 📖 | — | 2026-06-30 | 5/5 · 6–8 mk | 2020·21·22·24 | Wiki ingested (→ [[wiki/dfs-afs]]). Solutions: DFS_AFS_Solutions.pdf. UNIX not idempotent+stateless; DFS principles; cache validation; Vice+Venus+callbacks; AFS callback loss. |
| 6 | **Concurrency Control & Transactions** | 📖 | — | 2026-06-30 | 5/5 · 6–10 mk | 2021·22·24 | 2PC + multicast (→ [[wiki/replication-2pc]]). ACID, deadlock, locking, WFG, timestamp ordering, schedule trace, distributed vs centralized all covered → RPC_Concurrency_Solutions.pdf + [[wiki/rpc-concurrency]]. |
| 7 | **Distributed System Fundamentals** | 📖 | — | 2026-06-26 | 4/5 · 6–10 mk | 2020·21 | Lecture-01 ingested + solutions PDF (2020/21). Definition + examples, tightly vs loosely coupled, transparencies, scalability + challenges, marshalling/unmarshalling, distributed vs parallel, adv/disadv. |
| ↳ Definition + working definition + design goals | 📖 | — | 2026-06-26 | 5/5 · 1.75–3 mk | 2020 Q1a, 2021 Q1a | Slide-backed (Lecture-01). 9 design goals; working def: autonomous/programmable/async/failure-prone entities. |
| ↳ Tightly vs Loosely coupled systems | 📖 | — | 2026-06-30 | 4/5 · 3.25 mk | 2020 Q1b | Shared vs distributed memory; needs figures. Textbook (Sinha). Covered in Fundamentals_Solutions.pdf. |
| ↳ Transparencies (location/relocation/migration) | 📖 | — | 2026-06-30 | 4/5 · 3 mk | 2020 Q2a | 8 transparency types; differentiate the 3 named ones. Covered in Fundamentals_Solutions.pdf. |
| ↳ Distributed vs Parallel processing | 📖 | — | 2026-06-30 | 3/5 · 2.5 mk | 2020 Q1c | Why DS better than parallel. Covered in Fundamentals_Solutions.pdf. |
| ↳ Scalability + challenges | 📖 | — | 2026-06-30 | 4/5 · 2.5 mk | 2021 Q1c | Define + size/geo/admin scalability challenges. Covered in Fundamentals_Solutions.pdf. |
| ↳ Marshalling/Unmarshalling + ACID | 📖 | — | 2026-06-30 | 3/5 · 2 mk | 2021 Q1d | Serialization for transmission; ACID = Atomicity/Consistency/Isolation/Durability. Covered in Fundamentals_Solutions.pdf. |
| 8 | **MapReduce** | 📖 | — | 2026-06-30 | 3/5 · 4–6 mk | 2021·22 | Wiki ingested (→ [[wiki/mapreduce]]). Solutions: MapReduce_Solutions.pdf (all 7 Q 2021–24). Map-function limitations, straggler handling, job types. Recent — likely again. |
| 9 | **Paxos** | 📖 | — | 2026-06-30 | 4/5 · 2.5–6 mk | 2021·22·24 | Wiki ingested (→ [[wiki/paxos]]). Solutions: Paxos_Solutions.pdf. Leader<majority counterexample; 2f+1 math; same-ballot violation; P-B vs Paxos scenarios. |
| 10 | **DSO + Parallel DB + Data Mining** | 🔲 | — | — | 3/5 · 4.5–8 mk | 2021·22 | Distributed System Overhead, scalable parallel database, hidden-pattern extraction methodologies, bitemporal relation. |
| 11 | SQL vs NoSQL | 🔲 | — | — | 2/5 · ~5 mk | 2021 | Comparative analysis. Single appearance but high marks (4.75). |
| 12 | Load balancing (round robin) | 🔲 | — | — | 2/5 · 2 mk | 2021 | Short definition-style. |
| 13 | Heartbeating + Group Membership | 📖 | — | 2026-06-30 | 2/5 · ~4 mk | 2022 | Wiki ingested (→ [[wiki/failure-detection]]). All-to-all robustness = gossip-style; group membership = SWIM + infection dissemination. Solutions: FailureDetection_Solutions.pdf. |
| 14 | Fault detection & recovery | 📖 | — | 2026-06-30 | 3/5 · ~9 mk | 2020·24 | 2024 adds 2 questions. Wiki ingested. Core: completeness goal; async impossibility [Chandra & Toueg]; timeout + suspicion mechanism. Solutions: FailureDetection_Solutions.pdf. |

---

## 📌 Study strategy (5 days, 80/20)
- **Topics 1–4 are the spine.** They appear every year with the most marks. Master these cold first — they alone can cover 3 strong answers per section.
- **Topics 5–7 are the second layer.** Add these and you can comfortably pick your best 3 of 4 in each section.
- **Topics 8–10** are recent-trend insurance (Paxos/MapReduce/DSO show up in 2021–22). Touch if time.
- **Topics 11–14** are low-yield tail — skim only in the final pass, don't invest early.
- Many topics cluster: DSM ↔ Consistency ↔ DSO; RPC ↔ fundamentals; Cloud is self-contained. Study clustered.

## Source materials
- Slides: Lecture-01…10, Unit 3 & Unit 4 (Reading) in course folder.
- Past papers: `_Cloud prev.pdf` (2020 pp.1–2, 2021 pp.3–4, 2022 pp.5–6).
