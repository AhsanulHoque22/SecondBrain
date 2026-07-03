# CSE 715 — Computer Graphics · Past-Paper Analysis
> [[_Syllabus]] · [[_Topics]] · [[_TopicQuestionMap]] · [[00_Dashboard]]

## Papers analysed
- 2024 (3 pages, scanned) — `cse715 2024.pdf`
- 2023, 2022, 2021, 2020 (11 pages combined, scanned) — `cg 715 2023_to_2020.pdf`

## Exam structure
- Full marks: 54 (52.5 in 2020/2021) · Duration: 4 hours
- Format: **Answer any 3 from Section A (Q1–4) + any 3 from Section B (Q5–8)** — separate answer scripts for each section
- Each numbered question bundles 2–5 sub-parts (a,b,c…) worth 1–5 marks each, usually all from the same chapter cluster

## Question → chapter cluster (holds across all 5 years)
| Q# | Section | Chapter cluster |
|----|---------|------------------|
| Q1 | A | Ch2 — Image Representation (color models, LUT, direct coding, crop/resize, aspect ratio) |
| Q2 | A | Ch3 — Scan Conversion (DDA, Bresenham, circle, antialiasing, Koch curve, flood/boundary fill) |
| Q3 | A | Ch4 — 2D Transformations (rotation, scaling/magnification) + coordinate systems |
| Q4 | A | Ch5 — Clipping (Cohen-Sutherland, Sutherland-Hodgman/Weiler-Atherton) + convex/concave |
| Q5 | B | Ch7 — Projection (cavalier/cabinet, normalization, homogeneous coords) |
| Q6 | B | Ch10 — Hidden Surfaces (point-obscuring, Z-buffer) + Ch6 tilting |
| Q7 | B | Ch11 — Color/Shading (RGB interpolation, monitor color matrix, Phong) + point left/right test |
| Q8 | B | Ch12 — Ray Tracing (ray-sphere intersection, ray equation, ray vs vector) |

**Implication:** the exam is genuinely full-syllabus, not "pick a favorite quarter." Every chapter cluster shows up as its own question every year. The good news: it's numerical/procedural, not memorization-heavy — once you know the method for each question type, execution is fast repeated practice.

## Pattern table — ranked by 5-year frequency

