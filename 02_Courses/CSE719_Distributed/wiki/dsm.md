# Distributed Shared Memory (DSM)
> [[_index]] · [[consistency-models]] · [[rpc]] · Source: Lecture-09 (slides) + Sinha textbook (for replication strategies)

**Definition (exam):** DSM is an abstraction in which processes on different machines *virtually share memory pages*, so they program as if on one shared-memory multiprocessor — implemented on top of a message-passing network.

## Core ideas
- **Duality:** message-passing can be built over DSM (shared page as buffer) **and** DSM can be built over message-passing. Exams ask the latter.
- **Implementation:** each process keeps a **cache** of recently-accessed pages. Read/write hits cache → **page hit**; miss → **page fault** (kernel trap) → DSM software contacts other processes via **multicast**.

## Invalidate protocol (the default)
- **Owner** = process with the latest version of a page. Each page is in **R** (read) or **W** (write) state.
  - R state: owner has R copy; others *may* have R copies; **no W copy exists**.
  - W state: **only the owner** has a copy.
- **Read rules:** if you have the page (R or W) → read from cache, no messages. If you don't have it:
  - others hold R → multicast, get a copy, mark R, read.
  - another holds W → ask owner to **degrade to R**, get page, mark R, read.
- **Write rules:** if you own it in W → write to cache, no messages. Otherwise:
  - **multicast invalidate** all other copies → mark page W, become owner → write.

## Update protocol (the alternative)
- Multiple processes may hold the page in W. On a write, **multicast the new value** to all holders; everyone keeps reading/writing.
- **Update preferred when:** lots of sharing, writes to small variables, large page sizes.
- **Otherwise Invalidate is the default/preferred.**

## ⭐ False sharing (asked EVERY year — memorize)
- Cause: two processes write *unrelated variables that happen to land on the same page* → invalidate protocol **flip-flops** ownership → heavy network transfer though there's no real data sharing.
- **Minimize it by tuning page size to a process's locality of interest:**
  - page **too large** → false sharing.
  - page **too small** → too many page transfers (also inefficient).
  - → choose a moderate page size; co-locate related data, separate unrelated variables onto different pages.

## Consistency models (DSM can use any; speed↑ as consistency↓)
Linearizability → Sequential → Causal → PRAM/FIFO → Eventual (+ Release). Full detail: [[consistency-models]].

## ⚠️ Gaps not in Lecture-09 (from textbook — needed for 2020 paper)
- **NRNMB / NRMB / RMB / RNMB** replication strategies (2020 Q6c, 4 mk): Non-Replicated-Non-Migrating, Non-Replicated-Migrating, Replicated-Migrating, Replicated-Non-Migrating blocks. *Not in slides — pull from Sinha Ch.5 / Unit reading before exam.*
- **Why simple LRU fails for DSM block replacement** (2020 Q4c, 2.25 mk): blocks have *states* (shared/exclusive/read-only) unlike buffer-cache lines; replacing a modified/owner block needs writeback/transfer, so pure recency is wrong. *Verify from textbook.*

## Exam pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | 6a/6b/6c, 4b, 4c | schematic · false sharing · NRNMB strategies · weak vs release · LRU-fail |
| 2021 | 3c/3d, 8b | false sharing · consistency types · define+illustrate DSM |
| 2022 | 4c/4d, 8b, 8c | false sharing · consistency types · DSM over message-passing · **Invalidate vs Update** |

**Highest-probability answers to have cold:** false sharing (def + minimize), Invalidate vs Update comparison, "implement DSM over message-passing" (cache + page fault + multicast).
