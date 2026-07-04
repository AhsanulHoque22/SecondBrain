# 2D Transformations (Chapter 4)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Mapping a point/object's coordinates to new coordinates via a matrix operation — translation, rotation, scaling, reflection, or shear — either moving the object itself (geometric transformation) or re-expressing it relative to a different reference frame (coordinate transformation).

## Key facts / formulas
1. **Rotation about origin** (CCW by $\theta$): $x'=x\cos\theta-y\sin\theta,\ y'=x\sin\theta+y\cos\theta$. Derivation: $P(x,y)=(l\cos\alpha,l\sin\alpha)$, rotate to angle $\alpha+\theta$, expand with angle-sum identities.
2. **Scaling about origin:** $x'=s_x\cdot x,\ y'=s_y\cdot y$.
3. **The universal arbitrary-fixed-point recipe** (rotation AND scaling): translate fixed point $F$ to origin → apply transform → translate back. $$\text{Rotate about }F:\ x'=f_x+(x-f_x)\cos\theta-(y-f_y)\sin\theta,\ \ y'=f_y+(x-f_x)\sin\theta+(y-f_y)\cos\theta$$ $$\text{Scale about }F:\ x'=f_x+s(x-f_x),\ \ y'=f_y+s(y-f_y)$$
4. **Reflections:** about $x$-axis flips $y$-sign, about $y$-axis flips $x$-sign, about origin flips both (=180° rotation).
5. **Shear:** $x$-shear $x'=x+sh_x\cdot y,\ y'=y$; $y$-shear $x'=x,\ y'=y+sh_y\cdot x$.
6. **Geometric vs.\ Coordinate transformation:** geometric moves the *object* (axes fixed); coordinate moves the *axes* (object fixed) — mathematically the inverse relationship, same matrix machinery.
7. **Why normalized/device-independent coordinates:** monitor resolutions vary; defining pictures in a standard normalized range (e.g. unit square) and applying a separate workstation transform per device keeps the same picture correct on every display.

## Exam pattern
**⚠️ Question number shifts: Q3 in 2020(Group-B)/2021/2022/2023, but the numeric rotation+scaling pair sits in Q4 for 2020(Group-A) and 2024.**

| Year | Q# | What it asks |
|---|---|---|
| 2024 | A-Q4(a-e) | Identify transforms from a figure; derive rotation matrix; translate a segment; steps to rotate a line about a point; 2D shear matrices |
| 2023 | A-Q3(a-c) | Coordinate-system rationale; 45° rotation of a triangle about origin + about a vertex; 3D scaling (related) |
| 2022 | A-Q3(a-c) | Coordinate-system rationale; scale a triangle ×3/×0.5 about a fixed vertex; 45° rotation about origin + about (2,3) |
| 2021 | A-Q3(a-c) | Geometric vs coordinate transformation; magnify a pentagon ×2 about a fixed vertex; 60° rotation of a rectangle about a point |
| 2020 | A-Q4(a-c) + B-Q5(d)/Q6(a) | 90° rotation about a point; magnify a triangle ×2 about a fixed vertex; 8-way symmetry (Ch3, cross-ref); geometric vs coordinate transform; coordinate-system rationale |

🔁 Repeats every year: rotate/scale about an arbitrary fixed point (never just the origin alone). 2× theory one-liners (coordinate-system rationale, geometric-vs-coordinate) rotate in and out depending on the year — both are worth memorizing since either can appear.

## Weak spots / common mistakes
- Forgetting the fixed point is **not** the origin — always translate-transform-translate-back, never apply the raw origin-centered matrix directly to a point when a fixed vertex is named.
- Confusing the two recurring theory questions: "geometric vs coordinate transformation" (definitional, about *what* is being described) vs. "why a device-independent coordinate system" (about *display resolution*, unrelated concept despite similar wording).
- 2020's fixed-point letter can collide with a vertex name (e.g. rotate about "$B(-1,-1)$" when the rectangle already has its own vertex $B$) — treat the given pivot coordinates as authoritative, not the label.
- 2024's figure-identification question (Q4a) has no numeric answer — grade depends on reading vertical/horizontal flip cues correctly from your own paper's diagram, not from memorized coordinates.

## Full solutions
[[Chapter4_Solutions.pdf]] — all 5 years (2020–2024), every sub-part answered including the previously-untracked 2022 scaling question and all 2024 Q4 sub-parts.

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]] · [[wiki/scan-conversion|Scan Conversion (Ch3)]]