| Topic | Years appeared | Question type | Marks | Priority |
|---|---|---|---|:---:|
| Cohen-Sutherland region codes + line clipping | 2020 2021 2022 2023 2024 | Compute region codes for given points; clip line(s) | 3–4 | ⭐⭐⭐ |
| Normalization transformation (window→viewport) | 2020 2021 2022 2023 2024 | Derive mapping matrix for given window/viewport corners | 2–3 | ⭐⭐⭐ |
| Rotation — derive matrix + apply (origin or arbitrary point) | 2020 2021 2022 2023 2024 | Derive rotation matrix from geometry; rotate given points/polygon | 2–4 | ⭐⭐⭐ |
| Scaling/Magnification about a fixed point | 2020 2021 2022 2023 2024 | Magnify/reduce polygon keeping a vertex fixed | 2–4 | ⭐⭐⭐ |
| Cavalier/Cabinet (parallel/oblique) projection | 2020 2021 2022 2023 2024 | Find projection matrix for unit cube, given θ | 2.5–4 | ⭐⭐⭐ |
| Perspective vs Parallel projection | 2020 2021 2022 2023 2024 | Differentiate; who uses which (architects/engineers) | 1–4 | ⭐⭐⭐ |
| Z-Buffer algorithm | 2020 2021 2022 2023 2024 | Max objects representable; trace 2×2 pixel display, determine visible color | 4.5–4.75 | ⭐⭐⭐ |
| Image crop / sub-image coordinates | 2020 2021 2022 2023 2024 | Center-crop or corner-crop coordinates given two image sizes | 1.5–3 | ⭐⭐⭐ |
| DDA + Bresenham line algorithms | 2020 2021 2023 2024 | Trace raster locations step by step; explain why Bresenham is faster/exact | 3–4 | ⭐⭐ |
| Koch curve / fractal generation | 2020 2021 2022 2023 | Draw next generation from given rule | 1 | ⭐⭐ |
| Point-obscures-point (visibility via viewpoint) | 2020 2021 2022 2023 | Given 3 points + viewpoint, determine occlusion order | 3 | ⭐⭐ |
| Direct coding + lookup table bit math | 2020 2021 2022 2024 | Bits per pixel ↔ number of colors ↔ table size | 1–2 | ⭐⭐ |
| Ray–sphere intersection | 2020 2021 2022 2023 | Given ray + sphere(s), determine intersection | 3.5–3.75 | ⭐⭐ |
| Sutherland-Hodgman / Weiler-Atherton polygon clipping | 2021 2022 2023 2024 | Clip polygon against window edge-by-edge (2024 upgraded to Weiler-Atherton) | 3–4 | ⭐⭐ |
| CG vs Image Processing / HCI | 2020 2021 2022 2023 | Short distinguishing answer | 1–3 | ⭐⭐ |
| Antialiasing / why slanted lines look dimmer | 2021 2022 2023 | Explain + how to fix | 1.5–2 | ⭐⭐ |
| Geometric vs Coordinate transformation | 2020 2021 2022 | Distinguish the two | 1–3.5 | ⭐ |
| RGB color interpolation along a scanline | 2020 2021 2022 | Given colors at two points on a line, find color at third point | 1.75–2.5 | ⭐ |
| Ray vs Vector distinction | 2020 2021 2022 | "Show a ray is not a vector" / difference | 1 | ⭐ |
| Ray equation r(t)=s+td — point finding | 2020 2021 2022 | Plug in t values, get coordinates | 2.5–3 | ⭐ |
| Convex/concave polygon identification | 2020 2021 2022 | Identify + justify from given shapes | 1.5–2 | ⭐ |
| Aspect ratio / resize distortion | 2020 2021 2022 2023 | Compute resized dimensions; geometric distortion check | 1–2 | ⭐ |
| Midpoint circle algorithm + 8-way symmetry | 2020 2022 2023 | Raster locations for given radius/center; explain symmetry | 1.5–4 | ⭐ |
| Tilting (3D composite rotation, x then y) | 2021 2022 | Derive tilting matrix; does order matter? | 3–3.5 | low |
| Monitor color transformation matrix M | 2021 2023 | Given chromaticity + white point, find M | 3 | low |
| Isometric/Dimetric/Trimetric projection | 2020 2023 | Draw/differentiate | 2.25–4 | low |
| Perspective foreshortening + vanishing point | 2020 2021 | Explain with diagram | 1.75–2 | low |
| Phong illumination model | 2022 2023 | Explain diagram / diffuse+specular significance | 1.5–3 | low |
| Flood-fill / boundary-fill (8-connected) | 2020 2023 | Fill given shape, justify | 2.5–3 | low |
| Halftoning + dither matrix (2×2→4×4 recurrence) | 2024 | Explain halftone pattern; construct D₄ from D₂ | 2–3 | ⚠️ new 2024 |
| Circular clipping window | 2024 | Inside/outside/intersecting test + clip | 3 | ⚠️ new 2024 |
| Trapezoid-primitive polygon fill + vertex/edge/surface matrices | 2024 | Steps of trapezoid fill; count trapezoids; list matrices | 1–2 each | ⚠️ new 2024, no textbook resource |
| Axonometric projection significance | 2024 | Short explain | 2 | ⚠️ new 2024 |
| 3D scaling application | 2023 | Apply scale params to 3D points | 4 | rare |
| Painter's algorithm vs Z-buffer | 2023 | Differentiate | 2 | rare |
| Perspective projection anomalies (4) | 2023 | List + explain | 4 | rare |
| Orthographic vs Oblique projection | 2023 | Differentiate | 1 | rare |
| Back-face / visible-surface definition | 2024 | Define with example | 2 | rare |
| Color gamut of a monitor | 2022 | Explain | 1 | rare |
| Point left/right-of-line test | 2021 2022 | C=(x2-x1)(y-y1)-(y2-y1)(x-x1) — interpret sign | 1 | rare, quick to learn |
| Bezier / B-spline / Hermite curves | **0/5 — never appeared** | — | — | ⚠️ **syllabus mandates it anyway (Ch9), 5-year PYQ record says otherwise — see [[_Syllabus]] note** |

## Key repeating setups (memorise the method, not the numbers — numbers change every year)
- **Region-code clipping:** always 4-bit TOP/BOTTOM/RIGHT/LEFT vs a rectangular window — practice the bitwise AND/OR logic, not specific coordinates.
- **Cavalier (θ, tan α=1) / Cabinet (θ, tan α=0.5) projection matrix** for a unit cube — same derivation every year, only θ changes.
- **Z-buffer 2×2 trace:** always given a small cube/box figure with 2 objects (A, B) and a back-clipping plane — walk pixel-by-pixel comparing depth.
- **Ray r(t) = s + td:** always asks to plug in several t values, or intersect with a sphere via the quadratic in t.
