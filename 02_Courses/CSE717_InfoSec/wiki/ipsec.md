# IPsec (IP Security) — CSE 717 InfoSec

**Definition:** IPsec is a suite of protocols that provides security services (confidentiality, authentication, integrity) at the IP network layer using two protocols — ESP and AH — plus four supporting document sets.

---

## Architecture — 7 Components

| # | Component | Role |
|---|-----------|------|
| 1 | **Architecture** | General concepts, definitions, protocols, algorithms, security requirements |
| 2 | **ESP Protocol** | Encapsulation Security Payload → **Confidentiality** |
| 3 | **Encryption Algorithm** | Documents for encryption algorithms used with ESP |
| 4 | **AH Protocol** | Authentication Header → **Authentication + Integrity** |
| 5 | **Authentication Algorithm** | Documents for auth algorithms used by AH and ESP |
| 6 | **DOI** (Domain of Interpretation) | Identifier supporting both AH and ESP; binds shared parameter values |
| 7 | **Key Management** | Describes key exchange between sender and receiver |

**Three services:** Confidentiality (ESP) · Authentication (AH) · Integrity (AH)

**Architecture diagram flow:** Architecture → {ESP Protocol, AH Protocol} → {Encryption Alg, Authentication Alg} → DOI → Key Management

---

## Security Associations (SA)

A **Security Association** is a one-way logical connection providing security services for traffic between two endpoints.

**Uniquely identified by three parameters:**
1. **SPI** (Security Parameters Index) — 32-bit value in AH/ESP header
2. **Destination IP Address** — receiving endpoint
3. **Security Protocol** — AH or ESP

**One-way:** SA is unidirectional. Bidirectional communication needs **two SAs**. Each SA stores: sequence number, anti-replay window, keys, mode (transport/tunnel), SA lifetime.

---

## Transport Mode vs Tunnel Mode

| | Transport Mode | Tunnel Mode |
|--|----------------|-------------|
| **Protects** | IP payload only | Entire original IP packet |
| **IP header** | Original unchanged | New outer IP header added |
| **Use case** | End-to-end host-to-host | Gateway-to-gateway VPN |
| **Overhead** | Lower | Higher |

---

## RFC 4301 — Six Security Services

1. **Access control** — policy-based filtering of which packets pass
2. **Connectionless integrity** — detects per-datagram tampering
3. **Data origin authentication** — verifies packet sender
4. **Anti-replay (rejection of replayed packets)** — sliding window + sequence numbers
5. **Confidentiality** — encryption of IP payload (ESP)
6. **Limited traffic flow confidentiality** — conceals traffic patterns in tunnel mode

**Mnemonic:** ACC-D-RC — Access, Connectionless integrity, data origin auth, Duplicate-replay rejection, Confidentiality, traffic flow Confidentiality

---

## Application Areas

1. Secure branch-office connectivity (site-to-site VPN)
2. Secure remote access VPN for employees
3. B2B extranet/partner connectivity
4. Enhanced e-commerce security

---

## All Past-Paper Questions

| Year | Question | Marks | Content |
|------|----------|-------|---------|
| 2024 | Q5(c) | 3 | Architecture + security associations |
| 2021 | Q4(b) | 2.5 | Application areas + session vs connection state |
| 2021 | Q4(c) | 2.5 | Architecture |
| 2020 | Q8(a) | 2.25 | Benefits + transport vs tunnel mode |
| 2020 | Q8(b) | 2.25 | RFC 4301 services |
| 2020 | Q8(c) | 2.25 | Application areas + session/connection state |
| 2020 | Q8(d) | 2 | Architecture diagram |

---

## Exam Pattern

- **3/5 years (2020, 2021, 2024)**, 2.25–9 marks.
- **Architecture** appears in ALL three years — draw it every time.
- Same sub-question cluster recurs: architecture + transport/tunnel + RFC4301 + application areas + SA.
- Source: Lc#7 pp.14–21.

---

## Weak Spots / Common Mistakes

- ESP = confidentiality; AH = authentication + integrity. Don't swap them.
- SA is **one-way** — state this explicitly, especially for 2024 Q5(c).
- RFC 4301 has 6 services; know all six by name.
- "Session state vs connection state": an SA = one connection (one-way); a session = two SAs (bidirectional).

---

## Related Topics

- [[rsa]] — public-key crypto protected by IPsec tunnel in practice
- [[aes]] — encryption algorithm used within ESP
- [[digital_signature]] — authentication layer complementary to IPsec
