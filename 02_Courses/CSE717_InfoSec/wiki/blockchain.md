# Blockchain & Bitcoin
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
A **blockchain** is a distributed, append-only ledger of blocks, where each block stores a cryptographic hash of the previous block (chaining them together) plus a **Merkle root** summarizing its transactions — making tampering detectable. **Bitcoin** is a decentralized P2P digital currency built on top of a blockchain, secured via mining (Proof of Work).

## Key facts / algorithm
**Block header fields (6):** Version, Previous Block Header Hash (chains blocks), Merkle Root Hash (all txns), Time, nBits (PoW difficulty target), Nonce.

**Why hashing secures the chain:**
1. Each block's hash = fingerprint of its full contents (header + Merkle root of txns).
2. Block $n$ stores hash of block $n-1$ as "Previous Hash".
3. Edit block $k$ → its hash changes → block $k+1$'s stored "Previous Hash" no longer matches → tamper detected.
4. Attacker must recompute hashes of block $k$ through the latest block to hide the tamper.

**Proof of Work (PoW):** find a nonce so $\text{hash}(\text{header}\|\text{nonce})$ meets a difficulty target (e.g. leading zeros) — hard to find, easy to verify. Recomputing PoW for all blocks after a tamper is computationally infeasible faster than the honest network → immutability.

**Merkle tree:** leaf = hash of each transaction; pairs hashed up to a single Merkle root stored in the header. Any transaction change → root changes → integrity check without scanning every transaction.

**Bitcoin ≠ Blockchain:** Bitcoin is the currency/consensus network; blockchain is the underlying data structure. Mining = competing to solve PoW, winner gets block reward + fees; difficulty self-adjusts for ~10 min/block.

**Input/output scripts (bitcoin transactions):** output script ("locking script") = spending condition (valid signature required); input script ("unlocking script") = signature + pubkey provided by spender; validation = combined script executes to TRUE → proves ownership of private key without revealing it.

**Types of blockchain:** Public (open, e.g. Bitcoin/Ethereum), Private (permissioned, one org, e.g. Hyperledger/Corda), Hybrid (mix, e.g. Dragonchain).

**Blockchain vs shared database:** blockchain = insert-only, full replication, global consensus rules, disintermediation allowed, fully confidential; shared DB = CRUD, master-slave/multi-master, local constraints, no disintermediation.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q3(b) | Explain how blockchain ensures security in terms of hashing + Proof of Work (3) |
| 2021 | Section B Q3(a) | (i) How is blockchain related to cryptography (2.75), (ii) what is bitcoin (2) |
| 2021 | Section B Q3(b) | Discuss input/output scripts for signature validation in bitcoin (4) |
| 2020/2022/2023 | — | No question found (an earlier "2022 Q8 Merkle/ETH-BTC" entry was a tracker error — corrected 2026-06-15) |

🔁 2/5 years confirmed (2021, 2024), 3–8.75 marks. NEW dedicated 2026 materials (Lc#11A/11B) → bonus material (Merkle tree, ETH vs BTC, types of chain, blockchain vs shared DB) likely insurance for 2026.

## Weak spots / common mistakes
- Conflating "Bitcoin" and "blockchain" — Bitcoin is one application built on blockchain technology, not a synonym.
- For the hashing+PoW security question, must explain BOTH halves: hashing → detectability, PoW → infeasibility of cover-up (re-mining every subsequent block).
- Input/output script question: emphasize that signature verification proves private-key ownership WITHOUT revealing the private key.
- If asked to "draw something" with no other guidance, default to the 3-block hash-chain diagram (most reusable across sub-questions).

## Related topics
[[wiki/des_feistel|DES/Feistel]] and [[wiki/digital_signature|Digital Signature]] — share the underlying hashing/digital-signature primitives that blockchain builds on.
