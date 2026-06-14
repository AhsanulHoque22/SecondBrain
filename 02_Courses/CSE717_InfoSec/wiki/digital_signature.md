# Digital Signature — Generic Model, Properties, Vulnerabilities
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
A **digital signature** is a value computed from a message and the signer's **private key**, attached to the message to provide **authentication**, **integrity**, and **non-repudiation** — anyone with the signer's **public key** can verify it, but only the signer could have produced it.

## Key steps / algorithm
**Generic model (sender → receiver):**
1. Sender computes hash $h = H(M)$.
2. Sender encrypts $h$ with **private key** $PR_a$ → digital signature $DS$.
3. Sender transmits $(M, DS)$.
4. Receiver decrypts $DS$ with sender's **public key** $PU_a$ → recovers $h$.
5. Receiver independently computes $h' = H(M)$ on received message.
6. **Compare** $h$ vs $h'$ — equal → authentic & unmodified; not equal → reject.

**Properties a signature must have:** verify author + date/time, authenticate contents at signing time, verifiable by third parties (dispute resolution).

**Scheme requirements:** depends on message; uses sender-unique info (private key); easy to produce & verify; computationally infeasible to forge (new message for existing sig, OR fraudulent sig for given message); practical to store.

**Attack types → forgery outcomes:** key-only / known-message / chosen-message attacks → total break / universal / selective / existential forgery.

**Direct digital signature:** order = **sign-then-encrypt** (sign plaintext, then encrypt msg+sig with shared key). Threats: (1) key compromise → forged signatures, (2) false repudiation (sender falsely claims key was stolen). Mitigation: timestamps + trusted third party.

**RSA private-key leak:** NO forward secrecy — all past ciphertexts decryptable, past signatures untrustworthy → revoke & rotate immediately.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | Q2(a) + Section B Q2(c) | What is DS + vulnerable attack types (3+3) |
| 2024 | Section B Q8(d) | Draw generic model (1) |
| 2023 | Q2(a) + Section B Q5(c) | What is DS + attack types (3+3) |
| 2023 | Section B Q5(d) | RSA key-reuse safety after private-key leak (1) |
| 2022 | Section B Q5(b) | Properties + scheme requirements |
| 2022 | Q7(a) | Sign-then-encrypt order + threats to direct DS |
| 2021 | Section B Q2(c) | Draw generic model (2) |
| 2020 | Q7(a) | Draw + explain generic model (4.75) |

🔁 5/5 years — diagram form (2020/2021/2024) + conceptual form (2022/2023/2024) alternate/combine.

## Weak spots / common mistakes
- Mixing up which key signs (private) vs which key verifies (public) — opposite of encryption-for-confidentiality (public encrypts, private decrypts).
- Forgetting the **compare step** ($h$ vs $h'$) — this IS the verification, not just decryption.
- Confusing "existential forgery" (weakest, ≥1 valid pair) with "universal forgery" (any message) — order matters if asked to rank severity.

## Related topics
[[wiki/des_feistel|DES/Feistel/S-box/Avalanche/3-DES]] (paired cheat sheet, same exam slot pattern), [[wiki/hash_functions|Hash Functions]] (hash function $H(M)$ used in step 1)
