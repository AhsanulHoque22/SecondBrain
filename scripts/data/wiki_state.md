# Study Brain — Compiled State
_Updated: 2026-07-05 by overnight rollover_

## Active exam
🎯 CSE 715 — Computer Graphics · **Wed 8 Jul 2026, 10:30 AM** · 2 days from 2026-07-06 · Phase: 🔒 Lockdown, day 1 of 2 (pure revision + timed past papers, Graphics only — no Livora, no other subjects). 07-05 closed Ch5/Ch6/Ch7 (Cohen-Sutherland clipping, normalization transform, Cavalier/Cabinet projection, perspective-vs-parallel — all now 📖, 30/51 topics 📖). Z-Buffer (TIER1, 5/5 yield) still 🔲 — the planned block got skipped and needs a gap-fill pass before pure revision mode.

## Topics — CSE715 Computer Graphics
| Topic | Status | Conf | Next Recall |
|-------|:------:|:----:|:-----------:|
| Cohen-Sutherland region codes + line clipping | 📖 | — | 2026-07-07 |
| Normalization transformation (window→viewport) | 📖 | — | 2026-07-07 |
| Rotation — derive matrix + apply | 📖 | — | 2026-07-06 |
| Scaling/magnification about a fixed point | 📖 | — | 2026-07-06 |
| Cavalier/Cabinet projection matrices | 📖 | — | 2026-07-07 |
| Perspective vs Parallel projection | 📖 | — | 2026-07-07 |
| ↳ General parallel/perspective derivation (homogeneous coords) | 📖 | — | 2026-07-07 |
| ↳ Orthographic multiview (top/front/side) drawing | 🔲 | — | — |
| Z-Buffer algorithm | 🔲 | — | — |
| Image crop / sub-image coordinates | 📖 | — | 2026-07-06 |
| ↳ RGB/CMY color model + subtractive color + perceptual terms | 📖 | — | 2026-07-06 |
| ↳ Image file format (header/data, RLE compression) | 🔲 | — | — |
| ↳ Pixel color-attribute pseudocode (setPixel/getPixel/LUT ops) | 🔲 | — | — |
| ↳ Mandelbrot/Julia set visualization | 🔲 | — | — |
| DDA + Bresenham line algorithms | 📖 | — | 2026-07-06 |
| Koch curve / fractal generation | 📖 | — | 2026-07-06 |
| Point-obscures-point visibility via viewpoint | 🔲 | — | — |
| Direct coding + lookup table bit math | 📖 | — | 2026-07-06 |
| Ray–sphere intersection | 🔲 | — | — |
| Sutherland-Hodgman / Weiler-Atherton polygon clipping | 📖 | — | 2026-07-07 |
| CG vs Image Processing/HCI | 📖 | — | 2026-07-06 |
| Antialiasing / slanted-line dimming | 📖 | — | 2026-07-06 |
| Geometric vs Coordinate transformation | 📖 | — | 2026-07-06 |
| ↳ Coordinate-system rationale (device-independent/NDC) | 📖 | — | 2026-07-06 |
| ↳ 2D transform extras: translation, shear, composite-rotation, figure-ID | 📖 | — | 2026-07-06 |
| RGB scanline color interpolation | 🔲 | — | — |
| Ray vs Vector distinction | 🔲 | — | — |
| Ray equation r(t)=s+td point-finding | 🔲 | — | — |
| Convex/concave polygon identification | 📖 | — | 2026-07-07 |
| Aspect ratio / resize distortion | 📖 | — | 2026-07-06 |
| Midpoint circle algorithm + 8-way symmetry | 📖 | — | 2026-07-06 |
| Tilting (3D composite rotation, x then y) | 📖 | — | 2026-07-07 |
| Monitor color transformation matrix M | 🔲 | — | — |
| Isometric/Dimetric/Trimetric projection | 📖 | — | 2026-07-07 |
| Perspective foreshortening + vanishing point | 📖 | — | 2026-07-07 |
| Phong illumination model | 🔲 | — | — |
| Flood-fill / boundary-fill (8-connected) | 📖 | — | 2026-07-06 |
| ↳ Scan-line polygon fill algorithm (edge list) | 🔲 | — | — |
| Point left/right-of-line test | 🔲 | — | — |
| Halftoning + dither matrix (D2→D4) | 📖 | — | 2026-07-06 |
| Circular clipping window | 🔲 | — | — |
| Trapezoid-primitive polygon fill | 🔲 | — | — |
| Axonometric projection significance | 📖 | — | 2026-07-07 |
| 3D scaling application | 📖 | — | 2026-07-07 |
| Painter's algorithm vs Z-buffer | 🔲 | — | — |
| Perspective projection anomalies (4) | 📖 | — | 2026-07-07 |
| Orthographic vs Oblique projection | 📖 | — | 2026-07-07 |
| Back-face / visible-surface definitions | 🔲 | — | — |
| Color gamut of a monitor | 🔲 | — | — |
| Bezier / B-spline / Hermite curves | 🔲 | — | — |
| Octree/Quadtree/BST-tree/Fractal Geometry | 🔲 | — | — |

