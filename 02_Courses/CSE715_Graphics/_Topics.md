# CSE 715 — Computer Graphics · Topic Tracker
> [[_Syllabus]] · [[_TopicQuestionMap]] · [[00_Dashboard]] · [[01_Master_Plan]]

Status: 🔲 not started · 📖 learning · 🔁 needs recall · ✅ can explain it cold

| Topic | Status | Conf | Last Reviewed | Next Recall | Yield | Notes / weak spots |
|-------|:------:|:----:|:-------------:|:-----------:|:-----:|--------------------|
| Cohen-Sutherland region codes + line clipping | 🔲 | — | — | — | 5/5 · 3–4 marks | 4-bit TOP/BOTTOM/RIGHT/LEFT vs rectangle window |
| Normalization transformation (window→viewport) | 🔲 | — | — | — | 5/5 · 2–3 marks | Derive from window/viewport corners |
| Rotation — derive matrix + apply | 🔲 | — | — | — | 5/5 · 2–4 marks | Origin AND arbitrary-point variants both asked |
| Scaling/magnification about a fixed point | 🔲 | — | — | — | 5/5 · 2–4 marks | Keep a named vertex fixed |
| Cavalier/Cabinet projection matrices | 🔲 | — | — | — | 5/5 · 2.5–4 marks | tan α=1 (cavalier) vs tan α=0.5 (cabinet); θ varies |
| Perspective vs Parallel projection | 🔲 | — | — | — | 5/5 · 1–4 marks | Who uses which (architects/engineers) |
| Z-Buffer algorithm | 🔲 | — | — | — | 5/5 · 4.5–4.75 marks | Max objects representable + 2×2 pixel trace |
| Image crop / sub-image coordinates | 📖 | — | 2026-07-04 | — | 5/5 · 1.5–3 marks | Center-crop AND corner-crop variants. Question analysis + [[Chapter2_Solutions.pdf]] done — all 5 years solved. Needs active recall to reach ✅. |
| ↳ RGB/CMY color model + subtractive color + perceptual terms | 📖 | — | 2026-07-04 | — | 3/5 · 1–3 marks | RGB↔CMY conversion formula; why printers use K (black) ink; Hue/Saturation/Brightness↔wavelength/purity/intensity. Solved in [[Chapter2_Solutions.pdf]]. |
| ↳ Image file format (header/data, RLE compression) | 🔲 | — | — | — | 0/5 PYQ | Schaum's §2.6 — no past-paper hit, low priority |
| ↳ Pixel color-attribute pseudocode (setPixel/getPixel/LUT ops) | 🔲 | — | — | — | 0/5 PYQ | Schaum's §2.7, many textbook solved-problems (2.31–2.36) but never asked 2020–24 |
| ↳ Mandelbrot/Julia set visualization | 🔲 | — | — | — | 0/5 PYQ | Schaum's §2.8 — complex-number based, no PYQ signal, lowest priority in Ch2 |
| DDA + Bresenham line algorithms | 📖 | — | 2026-07-04 | — | 4/5 · 3–4 marks | Trace raster locations; explain why Bresenham wins. Verified against raw papers — 2024 is actually Q3(c) not Q1(c). Solved in [[Chapter3_Solutions.pdf]]. |
| Koch curve / fractal generation | 📖 | — | 2026-07-04 | — | 4/5 · 1–1.5 marks | Draw next generation from stated rule — 2 variants: square-bump (×5 segs/edge) and classic triangular (×4 segs/edge). Solved in [[Chapter3_Solutions.pdf]]. |
| Point-obscures-point visibility via viewpoint | 🔲 | — | — | — | 4/5 · 3 marks | Given 3 points + viewpoint, order by occlusion |
| Direct coding + lookup table bit math | 📖 | — | 2026-07-04 | — | 4/5 · 1–2 marks | bits↔colors↔table-size arithmetic. Solved in [[Chapter2_Solutions.pdf]]. |
| Ray–sphere intersection | 🔲 | — | — | — | 4/5 · 3.5–3.75 marks | Quadratic in t; may involve 2 spheres |
| Sutherland-Hodgman / Weiler-Atherton polygon clipping | 🔲 | — | — | — | 4/5 · 3–4 marks | 2024 upgraded to Weiler-Atherton — learn both |
| CG vs Image Processing/HCI | 📖 | — | 2026-07-04 | — | 4/5 · 1–3 marks | Short distinguishing answer. Solved in [[Chapter2_Solutions.pdf]]. |
| Antialiasing / slanted-line dimming | 📖 | — | 2026-07-04 | — | 3/5 · 1–2 marks | Explain cause (√2 vs 1 unit pixel spacing) + fix (area/super-sampling). Solved in [[Chapter3_Solutions.pdf]]. |
| Geometric vs Coordinate transformation | 🔲 | — | — | — | 3/5 · 1–3.5 marks | Definitional distinction |
| RGB scanline color interpolation | 🔲 | — | — | — | 3/5 · 1.75–2.5 marks | Linear interpolation given colors at 2 points on a line |
| Ray vs Vector distinction | 🔲 | — | — | — | 3/5 · 1 mark | "Show a ray is not a vector" |
| Ray equation r(t)=s+td point-finding | 🔲 | — | — | — | 3/5 · 2.5–3 marks | Plug in t values |
| Convex/concave polygon identification | 🔲 | — | — | — | 3/5 · 1.5–2 marks | Justify from shape |
| Aspect ratio / resize distortion | 📖 | — | 2026-07-04 | — | 4/5 · 1–2 marks | Compute resized dims; geometric distortion check. Solved in [[Chapter2_Solutions.pdf]]. |
| Midpoint circle algorithm + 8-way symmetry | 📖 | — | 2026-07-04 | — | 3/5 · 1.5–4 marks | Raster locations for given radius/center — full octant-trace method verified. Solved in [[Chapter3_Solutions.pdf]]. |
| Tilting (3D composite rotation, x then y) | 🔲 | — | — | — | 2/5 · 3–3.5 marks | Derive matrix; does order matter? |
| Monitor color transformation matrix M | 🔲 | — | — | — | 2/5 · 3 marks | Given chromaticity + white point (D65) |
| Isometric/Dimetric/Trimetric projection | 🔲 | — | — | — | 2/5 · 2.25–4 marks | Draw/differentiate |
| Perspective foreshortening + vanishing point | 🔲 | — | — | — | 2/5 · 1.75–2 marks | Explain with diagram |
| Phong illumination model | 🔲 | — | — | — | 2/5 · 1.5–3 marks | Diffuse + specular significance |
| Flood-fill / boundary-fill (8-connected) | 📖 | — | 2026-07-04 | — | 2/5 · 2.5–3 marks | Justify fill on given shape — key trap: same connectivity for boundary+fill leaks on diagonal edges. Solved in [[Chapter3_Solutions.pdf]]. |
| ↳ Scan-line polygon fill algorithm (edge list) | 🔲 | — | — | — | 0/5 PYQ | Schaum's §3.7 — geometric (vertex-based) fill, no past-paper hit, theory only |
| Point left/right-of-line test | 🔲 | — | — | — | 2/5 · 1 mark | C=(x2-x1)(y-y1)-(y2-y1)(x-x1), interpret sign |
| Halftoning + dither matrix (D2→D4) | 📖 | — | 2026-07-04 | — | 1/5 · 2–3 marks | 2024 only, recurrence relation given in-paper. Solved in [[Chapter2_Solutions.pdf]] (Bayer matrix result). |
| Circular clipping window | 🔲 | — | — | — | 1/5 · 3 marks | Inside/outside/intersecting + clip |
| Trapezoid-primitive polygon fill | 🔲 | — | — | — | 1/5 · 1–2 marks each | No textbook resource — 2024 lecture-only topic |
| Axonometric projection significance | 🔲 | — | — | — | 1/5 · 2 marks | Short explain |
| 3D scaling application | 🔲 | — | — | — | 1/5 · 4 marks | Apply given scale params to 3D points |
| Painter's algorithm vs Z-buffer | 🔲 | — | — | — | 1/5 · 2 marks | Differentiate |
| Perspective projection anomalies (4) | 🔲 | — | — | — | 1/5 · 4 marks | List + explain |
| Orthographic vs Oblique projection | 🔲 | — | — | — | 1/5 · 1 mark | Differentiate |
| Back-face / visible-surface definitions | 🔲 | — | — | — | 1/5 · 2 marks | Define with example |
| Color gamut of a monitor | 🔲 | — | — | — | 1/5 · 1 mark | Short explain |
| Bezier / B-spline / Hermite curves | 🔲 | — | — | — | 0/5 PYQ, syllabus-mandated | See [[_Syllabus]] conflict note — deprioritized to last given time crunch |
| Octree/Quadtree/BST-tree/Fractal Geometry (Hearn&Baker) | 🔲 | — | — | — | 0/5 PYQ, syllabus-mandated | p.359 Octrees + named pages; no-PYQ, deprioritized |

## Column guide
- **Conf** — confidence 1–5 (1=shaky, 5=bulletproof). Update after every recall pass.
- **Last Reviewed** — date you last marked ✅ or completed a 🔁 pass (YYYY-MM-DD). Claude writes this.
- **Next Recall** — auto-computed by spaced_rep.py. Claude writes this after each update.

## Status rules
- ✅ only when you can explain it cold without notes AND solve a past-paper question on it.
- Re-reading ≠ ✅.
- High Yield + 🔲 status = today's target.
