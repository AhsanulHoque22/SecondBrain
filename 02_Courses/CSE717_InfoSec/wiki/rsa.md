# RSA — Key Generation & Encryption/Decryption
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
**RSA** is an asymmetric (public-key) cryptosystem where a user generates a key pair $\{e,n\}$ (public) and $\{d,n\}$ (private) from two secret primes $p,q$; encryption is $C=M^e\bmod n$ and decryption is $M=C^d\bmod n$ — security rests on the difficulty of factoring $n=pq$.

## Key steps / algorithm
**The 8-step pipeline (Lc#6 p16, identical every year, only the numbers change):**
1. Select two primes $p \neq q$.
2. $n = p \times q$.
3. $\phi(n) = (p-1)(q-1)$.
4. Select $e$: $\gcd(e,\phi(n))=1$, $1<e<\phi(n)$.
5. $d = e^{-1}\bmod\phi(n)$ via **Extended Euclidean** (Topic 7 Cheat Sheet B).
6. Public key $=\{e,n\}$, Private key $=\{d,n\}$.
7. Encrypt: $C=M^e\bmod n$ ($M<n$).
8. Decrypt: $M=C^d\bmod n$.

**Mandatory technique — square-and-multiply** for $M^e\bmod n$: write $e$ in binary; scan left→right starting result$=1$; always square mod $n$; if bit$=1$, also multiply by $M$ mod $n$. ($e=17=10001_2$ → 4 squarings + 1 multiply.)

**Worked example (Lc#6 pp17–19):** $p=13,q=11 \Rightarrow n=143,\phi(n)=120$. Pick $e=13 \Rightarrow d=37$ (since $13\times37=481=4\times120+1$). Public$=\{13,143\}$, Private$=\{37,143\}$. Encrypt $P=13\to C=13^{13}\bmod143=52$. Decrypt $C=52\to52^{37}\bmod143=13$ ✓.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q2(c),(d) | Encrypt "DATA" with $p=61,q=53,e=17$ (ASCII per letter) → $\{1759,2790,2159,2790\}$ (3); decrypt $c=17 \to 3170$, outside ASCII range — method marks (3) |
| 2023 | Section B Q7(c),(d) | Encrypt "CU" with $p=43,q=59$ ($e$ illegible in scan — full pipeline demoed with $e=13$) → $\{2044,1246\}$ (3); decrypt "0981 0461" — same procedure (2) |
| 2022 | Q6 | Encrypt $M=3$, $p=13,q=7$, choose $e<10$ (got $e=5,d=29,C=61$) + explain why eavesdropper can't decrypt without $d$ (3+3+2+8=16) |
| 2021 | Section B Q2(a),(b) | $p=3,q=11,e=7,M=2\to C=29,d=3$ (2.75); given $e=31,n=3599\to d=3031$ (2+2) |
| 2020 | Q6(a),(b) | Identical to 2021 B2 — $p=3,q=11,e=7,M=2$ (4.75); $e=31,n=3599\to d=3031$ (2+2) |

🔁 5/5 years, 5–16 marks — **largest single-topic block some years**. "Given $e,n$, find $d$" with $e=31,n=3599$ repeats verbatim 2020 & 2021 → memorize $n=59\times61,\phi(n)=3480,d=3031$.

## Weak spots / common mistakes
- Trying to compute $M^e$ by direct multiplication instead of square-and-multiply — always write $e$ in binary first.
- Forgetting $\phi(n)$ depends only on $p,q$ (not $e$) — if $e$ is missing/illegible, $n$ and $\phi(n)$ can still be computed and a valid $e$ chosen to demonstrate the full method.
- When "choose $e<k$" is asked, pick the **smallest** valid $e$ coprime to $\phi(n)$ — usually 5 or 7 for small $\phi(n)$.
- "Why can't an eavesdropper decrypt?" → answer is **factoring $n$ is infeasible for large primes** (RSA hardness assumption), NOT "because the key is secret" alone.

## Related topics
[[wiki/number_theory|Number Theory & Modular Arithmetic]] — RSA reuses Extended Euclidean (Cheat Sheet B, for step 5) and Euler's totient $\phi(n)=(p-1)(q-1)$ (Cheat Sheet E) directly. [[wiki/digital_signature|Digital Signature]] — RSA private-key leak/forward-secrecy question (2023 Section B Q5(d)) answered there.
