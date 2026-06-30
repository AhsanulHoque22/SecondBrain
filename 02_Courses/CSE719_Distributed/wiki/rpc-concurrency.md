# RPC & Concurrency Control
> [[_index]] · [[distributed-fundamentals]] · [[replication-2pc]] · [[consistency-models]] · Source: Lecture-10 · Solutions: `RPC_Concurrency_Solutions.pdf`

**Definition:** RPC (Remote Procedure Call) allows a function in one process to invoke a function in a different process/host as if it were a local call, with all network complexity hidden in middleware. Concurrency control ensures concurrent transactions maintain ACID properties.

## RPC Components
| Component | Location | Role |
|---|---|---|
| **Client stub** | Caller process | Same signature as callee; marshals args; enables same caller code for LPC and RPC |
| **Communication module** | Both sides | Forwards REQUEST/REPLY messages to correct hosts |
| **Dispatcher** | Server | Routes incoming request to correct server stub by procedure ID |
| **Server stub** | Server process | Unmarshals args; calls callee; marshals return value |

Stubs are **auto-generated** from IDL (Interface Definition Language) by stub compilers (e.g., `rpcgen` for Sun RPC). Programmer only writes caller and callee.

## RPC Call Semantics
| Retransmit? | Filter dups? | Re-execute or retransmit? | Semantics | Example |
|---|---|---|---|---|
| Yes | No | Re-execute | At least once | Sun RPC |
| Yes | Yes | Retransmit reply | At most once | Java RMI |
| No | N/A | N/A | Maybe | CORBA |

## RPC Design Issues (asked verbatim 2021 & 2022)
1. **Call semantics** — exactly-once impossible under failures; choose at-most/at-least/maybe
2. **Marshalling** — different endianness; CDR (Common Data Representation) as wire format
3. **Binding** — static (hardcoded) vs dynamic (name server lookup at runtime)
4. **Transport protocol** — UDP (lightweight, needs RRA) vs TCP (reliable, heavier)
5. **Fault tolerance** — server crash before/after execution; client cannot distinguish
6. **Security** — authentication + authorization across trust boundaries
7. **Heterogeneity** — different OS/language/hardware; CDR + stubs solve this
8. **Performance** — RPC much slower than LPC; minimize unnecessary RPCs

## Marshalling
- Caller marshals arguments to CDR format → sends REQUEST → server unmarshals to platform format → calls callee
- Return: callee result marshalled at server stub → REPLY → unmarshalled at client stub → returned to caller
- **Big-endian** (IBM z): MSB at lowest address; **Little-endian** (Intel): LSB at lowest address

## RRA Protocol
Steps: (1) Client sends REQUEST ⟨req_id, proc_id, args⟩ → (2) Server executes, stores reply → (3) Server sends REPLY ⟨req_id, result⟩ → (4) Client sends ACKNOWLEDGE ⟨req_id⟩ → (5) Server discards stored reply.

**Concurrent extension**: Client sends REQUEST to all k servers simultaneously → waits for all k REPLYs → sends ACK to all. Enables parallel execution on multiple servers.

## Callback & Lightweight RPC
- **Callback RPC**: Server initiates RPC back to client when async event occurs. Client registers callback function. Used by AFS callback breaks.
- **Lightweight RPC**: Same-machine optimization. Uses shared memory (A-stack) instead of network; eliminates marshalling. 2–10× faster than standard RPC.

## ACID Properties
| Letter | Property | Definition |
|---|---|---|
| **A** | Atomicity | All-or-nothing: full commit or full rollback, no partial execution |
| **C** | Consistency | Server starts and ends in consistent state; integrity constraints preserved |
| **I** | Isolation | Non-final effects not visible to other transactions; appears serial |
| **D** | Durability | Committed effects survive failures; saved in stable storage |

## Concurrency Problems
- **Lost Update**: T1 and T2 both read X=10, both write X=9 → one update overwritten
- **Inconsistent Retrieval**: T2 reads X after T1 updates it but Y before T1 updates Y → inconsistent snapshot

