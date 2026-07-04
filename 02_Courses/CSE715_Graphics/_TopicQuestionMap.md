# CSE 715 — Computer Graphics · Topic → Question Map
> [[_Topics]] · [[_Syllabus]] · [[_PastPapers]]
> Read only when starting a block for a specific topic (per session protocol — not at session start).

## TIER 1

**Cohen-Sutherland region codes + line clipping**
- 2024 Q5b — region codes for P1–P5 vs window (10,30,10,25); is A(5,5)-B(12,20) visible/clip
- 2023 Q8a — clip (5,5)-(15,10) in window (0,0,10,10)
- 2022 Q4a — region codes A,B,C,D vs window (2,5,1,9); clip AB, CD
- 2021 Q4a — region codes M,N,P,Q vs given rectangle; clip MN, PQ
- 2020 Q6b — region codes A,B,C,D vs window (1,5,1,7); clip AB, CD

**Normalization transformation (window→viewport)**
- 2024 Q5a — window(1,1)-(3,5) → (i) full NDC (ii) viewport with corner (vx,vy)
- 2022 Q4c — window(1,1)-(2,2) → viewport(0,0)-(1/2,1/2)
- 2021 Q7d — window(1,4)-(3,4), preserve aspect ratio → NDC
- 2020 Q5a,b — workstation transform (NDC→device 0-199,0-639); window(1,1)-(2,2)→viewport(0,0)-(1/2,1/2)

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

**Cavalier/Cabinet projection matrices**
- 2023 Q5a — cavalier θ=60°, cabinet θ=45°
- 2022 Q5b/6c — cavalier θ=30°, cabinet θ=45° for a unit cube
- 2021 Q5b — cavalier θ=45°, cabinet θ=30°

**Perspective vs Parallel projection**
- 2023 Q4b — orthographic vs oblique; Q1f projection choice for photographing university
- 2022 Q6b — why easier to locate hidden surfaces with parallel projection
- 2021 Q6b — distinguish perspective/parallel; who uses which
- 2020 Q8a — distinguish; who uses which (architects/engineers)

