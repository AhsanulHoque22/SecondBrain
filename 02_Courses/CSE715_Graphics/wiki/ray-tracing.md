# Ray Tracing (Chapter 12)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Five subtopics: **ray vs vector** distinction, the **parametric ray equation** $\mathbf{r}(t)=\mathbf{s}+t\mathbf{d}$, **ray–sphere intersection**, how ray tracing **integrates hidden-surface removal + projection** into one process, and the 2024-only **point/plane same-side test**.

## Key steps / algorithm
**Ray vs vector:** vector = direction+magnitude, position-free; ray = direction+fixed starting point, one-sided ($t\ge0$).

**Ray equation:** $\mathbf{r}(t)=\mathbf{s}+t\mathbf{d}$ — plug in $t$ component-wise on I,J,K.

**Ray–sphere intersection:** quadratic $At^2+2Bt+C=0$ with $A=|\mathbf{d}|^2$, $B=(\mathbf{s}-\mathbf{c})\cdot\mathbf{d}$, $C=|\mathbf{s}-\mathbf{c}|^2-R^2$. Roots' signs tell the story: both negative → no real intersection; differ in sign → ray starts **inside**, intersects once; both positive → intersects **twice** (enters then exits), smaller root = nearer point.

**Why ray tracing is efficient:** each primary ray is a projector (viewpoint-converging = perspective, parallel = parallel projection); only the **closest** surface hit determines the pixel color, which is hidden-surface removal for free. One ray/intersection test does projection + hidden-surface removal + shading (local/reflected/transmitted contributions) simultaneously.

**Point/plane same-side test:** plane $ax+by+cz=d$, normal $=(a,b,c)$; $f(P)=ax+by+cz-d$, same sign at two points → same side (3D analogue of the [[wiki/color-shading-models|Ch11 point left/right test]]).

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2021 | B-Q8(a) | Describe how hidden-surface removal + projection integrate into ray tracing [1.5] |
| 2021 | B-Q8(b) | Ray equation, find points at t=0,1,7,4,3 [2.5] |
| 2021 | B-Q8(c) | Difference between vector and ray [1] |
| 2021 | B-Q8(e) | Two-sphere intersection (=Schaum's Solved Prob 12.15 exactly) [3.75] |
| 2022 | B-Q7(c) | Homogeneous coords purpose + ray tracing benefits (related, bundled w/ Ch11 Q7) [3] |
| 2022 | B-Q8(a) | Show a ray is not a vector [1] |
| 2022 | B-Q8(c) | Ray equation, find points at t=1,2,-4,3,7 [3] |
| 2022 | B-Q8(d) | Sphere r=2 at origin, ray from (3,0,0) dir (-3,1,0) — 2 intersections [4] |
| 2023 | B-Q8(c) | Two-sphere setup, different ray from 2021's — hits only S1 [3.5] |
| 2024 | B-Q8(b) | Why Ray Tracing is efficient [2] |
| 2024 | B-Q8(c) | Distinguish ray and vector [2] |
| 2024 | B-Q8(d) | Plane 5x-3y+6z=7: normal + same-side test for 2 points [2+2] |

🔁 **Correction (2026-07-07):** 2020 has **zero** ray-tracing content of any kind (previously mistracked as having ray-sphere/ray-vector/ray-equation questions — its actual Q7/Q8 are point left/right, polygon orientation, 3D rotation, projections, point-obscures-viewpoint).

## Weak spots / common mistakes
- Don't forget the sign-of-roots interpretation table for ray–sphere: same-sign-both-negative ≠ same-sign-both-positive ≠ differing signs — each means something different (miss / exits-twice / starts-inside).
- 2021 Q8(e) and 2023 Q8(c) use the **same two sphere centers/radii** but a **different ray** each year — don't reuse the 2021 answer for 2023 by mistake.
- "Ray is not a vector" needs the fixed-starting-point argument, not just "different names."
- Plane same-side test: the sign of $f(P)$ alone doesn't tell you *which* side is "positive" — it only tells you whether two points share a side.

## Full solutions
[[Chapter12_Solutions.pdf]] — all 2021–2024 instances worked numerically, plus the theory framework (ray vs vector, ray equation, ray–sphere quadratic, ray-tracing algorithm, point/plane test).

## Related topics
[[wiki/color-shading-models|Color & Shading Models (Ch11)]] · [[wiki/z-buffer|Z-Buffer (Ch10)]] · [[_Syllabus]] · [[_TopicQuestionMap]]
