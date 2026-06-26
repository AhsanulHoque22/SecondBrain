# Distributed System Fundamentals
> [[_index]] · [[dsm]] · [[consistency-models]] · Source: Lecture-01 (intro) + DS textbook (Tanenbaum/Sinha) · Solutions: `Fundamentals_Solutions.pdf`

**Definition (exam):** A distributed system is a collection of *independent computers that appears to its users as a single coherent system*, made of autonomous, asynchronous, failure-prone entities communicating over an unreliable network.

## Working definition (Lecture-01)
Entities = processes on devices; medium = wired/wireless network. Each entity is **autonomous, programmable, asynchronous, failure-prone**.
**Examples:** Web, NFS, DNS, BitTorrent (P2P), cloud (EC2/Azure), datacenter (Google).

## 9 design goals (Lecture-01)
Heterogeneity · Robustness · Availability · Transparency · Concurrency · Efficiency · Scalability · Security · Openness.

## Hard issues
No global clock (asynchrony) · unpredictable failures (can't tell crash vs slow link) · variable bandwidth & latency · large/variable scale.

## Exam sub-topics (mostly textbook, not slides)
| Sub-topic | Key answer |
|---|---|
| **Tightly vs loosely coupled** | Tightly = shared memory (multiprocessor); loosely = private memory + message passing (multicomputer). Draw both diagrams. |
| **Transparencies** | Location (where), Relocation (moves *while in use*), Migration (moves between accesses, name unchanged). Differentiate these 3. |
| **Distributed vs parallel** | DS wins on scalability, sharing, fault tolerance (no single point of failure), cost, geo-distribution. |
| **Scalability** | Ability to grow (size/geo/admin) without perf loss. Challenges: centralised component/data/algorithm, latency, replica consistency, multiple admin domains. |
| **Marshalling/Unmarshalling** | Pack data into a byte stream for transmission (serialize) / unpack at destination. |
| **ACID** | Atomicity (all-or-nothing), Consistency (valid→valid), Isolation (no interference), Durability (survives crash). |

## Exam pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | 1a/1b/1c, 2a, 2c | define+examples · coupling+figures · DS vs parallel · transparencies · design principles |
| 2021 | 1a/1b/1c/1d | define+examples · adv/disadv · scalability+challenges · marshalling+ACID |

⭐ **Section-A Q1 = fundamentals both years.** Definition + examples are guaranteed opening marks — have them cold.
