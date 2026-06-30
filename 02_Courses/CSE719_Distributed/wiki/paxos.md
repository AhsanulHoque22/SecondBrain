# Paxos
> [[_index]] · [[distributed-fundamentals]] · [[replication-2pc]] · [[failure-detection]] · Source: Lecture-07 · Solutions: `Paxos_Solutions.pdf`

**Definition:** Paxos is a consensus algorithm providing safety (no two processes decide different values) and eventual liveness (consensus reached if conditions eventually stabilise). Invented by Leslie Lamport.

## Consensus Problem
- N processes, each with private input (0 or 1); goal: all decide same value.
- **Validity:** decided value was proposed by some process.
- **Agreement:** no two correct processes decide different values.
- **Non-triviality:** both outcomes reachable from some initial state.
- Consensus possible in synchronous systems; **impossible in asynchronous** (FLP 1985).
- Equivalent to (or harder than): perfect failure detection, leader election, total-order multicast.

## Paxos Properties
| Property | Meaning |
|---|---|
| **Safety** | Two processes never decide different values — always holds |
| **Eventual Liveness** | If things go well, consensus reached — no timing guarantee |
| **FLP** | Paxos is NOT guaranteed to terminate (ever, or within bounded time) |

Used by: Apache ZooKeeper (Yahoo!), Google Chubby, Active Disk Paxos.

## Three-Phase Protocol
Each Paxos round has a unique **ballot id** (monotonically increasing). If in round j and hear from round j+1 → abort and join j+1.

| Phase | Name | Steps |
|---|---|---|
| 1 | Election | Candidate picks ballot id n > all seen; broadcasts Prepare(n); processes respond OK if n > highest seen (log n to disk; include any previously accepted value) |
| 2 | Proposal (Bill) | Leader sends Accept(n, v) to all; adopt v=v' from highest-ballot OK if any; acceptors log and respond OK |
| 3 | Decision (Law) | On majority OKs → multicast Decide(v); all log to disk |

**Majority = ⌊N/2⌋ + 1.** Any two majority sets intersect — core safety invariant.

**Point of no-return:** When majority has accepted v in Phase 2. Decision is implicit even before leader knows. Any future round either decides v or fails (intersection guarantees new leader finds v').

## Fault Tolerance Math
| Condition | Result |
|---|---|
| N = 2f | f fail → f remain < f+1 (majority of 2f) → protocol stalls |
| N = 2f+1 | f fail → f+1 remain = majority of 2f+1 → protocol proceeds |
| **Minimum: N ≥ 2f+1** | Derived from: N − f > N/2 → N > 2f |

Safety also requires N ≥ 2f+1: two quorums of size f+1 from 2f+1 nodes always intersect (pigeonhole: (f+1)+(f+1) = 2f+2 > 2f+1).

## Failure Handling
| Failure | Response |
|---|---|
| Process crash | Excluded from quorum; on restart reads log for past ballot ids and accepted values |
| Leader crash | Any process starts new round with higher ballot id |
| Message dropped | Timeout → start new round |
| Protocol stalls | Tough luck (FLP); eventual liveness only |

## Key Safety Violations (Exam Traps)
**Leader waits for < majority in Phase 1:**
Two quorums of size k < ⌊N/2⌋+1 can be disjoint. New leader's Phase 1 set has no witness to v' → proposes different v → two values decided → **safety violated**.

Counterexample (N=5, k=2): Round 1 leader L1 gets OKs from {A1,A2}, commits v1. Round 2 leader L2 gets OKs from {A3,A4} (disjoint), commits v2 ≠ v1.

**Same ballot id from two proposers (modified reject rule):**
If acceptors accept equal ballot ids (not just strictly greater), two proposers with ballot n=5 can each achieve quorums that overlap on shared acceptors → both commit different values → **safety violated**.

Counterexample (N=3): LA gets OKs from {P1,P2} (ballot 5), LB gets OKs from {P2,P3} (ballot 5, accepted because 5≥5). LA commits vA, LB commits vB ≠ vA. P2 accepted both.

## Primary-Backup vs Paxos Decision
| Use Paxos when | Use Primary-Backup when |
|---|---|
| Correctness is absolute (lock server, financial) | Write-once or read-heavy workloads |
| Split-brain is catastrophic | Brief downtime on failover is acceptable |
| No single node can be trusted as sole leader | Paxos overhead exceeds benefit |

| Scenario | Choice | Reason |
|---|---|---|
| Stock exchange lock server | **Paxos** | Split-brain = two clients hold same lock = financial harm |
| Documentary movie storage | **Primary-backup** | Write-once, read-many; simple replication sufficient |
| Login server | **Primary-backup** | Read-heavy, stateless; brief failover downtime acceptable |

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2021 | Q8c | Leader waits < majority → how breaks Paxos (2.5 mk) |
| 2022 | Q2b | Same ballot id + equal-accept rule → correct? counterexample (6 mk) |
| 2024 | Q2a | Define consensus algorithms (1.5 mk, shared with L10) |
| 2024 | Q7a | Why 2f+1 nodes for f failures (3 mk) |
| 2024 | Q7b | Leader waits < majority → how breaks Paxos (verbatim repeat of 2021) (3 mk) |
| 2024 | Q7c | 3 scenarios: choose Paxos or primary-backup (3 mk) |

⭐ **"Leader < majority" question is verbatim 2021 and 2024. Know the counterexample cold.**
⭐ **2f+1 derivation:** N − f > N/2 → N > 2f → N ≥ 2f+1.
⭐ **Safety invariant:** Any two majority sets intersect. Everything else follows from this.
