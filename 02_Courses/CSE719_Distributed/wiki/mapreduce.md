# MapReduce & Hadoop
> [[_index]] · [[cloud-computing]] · [[distributed-fundamentals]] · Source: Lecture-03 · Solutions: `MapReduce_Solutions.pdf`

**Definition:** MapReduce is a programming framework for **distributed and parallel processing on large datasets** using two phases: **Map** (per-record transformation) and **Reduce** (per-key aggregation). Hadoop is the open-source implementation.

## Pipeline
```
Input (DFS) → [Map tasks, in parallel] → intermediate (k,v) to local disk
           → [Shuffle: hash(key)%R → Reduce#] → [Reduce tasks, in parallel] → Output (DFS)
```
**Barrier:** No Reduce starts until ALL Maps complete.

## Storage model
| Phase | Where data lives |
|---|---|
| Map input | Distributed FS (GFS/HDFS) |
| Map output | Local disk of Map node |
| Reduce input | Pulled from Map nodes' local disks (network) |
| Reduce output | Distributed FS |

## Two Map Function Limitations (asked 2022 Q4a AND 2024 Q1d — verbatim repeat)
1. **No side effects / Pure/Deterministic** — same input → same output always; cannot write to shared external state. Required for safe re-execution on failure and speculative execution.
2. **No inter-task communication / Independent records** — Map sees one record at a time; cannot access sibling Map outputs or other input records. Enables trivial parallelism.

## Straggler Handling: Speculative Execution (2022 Q4b)
- **Straggler** = slow task (bad disk / CPU contention / network) that holds up whole job via barrier
- Framework tracks **progress %** of each task
- Near completion: launch **backup copy** of straggler on another worker
- Accept output from whichever finishes first; kill the other
- Safe because Map is deterministic (two copies produce identical output)

## Fault Tolerance: MPI vs MapReduce (2024 Q1a, Q1b)
| | MPI (HPC) | MapReduce |
|---|---|---|
| Mechanism | Global checkpoint/restart | Task-level re-execution |
| On failure | ALL processes roll back to checkpoint | Only failed task(s) re-scheduled |
| State saved | Entire global memory state | Nothing (tasks are stateless) |
| Developer effort | Must write checkpoint code | Zero — framework handles it |
| Scalability | Poor (failures frequent at 10K+ nodes) | Good |

**MPI checkpoint failure at scale:** 10,000 nodes × 1 failure/year/node → failure every ~53 min. Checkpoint overhead (write all state) exceeds MTBF.

## GFS Locality Optimization (2024 Q1c)
- GFS API exposes **block replica locations** to clients
- MapReduce master queries GFS to learn where each input block lives
- Schedules Map tasks with priority:
  1. **Same machine** as a replica → local disk read (fastest)
  2. **Same rack** as a machine with replica → intra-rack read
  3. **Anywhere** (fallback)
- Effect: eliminates most cross-rack network reads in Map phase → huge performance gain (network is the scarcest datacenter resource)

## MapReduce Job Types (2021 Q7c)
| Job | Map emits | Reduce emits |
|---|---|---|
| Word count | (word, 1) | (word, total_count) |
| Distributed grep | line if matches pattern | line (identity) |
| Reverse web-link graph | (target_page, source_page) | (target, [source list]) |
| URL access frequency | (URL, 1) | (URL, count) → chain 2nd MR for % |
| Distributed sort | (value, _) identity | (key, value) identity; range partition |
| Inverted index | (word, docID) | (word, [docID list]) |

## YARN Scheduler (Hadoop 2.x+)
- **YARN** = Yet Another Resource Negotiator
- Container = fixed CPU + fixed memory unit
- **Resource Manager (RM):** global scheduler
- **Node Manager (NM):** per-server daemon; heartbeats to RM; marks failed tasks idle → restarts
- **Application Master (AM):** per-job; negotiates containers from RM; detects task failures
- **RM failure:** use old checkpoints + secondary RM

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2021 | Q7c | types of MapReduce jobs |
| 2022 | Q4a, Q4b | Map function limitations · straggler handling |
| 2024 | Q1a, Q1b, Q1c, Q1d | HPC checkpoint/restart · MR vs MPI fault tolerance · GFS locality · Map limitations (repeat) |

⭐ **2024 dedicates ALL of Q1 to MapReduce — treat as core topic, yield 4/5.**
⭐ **Map limitations question is verbatim repeated 2022→2024 — know both points with WHY.**
