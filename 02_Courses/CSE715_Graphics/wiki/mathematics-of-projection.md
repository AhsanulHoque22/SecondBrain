# Mathematics of Projection (Chapter 7)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Mapping a 3D point onto a 2D view plane via a projector — either converging to a center of projection (**perspective**, realistic but size-distorting) or all parallel to a fixed direction $\mathbf V$ (**parallel**, true-scale — orthographic if $\mathbf V\perp$ view plane, oblique otherwise).

## Key steps / algorithm
1. **Standard perspective** ($Per_{\mathbf K}$, center $C(0,0,-d)$, view plane = $xy$): $x'=\frac{dx}{z+d},\ y'=\frac{dy}{z+d},\ z'=0$ — nonlinear in 3D, linear as a $4\times4$ homogeneous matrix $\mathrm{diag}(d,d,0)$ with bottom row $(0,0,1,d)$.
2. **General parallel projection** onto $xy$, direction $\mathbf V=a\mathbf I+b\mathbf J+c\mathbf K$: $x'=x-\frac{a}{c}z,\ y'=y-\frac{b}{c}z,\ z'=0$.
3. **Oblique projection parametrized by $(f,\theta)$**: $Par_{\mathbf V}=\begin{pmatrix}1&0&f\cos\theta&0\\0&1&f\sin\theta&0\\0&0&0&0\\0&0&0&1\end{pmatrix}$. **Cavalier** $f=1$ (no depth foreshortening); **Cabinet** $f=\tfrac12$ (depth halved, looks more natural).
4. **Isometric/dimetric/trimetric** = orthographic axonometric (direction of projection not parallel to any axis) distinguished by how many of the 3 axis-angles are equal: all 3 (isometric), exactly 2 (dimetric), none (trimetric).
5. **4 perspective anomalies**: foreshortening (farther = smaller), vanishing points (non-view-plane-parallel lines converge), view confusion (behind-camera objects flip upside-down/backward), topological distortion (a segment crossing the center-of-projection's parallel plane projects to an infinite broken line).

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | B-Q6(c,d)/Q8(a) | Axonometric significance [2]; Cabinet properties [1]; draw top/front/right views [3] |
| 2023 | A-Q1(f,i)/Q4(b,c)/B-Q5(a,c)/Q8(b) | Projection choice for a picture; isometric/dimetric/trimetric; ortho vs oblique; 4 anomalies; cavalier θ=60°/cabinet θ=45°; derive general Par_V; derive Per_K via homogeneous coords |
| 2022 | B-Q5(a,b) | Perspective vs parallel + architects/engineers [1]; cavalier θ=30°/cabinet θ=45° [4] |
| 2021 | B-Q5(a,b,c) | Same distinguish question [1.5]; cavalier θ=45°/cabinet θ=30° [4]; foreshortening+vanishing point [2] |
| 2020 | B-Q6(d)/Q8(a,b) | Foreshortening+vanishing point [1.75]; distinguish perspective/parallel [3]; draw isometric/dimetric/trimetric [2.25] |

🔁 Repeats: some projection-comparison question every year, but the **exact wording changes** — don't assume "perspective vs parallel, architects/engineers" verbatim shows up in 2023/2024 (it doesn't; they ask orthographic-vs-oblique or axonometric-significance instead). Cavalier/cabinet full matrix derivation is 2021–2023 only (2020 has none, 2024 is qualitative-only).

## Weak spots / common mistakes
- **Cavalier/cabinet formula is one line:** $Par_{\mathbf V}$'s only nonzero off-diagonal entries are $f\cos\theta$ and $f\sin\theta$ in column 3 — don't re-derive the whole oblique-projection argument from scratch every time, just plug $\theta$ and $f$ (1 or $\tfrac12$) into the memorized matrix.
- **2020 has no cavalier/cabinet question** — don't waste revision time assuming every year needs it; confirmed by re-reading every page of the 2020 paper directly.
- Isometric/dimetric/trimetric is about the **projection direction's angles with the axes**, not about the drawing looking "more 3D" — dimetric ≠ "a worse isometric," it's a distinct equal-2-of-3 case.
- The 4 anomalies question wants **all four named and explained**, not just foreshortening + vanishing points (the two everyone remembers) — view confusion and topological distortion are worth marks too.

## Full solutions
[[Chapter7_Solutions.pdf]] — all 5 years (2020–2024), every sub-part answered, including two corrections found by re-verifying against the raw scans: cavalier/cabinet is 3/5 years not 5/5, and the "perspective vs parallel" question was mis-numbered as Q6b in prior tracking (it's actually Q5a in both 2021 and 2022).

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]] · [[wiki/3d-transformations|3D Transformations (Ch6)]]
