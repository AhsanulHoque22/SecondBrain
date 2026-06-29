# Cloud Computing
> [[_index]] · [[distributed-fundamentals]] · [[dsm]] · Sources: Lecture-02 + Unit 3/4 readings · Solutions: `Cloud_Solutions.pdf`

**Definition (NIST, exam-ready):** Cloud computing is a model for enabling convenient, **on-demand network access to a shared pool of configurable computing resources** that can be **rapidly provisioned and released** with minimal management effort.

**Definition (Vaquero):** A large pool of easily usable and accessible **virtualised resources** dynamically reconfigured to adjust to variable load, with optimum utilisation via a **pay-per-use** model, guarantees offered via SLAs.

## Three Service Models (SaaS / PaaS / IaaS)
| Model | What the provider delivers | Examples | User manages |
|---|---|---|---|
| **SaaS** | End-user applications via browser | Google Docs, Salesforce, Office 365 | Nothing |
| **PaaS** | Runtime, middleware, DB, dev tools | Google App Engine, Heroku | App code only |
| **IaaS** | Virtual machines, storage, networking | AWS EC2/S3, Azure VMs, GCE | OS + everything above |

Stack (bottom → top): Physical → Hypervisor → IaaS VMs → PaaS runtime → SaaS app.

## Virtualization (IaaS enabler)
- **Hypervisor** abstracts physical hardware into multiple isolated VMs (Guest OS + apps).
- Stack: Physical hardware → Hypervisor → VMs → Workloads → Provisioning layer.
- Benefits to providers: (1) server utilisation from ~20% → >80%; (2) new VM in seconds.

## Deployment Models
| Model | Who uses it | Key point |
|---|---|---|
| **Public** | Open market (anyone) | IBM, Google, Amazon; concerns: limited SLA, trust |
| **Private** | Single org/enterprise | On-premises (EUCALYPTUS); full control, compliance |
| **Hybrid** | Org + external vendor | Private for sensitive data; public for bursting |
| **Community** | Consortium (shared concerns) | Research universities, government agencies |

**Cloud Burst:** Use local private cloud normally; when capacity is exceeded, spill into public cloud.

## EUCALYPTUS
- **Elastic Utility Computing Architecture for Linking Your Programs To Useful Systems**
- Open-source private cloud framework; implements **AWS-compatible API** (EC2 tools work unchanged)
- Why used: org wants cloud elasticity but cannot put data in public cloud (security/compliance)
- Deployment model it creates: **Private cloud**

## Why Cloud? (Benefits)
| Benefit | Key point |
|---|---|
| Flexibility | Any SW platform; access from any internet-connected device |
| Scalability | Instant; add/cancel via software; illusion of infinite resources |
| Cost | Pay-as-you-go; no upfront; SMEs access giant infrastructure |
| Maintenance | Vendor responsibility (patches, monitoring, backup, security updates) |
| Utilisation | Consolidation of CPU cycles, storage, bandwidth |
| Availability | Access from anywhere, any time |
| Reliability | Fault tolerance managed by provider |
| CO2 | Server consolidation → higher utilisation → reduced power usage |

## Drawbacks
Security · Privacy · Vendor lock-in · Network-dependent · Migration (data egress)

## Scaling
- **Vertical (Scale Up):** add CPU/RAM to same machine. Limit: hardware ceiling. No downtime, no app changes. Single point of failure.
- **Horizontal (Scale Out):** add more machines. No upper limit. Needs load balancer / stateless design. Better fault tolerance. Cloud favours this.

## Multi-Tenancy
Multiple tenants share same physical infra + software instance; data logically isolated.
- Economic model: spread fixed costs → lower per-customer price.
- Risks: data leakage between tenants; noisy-neighbour performance degradation.
- SaaS Level 4 = single instance, configurable per-tenant views (most efficient).

## Phases in Cloud Architecture (exam 1-mark)
1. Infrastructure phase (IaaS): physical HW → virtualised via hypervisor
2. Platform phase (PaaS): runtime + middleware on top of VMs
3. Application phase (SaaS): end-user software, fully provider-managed

## IaaS vs PaaS comparison (2024 exam trade-off question)
| | IaaS | PaaS |
|---|---|---|
| Dev speed | Slow (configure OS + middleware) | Fast (deploy code only) |
| Op. overhead | High (team manages OS/patches) | Low (provider manages) |
| Vendor lock-in | Low (portable VMs) | High (proprietary APIs) |
| Scalability | Manual (configure rules) | Automatic |
| Best for | DB servers, legacy apps | App tier, microservices, rapid dev |

## Reserved vs On-Demand Instances (cost calc)
- **Reserved:** upfront commitment; 30–70% cheaper; use for always-on base load.
- **On-demand:** no commitment; full rate; use for spiky/variable workload.
- Decision rule: if instance runs >50% of the time → reserve it.

## Exam Pattern
| Year | Q | Asks |
|------|---|------|
| 2020 | Q8a/b/c | cloud definition+pros/cons · e-commerce services+models · health management aspects |
| 2021 | Q3a, Q4c, Q5a–d | e-commerce · phases · on-demand · cloud def+platforms · layers+vs-distributed · EUCALYPTUS |
| 2022 | Q1a/b/c, Q2a | define+horiz/vert scaling · e-commerce · multi-tenancy · EC2 vs physical |
| 2024 | Q5a/b, Q6b/c | benefits+drawbacks · virtualization · IaaS vs PaaS · cost calculation |

⭐ **E-commerce deployment question verbatim 3 years (2020/2021/2022) — must know cold.**
⭐ **2024 adds virtualization + IaaS/PaaS trade-off + cost arithmetic — new subtopics to know.**
