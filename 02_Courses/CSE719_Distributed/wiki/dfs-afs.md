# Distributed File Systems & AFS
> [[_index]] · [[distributed-fundamentals]] · [[replication-2pc]] · Source: Lecture-08 · Solutions: `DFS_AFS_Solutions.pdf`

**Definition:** A DFS stores files on server machines; clients access them via RPCs using the same interface as local files (transparency). AFS (Andrew File System) is a scalable DFS using whole-file client-side caching with server-initiated callbacks.

## DFS Desirable Properties (Exam: "design principles")
1. **Transparency** — same API as local (Unix) files; location/replication invisible to client code
2. **Concurrency** — multiple clients read/write simultaneously; one-copy update semantics
3. **Replication** — fault tolerance via multiple server copies
4. **Security** — authentication + authorization (ACL or Capability List)
5. **Scalability** — stateless servers + client-side caching; performance doesn't degrade with more clients
6. **Stateless / Idempotent** — no per-client state on server; absolute positions, not pointers; crash recovery with no state to restore
7. **Heterogeneity** — works across different OS/hardware via common interface (VFS layer in NFS)

## Why UNIX Semantics is Hard in DFS
UNIX operations are **stateful** and **non-idempotent**:

| Unix feature | Problem in DFS |
|---|---|
| File descriptors | Server tracks per-client open state; crash → state lost |
| Read-write pointer | Same call returns different data → not idempotent → can't retry safely |
| Immediate write visibility | Across network with caching → one-copy semantics violated |
| Open-then-unlink | Distributed reference counting across clients is complex |

**Root cause (from slides):** "Unix file system operations are neither idempotent nor stateless."

**Example:** Client sends read(fd, buf, 1024). Server advances pointer, response lost. Client retries → server advances again → bytes skipped permanently.

## Vanilla DFS: Flat File Service
Replaces Unix stateful API with stateless, idempotent API:
- `Read(file_id, buffer, position, num_bytes)` — absolute position, no pointer
- `Write(file_id, buffer, position, num_bytes)`
- `Create/Delete(file_id)`, `Get/Set_attributes(file_id, buffer)`
- Directory service: `lookup(dir, name)` → `file_id`

No file descriptors = no open state at server = transparent crash recovery.

## DFS Security
- **Authentication**: verify user identity (Kerberos tickets, challenge-response)
- **Authorization**: two mechanisms:

| Mechanism | Stored per | Easy to ask |
|---|---|---|
| **ACL (Access Control List)** | File (list of users + access modes) | Who can access this file? |
| **Capability List** | User (list of files + access modes) | What can this user do? |

## NFS (Network File System)
Sun Microsystems, 1980s. Three-layer architecture:
- **VFS module** (client): gives transparency; routes calls to local FS or NFS client; uses **v-nodes** (virtual inodes — local → disk i-node; remote → NFS server address)
- **NFS Client**: kernel-integrated; performs RPCs to NFS Server
- **NFS Server**: flat file service + directory service; supports **mounting** (re-point path, no copy)

**Server caching (write strategies):**
| Strategy | Speed | Consistency |
|---|---|---|
| Delayed write | Fast | Poor (crash before flush = data lost) |
| Write-through | Slow | Good (disk written before ack) |

**Cache validation in NFS:** Client-initiated polling — client sends timestamp of cached block; server confirms if still current (or returns new version). Configurable attribute cache timeout.

## AFS (Andrew File System)
CMU, 1980s. Key insight: whole-file caching on client local disk → zero server RPCs after first fetch.

### Two Processes
| Process | Location | Role |
|---|---|---|
| **Vice** | Server | Stores files on disk; authentication; maintains callback lists; sends callback breaks on file change |
| **Venus** | Client workstation | Intercepts file calls; manages local disk cache; fetches from Vice on miss; uploads on close |

### AFS Operation Flow
1. Venus intercepts `open(file)`
2. Cache miss → Venus fetches **entire file** from Vice to local disk
3. Vice issues **callback promise**: "I'll notify you if this file changes"
4. `read`/`write` served from **local disk** — zero RPCs
5. `close` (if modified) → Venus uploads new version to Vice
6. Vice sends **callback break** to all Venus processes that cached the old version → they mark cache invalid

### Session Semantics
Modified file not visible to other clients until writer `close()`s (uploads) and reader re-`open()`s (re-fetches). Weaker than Unix one-copy semantics but enables orders of magnitude better scalability.

### Callback Message Loss
**Problem:** If callback break message from Vice to Venus is lost → Venus serves stale cached data.

**AFS solution:**
1. Venus does not trust callbacks indefinitely after disconnection
2. On **reconnect with Vice**: Venus validates all cached files by sending version numbers → Vice confirms valid or sends new version
3. During disconnection: Venus re-fetches any uncertain file before serving it

## Cache Validation Comparison
| Approach | Who initiates | Server load | Used by |
|---|---|---|---|
| Client polling (timestamp) | Client (periodic) | High (poll per client) | NFS |
| Callbacks | Server (on change) | Low (only on modification) | AFS |

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | Q7a | Why UNIX semantics hard in DFS (2.5 mk) |
| 2020 | Q7b | DFS design principles (4 mk) |
| 2020 | Q7c | Cache validation (2.25 mk) |
| 2021 | Q3b | UNIX semantics difficulty (2 mk) |
| 2021 | Q6c | DFS requirements/design issues (2 mk) |
| 2021 | Q6d | What is AFS + file service architecture (2 mk) |
| 2022 | Q6c | AFS + AFS architecture (2 mk) |
| 2024 | Q3b | Security in DFS + message ordering paradigms (3 mk) |
| 2024 | Q4d | Venus + Vice + AFS callback message loss (3 mk) |

⭐ **DFS appears ALL 4 years (2020–2024) — single highest-yield blind spot.**
⭐ **UNIX not idempotent + not stateless** = root cause answer for every "why hard" question.
⭐ **Vice = server (stores, callbacks); Venus = client (caches, intercepts).**
⭐ **Callback loss** → revalidate on reconnect (not re-fetch everything — only invalidated entries).
