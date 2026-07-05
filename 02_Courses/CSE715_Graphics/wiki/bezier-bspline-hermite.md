# Bezier / B-Spline / Hermite Curves (Chapter 9)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Curve-representation schemes that build a smooth curve from control points (a "guiding polyline") using blending/basis functions — Hermite (interpolates points + prescribed tangents), Bezier-Bernstein (global control), Bezier-B-spline (local control).

## Key steps / algorithm
1. **Hermite cubic:** $H(x)=\sum[y_iH_i(x)+y_i'\bar H_i(x)]$ — passes through data points with prescribed derivative/tangent at each.
2. **B-spline (recursive):** $B_{i,0}=1$ on $[t_i,t_{i+1}]$ else 0; $B_{i,n}=\frac{x-t_i}{t_{i+n}-t_i}B_{i,n-1}+\frac{t_{i+n+1}-x}{t_{i+n+1}-t_{i+1}}B_{i+1,n-1}$. Nonzero only on $[t_i,t_{i+n+1}]$ — **local support**.
3. **Bernstein polynomial:** $BE_{k,n}(x)=\binom{n}{k}x^k(1-x)^{n-k}$.
4. **Bezier curve:** $P(t)=\sum x_iBE_{i,n}(t)$ etc., $0\le t\le1$. Properties: endpoint interpolation, tangent matches polyline ends, convex hull, but **global** control (move one point, whole curve reshapes).
5. **Bezier-B-spline:** same curve using $B_{i,m}(t)$ instead of Bernstein — same nice properties but **local** control (move one point, only nearby span reshapes) + closer fit + control-point multiplicity.

## Exam pattern
**0/5 hits in 2020–2024 past papers** — confirmed by direct re-verification of every question in every paper. `Syllabus.txt` explicitly mandates covering it anyway ("Chapter 9: Bezier Curve, solve problems, B-spline, Hermite Curve, exercise and solved questions"), overriding the usual "skip if not in past papers" rule.

## Weak spots / common mistakes
- Global vs.\ local control is the single most quotable Bezier-Bernstein vs.\ Bezier-B-spline distinction — memorize that one contrast first.
- Don't confuse "Bezier curve" (uses Bernstein basis) with "B-spline" (uses the recursive $B_{i,n}$ basis) — Bezier-B-spline is the hybrid that swaps Bernstein for B-spline inside the Bezier-style parametric form.

## Full solutions
[[Chapter9_Solutions.pdf]] — book definitions + solved textbook exercises (knot-set construction, B-spline zero-outside-support proof, a worked Bezier curve point evaluation). No past-paper questions exist to solve.

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]]
