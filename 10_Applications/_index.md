---
title: Applications
tags:
  - applications
---

# Applications

Tracker for all job/program applications. Each application gets its own subfolder under this one.

## Shared assets

- ![[Ahsanul_Hoque_CV.pdf]] — **the CV**, single canonical file. Compiled output of `Ahsanul_Hoque_CV_LaTeX.tex`; this is what actually gets sent out.
- `Ahsanul_Hoque_CV_LaTeX.tex` — editable LaTeX source. Edit this, then recompile and overwrite `Ahsanul_Hoque_CV.pdf`: `latexmk -pdf Ahsanul_Hoque_CV_LaTeX.tex && cp Ahsanul_Hoque_CV_LaTeX.pdf Ahsanul_Hoque_CV.pdf && rm Ahsanul_Hoque_CV_LaTeX.pdf`
  - 2026-07-27: rebuilt to match the original hand-made PDF's look (sans-serif, left-aligned header, all-caps section rules), then added Scraper Pipeline and Second Brain projects. `Ahsanul_Hoque_CV.pdf` now *is* this LaTeX output — no separate frozen original is kept.

## Applications

*(none yet — create a subfolder per application, e.g. `10_Applications/[Company_Role]/`)*
