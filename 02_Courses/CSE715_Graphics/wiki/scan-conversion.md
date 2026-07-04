# Scan Conversion (Chapter 3)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
The process of converting a continuous-space graphical primitive (point, line, circle, polygon) into the discrete set of pixels that approximate it in image space — also called rasterization.

## Key facts / formulas
1. **DDA line:** $y_{i+1}=y_i+m$ (if $|m|\le1$, step $x$ by 1) or $x_{i+1}=x_i+1/m$ (if $|m|>1$, step $y$ by 1). Floating-point add each step, no multiply, but rounding drift possible.
2. **Bresenham line** ($0\le m\le1$): $\mathrm{Inc}_1=2\Delta y$, $\mathrm{Inc}_2=2(\Delta y-\Delta x)$, $d_1=\mathrm{Inc}_1-\Delta x$. If $d>0$: upper pixel, $d\mathrel{+}=\mathrm{Inc}_2$; else: lower pixel (same $y$), $d\mathrel{+}=\mathrm{Inc}_1$. All-integer — no floating point at all, which is *why* it beats DDA.
3. **8-way circle symmetry:** from one octant point $(x,y)$: $(x,y),(y,x),(-y,x),(-x,y),(-x,-y),(-y,-x),(y,-x),(x,-y)$.
4. **Midpoint circle:** $x=0,y=r,p_1=1-r$. If $p<0$: $T=(x{+}1,y)$, $p\mathrel{+}=2x+3$; else: $S=(x{+}1,y{-}1)$, $p\mathrel{+}=2(x-y)+5$, $y{-}{-}$. Loop while $x\le y$. To center elsewhere, add $(x_c,y_c)$ to every plotted point.
5. **4-connected vs 8-connected fill trap:** using the *same* connectivity rule for a diagonal boundary and its fill is self-contradictory — an 8-connected fill can leak through the corner-gaps of a 4-connected diagonal staircase boundary. Pair 8-connected boundary with 4-connected fill (or vice versa).
6. **3 adverse effects of scan conversion:** staircase/jaggies, unequal brightness (slanted-line pixels are √2 units apart vs 1 unit for axis-aligned — same intensity, lower density, looks dimmer), picket fence problem (global vs local aliasing).
7. **Anti-aliasing fixes:** area sampling (pre-filter, % overlap), super sampling (post-filter, subpixel fraction covered), lowpass filtering (weighted neighbor average, weights sum to 1), pixel phasing (hardware nudge).
8. **Koch-curve family:** both built by replacing a segment's middle third with a bump and recursing. Classic (triangular bump, Koch snowflake): ×4 segments/edge/iteration, turns +60,-120,+60. Quadratic (square bump): ×5 segments/edge/iteration, turns +90,-90,-90,+90. Segment count at generation $n$ = $E\times(\text{multiplier})^n$ for a base shape with $E$ edges.

## Exam pattern
**⚠️ The question number for this cluster shifts every year — do not assume "Q2 = Scan Conversion."**

| Year | Q# | What it asks |
|---|---|---|
| 2024 | A-Q3(c) | DDA + Bresenham trace (2,3)→(10,7); do they agree? (No — m=0.5 tie) |
| 2023 | A-Q1(c),Q2(a-d) | Bresenham vs DDA; slanted-line dimming; midpoint circle r=10 3rd-quadrant; flood-fill hexagon 8-conn; Koch curve gen3 |
| 2022 | A-Q2(a-d) | 8-way symmetry; midpoint circle r=10 center(50,50); slanted-line dim+fix; Koch curve triangle→star gen3 |
| 2021 | A-Q1(f),Q2(a-b) | Koch curve (square bump) gen2; line(1,1)-(10,7) basic+Bresenham full trace; 3 adverse effects + lowpass filter |
| 2020 | A-Q2(d),Q3(b-c),Q4(c) | flood-fill arrow 8-conn; DDA(1,1)-(5,8); Bresenham(0,0)-(8,5); 8-way symmetry |

🔁 Repeats every year: a full line-trace (DDA and/or Bresenham) and a circle/Koch/antialiasing conceptual question. 2022 is the only year with no DDA/Bresenham numeric trace.

## Weak spots / common mistakes
- Bresenham's tie-breaking convention (`d≤0` → lower pixel) can disagree with DDA's rounding (`Floor(y+0.5)` always rounds an exact .5 up) — slopes like m=0.5 are genuine ties, not an error in either algorithm.
- Forgetting to translate a circle's octant points by $(x_c,y_c)$ when the center isn't the origin.
- Assuming 8-connected fill is always "more thorough" — it's actually the *riskier* choice against a diagonal (4-connected) boundary, since it can leak through the staircase corner-gaps.
- Koch curve generation-numbering is inconsistent across years (some papers label the base line as "generation 0", others as "First Generation") — always count *how many times the replacement rule has been applied*, not the label.

## Full solutions
[[Chapter3_Solutions.pdf]] — all 5 years (2020–2024), every sub-part answered.

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]] · [[wiki/image-representation|Image Representation (Ch2)]]
