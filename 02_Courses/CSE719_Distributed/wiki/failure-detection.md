# Failure Detection & Group Membership
> [[_index]] · [[distributed-fundamentals]] · [[cloud-computing]] · Source: Lecture-04 · Solutions: `FailureDetection_Solutions.pdf`

**Definition:** A failure detector is a distributed module that monitors process liveness and reports crashes to the application so recovery actions can be taken. Group membership protocols maintain a consistent view of which processes are currently alive.

## Why Failures Must Be Detected
- 1 machine fails once per 10 years → 120 servers: MTTF = 1 month; 12,000 servers: MTTF = 7.2 hrs
- Failures are the **norm**, not the exception, in datacenters

## Desirable Properties
| Property | Definition | In practice |
|---|---|---|
| **Completeness** | Every failure is eventually detected | **Guaranteed** |
| **Accuracy** | No alive process is declared failed | **Probabilistic only** — $PM(T)$ |
| **Speed** | Time until *some* process detects the failure | As fast as $T'$ (SWIM period) |
| **Scale** | Equal load per member; no bottleneck | O(1) per node (SWIM) |

**Key theorem [Chandra & Toueg 1996]:** Completeness + Accuracy are **impossible to achieve simultaneously** in asynchronous/lossy networks. A perfect failure detector would solve consensus — FLP impossibility proves consensus is impossible in async networks.

## Heartbeating Variants
| Variant | Mechanism | Problem |
|---|---|---|
| Centralized | All → one monitor; timeout = fail | Hotspot / single point of failure |
| Ring | Each node monitors ring successor | Unpredictable with simultaneous failures |
| All-to-All | Every node → every other node | O(N) messages/node/period; doesn't scale |
| **Gossip-style** | Random subset gossip; merge lists | O(N·logN/T) load; robust via multi-path |
| **SWIM** | Ping → if no ack, indirect via K nodes | O(1) load; constant detection time |

## Gossip-Style Heartbeating (2022 Q6b answer)
1. Each member maintains array of ⟨address, heartbeat-counter⟩ for all members
2. Every gossip period $t_g$: pick random subset, send full membership list
3. Recipients merge lists (keep higher counter)
4. If counter not incremented within $T_{\text{fail}}$ → mark **failed**
5. After $T_{\text{cleanup}}$ → delete entry (prevents stale re-introduction)

**Robustness over all-to-all:** failure info travels via multiple independent random paths → single link failure cannot prevent detection.

## SWIM Failure Detector Protocol
1. $p_i$ pings random $p_j$ every protocol period $T'$
2. No ack → send **ping-req** to $K$ random members; they relay ping/ack to $p_j$
3. Still no ack → mark $p_j$ **Suspected**
4. After $T_{\text{cleanup}}$ → declare $p_j$ **Failed**

| Metric | SWIM | Heartbeating |
|---|---|---|
| First detection time | Constant: $T' \cdot \lceil e/(e-1) \rceil$ | O(N) |
| Process load | O(1) / constant | O(N/T) |
| False positive rate | Tunable via K | Fixed |
| Completeness | Within O(log N) periods | Yes |

## Group Membership Protocol Design (2022 Q6d answer)
Two separated sub-protocols:

**I. Failure Detector** (SWIM preferred):
- Ping → indirect via K nodes → Suspect → Fail
- Separating FD from dissemination allows independent optimization

**II. Dissemination** (infection-style preferred):
- Piggyback membership updates (join/fail/suspect) on existing SWIM ping/ack messages
- Zero extra messages; spreads in O(log N) rounds

**Additional elements:**
- **Suspicion mechanism:** Alive → Suspected → Failed (reduces false positives from congestion)
- **Incarnation numbers:** only the process itself can increment its counter; (Failed, inc#) overrides everything; (Suspect, inc#) > (Alive, inc#); higher inc# overrides lower → prevents stale gossip

## Why Perfect Detection is Impossible in Async Networks (2024 Q2d answer)
- Asynchronous network: message delay is **unbounded**
- $p_i$ cannot distinguish: (a) $p_j$ crashed vs (b) $p_j$'s message is delayed
- Any timeout $T_{\text{fail}}$:
  - Too short → false positive on slow process → violates Accuracy
  - Too long → misses fast detection → violates instantaneousness
  - No fixed timeout is simultaneously correct and fast for all possible delays
- Formal: perfect FD ⟹ can solve consensus; but FLP impossibility ⟹ consensus impossible

## Server Cannot Bound Response Time (2024 Q3a answer)
**Why:** (1) unbounded network delay; (2) message loss; (3) OS scheduling preemption; (4) no global clock

**What to do:** Use timeout $T_{\text{fail}}$ → Suspect → indirect ping via K nodes → declare Failed; accept probabilistic accuracy $PM(T)$; tune $T_{\text{fail}}$ to balance detection speed vs false positive rate.

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | Q2b | Techniques for fault detection and recovery |
| 2022 | Q6b | How to increase robustness of all-to-all heartbeating |
| 2022 | Q6d | How to design a group membership protocol |
| 2024 | Q2d | Primary goal of FD; why perfect detection impossible in async networks |
| 2024 | Q3a | Why server can't bound response time; what should it do |

⭐ **2024 Q2d and Q3a share the same core argument** — asynchronous impossibility + timeout-based mitigation. Learn once, write twice.
⭐ **Key terms for exam:** Completeness, Accuracy, asynchronous network, unbounded delay, Chandra & Toueg, gossip-style, SWIM, $T_{\text{fail}}$, suspicion mechanism, incarnation number, infection-style dissemination.
