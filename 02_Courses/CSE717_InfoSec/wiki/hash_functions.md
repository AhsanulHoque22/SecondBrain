# Hash Functions & Hash Table Collision Resolution
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
A hash function maps an input of any size to a fixed-size output (the "hash" or "digest"); it is **irreversible** (unlike encryption) and is used for security, integrity, and authentication, not for hiding data.

## Key steps / algorithm
**6 properties of a good hash function:**
1. **Deterministic** — same input → same output, always.
2. **Quick computation** — must be fast for the system to be efficient.
3. **Pre-image resistance** — given H(A), infeasible to find A.
4. **Avalanche effect** — small input change → large output change.
5. **Collision resistant** — infeasible to find A≠B with H(A)=H(B).
6. **Puzzle friendly** — hard to pick an input for a pre-defined output.

**Collision resolution (open addressing) — probe sequences:**
1. **Linear probing:** if `h(k) mod m` full, try `+1, +2, +3, ...`
2. **Quadratic probing:** if full, try `+1², +2², +3², ...`
3. **Double hashing:** `h_new = (h1(k) + i·h2(k)) mod m`, i=0,1,2,... — best collision avoidance.

**Insertion drill (for any method):** for each key in order — compute primary hash → if slot free, place it → else apply probe sequence until an empty slot found.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Section B Q7(c) | Double hashing: h1=k mod13, h2=7+(k mod7), insert 6 keys, m=13 |
| 2023 | Section B Q8(c) | Linear probing: h(k)=(k+2) mod13, insert 6 keys, m=13 |
| 2023 | Section B Q5(b) | Enumerate properties of a good hash function (2.5) |

🔁 Repeats every year (2023 & 2024): a 6-key insertion trace into a hash table of size m=10–13, using one of the open-addressing probe methods.

## Weak spots / common mistakes
- Forgetting to **re-probe from the updated slot using the SAME formula** (linear: always +1 from current; double hashing: always +i·h2(k) from the ORIGINAL h1(k), not the last probed slot).
- Mixing up h1 and h2 roles in double hashing — h1 gives the starting slot, h2 gives the step size.
- Quadratic probing formula not seen in 2020-2024 papers — low priority, but know `f(i)=i²` as backup.

## Related topics
[[wiki/security_fundamentals|Security Fundamentals]] (hashing applications: passwords, MAC/HMAC, digital signatures, blockchain)
