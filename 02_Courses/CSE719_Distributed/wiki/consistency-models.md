# Consistency Models
> [[_index]] · [[dsm]] · [[replication-2pc]] · Source: Lecture-09 · Solutions: `DSM_Consistency_Solutions.pdf`

**Definition:** A consistency model defines the contract between a distributed system and programmers regarding how writes propagate and when they become visible across processes.

## Consistency Ladder (weakest → strongest)
| Model | Guarantee | Cost |
|---|---|---|
| **Eventual** | Writes propagate eventually; no ordering | Lowest |
| **PRAM/FIFO** | Writes by one process seen in order by all | Low |
| **Causal** | Causally-related writes seen in causal order everywhere | Medium |
| **Weak** | Consistent at synchronisation barriers only | Medium |
| **Release** | Flush at release; import at acquire; consistent at lock boundaries | Medium |
| **Sequential** | All nodes see same total order of all operations | High |
| **Linearizability** | Sequential + real-time: each op appears instantaneous | Highest |

## Causal Consistency
- Causally related writes (happen-before) must be seen in causal order by ALL processes
- Concurrent (unrelated) writes may appear in different orders at different processes
- Implementation: vector clocks; delay delivery until all causal predecessors delivered
- **Best application:** Social media timelines — reply must appear after original post; unrelated posts from different users can appear in any order

## Weak vs Release Consistency
| | Weak | Release |
|---|---|---|
| Sync types | All sync ops treated equally | Distinguishes acquire (lock) and release (unlock) |
| Flush trigger | Every sync point | Only at release |
| Import trigger | Every sync point | Only at acquire |
| Messages | More | Fewer |
| Optimisation | None | Lazy release consistency (delay flush to next acquire) |

**Release preferred for DSM** — fewer messages, compatible with standard lock-based programs, lazy variant further reduces overhead.

## Strong vs Weak for Scenarios
| Scenario | Choice | Why |
|---|---|---|
| Video-sharing site (YouTube) | **Weak** | Stale view counts acceptable; millions of reads from local replicas; strong = too slow |
| Law enforcement evidence | **Strong (Linearizability)** | No stale reads; non-repudiation; legal audit requires single consistent view |
| Social media feed | **Causal** | Reply must follow original post; unrelated posts can be in any order |
| Stock exchange | **Strong** | Financial transactions require total order and no stale reads |

## Linearizability
- Each operation appears to execute atomically at some instant between invocation and completion
- Real-time ordering: if op A completes before op B starts, A precedes B in global order
- Implies sequential consistency + real-time constraint
- Used by: ZooKeeper, Google Chubby, distributed locks

**Methods to ensure serializability:**
1. **Two-Phase Locking (2PL):** acquire all locks before releasing any; growing then shrinking phase
2. **Timestamp Ordering:** each txn gets timestamp; abort if accessing out of order
3. **Optimistic CC (OCC):** execute freely, validate at commit time; abort if conflict
4. **MVCC:** multiple versions per data item; reads access version at txn start timestamp

## Quorum-Based Consistency
For N replicas:
- **R + W > N** (read-write overlap: any read set shares at least one replica with any write set)
- **W > N/2** (write-write overlap: any two write sets overlap)

**For N = 9:** W ≥ 5, R ≥ 10 − W

| W | Min R | Notes |
|---|---|---|
| 5 | 5 | Balanced |
| 7 | 3 | Read-optimised |
| 9 | 1 | Maximum read speed; writes require all 9 |

**Example (W=5, R=5, N=9):** Any 5 readers share ≥1 replica with any 5 writers (5+5−9=1). That shared replica has latest write → reader gets current value. ✓

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | Q4a | Causal consistency + best application (3 mk) |
| 2020 | Q4b | Weak vs release + which for DSM (3.5 mk) |
| 2021 | Q2a | Strong vs weak; adv/disadv for video site (3 mk) |
| 2021 | Q2b | Why strong for law enforcement (1.75 mk) |
| 2021 | Q2c | 9 replicas quorum constraints + worked example (4 mk) |
| 2021 | Q3d | Consistency definition + types with DSM (2 mk) |
| 2022 | Q4d | Consistency + types (3 mk) |
| 2024 | Q2b | Linearizability + serializability methods (1.5 mk) |

⭐ **Quorum example N=9: W≥5, R≥5 minimum. Know the two rules cold.**
⭐ **Release > Weak for DSM: distinguish acquire/release, fewer messages.**
⭐ **Linearizability = sequential + real-time. Used for locks, coordination.**