## Carry-forward
- Z-Buffer algorithm (Ch10) — still 🔲, TIER1, 5/5 yield. Skipped planned block yesterday. Tomorrow's Block 1 — non-negotiable gap-fill before revision mode.
- Ray-sphere intersection (Ch12) — still 🔲, TIER2, 4/5 yield. Tomorrow's Block 2 if time allows.
- 20-item AI/InfoSec recall backlog still not cleared — due again 2026-07-06, 26–33 days overdue on AI items, 19d on Number Theory. Parked through Mon/Tue lockdown — will keep slipping until after the Graphics exam.
- CSE719 exam outcome still unconfirmed — 07-01 EOD log left blank, no 07-03 daily log exists. Low priority, not blocking.

## Recall due 2026-07-06
- 🔁 Intelligent Agents + Environments (PAGE) `CSE713_AI` | conf 4/5
- 🔁 Search: UCS, Greedy, A, IDDFS — trace on graph `CSE713_AI` | conf 4/5
- 🔁 Forward + Backward Chaining + Rule-Based System `CSE713_AI` | conf 5/5
- 🔁 ↳ PL Basics: satisfiability, validity, entailment, Modus Ponens `CSE713_AI` | conf 5/5
- 🔁 ↳ Resolution in PL: clause form (4-step), refutation proof `CSE713_AI` | conf 5/5
- 🔁 Alpha-Beta Pruning + Minimax `CSE713_AI` | conf 5/5
- 🔁 FOL + Resolution + Inference (Marcus/Pompeii) `CSE713_AI` | conf 5/5
- 🔁 Hill Climbing + Simulated Annealing `CSE713_AI` | conf 5/5
- 🔁 STRIPS + Partial-Order Planning (Block World) `CSE713_AI` | conf 5/5
- 🔁 ↳ Canonical Form Conversion (9-step algorithm) `CSE713_AI` | conf 5/5
- 🔁 ↳ Evidential Reasoning (ER): Dempster-Shafer, degree of belief `CSE713_AI` | conf 5/5
- 🔁 ↳ FOL Syntax: Terms, Predicates, Functions, ∀, ∃, Sentences `CSE713_AI` | conf 5/5
- 🔁 ↳ FOL Translation (car/drone/robot scenario) `CSE713_AI` | conf 5/5
- 🔁 ↳ Knowledge Representation and Mapping (roles) `CSE713_AI` | conf 5/5
- 🔁 ↳ Resolution in FOL: Unification, Skolemization, refutation `CSE713_AI` | conf 5/5
- 🔁 Bayes' Theorem + Bayesian Networks `CSE713_AI` | conf 3/5
- 🔁 ↳ Extended Bayes' Theorem `CSE713_AI` | conf 3/5
- 🔁 ↳ Uncertainty Concept (doorbell) `CSE713_AI` | conf 3/5
- 🔁 ↳ McCulloch-Pitts Neuron + Perceptron + Learning Rule `CSE713_AI` | conf 3/5
- 🔁 Number Theory & Modular Arithmetic (Euclidean, Fermat, Euler, CRT, Miller-Rabin, discrete log) `CSE717_InfoSec` | conf 5/5

**Parked** — do not touch until after the 2026-07-08 Graphics exam (last-2-days rule).

## Recent pattern (last 3 days)
- 2026-07-03/04: 07-04 recovery day — CSE715 exam-Wednesday reset finally done, syllabus mapped, past papers analysed, 49 topics ranked, then Ch2/3/4 fully solved + wiki-ingested (16 topics → 📖).
- 2026-07-04: EOD log field left blank despite real work — confirmed via git log, not the log narrative.
- 2026-07-05: Ch5/Ch6/Ch7 fully question-analysed + solved (5yr PYQ) + wiki-ingested (3 commits). 30/51 topics now 📖. Z-Buffer block skipped — the one gap heading into lockdown. EOD log left blank again (same pattern).
