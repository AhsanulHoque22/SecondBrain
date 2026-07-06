# CSE 715 — Computer Graphics · Topic → Question Map
> [[_Topics]] · [[_Syllabus]] · [[_PastPapers]]
> Read only when starting a block for a specific topic (per session protocol — not at session start).

## TIER 1

**Cohen-Sutherland region codes + line clipping** — ✅ verified against raw scanned papers 2026-07-05, full solutions in [[Chapter5_Solutions.pdf]]
- 2024 Q5b — window Xmin=10,Xmax=30,Ymin=10,Ymax=25; region codes for P1(5,5),P2(20,30),P3(35,15),P4(15,8),P5(12,20); A(5,5)-B(12,20) requires clipping → visible portion (10,15.71)-(12,20)
- 2023 Q8a — clip (5,5)-(15,10) in window Xmin=0,Ymin=0,Xmax=10,Ymax=10 → clipped to (5,5)-(10,7.5)
- 2022 Q4a — region codes A(6,2),B(3,8),C(-1,2),D(2,4) vs window Xmin=2,Xmax=5,Ymin=1,Ymax=9; clip AB→(5,4)-(3,8); CD clips to single point D (line grazes boundary exactly at D)
- 2021 Q4a — region codes M(8,11),N(16,7),P(6,8),Q(3,5) vs window from A(4,4),B(14,4),C(14,10),D(4,10) i.e. Xmin=4,Xmax=14,Ymin=4,Ymax=10; clip MN→(10,10)-(14,8); PQ→(4,6)-(6,8)
- 2020 Q6b — region codes A(6,2),B(3,8),C(-1,2),D(2,4) vs window Xmin=1,Xmax=5,Ymin=1,Ymax=7; clip AB→(5,4)-(3.5,7); CD→(1,3.33)-(2,4)

**Normalization transformation (window→viewport)** — ✅ verified against raw scanned papers 2026-07-05, full solutions in [[Chapter5_Solutions.pdf]]. **Correction:** previous entry had 2021/2022 swapped — re-verified directly against the scans.
- 2024 Q5a — window(1,1)-(3,5) → (i) full NDC (ii) viewport with corner (vx,vy)
- 2022 Q4c — window (scan partly illegible, read as (1,1)-(3,4)), preserve aspect ratio → NDC (only variant with no explicit viewport given)
- 2021 Q7d — window(1,1)-(2,2) → viewport(0,0)-(1/2,1/2) *(topic map previously said "2022 Q4c" — wrong; this exact question is 2021 Q7d)*
- 2020 Q5a,b — workstation transform (NDC→device 0-199,0-639); window(1,1)-(2,2)→viewport(0,0)-(1/2,1/2) *(identical numbers to 2021 Q7d, different year)*

