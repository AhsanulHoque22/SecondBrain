# 3D Transformations (Chapter 6)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Direct 3D generalization of Chapter 4: translation, scaling, and rotation about a canonical axis ($x$, $y$, or $z$), composed by matrix multiplication into composite transformations (tilting, rotation about an arbitrary axis, mirror reflection).

## Key steps / algorithm
1. **Translation:** $x'=x+a,y'=y+b,z'=z+c$ for $\mathbf V=a\mathbf I+b\mathbf J+c\mathbf K$.
2. **Scaling about origin:** $x'=s_x x,\ y'=s_y y,\ z'=s_z z$ — same idea as 2D, one more axis.
3. **Canonical rotation matrices** (book notation $R_{\theta,\mathbf K}$=about $z$, $R_{\theta,\mathbf J}$=about $y$, $R_{\theta,\mathbf I}$=about $x$) — each is the familiar 2D rotation matrix embedded in the plane perpendicular to its axis.
4. **Tilting** = rotate about $x$ by $\theta_x$, then about $y$ by $\theta_y$: $T=R_{\theta_y,\mathbf J}\cdot R_{\theta_x,\mathbf I}$. Reversing the order gives a **different** matrix — rotation order always matters in 3D.
5. **Arbitrary-axis rotation** $R_{\theta,L}$: translate axis point to origin → align axis direction with $\mathbf K$ (via $A_{\mathbf V}$, two canonical rotations) → rotate by $\theta$ about $\mathbf K$ → reverse the align → reverse the translate.
6. **Mirror reflection:** about the $xy$-plane, just negate $z$ ($M=\mathrm{diag}(1,1,-1)$); about an arbitrary plane, same translate-align-reflect-reverse recipe as arbitrary-axis rotation.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2022 | B-Q5(c) | Define tilting (rotate $x$ then $y$); find the tilting matrix; does order matter? [3.5] |
| 2023 | A-Q3(c) | Scale 3D object (4 points) by (3,2,3) on X,Y,Z — shared with Ch4 scaling |

🔁 This is the lightest chapter by far — only 1 genuine tilting question (2022) across 5 years, plus one 3D-scaling question (2023) that's really Ch4 material applied in 3D. **Correction (2026-07-05):** tilting was previously tracked as appearing in both 2021 and 2022 — direct re-verification against all pages of the 2021 paper found no tilting question that year; it is 2022-only.

## Weak spots / common mistakes
- Matrix multiplication order: "rotate about $x$ then $y$" means $x$'s matrix is applied first, so it sits on the **right** in the product: $T=R_{\theta_y,\mathbf J}\cdot R_{\theta_x,\mathbf I}$, not the other way round.
- The "does order matter" follow-up always has the same answer for composite 3D rotations: **yes**, because matrix multiplication doesn't commute — show the reversed product and point out one differing entry, don't just assert it.
- 3D scaling about the origin has no interaction between axes — don't overthink it, it's three independent 1D multiplications.

## Full solutions
[[Chapter6_Solutions.pdf]] — both years' questions solved exactly, plus mirror reflection and arbitrary-axis rotation covered for syllabus completeness even though never asked in 5 years.

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]] · [[wiki/2d-transformations|2D Transformations (Ch4)]]
