# CSE 715 — Computer Graphics · Syllabus (ranked by yield)
> [[_Topics]] · [[_TopicQuestionMap]] · [[_PastPapers]] · [[00_Dashboard]]

> Built 2026-07-04 from `Syllabus.txt` (professor's chapter guide) + 5-year past-paper analysis (2020–2024).
> **Primary textbook = Schaum's Outline of Computer Graphics (Xiang & Plastock)** — chapter numbers in `Syllabus.txt` match this book, NOT the Hearn & Baker book. Confirmed by cross-checking: Ch2=Image Representation (Direct Coding/LUT), Ch5 §5.3/5.5=Line Clipping/2D pipeline example, Ch7=Projection math, Ch10 §10.2=Z-Buffer, Ch11=Phong/Shading, Ch12=Ray Tracing — all exact matches.
> Hearn & Baker is used **only** for the 5 no-resource topics the syllabus calls out by page number (Octrees p.359, Quadtree, BST-Tree, Fractal Geometry, B-spline, types of Shading).

---

## Reality check on the syllabus's own hedging
`Syllabus.txt` repeatedly says "cover X only if previous year question covers it." Now that we have all 5 years (2020–2024), here's what that resolves to:

- **Ch5 hedge resolved:** syllabus said "5.3, 5.5 most important, rest depends on PYQ." PYQs show Cohen-Sutherland (line/point clipping, §5.2/5.3) **and** Sutherland-Hodgman/Weiler-Atherton (polygon clipping, §5.4) both appear almost every year. Treat all of Ch5 as TIER 1, not just 5.3/5.5.
- **Ch6/7 hedge resolved:** tilting (Ch6) appears 2/5 years; cavalier/cabinet + perspective-vs-parallel (Ch7) appear 5/5 years. Ch7 is TIER 1, Ch6 is TIER 3.
- **Ch9 conflict — flag for you:** syllabus explicitly says Bezier/B-spline/Hermite curves are important *regardless* of PYQ ("solve problems... exercise and solved questions" — not gated like the rest of Ch9). But **zero** of the last 5 papers asked about them. Given only 2 real learning days before revision lockdown, this is a judgment call: I'm ranking it TIER 5 (last, stretch-goal) unless you tell me otherwise — the professor could be the one who finally asks it this year, but 0/5 is 0/5.
- Ch8 (3D Viewing/Clipping) confirmed **skip** — no PYQ hits in 5 years, syllabus already says skip.

---

## TIER 1 — Every single year, 5/5 (must be cold before revision days)
| Topic | Ch | Source pages |
|---|---|---|
| Cohen-Sutherland region codes + line clipping | 5 (§5.2–5.3) | Schaum's Ch5 |
| Normalization transformation (window→viewport) | 5 (§5.1) | Schaum's Ch5 |
| Rotation — derive matrix + apply | 4 (§4.1–4.2) | Schaum's Ch4 |
| Scaling/magnification about a fixed point | 4 (§4.1–4.2) | Schaum's Ch4 |
| Cavalier/Cabinet projection matrices | 7 (§7.3) | Schaum's Ch7 |
| Perspective vs Parallel projection | 7 (§7.1–7.3) | Schaum's Ch7 |
| Z-Buffer algorithm (trace + max objects) | 10 (§10.2) | Schaum's Ch10 |
| Image crop / sub-image coordinate math | 2 (§2.1–2.2) | Schaum's Ch2 |

## TIER 2 — 4/5 years
| Topic | Ch |
|---|---|
| DDA + Bresenham line algorithms (trace + compare) | 3 |
| Koch curve / fractal generation | 3 (or 9-adjacent) |
| Point-obscures-point visibility via viewpoint | 10 |
| Direct coding + lookup table bit math | 2 |
| Ray–sphere intersection | 12 |
| Sutherland-Hodgman / Weiler-Atherton polygon clipping | 5 (§5.4) |

## TIER 3 — 2–3/5 years
CG vs Image Processing/HCI (Ch1/2) · Antialiasing / slanted-line dimming (Ch3) · Geometric vs Coordinate transformation (Ch4) · RGB scanline color interpolation (Ch11) · Ray vs Vector distinction (Ch12) · Ray equation point-finding (Ch12) · Convex/concave polygon ID (Ch3/5) · Aspect ratio/resize distortion (Ch2) · Midpoint circle + 8-way symmetry (Ch3)

## TIER 4 — 1–2/5 years, know the shape of the answer
Tilting/composite 3D rotation (Ch6) · Monitor color transform matrix M (Ch11) · Isometric/Dimetric/Trimetric (Ch7) · Perspective foreshortening + vanishing point (Ch7) · Phong model (Ch11) · Flood/boundary fill (Ch3) · Point left/right-of-line test (Ch3/5)

## TIER 5 — 2024-only "new" topics (recency risk — could repeat) + syllabus-mandated zero-yield topics
Halftoning + dither matrix (Ch2, 2024) · Circular clipping window (Ch5, 2024) · Trapezoid-primitive polygon fill (no textbook resource, 2024) · Axonometric projection (Ch7, 2024) · 3D scaling application (Ch6, 2023) · Painter's vs Z-buffer (Ch10, 2023) · Perspective anomalies (Ch7, 2023) · Back-face/visible-surface definitions (Ch10, 2024) · **Bezier/B-spline/Hermite curves (Ch9, 0/5 PYQ but syllabus-mandated)** · Octree/Quadtree/BST-tree/Fractal Geometry (Hearn&Baker, no PYQ)

## Confirmed skip
Ch8 — Three-Dimensional Viewing and Clipping (no PYQ hits, syllabus says skip)

---

## Compressed reality: 2 core-learning days, then lockdown
Exam is Wed 8 Jul, 10:30 AM. Per the Weekly Engine, Mon 6 Jul + Tue 7 Jul = pure revision/timed papers only. That leaves **today (Sat 4 Jul) and tomorrow (Sun 5 Jul)** as the only two days to learn anything new. TIER 1+2 (14 topics) is the realistic target for those two days — it covers every question cluster (Q1–Q8) at a "can attempt confidently" level. TIER 3–5 get whatever time is left, in order, and get triaged hard during the Mon/Tue revision pass based on which questions you're weakest on after a timed mock.