**Rotation — derive matrix + apply** — ✅ verified against raw scanned papers 2026-07-04, full solutions in [[Chapter4_Solutions.pdf]]
- 2024 Q4b — derive CCW rotation matrix from geometry (P(x,y)→P'(x',y'))
- 2023 Q3b — rotate P(-1,2),Q(4,4),R(1,-4) 45° about origin and about Q(4,4)
- 2022 **Q3c** — 45° rotation of A(5,6),B(2,1),C(5,3) about origin and (2,3) *(topic map previously said "Q3c-equivalent" — confirmed exact: Q3c)*
- 2021 Q3c — 60° rotation of rectangle A(1,1),B(1,2),C(2,2),D(2,1) about E(-1,-1)
- 2020 Q4a — 90° rotation of rectangle A(1,1),B(1,2),C(2,2),D(2,1) about B(-1,-1)

**Scaling/magnification about a fixed point** — ✅ verified 2026-07-04, full solutions in [[Chapter4_Solutions.pdf]]
- 2023 Q3c — scale 3D object A,B,C,D by (3,2,3) on X,Y,Z (also 3D scaling, Tier 5 — answered in both places)
- 2022 **Q3b — previously MISSING from this map.** Magnify triangle P(-1,2),Q(2,4),R(0,0) keeping Q(2,4) fixed: (i) ×3 (ii) ×0.5
- 2021 Q3b — magnify pentagon ARTHE ×2 keeping E(1,6) fixed
- 2020 Q4b — magnify triangle A,B,C ×2 keeping B(2,1) fixed

**Coordinate-system rationale (device-independent/NDC)** — new subtopic split out 2026-07-04, solved in [[Chapter4_Solutions.pdf]]
- 2023 Q3a — "monitor sizes vary — what coordinate system is required and why?" [1]
- 2022 Q3a — identical question [1]
- 2020 Q6a — identical question, bundled with Group-B Q6 (Cohen-Sutherland region codes) instead of the Q3/Q4 transformation cluster [~1]
- 2021 — **not asked this year**

**2D transform extras (2024-only): translation, shear, composite-rotation steps, figure ID** — new subtopic split out 2026-07-04, solved in [[Chapter4_Solutions.pdf]]
- 2024 Q4a [2] — given shape (a) and 4 transformed variants (b)-(e), name the transformation used for each
- 2024 Q4c [2] — translate segment P1(1,2)-P2(3,3) by (-1,-2)
- 2024 Q4d [2] — steps needed to rotate an arbitrary line about a point P1 (translate-rotate-translate-back recipe)
- 2024 Q4e [1] — write the 2D shear transformation matrices

**Cavalier/Cabinet projection matrices** — ✅ verified against raw scanned papers 2026-07-05, full solutions in [[Chapter7_Solutions.pdf]]. **Correction:** 2020 has NO such question (previously wrongly assumed 5/5); 2024 only has qualitative "properties of Cabinet" (Q6d, no θ/matrix).
- 2023 Q5a — cavalier θ=60° → Par=(1,0,1/2,0;0,1,√3/2,0;...); cabinet θ=45° → (1,0,√2/4,0;0,1,√2/4,0;...)
- 2022 Q5b — cavalier θ=30° → (1,0,√3/2,0;0,1,1/2,0;...); cabinet θ=45° → same as 2023's cabinet
- 2021 Q5b — cavalier θ=45° → (1,0,√2/2,0;0,1,√2/2,0;...); cabinet θ=30° → (1,0,√3/4,0;0,1,1/4,0;...)
- 2024 Q6d — qualitative "properties of Cabinet projection" only [1 mark], no matrix/θ given

**Perspective vs Parallel projection** — ✅ verified against raw scanned papers 2026-07-05, full solutions in [[Chapter7_Solutions.pdf]]. **Correction:** previous entries wrongly numbered 2021/2022 as "Q6b" with wrong content (2022's real Q6b is "why are hidden surface algorithms needed", a Ch10 question) — the actual perspective/parallel question both years is **Q5a**.
- 2023 — no exact-phrasing match; has Q4b orthographic-vs-oblique [1] and Q1f "projection for photographing university" [~1] instead
- 2022 Q5a — differentiate perspective/parallel; who uses which [1]
- 2021 Q5a — distinguish perspective/parallel; who uses which [1.5]
- 2020 Q8a — distinguish; who uses which (architects/engineers) [3]

**Z-Buffer algorithm** — ✅ verified against raw scanned papers 2026-07-06, full solutions in [[ZBuffer_Solutions.pdf]]. **Correction:** 2020 has no Z-buffer question at all (that year's Ch10 content is only "point-obscures-point via viewpoint," Q8c, tracked separately); full numeric trace is 2021/2022 only.
- 2024 Q7d — illustrate Z-buffer, advantages/disadvantages [2]
- 2023 Q7d — differentiate Painter's algorithm vs Z-buffer [2] (lighter touch, no numeric trace)
- 2022 Q6c — max objects representable (answer: unlimited/arbitrary — memory is per-pixel not per-object); 2×2 pixel trace for objects A,B [4.5]
- 2021 Q6d — same structure, different geometry [4.75] *(topic map previously said "Q6c" — actual letter is Q6d, confirmed against scan)*
- 2020 — none (see correction above)

**Image crop / sub-image coordinates** — ✅ verified against full source text 2026-07-04
- 2024 Q2b — crop 128×128 from center of 512×512 → upper-left corner = ((512-128)/2, (512-128)/2) = (192,192)
- 2023 Q1b — crop 786×660 from center of 1200×1200 → lower-left = (207,270), upper-right = (993,930)
- 2021 Q1e — crop 700×700 from center of 900×800 → lower-left = (100,50), upper-right = (800,750)
- 2020 Q2c — crop 700×700 from center of 900×800 (same as 2021 Q1e — recurring exact setup)

**Aspect ratio / resize distortion** — ✅ verified, merged with image-crop cluster (same Q1)
- 2022 Q1b — resize 1680×1050 → 1024 wide, same AR → height = 1024×1050/1680 = 640
- 2022 Q1e — 5×3.5in image at 3.5×4in, no distortion? AR 5/3.5=1.4286 vs 3.5/4=0.875 → distortion occurs, answer NO
- 2021 Q1d — resize 1024×675 onto 800×527 and 1800×1100 devices → AR 1024/675=1.517 vs 800/527=1.518 (negligible, ~no distortion) vs 1800/1100=1.636 (noticeably distorted)
- 2020 Q1b — 5×3.5in at 3.5×4in, same check as 2022 Q1e → distortion occurs
- 2020 Q1d — height=2in, AR=1.5 → width = 1.5×2 = 3in

## TIER 2

**DDA + Bresenham line algorithms** — ✅ verified against raw scanned papers 2026-07-04, full solutions in [[Chapter3_Solutions.pdf]]
- 2024 **Q3(c)** — DDA and Bresenham trace (2,3)→(10,7); do they choose same pixel? **(No — m=0.5 is an exact tie every other step, and DDA/Bresenham break the tie oppositely.)** *(topic map previously said "Q1c" — wrong; Q1 in 2024 is generic Ch1 concepts, the line-trace question is Q3(c).)*
- 2023 Q1(c) — how Bresenham overcomes DDA limitations (1 mark, conceptual only, no trace)
- 2021 Q2(a) — line (1,1)→(10,7): basic-algorithm raster locations, why slower, Bresenham explanation, Bresenham raster locations (6 marks total, 4 sub-parts)
- 2020 Q3(b),(c) — DDA (1,1)→(5,8) [3.75]; Bresenham (0,0)→(8,5) [4]
- 2022 — **not asked this year** (2022's Q2 cluster is circle/antialiasing/Koch only, no line-trace question)

**Koch curve / fractal generation** — ✅ verified 2026-07-04, full solutions in [[Chapter3_Solutions.pdf]]
- 2023 **Q2(d)** — square-bump (quadratic Koch) variant, draw 3rd generation from given gen1/gen2 (25 segments)
- 2022 **Q2(d)** — classic triangular-bump Koch, triangle→star shown, draw 3rd generation (48 segments, Koch snowflake iteration 2)
- 2021 **Q1(f)** — Quadratic Koch curve (square bump), draw generation 2 (same construction as 2023 Q2d, just numbered one generation lower)
- 2020 — **not asked this year** (no Koch curve question found in the 2020 paper)

**Point-obscures-point visibility via viewpoint**
- 2023 Q6a — A(5,1,-2),B(10,4,9),C(15,-2,-3), V(0,1,-10)
- 2022 Q6a — A(1,5,-2),B(1,4,9),C(-2,-2,-3), V(0,1,-10)
- 2021 Q6a — P1(1,3,1),P2(3,6,-11),P3(2,6,-5), C(0,0,7)
- 2020 Q8c — P1(1,2,0),P2(3,6,20),P3(2,4,10), C(0,0,-10)

**Direct coding + lookup table bit math** — ✅ verified against full source text 2026-07-04
- 2024 Q2c — 10-bit grayscale pixel values in LUT → entries required = 2¹⁰ = 1024
- 2022 Q1c — 2-byte pixel in LUT → bits occupied = 2¹⁶×24 = 1,572,864 bits (196,608 bytes)
- 2022 Q1d — direct coding CMY: 3 bits cyan, 3 bits magenta, 4 bits yellow → colors = 2³×2³×2⁴ = 1024
- 2021 Q1b — 2-byte pixel in 24-bit LUT → bits occupied = 2¹⁶×24 = 1,572,864 bits
- 2021 Q1c — direct coding RGB, 12 bits/primary → colors = 2¹²×2¹²×2¹² = 2³⁶ = 68,719,476,736
- 2020 Q2b — direct coding RGB, 10 bits/primary → colors = 2¹⁰×2¹⁰×2¹⁰ = 1,073,741,824

**RGB/CMY color model + subtractive color + perceptual terms** — new subtopic, split out from Direct Coding 2026-07-04
- 2024 Q2a — color model concept: why RGB (additive/display) and CMY (subtractive/print) both used
- 2023 Q1g — name 3 perceptual color terms + physical properties (Hue↔wavelength, Saturation↔purity, Brightness↔intensity)
- 2022 Q1f — why color printers use subtractive model (pigments absorb/reflect light vs. displays emit light)
- 2020 Q2a — define subtractive color model + example; why color printers use separate black (K) ink (cost + hard to mix true black from CMY)

**Ray–sphere intersection** — ✅ re-verified against all 5 raw scans 2026-07-07, solved in [[Chapter12_Solutions.pdf]]. **Correction:** 2020 has zero ray-tracing content of any kind (its Q7/Q8 are point left/right, polygon orientation, 3D rotation, projections, and point-obscures-viewpoint — no ray equation, no ray-sphere). Real years: 2021, 2022, 2023 only (3/5, not 4/5).
- 2023 Q8c [3.5] — S1 r=8 at (2,4,1), S2 r=10 at (10,-2,-5); ray s=2I+5K, d=I-2J — intersects S1 once (originates inside, t≈1.393), misses S2 (discriminant <0)
- 2022 Q8d [4] — sphere r=2 at origin; ray from (3,0,0) dir (-3,1,0) — two intersections, t≈0.343 and t≈1.457
- 2021 Q8e [3.75] — S1 r=8 at (2,4,1), S2 r=10 at (10,-2,-5); ray s=2J+5K, d=I-2K — this is Schaum's own worked example (Solved Prob. 12.15): ray starts inside S1, enters S2 before exiting S1, then exits S2 (spheres overlap)

**Sutherland-Hodgman / Weiler-Atherton polygon clipping** — ✅ verified 2026-07-05, full solutions in [[Chapter5_Solutions.pdf]]
- 2024 Q6a — Weiler-Atherton: window ABCD=(1,1),(5,1),(5,4),(1,4) vs triangle P(2,2),Q(4,2),R(3,5) — exit E1(10/3,4), entry E2(8/3,4); clipped CCW: P,Q,E1,E2
- 2023 Q4a — Sutherland-Hodgman: A(1,1),B(4,1),C(4,4),D(1,4) vs window W(2,2),X(3,2),Y(3,3),Z(2,3) — fully numeric, clipped result = the window itself (2,3),(2,2),(3,2),(3,3)
- 2022 Q4b — SH clipping steps, given polygon figure P1-P8 (no coordinates in paper — figure/method-only answer)
- 2021 Q4b — SH clipping abcdefghijkl vs MNOP, order: left PM, bottom PO (no coordinates in paper — figure/method-only answer)

## TIER 3 (brief refs — lower priority, drill only after Tier 1–2 solid)
- **CG vs Image Processing/HCI:** 2023 Q1a — differentiate CG from image processing (1 mark); 2022 Q1a — CG vs image processing/HCI (both distinctions); 2021 Q1a — how does image processing differ from CG; 2020 Q1a — which discipline describes producing/synthesizing digital images (justify: CG = object definition → image; image processing = image → image, pixel-based)
- **Antialiasing/slanted lines:** ✅ verified 2026-07-04, solved in [[Chapter3_Solutions.pdf]] — 2023 Q2(a) why dimmer only [1]; 2022 Q2(c) why dimmer + how to fix [2]; 2021 Q2(b) "3 adverse effects" + lowpass-filter kernel application [2.75, bundled with the line-trace question]
- **Geometric vs Coordinate transform:** ✅ verified 2026-07-04, solved in [[Chapter4_Solutions.pdf]] — 2021 Q3a [1.25]; 2020 Q5d [~1] *(2022's occurrence was mis-attributed to Q3a — that question is actually the separate Coordinate-system-rationale question above; 2022 does not ask Geometric vs Coordinate transformation)*
- **RGB scanline interpolation:** ✅ re-verified against raw scans 2026-07-07, solved in [[Chapter11_Solutions.pdf]] — **corrected:** 2021 Q7c (P1 line6 RGB(1,1,0), P2 line15 RGB(0.6,0.5,0.2), find line8 [2]); 2022 Q7d (P1 line13 RGB(0.4,5,0), P2 line15 RGB(2,0.5,7), find line12 [2.5]); 2023 Q7c (P1 line3 RGB(5,5,0), P2 line9 RGB(2,0.5,7), find line5 [2]). No 2020 occurrence found (previous "2020 Q7d-equiv 2021 paper" note was garbled/wrong).
- **Ray vs Vector:** ✅ re-verified against raw scans 2026-07-07, solved in [[Chapter12_Solutions.pdf]] — **corrected:** 2021 Q8c [1] "difference between vector and ray", 2022 Q8a [1] "show that a ray is not a vector", 2024 Q8c [2] "distinguish between ray and vector" (previous "2020" attribution was wrong — 2020 has no ray content; 2023 doesn't ask this either)
- **Ray equation point-finding:** ✅ re-verified 2026-07-07, solved in [[Chapter12_Solutions.pdf]] — 2021 Q8b [2.5] (s=2I+J-3K,d=I+2K, t=0,1,7,4,3), 2022 Q8c [3] (s=2I-3J-7K,d=I-J-2K, t=1,2,-4,3,7). No 2020 occurrence.
- **Ray tracing integrates hidden-surface+projection:** 2021 Q8a [1.5] "describe how", 2022 Q7c-related [3, bundled with homogeneous-coordinates question], 2024 Q8b [2] "why Ray Tracing is efficient" — solved in [[Chapter12_Solutions.pdf]]
- **Point/plane same-side test (3D):** 2024 Q8d [2+2] — plane 5x-3y+6z=7, find normal + test if P1(1,4,2)/P2(-5,-1,3) same side — solved in [[Chapter12_Solutions.pdf]]
- **Convex/concave polygon ID:** ✅ verified 2026-07-05, solved in [[Chapter5_Solutions.pdf]] — 2020 Q6c (4 shapes incl. pentagon), 2021 Q4c (3 shapes), 2022 Q7b (draw example diagram, 1 mark) — lives in the Ch5-Clipping cluster, not Ch3
- **Midpoint circle + 8-way symmetry:** ✅ verified 2026-07-04, solved in [[Chapter3_Solutions.pdf]] — 2023 Q2(b) r=10 center-origin, 3rd-quadrant points [4]; 2022 Q2(a) 8-way symmetry explain [1.5] + Q2(b) r=10 center(50,50) [4]; 2020 Q4(c) show 8-way symmetry [1]

## TIER 4 (one appearance each — learn the method fast, don't over-invest)
Tilting: ✅ verified 2026-07-05, solved in [[Chapter6_Solutions.pdf]] — **2022 Q5c only** (3.5 marks: "Define tilting as a rotation about the x-axis followed by a rotation about the y-axis. Find the tilting matrix; does order matter?"). *(Previous entry said "2022 (Q3c-equiv), 2021 Q5c/6c-area" — wrong; re-read all pages of the 2021 paper directly and confirmed no tilting question exists that year. Corrected to 1/5, not 2/5.)* · Monitor matrix M: ✅ re-verified 2026-07-07, solved in [[Chapter11_Solutions.pdf]] — **corrected:** 2021 Q7a (D65 xw=0.313,yw=0.329,Yw=1.0, phosphors R(0.62,0.34)/G(0.29,0.59)/B(0.15,0.06) [3]), 2023 Q7b (xw=0.3,yw=0.2,Yw=1.0, same phosphor coords [3]) — previous note had years right but no detail · Isometric/Dimetric/Trimetric: ✅ verified 2026-07-05, solved in [[Chapter7_Solutions.pdf]] — 2023 Q1i (differentiate), 2020 Q8b (draw diagrams) · Foreshortening/vanishing point: ✅ verified 2026-07-05, solved in [[Chapter7_Solutions.pdf]] — 2021 Q5c, 2020 Q6d · Phong model: ✅ re-verified against raw scans 2026-07-07, solved in [[Chapter11_Solutions.pdf]] — **correction:** 2022 is Q7e "enumerate significance of diffuse/specular reflection" [1.5] (previous note said Q6d — wrong, re-checked full raw page); 2023 is Q6d "explain the L/N/R/V Phong diagram" [3] · **Flood/boundary fill: 2023 Q2(c) hexagon [3], 2020 Q2(d) arrow [2.5] — ✅ verified 2026-07-04, solved in [[Chapter3_Solutions.pdf]] (both are "will 8-connected fill leak on diagonal edges" reasoning questions)** · Point left/right test: ✅ re-verified 2026-07-07, solved in [[Chapter11_Solutions.pdf]] — 2020 Q7a [2.25] "show the conditions to identify whether a point locates right or left side of a line segment", 2022 Q7a [1] "C=(x2-x1)(y-y1)-(y2-y1)(x-x1), what are the conditions" — lives in Q7/Ch11 cluster, not Ch3

## TIER 5 (2024-only or syllabus-mandated zero-yield)
Halftoning+dither: 2024 Q2d, Q3a,b · Circular clipping: 2024 Q5c — answered as Related bundle in [[Chapter5_Solutions.pdf]] (center (10,10) r=6, chord intersects circle at ≈(4.04,10.73) and ≈(7.64,15.51)) · Trapezoid fill: 2024 Q7b,c,e · Axonometric: 2024 Q6c — ✅ verified 2026-07-05, solved in [[Chapter7_Solutions.pdf]] (plus Q6d cabinet properties [1], Q8a orthographic top/front/side multiview [3], bundled in same doc) · 3D scaling: 2023 Q3c — A(3,0,3),B(3,3,6),C(3,0,1),D(0,0,0) scaled (3,2,3) on X,Y,Z → A'(9,0,9),B'(9,6,18),C'(9,0,3),D'(0,0,0); solved in [[Chapter4_Solutions.pdf]] and [[Chapter6_Solutions.pdf]] · Painter's vs Z-buffer: 2023 Q7d · Perspective anomalies: 2023 Q4c — ✅ verified 2026-07-05, solved in [[Chapter7_Solutions.pdf]] (foreshortening, vanishing points, view confusion, topological distortion) · Orthographic vs Oblique: 2023 Q4b — ✅ verified 2026-07-05, solved in [[Chapter7_Solutions.pdf]] · Back-face/visible surface: 2024 Q1c, Q7a · Color gamut: 2022 Q8b "explain the color Gamut of the monitor" [1] — solved in [[Chapter11_Solutions.pdf]] · **Bezier/B-spline/Hermite: no PYQ hit 2020–2024 (re-confirmed 2026-07-06)** — syllabus-mandated theory + solved exercises (no past-paper questions to solve) in [[Chapter9_Solutions.pdf]]

## Note on accuracy
This map was built from scanned/handwritten past papers read in one pass — Tier 3–5 year attributions may have minor mix-ups between adjacent years since several questions repeat near-identically. Re-verify the specific year during block study if it matters for your prep; the topic identification itself is solid.

**Chapter 3 (Scan Conversion) cluster fully re-verified against the raw scanned papers on 2026-07-04** during question-analysis — see [[Chapter3_Solutions.pdf]]. Key corrections: the exact question number for this cluster **shifts every year** (Q2 in 2022/2023, Q1+Q2 split in 2021, Q2+Q3+Q4 split in 2020, Q3 only in 2024) — don't assume "Q2 = Scan Conversion" holds across all years despite what the general Q#→chapter table in [[_PastPapers]] implies. Convex/concave polygon ID and the point left/right-of-line test, though conceptually scan-conversion/geometry topics, are both asked inside other questions' clusters (Q4/Ch5-Clipping and Q7/Ch11 respectively) — answered there, not in Chapter 3.
