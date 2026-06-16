# Quantum Attacks & ECC — CSE 717 InfoSec

**Definition:** Quantum attacks leverage quantum computing properties (superposition, entanglement) to break classical cryptographic algorithms. ECC (Elliptic Curve Cryptography) uses point arithmetic on the curve $y^2 \equiv x^3 + ax + b \pmod{p}$ for public-key encryption.

---

## Quantum Attack Summary

| Algorithm | Target | Impact |
|-----------|--------|--------|
| Shor's Algorithm | RSA (integer factorization) | **Completely breaks** RSA |
| Shor's Algorithm | ECC (ECDLP — discrete log) | **Completely breaks** ECC |
| Grover's Algorithm | Symmetric (AES, DES, SHA) | Halves key strength — quadratic speedup only |

**Why RSA/ECC are fully broken:** Shor's gives polynomial-time solution to factorization and discrete log. Classical: exponential. Quantum: polynomial.

**Why symmetric is less vulnerable:** Grover gives only $\sqrt{N}$ speedup. AES-128 drops to ~64-bit equivalent. AES-256 remains quantum-resistant. Security loss is manageable by increasing key size.

---

## ECC Point Doubling Algorithm (Case B: $P = Q$)

| Step | Action |
|------|--------|
| 1 | $\lambda = (3x_1^2 + a)/(2y_1) \bmod p$ — compute numerator, find modular inverse of denominator |
| 2 | $x_3 = \lambda^2 - 2x_1 \bmod p$ |
| 3 | $y_3 = \lambda(x_1 - x_3) - y_1 \bmod p$ |
| 4 | If negative result, add multiples of $p$ until positive: $(-a) \bmod p = p - (a \bmod p)$ |

**For $P \neq Q$ (addition):** $\lambda = (y_2 - y_1)/(x_2 - x_1) \bmod p$; then $x_3 = \lambda^2 - x_1 - x_2$, $y_3 = \lambda(x_1-x_3)-y_1$

---

## 2024 Exam Question (Only Year)

**Q6(a) [3 marks]:** Curve $E: y^2 = x^3 + 2x + 3$ over $F_{19}$, compute $2P$ for $P=(3,6)$

| Step | Calculation | Result |
|------|-------------|--------|
| $\lambda$ numerator | $3(9)+2 = 29 \bmod 19$ | $10$ |
| $\lambda$ denominator inverse | $12^{-1} \bmod 19$: $12 \times 8 = 96 \equiv 1$ | $8$ |
| $\lambda$ | $10 \times 8 = 80 \bmod 19$ | $4$ |
| $x_3$ | $4^2 - 2(3) = 16-6$ | $10$ |
| $y_3$ | $4(3-10)-6 = -34 \bmod 19 = -34+38$ | $4$ |

**Answer: $2P = (10, 4)$** — Verification: $4^2 = 16$, $10^3+2(10)+3 = 1023 \equiv 16 \pmod{19}$ ✓

**Q6(b) [2 marks]:** RSA/ECC rely on factorization/ECDLP which Shor solves polynomially. Symmetric crypto has no such structure; Grover only halves key strength.

---

## Exam Pattern

- **1/5 years (2024 only)** — low yield, don't over-invest.
- Only numeric type: point doubling on a curve mod prime.
- The conceptual "why quantum breaks ECC/RSA" is the easier 2 marks — guaranteed if Quantum appears.
- Source: Lc#6 pp.22-35 (ECC formulas + worked examples), Lc#7 pp.1-13 (Quantum basics + why ECC/RSA vulnerable).

---

## Weak Spots / Common Mistakes

- Use **doubling formula** ($\lambda = (3x_1^2+a)/(2y_1)$) when $P=Q$, not the addition formula.
- Division mod $p$ = multiply by modular inverse, NOT regular division.
- Always verify with $(-a) \bmod p = p - (a \bmod p)$ for negative intermediates.
- The exam curve ($b=3$, $p=19$) differs from the lecture example ($b=2$, $p=17$) — same method, different numbers.

---

## Related Topics

- [[rsa]] — also broken by Shor's; RSA security = integer factorization hardness
- [[number_theory]] — modular inverse (Extended Euclidean) is central to ECC computation
- [[aes]] — symmetric crypto, less vulnerable to quantum (Grover only)