**Serial equivalence check**: Mark each conflict pair (same object, ≥1 write) as (Ti,Tj) if Ti went first. If all pairs consistent → serially equivalent. If mixed → NOT SE → problem exists.

Conflicting pairs: read-write, write-read, write-write on same object. NOT read-read; NOT ops on different objects.

## Locking Schemes
- **Exclusive locking**: One lock per object; at most one transaction inside. Mutual exclusion.
- **Read-write locks**: Read mode (multiple allowed); write mode (exclusive). Lock promotion: read→write if no others.
- **Two-Phase Locking (2PL)**: Growing phase (acquire/promote only) → Shrinking phase (release only). Strict 2PL: release only at commit. **Guarantees serial equivalence but does NOT prevent deadlocks**.

## Timestamp Ordering
Each transaction gets timestamp on open. Before write: abort if any later txn already read/written. Before read: abort if any later txn already written.
- **Validation phase**: check all accesses satisfy timestamp ordering
- **Update phase**: if valid, apply tentative writes permanently

No deadlocks. High abort rate under write contention.

## Wait-For-Graph (WFG)
- Nodes = transactions; edge T_i → T_j = T_i waiting for T_j to release lock
- **Cycle in WFG = deadlock**
- Deadlock detection algorithm must satisfy: **Safety** (no false positives) + **Liveness** (no false negatives)
- In distributed systems: each server has local WFG; deadlock detector collects all, builds global WFG, detects cycles

## Distributed vs Centralized Concurrency
1. **No global clock** → no trivial total ordering; need vector clocks / Lamport timestamps
2. **Partial failures** → some servers commit, others crash → violates atomicity; need 2PC
3. **No global lock manager** → distributed WFG; deadlock detection requires coordination
4. **Network delays** → cannot distinguish slow from crashed; exactly-once semantics hard
5. **Concurrent access is structural** → isolation must be enforced via message-passing protocols

## Deadlock Scenario: N rowers, N+1 boitthas
With N rowers each needing 2 boitthas and N+1 total: **no deadlock possible**. After each rower grabs their first (N taken), 1 remains → at least one rower can grab second → proceeds → drops 2 → others proceed. Circular wait cannot form.

With exactly N boitthas and N rowers: **deadlock possible** — all grab one, none can get second.

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | Q3a | RPC motivation + schematic diagram (4.5 mk) |
| 2020 | Q3b | Stub: what, how generated, purpose (4.25 mk) |
| 2020 | Q5a | RRA protocol steps + figure |
| 2020 | Q5c | Callback RPC + Lightweight RPC (2 mk) |
| 2020 | Q5d | Concurrent RRA for multiple servers (2.75 mk) |
| 2021 | Q6a | Concurrency control + deadlock + locking (2.75 mk) |
| 2021 | Q6b | Timestamp ordering: validation + update phases (2 mk) |
| 2021 | Q8a | RPC definition + design issues (2.75 mk) |
| 2022 | Q7a | Schedule trace: T0/T1 serial-equivalence analysis (4 mk) |
| 2022 | Q7b | Concurrency control + preventing isolation (3 mk) |
| 2022 | Q7c | Deadlock detection in distributed systems (2 mk) |
| 2022 | Q8a | RPC definition + design issues (3 mk) |
| 2024 | Q3c | WFG purpose + example + algorithm conditions (3 mk) |
| 2024 | Q5c | Marshalling + communication paradigm comparison (4 mk) |
| 2024 | Q6a | Distributed vs centralized concurrency (3 mk) |
| 2024 | Q8a | ACID definition, one sentence per letter (3 mk) |
| 2024 | Q8b | Rowing crew deadlock analysis (3 mk) |

⭐ **RPC design issues** asked verbatim 2021 & 2022 — know all 8 cold.
⭐ **Serial equivalence check**: mark conflict pairs per object; mixed ordering = NOT SE.
⭐ **WFG**: safety (no false +) + liveness (no false −). Cycle = deadlock.
⭐ **2PL**: growing phase (acquire only) → shrinking phase (release only). Does NOT prevent deadlock.
⭐ **Boittha rule**: N rowers + N+1 boitthas → no deadlock; N boitthas → deadlock possible.
