# CSE 719 — Distributed & Cloud Computing · Topic Tracker
> [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold
Built 2026-06-26 from 3-year past-paper analysis (2020 / 2021 / 2022, Univ. of Chittagong, CSE 513/813).
**Exam: Wed 1 Jul 2026, 10:30 AM.** Format: ~52.5–54 marks, 4 hours, **answer any 3 of 4 from each Section (A & B)**.

---

## 🎯 Ranked by yield (study top-down)

| # | Topic | Status | Conf | Last Rev | Yield | Recurs | Notes / weak spots |
|---|-------|:------:|:----:|:--------:|:-----:|:------:|--------------------|
| 1 | **DSM (Distributed Shared Memory)** | 📖 | — | 2026-06-26 | 5/5 · 9–12 mk | 2020·21·22 | Wiki ingested (Lecture-09 → [[wiki/dsm]]). False sharing + Invalidate/Update + consistency covered. GAP: NRNMB strategies & LRU-fail are textbook-only — pull before exam. Next: active recall. |
| 2 | **Cloud Computing fundamentals** | 🔲 | — | — | 5/5 · 8–12 mk | 2020·21·22 | E-commerce scenario asked ALL 3 years. + definition, deployment vs service models, horizontal/vertical scaling, multi-tenancy, EUCALYPTUS, layers, on-demand, pros/cons. |
| 3 | **RPC (Remote Procedure Call)** | 🔲 | — | — | 5/5 · 6–9 mk | 2020·21·22 | Design issues asked every year. + stub (gen/purpose), RRA protocol steps, callback & lightweight RPC, schematic diagram. |
| 4 | **Consistency models** | 🔲 | — | — | 5/5 · 5–9 mk | 2020·21·22 | Strong/weak/causal/release; quorum (read+write size constraints, 9-replica example). Overlaps DSM — study together. |
| 5 | **Distributed File Systems + AFS** | 🔲 | — | — | 4/5 · 6–8 mk | 2020·21·22 | UNIX semantics difficulty, DFS design principles/requirements, cache validation, **Andrew File System** + file service architecture. |
| 6 | **Concurrency Control & Transactions** | 🔲 | — | — | 4/5 · 6–10 mk | 2021·22 | Deadlock + locking schemes, timestamp ordering, ACID, isolation/serializability, deadlock detection in distributed sys, transaction-schedule trace. Heavy in recent papers. |
| 7 | **Distributed System Fundamentals** | 🔲 | — | — | 4/5 · 6–10 mk | 2020·21 | Definition + examples, tightly vs loosely coupled, transparencies (location/relocation/migration), scalability + challenges, marshalling/unmarshalling, distributed vs parallel, adv/disadv. |
| 8 | **MapReduce** | 🔲 | — | — | 3/5 · 4–6 mk | 2021·22 | Map-function limitations, straggler handling, job types. Recent — likely again. |
| 9 | **Paxos** | 🔲 | — | — | 3/5 · 2.5–6 mk | 2021·22 | Leader-waits-less-than-majority counterexample; proposal-number correctness. Recent + tricky. |
| 10 | **DSO + Parallel DB + Data Mining** | 🔲 | — | — | 3/5 · 4.5–8 mk | 2021·22 | Distributed System Overhead, scalable parallel database, hidden-pattern extraction methodologies, bitemporal relation. |
| 11 | SQL vs NoSQL | 🔲 | — | — | 2/5 · ~5 mk | 2021 | Comparative analysis. Single appearance but high marks (4.75). |
| 12 | Load balancing (round robin) | 🔲 | — | — | 2/5 · 2 mk | 2021 | Short definition-style. |
| 13 | Heartbeating + Group Membership | 🔲 | — | — | 2/5 · ~4 mk | 2022 | All-to-all heartbeat robustness, group membership protocol design. Recent. |
| 14 | Fault detection & recovery | 🔲 | — | — | 2/5 · ~3 mk | 2020 | Techniques in distributed OS. |

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
