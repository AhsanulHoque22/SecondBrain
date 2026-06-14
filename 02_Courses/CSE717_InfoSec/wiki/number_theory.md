# Number Theory & Modular Arithmetic
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
A collection of **modular arithmetic tools** — GCD/Extended Euclidean, Fermat's Little Theorem, Euler's Theorem, CRT, Miller-Rabin, and discrete logarithms — used to prove and compute properties of integers mod $n$; this toolkit is the **mathematical foundation for RSA** (Topic 8) and digital signatures (Topic 14).

## Key steps / algorithm
**A. GCD (Euclidean algorithm):** repeatedly $\gcd(a,b)=\gcd(b,a\bmod b)$ until remainder 0.

**B. Extended Euclidean → multiplicative inverse:** back-substitute to write $\gcd(a,b)=sa+tb$; if $\gcd=1$, $a^{-1}\equiv s\pmod b$.
- $1234^{-1}\bmod4321=3239$; $550^{-1}\bmod1769=550$ (self-inverse!).

**C. Linear congruence $ax\equiv b\pmod m$:** find $a^{-1}\bmod m$, then $x\equiv a^{-1}b\pmod m$.
- $33x\equiv18\pmod{280}\to x=26$ (using $33^{-1}=17$).

**D. Fermat's Little Theorem:** $a^{p-1}\equiv1\pmod p$ ($p$ prime, $\gcd(a,p)=1$). Reduce exponent mod $(p-1)$.
- Recurring seed: $3^{20x}\bmod11$ family — $3^{302}\bmod11=9$, $3^{301}\bmod11=3$, $3^{202}\bmod11=9$.

**E. Euler's Theorem:** $a^{\phi(n)}\equiv1\pmod n$ ($\gcd(a,n)=1$). Reduce exponent mod $\phi(n)$. If $\gcd(a,n)\neq1$, find the short repeating cycle directly.
- Recurring seed: $7^{1000}\bmod(10/11)=1$; special case $5^{1000}\bmod10=5$ (cycle, not Euler).

**F. CRT (NOT in Lc material):** pairwise-coprime moduli → unique solution mod $M=\prod m_i$. Shortcut: if every $a_i\equiv-1\pmod{m_i}$, then $x\equiv M-1$; if all $a_i=c$, then $x\equiv c\pmod M$.
- $x\equiv2,4,6\pmod{3,5,7}\to104$ (all $\equiv-1$). $x\equiv1\pmod{3,4,5,7}\to1$ (same constant).

**G. Miller-Rabin (NOT in Lc material):** write $n-1=2^kq$; compute $a^q\bmod n$; if not $\equiv\pm1$, square up to $k-1$ times looking for $-1$; never hitting it ⇒ composite.
- $n=21,a=2$: $2^5\bmod21=11$, square→$16$, never $20$ ⇒ composite ($21=3\times7$).

**H. Discrete log / cyclic groups (NOT in Lc material):** $\{1,...,p-1\}$ under mult. mod $p$ is cyclic of order $p-1$; a generator (primitive root) hits every residue. Find $x$ in $g^x\equiv h\pmod p$ by computing powers of $g$.
- $3^x\equiv11\pmod{17}\to x=7$. $3^x\bmod7$ for $x=1..6$ gives all distinct $\{3,2,6,4,5,1\}$ ⇒ 3 is primitive root mod 7.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q1(b,c) | Fermat + Euler pair (2.5+2.5) — exact numbers unknown |
| 2023 | Q1(b,c) | Fermat $3^{302}\bmod11=9$ (2.5); Euler $7^{1000}\bmod11=1$ (2.5) |
| 2023 | Q4(a) | CRT $x\equiv2,4,6\pmod{3,5,7}\to104$ (5) |
| 2023 | Section B Q7(b) | Linear congruence $33x\equiv18\pmod{280}\to26$ (3) |
| 2022 | Q3 | Miller-Rabin (3) + discrete log $3^x\equiv11\bmod17\to7$ (3) + Fermat $2^{83}\bmod5=3$ (2) + Euler special case $5^{1000}\bmod10=5$ (1) |
| 2021 | A3 | Discrete log (2.75) + ext. Euclidean $1234^{-1}\bmod4321=3239$ (2) + Fermat $3^{301}\bmod11=3$ (2) + Euler $X^{45}\equiv6\bmod35\to X{=}6,26$ (2) |
| 2020 | Q2 | CRT $x\equiv1\pmod{3,4,5,7}\to1$ (4.75) + discrete log + distinct $b^x\bmod7$ remainders (2+2) |
| 2020 | Q3 | Ext. Euclidean $550^{-1}\bmod1769=550$ (4.75) + Fermat $3^{202}\bmod11=9$ + Euler $7^{1000}\bmod10=1$ (2+2) |

🔁 5/5 years, 5–9 marks — HIGHEST-YIELD topic overall.

## Weak spots / common mistakes
- Forgetting Euler's theorem requires $\gcd(a,n)=1$ — when it doesn't (e.g. $5^{1000}\bmod10$), find the repeating cycle by direct computation instead.
- Sign errors in Extended Euclidean back-substitution — always verify with $a\times a^{-1}\equiv1$ before finalizing.
- CRT: check for the "$\equiv-1$" or "same constant" shortcuts before grinding through full $M_i, y_i$ computation.
- Miller-Rabin: remember the test can only prove **compositeness** definitively; passing means "probably prime", not certain.

## Related topics
[[wiki/digital_signature|Digital Signature]] (RSA key-leak/forward secrecy uses these same modular ideas) — direct prerequisite for **RSA (Topic 8)**, which reuses Extended Euclidean (key generation) and Euler's totient ($\phi(n)=(p-1)(q-1)$).