**Z-Buffer algorithm**
- 2024 Q7d — illustrate Z-buffer, advantages/disadvantages
- 2022 Q6c — max objects representable; 2×2 pixel trace for objects A,B
- 2021 Q6c — same structure, different geometry
- 2020 — (Painter's/Z-buffer style question embedded in Group-B Q6, general HSR)

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

**Ray–sphere intersection**
- 2023 Q8c — S1 r=8 at (2,4,1), S2 r=10 at (10,-2,-5); ray s=2I+5K, d=I-2J
- 2022 Q8d — sphere r=2 at origin; ray from (3,0,0) dir (-3,1,0)
- 2021 Q8e — same two-sphere setup as 2023
- 2020 — (ray equation embedded, no explicit sphere in this year's extract)

**Sutherland-Hodgman / Weiler-Atherton polygon clipping**
- 2024 Q6a — Weiler-Atherton: quad A,B,C,D vs triangle P,Q,R — entry/exit points, CCW order
- 2023 Q4a — Sutherland-Hodgman: A(1,1),B(4,1),C(4,4),D(1,4) vs window W,X,Y,Z
- 2022 Q4b — SH clipping steps, given polygon figure
- 2021 Q4b — SH clipping abcdefghijkl vs MNOP, order: left PM, bottom PO

## TIER 3 (brief refs — lower priority, drill only after Tier 1–2 solid)
- **CG vs Image Processing/HCI:** 2023 Q1a — differentiate CG from image processing (1 mark); 2022 Q1a — CG vs image processing/HCI (both distinctions); 2021 Q1a — how does image processing differ from CG; 2020 Q1a — which discipline describes producing/synthesizing digital images (justify: CG = object definition → image; image processing = image → image, pixel-based)
- **Antialiasing/slanted lines:** ✅ verified 2026-07-04, solved in [[Chapter3_Solutions.pdf]] — 2023 Q2(a) why dimmer only [1]; 2022 Q2(c) why dimmer + how to fix [2]; 2021 Q2(b) "3 adverse effects" + lowpass-filter kernel application [2.75, bundled with the line-trace question]
- **Geometric vs Coordinate transform:** ✅ verified 2026-07-04, solved in [[Chapter4_Solutions.pdf]] — 2021 Q3a [1.25]; 2020 Q5d [~1] *(2022's occurrence was mis-attributed to Q3a — that question is actually the separate Coordinate-system-rationale question above; 2022 does not ask Geometric vs Coordinate transformation)*
- **RGB scanline interpolation:** 2022 Q7c, 2021 Q7c, 2020 (Q7d-equiv 2021 paper)
- **Ray vs Vector:** 2022 Q8a, 2021 Q8c, 2020 Q7c(2021 paper actually — cross-check when drilling)
- **Ray equation point-finding:** 2022 Q8c, 2021 Q8b
- **Convex/concave polygon ID:** lives in the Q4/Ch5-Clipping cluster, not Ch3 — 2022 Q4c, 2021 Q4(c) [confirmed: "Identify the convex and concave polygons"], 2020 (Q6c 2021 paper) — will be answered alongside Chapter 5 (Clipping), not Chapter 3
- **Midpoint circle + 8-way symmetry:** ✅ verified 2026-07-04, solved in [[Chapter3_Solutions.pdf]] — 2023 Q2(b) r=10 center-origin, 3rd-quadrant points [4]; 2022 Q2(a) 8-way symmetry explain [1.5] + Q2(b) r=10 center(50,50) [4]; 2020 Q4(c) show 8-way symmetry [1]

## TIER 4 (one appearance each — learn the method fast, don't over-invest)
Tilting: 2022 (Q3c-equiv), 2021 Q5c/6c-area · Monitor matrix M: 2023 Q7a, 2021 Q7a · Isometric/Dimetric/Trimetric: 2023 Q1i, 2020 Q8b · Foreshortening/vanishing point: 2021 Q5c(2021 paper Q5c-equiv), 2020 Q6d · Phong model: 2022 Q6d, 2023 (image-based Q) · **Flood/boundary fill: 2023 Q2(c) hexagon [3], 2020 Q2(d) arrow [2.5] — ✅ verified 2026-07-04, solved in [[Chapter3_Solutions.pdf]] (both are "will 8-connected fill leak on diagonal edges" reasoning questions)** · Point left/right test: 2022 Q7a, 2021 Q7a — lives in Q7/Ch11 cluster, not Ch3

## TIER 5 (2024-only or syllabus-mandated zero-yield)
Halftoning+dither: 2024 Q2d, Q3a,b · Circular clipping: 2024 Q5c · Trapezoid fill: 2024 Q7b,c,e · Axonometric: 2024 Q6c · 3D scaling: 2023 Q3c · Painter's vs Z-buffer: 2023 Q7d · Perspective anomalies: 2023 Q4c · Orthographic vs Oblique: 2023 Q4b · Back-face/visible surface: 2024 Q1c, Q7a · Color gamut: 2022 Q8b · **Bezier/B-spline/Hermite: no PYQ hit 2020–2024**

## Note on accuracy
This map was built from scanned/handwritten past papers read in one pass — Tier 3–5 year attributions may have minor mix-ups between adjacent years since several questions repeat near-identically. Re-verify the specific year during block study if it matters for your prep; the topic identification itself is solid.

**Chapter 3 (Scan Conversion) cluster fully re-verified against the raw scanned papers on 2026-07-04** during question-analysis — see [[Chapter3_Solutions.pdf]]. Key corrections: the exact question number for this cluster **shifts every year** (Q2 in 2022/2023, Q1+Q2 split in 2021, Q2+Q3+Q4 split in 2020, Q3 only in 2024) — don't assume "Q2 = Scan Conversion" holds across all years despite what the general Q#→chapter table in [[_PastPapers]] implies. Convex/concave polygon ID and the point left/right-of-line test, though conceptually scan-conversion/geometry topics, are both asked inside other questions' clusters (Q4/Ch5-Clipping and Q7/Ch11 respectively) — answered there, not in Chapter 3.
