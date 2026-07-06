# Color & Shading Models (Chapter 11)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Five subtopics bundled in the same exam-question cluster (Section B, "Q7"): the **Phong illumination model**, **RGB scanline color interpolation**, the **monitor color transformation matrix $M$** (CIE XYZ↔RGB), the **point left/right-of-line test**, and **color gamut**.

## Key steps / algorithm
**Phong model:** $I = I_ak_a + I_p(k_d\,\mathbf{L}\!\cdot\!\mathbf{N} + k_s(\mathbf{R}\!\cdot\!\mathbf{V})^n)$ — ambient (flat fill) + diffuse (viewer-independent, $\propto\cos\theta$) + specular (viewer-dependent highlight, $\propto\cos^n\varphi$).

**RGB scanline interpolation:** $I' = I_1 + (I_2-I_1)\cdot\frac{y'-y_1}{y_2-y_1}$, component-wise on R,G,B; same formula for extrapolation outside $[y_1,y_2]$.

**Monitor matrix $M$:** (1) $X_w=\frac{x_w}{y_w}Y_w$, $Z_w=\frac{1-x_w-y_w}{y_w}Y_w$ from white point. (2) $z_r,z_g,z_b = 1-x-y$ for each phosphor. (3) Solve $\begin{pmatrix}X_w\\Y_w\\Z_w\end{pmatrix}=\begin{pmatrix}x_r&x_g&x_b\\y_r&y_g&y_b\\z_r&z_g&z_b\end{pmatrix}\begin{pmatrix}C_r\\C_g\\C_b\end{pmatrix}$ for $C_r,C_g,C_b$. (4) $M$'s columns are each phosphor's $(x,y,z)$ scaled by its $C$. **Check:** row sums of $M$ = $X_w,Y_w,Z_w$.

**Point left/right test:** $C=(x_2-x_1)(y-y_1)-(y_2-y_1)(x-x_1)$ (z-component of cross product $\overrightarrow{P_1P_2}\times\overrightarrow{P_1P}$). $C>0$ left, $C<0$ right, $C=0$ on the line.

**Color gamut:** triangle on the CIE chromaticity diagram with vertices = phosphor $(x,y)$ coords; colors inside are displayable.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2020 | B-Q7(a) | Show conditions for point left/right of a line segment [2.25] |
| 2021 | B-Q7(a) | Monitor matrix M, D65 white point + phosphor coords [3] |
| 2021 | B-Q7(c) | RGB interpolation, colors at line 6 & 15 → line 8 [2] |
| 2022 | B-Q7(a) | Point left/right test, formula given [1] |
| 2022 | B-Q7(d) | RGB interpolation (extrapolation case) [2.5] |
| 2022 | B-Q7(e) | Significance of diffuse/specular reflection in Phong [1.5] |
| 2022 | B-Q8(b) | Explain color gamut [1] |
| 2023 | B-Q6(d) | Explain the L/N/R/V Phong diagram [3] |
| 2023 | B-Q7(b) | Monitor matrix M, different white point, same phosphors [3] |
| 2023 | B-Q7(c) | RGB interpolation, colors at line 3 & 9 → line 5 [2] |

🔁 **Repeats every year 2020-2023** (2024 skips this cluster entirely — its B-Q7/Q8 go to visible-surface/trapezoid-fill/ray-tracing instead). **Correction (2026-07-07):** Phong's 2022 occurrence was previously mistracked as "Q6d" in `_TopicQuestionMap.md` — re-verified against the raw scan, it is actually **Q7e**.

## Weak spots / common mistakes
- Diffuse term is **viewer-independent** (only depends on L·N); specular **is** viewer-dependent (depends on R·V) — this distinction is exactly what "significance of diffuse/specular" questions are testing.
- RGB interpolation questions sometimes ask for a line **outside** the given range (2022 Q7d) — same linear formula still applies, fraction just falls outside [0,1].
- Monitor matrix $M$: don't forget $z_r=1-x_r-y_r$ (easy to drop the $1-$ and just use $-x_r-y_r$).
- Point left/right test: sign convention (left=positive) assumes standard right-handed xy axes — state that assumption if asked to "show the conditions."

## Full solutions
[[Chapter11_Solutions.pdf]] — all instances 2020–2023 worked numerically, plus the theory framework (Phong, interpolative shading types, monitor matrix derivation, color gamut, point left/right test).

## Related topics
[[wiki/z-buffer|Z-Buffer]] · [[_Syllabus]] · [[_TopicQuestionMap]]
