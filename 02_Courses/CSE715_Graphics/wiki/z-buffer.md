# Z-Buffer Algorithm (Chapter 10, §10.1-10.2)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
An image-space hidden-surface algorithm that keeps one depth value $Z_{\mathrm{buf}}(x,y)$ per pixel — the smallest $z$ seen so far — so that the closest (frontmost) surface always wins at each pixel.

## Key steps / algorithm
1. Initialize every pixel to background color; initialize $Z_{\mathrm{buf}}(x,y)=Z_{\mathrm{back}}$ (depth of the back clipping plane) for all pixels.
2. For each polygon $P$ in the scene, for each pixel $(x,y)$ it covers: compute $Z(x,y)$.
3. If $Z(x,y) < Z_{\mathrm{buf}}(x,y)$: update $Z_{\mathrm{buf}}(x,y)=Z(x,y)$ and set the pixel color to $P$'s color there. Otherwise leave unchanged.
4. **Max objects representable: unlimited/arbitrary** — memory is proportional to pixel count, not object count, since polygons are processed one at a time.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2022 | B-Q6(c) | Max objects + full 2×2 pixel trace for objects A,B [4.5] |
| 2021 | B-Q6(d) | Same structure, different A/B geometry [4.75] |
| 2023 | B-Q7(d) | Differentiate Painter's algorithm vs Z-buffer [2] |
| 2024 | B-Q7(d) | Illustrate + advantages/disadvantages [2] |

🔁 **Correction (2026-07-06):** previously tracked as 5/5 years — re-verified against every raw scan and found **2020 has no Z-buffer question at all** (that year's only Ch10 content is the separate "point-obscures-point via viewpoint" question). The full numeric 2×2 trace is 2021/2022 only; 2023/2024 ask lighter conceptual versions.

## Weak spots / common mistakes
- "Max objects representable" answer is **unlimited/arbitrary**, not a specific number — the whole point of the algorithm is that it doesn't need to store all objects at once.
- At each pixel, smallest $z$ wins — don't confuse with "largest z wins" (would be backwards, painting the farthest surface on top).
- Advantages: no sorting/ambiguity-resolution needed (unlike Painter's). Disadvantages: needs full-screen depth memory, no native transparency/anti-aliasing.

## Full solutions
[[ZBuffer_Solutions.pdf]] — all 4 years with a Z-buffer question, plus the illustrative 2×2 trace method and the Painter's-vs-Z-buffer comparison table.

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]]
