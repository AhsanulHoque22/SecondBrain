# Image Representation (Chapter 2)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
The study of how a digital image's pixel colors are stored (direct coding vs. lookup table), how images relate physically (aspect ratio, resolution, sub-image cropping), and how limited-color/bilevel devices simulate continuous tone (halftoning, dithering).

## Key facts / formulas
1. **CG vs Image Processing:** CG = object → image (synthesis); Image Processing = image → image (pixel ops on an existing image).
2. **RGB (additive, black=(0,0,0)) ↔ CMY (subtractive, black=(1,1,1)):** `RGB = (1,1,1) - CMY` and vice versa. Printers add K (black) because mixing CMY for true black is costly/muddy.
3. **Perceptual terms ↔ physical property:** Hue↔wavelength, Saturation↔purity, Brightness↔luminance/intensity.
4. **Direct coding:** colors = 2^(n_r) × 2^(n_g) × 2^(n_b) — bits per primary can differ.
5. **Lookup table:** entries = 2^(bits/pixel); storage = entries × bits/entry.
6. **Aspect ratio** = width/height. No distortion ⟺ w1/h1 = w2/h2.
7. **Center-crop coords:** lower-left = ((W-w)/2, (H-h)/2); upper-right = lower-left + (w,h).
8. **Halftoning:** variable dot size at fixed 45° pitch simulates continuous tone on bilevel devices.
9. **Dither matrix recurrence (Bayer):** D_2n = [[4Dn, 4Dn+2],[4Dn+3, 4Dn+1]].

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | A-Q2,Q3 | color model concept; crop coords; LUT entries; halftoning; dither matrix D2→D4 |
| 2023 | A-Q1(a,b,g) | CG vs IP; crop coords; perceptual color terms |
| 2022 | A-Q1(a-f) | resize/AR; LUT bits; direct coding CMY; distortion check; subtractive reasoning |
| 2021 | A-Q1(a-e) | CG vs IP; LUT bits; direct coding RGB; resize onto 2 devices; crop coords |
| 2020 | A-Q1,Q2 | discipline ID; distortion check; image formation pipeline; AR/width; subtractive color; direct coding; crop coords |
🔁 Repeats every year: crop-coordinate math, direct-coding bit arithmetic, LUT sizing, aspect-ratio distortion check. 2024 introduced halftoning/dither as new content — first appearance in 5 years, recency risk for 2025.

## Weak spots / common mistakes
- Forgetting upper-right = lower-left + (w,h), not just re-deriving from the big image's center independently.
- Confusing "bits the LUT occupies" (entries × bits/entry) with "bits per pixel" (just the index width).
- Mixing up which model is additive (RGB) vs subtractive (CMY) — RGB starts at black, CMY starts at white.
- Dither matrix recurrence: forgetting the block order (top-left=4Dn, top-right=4Dn+2, bottom-left=4Dn+3, bottom-right=4Dn+1).

## Full solutions
[[Chapter2_Solutions.pdf]] — all 5 years (2020–2024), every sub-part answered.

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]]
