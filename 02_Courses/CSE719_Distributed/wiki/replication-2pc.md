# Replication Control & Two-Phase Commit
> [[_index]] · [[distributed-fundamentals]] · [[failure-detection]] · Source: Lecture-05 · Solutions: `Replication_2PC_Solutions.pdf`

**Definition:** Replication = an object has identical copies maintained by separate servers. 2PC = protocol ensuring all servers in a distributed transaction commit or all abort.

## Why Replicate?
- **Fault-tolerance:** k replicas → tolerate (k-1) server failures
- **Load balancing:** read/write load spread across k replicas → k× improvement
- **Availability:** single server: (1−f); k replicas: (1−f^k)

| f | No replication | k=3 | k=5 |
|---|---|---|---|
| 0.1 | 90% | 99.9% | 99.999% |
| 0.01 | 99% | 99.9999% | 10 Nines |

## Two Challenges
1. **Replication Transparency:** client must not know replicas exist → achieved via **front-end** servers
2. **Replication Consistency (One-Copy Serializability):** concurrent transactions on replicated objects must behave as if on a single logical copy

## Passive vs Active Replication
| | Passive (Primary-Backup) | Active |
|---|---|---|
| Writes | → primary → backups | FE multicasts to ALL replicas |
| Ordering | Primary enforces total order | Requires total-order multicast |
| Failure | Election when primary fails | No single point of failure |
| Needs | Leader election (Paxos) | Total-order multicast + RSM |

**Replicated State Machine principle [Schneider 1990]:** Multiple copies of the same state machine, starting in same state, receiving same inputs in same order → arrive at same state with same outputs.

## Multicast Ordering Types (2024 Q4c)
| Ordering | Guarantee | Use case |
|---|---|---|
| **FIFO** | Same sender's messages delivered in send order | Sender-local order only |
| **Causal** | Causally related messages (happen-before) delivered in order | Vector clocks; social feeds |
| **Total (Atomic)** | ALL messages delivered in same order at ALL receivers | Active replication, replicated state machines |
| **Hybrid (*-Total)** | Total + FIFO or Total + Causal | Active replication with causality |

**Why ordering matters for overlapping groups:** Group G1={A,B} and G2={B,C} share node B. Without total ordering, B may see updates in different order than C, causing replicas to diverge. Total ordering ensures all nodes — including those in multiple groups — agree on same delivery sequence.

## Two-Phase Commit (2PC)
Problem: transaction T touches objects on servers S1…Sn. Need all-or-nothing atomicity = **Atomic Commit Problem = Consensus**.

**Phase 1 — Prepare:**
1. Coordinator sends PREPARE to all servers
2. Each server: (a) writes tentative updates to stable storage (disk); (b) votes YES or NO

**Phase 2 — Decision:**
- All YES within timeout → COMMIT: servers apply disk updates to permanent store; reply OK
- Any NO or timeout → ABORT: servers discard tentative updates

**Key invariants:**
- Server that voted YES cannot commit/abort unilaterally → must wait for coordinator
- Server that voted NO can abort immediately
- Writes to disk BEFORE voting = crash-safe

## 2PC Failure Handling
| Failure | Response |
|---|---|
| Server crash before vote | Abort on restart |
| Server crash after YES | On restart: poll coordinator for decision |
| PREPARE message lost | Server timeouts → votes NO → coordinator aborts |
| YES/NO message lost | Coordinator timeouts → aborts (pessimistic) |
| COMMIT/ABORT lost | Server polls coordinator repeatedly |
| Coordinator crash | New coordinator (re-elected) reads log from disk |

## 1PC vs 2PC
1PC problem: (1) server with corrupted object has no say — commits even if it can't; (2) server may crash before receiving COMMIT with updates still in memory.
2PC fix: Phase 1 gives every server a vote; data persisted before voting.

## ACID Under Crashes (2022 Q3a-c)
| Approach | Shortcomings |
|---|---|
| **Direct-to-disk per txn** | Extremely slow (disk I/O); partial write on crash (no atomicity); no rollback |
| **Memory buffer, flush every 50** | Crash before flush = lose up to 50 committed txns (Durability violated); large inconsistency window |
| **Memory + Write-Ahead Log** | Long recovery (replay log); log grows unboundedly; double-write overhead; log disk = single point of failure |

WAL (approach c) is best despite shortcomings — it provides Durability + Atomicity with fast in-memory operations.

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2022 | Q3a/b/c | ACID crash shortcomings: direct-disk / batch-memory / WAL |
| 2024 | Q2a | Consensus definition + logical vs physical concurrency |
| 2024 | Q2c | Atomic commit + 2PC for nested transactions |
| 2024 | Q4c | Types of multicast ordering in overlapping groups |

⭐ **2PC for nested transactions:** sub-transactions commit locally (tentatively) only; parent's ABORT rolls back ALL sub-transactions even after local commit.
⭐ **Multicast ordering:** know all 4 types (FIFO/Causal/Total/Hybrid) and the overlapping-group problem motivating Total ordering.
