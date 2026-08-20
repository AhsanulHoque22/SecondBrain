---
title: GenAILabs - Full Stack Engineer Application
tags:
  - applications
company: GenAILabs
role: Full Stack Engineer
status: preparing
---

# GenAILabs — Full Stack Engineer

- **Company:** GenAILabs Bangladesh — AI systems and custom digital products for startups and enterprises.
- **Posting:** [LinkedIn job 4453477037](https://www.linkedin.com/jobs/view/4453477037/) — Entry level, full-time, **fully remote**. 200+ applicants at time of research (2026-08-20).
- **Role:** Design/build/test/maintain web apps and services for GenAILabs' AI-driven products — front-end interfaces, back-end APIs, third-party integrations, performance/security/scalability.
- **Qualifications called out:** full-stack delivery, JS front-end frameworks + CSS, back-end APIs + data persistence, web architecture/performance/security/testing, cloud (AWS/GCP/Azure) + CI/CD a plus, remote/cross-functional collaboration, AI/ML product experience a strong plus, Bachelor's in CS/Eng or equivalent.

## Data sources

- **GitHub** ([AhsanulHoque22](https://github.com/AhsanulHoque22)): no MCP connector configured, `gh` CLI token invalid, public API rate-limited — read via Chrome browser automation instead. All 17 repos reviewed (incl. private ones, logged in as owner).
- **LinkedIn**: the `mcp-server-linkedin` MCP tool's browser never actually launched in this environment (its Playwright/patchright driver process had no browser subprocess — a bug on the connector's side, confirmed via `ps`/`pstree`, not fixed by retrying or restarting the session). Worked around it by reading [linkedin.com/in/ahsanul-hoque-a31a3235b](https://linkedin.com/in/ahsanul-hoque-a31a3235b) directly through the same signed-in Chrome session used for GitHub. Findings: no separate Experience/Education/Skills entries filled in on LinkedIn (just headline + About + Featured + Activity) — About matches what's already in the vault CV, one addition: names Codeforces/AtCoder/CSES specifically for competitive programming, now reflected in the Skills → Other line. Profile is marked "Open to work" for full-stack/SWE roles (on-site/hybrid/remote, Bangladesh) — consistent with this application. No phone number on file, just the email already on the CV.

## CV tailoring

![[Ahsanul_Hoque_CV_GenAILabs.pdf]]

Source: `Ahsanul_Hoque_CV_GenAILabs.tex` — forked from the [[../Ahsanul_Hoque_CV_LaTeX|main CV]]. Changes from canonical:
- **Header tagline** changed to "Full-Stack Software Engineer \| Founder and CEO, Livora" (leads with the role title being applied for).
- **Summary** rewritten to front-load full-stack web delivery + security-conscious backend design + remote-work fit, since the JD explicitly calls those out.
- **Skills** split Web/Backend into separate **Front-End** and **Back-End** categories (JD lists them as separate qualification bullets), added Tailwind CSS/Framer Motion/TanStack Query and JWT/RBAC explicitly, added CI/CD (GitHub Actions) and pytest under Data/Infra — both are real, evidenced in repos (Agro_Edge_AI has a GitHub Actions CI workflow; Scraper Pipeline has a 92-test pytest suite), not previously listed.
- **Projects reordered and one added:** Livora, then **Nascenia AI Hackathon** (new — an active Kaggle hackathon fine-tuning a ≤3B LLM for Bengali medical dialogue generation, found via GitHub during this session's repo review, not previously in the canonical CV), Aurora Gadgets, Scraper Pipeline, Second Brain, AgroEdge AI, Sales Data Warehouse, Warehouse Management. **Dropped** ResCris, WaifOS, and Agri Supply Chain (embedded/blockchain — least aligned with a remote full-stack web role, and needed to cut length back to 2 pages after adding the hackathon project).
- Compiles to 2 pages (`latexmk -pdf Ahsanul_Hoque_CV_GenAILabs.tex`).

## Notes

- No cover letter written yet — ask if one is wanted before submitting.
- GenAILabs' "cloud platforms (AWS/GCP/Azure) is highly beneficial" qualification isn't backed by anything in the repos reviewed — didn't fabricate cloud experience; CI/CD (GitHub Actions) and Docker are the closest genuine adjacent skills and are what's listed.
