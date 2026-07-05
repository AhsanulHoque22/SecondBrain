# 2D Viewing and Clipping (Chapter 5)
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Mapping a world-coordinate window to a normalized-device viewport (normalization transformation), and eliminating the parts of lines/polygons that fall outside a clipping window (Cohen–Sutherland for lines, Sutherland–Hodgman/Weiler–Atherton for polygons).

## Key steps / algorithm
1. **Normalization (window→viewport):** $vx=\frac{vx_{\max}-vx_{\min}}{wx_{\max}-wx_{\min}}(wx-wx_{\min})+vx_{\min}$ (same form for $vy$). Matrix $N=$ translate(viewport min)·scale($s_x,s_y$)·translate($-$window min). **Aspect-preserving variant** (only window given): compute $a_w=$width/height; fill the longer NDC axis fully, scale the shorter proportionally so $s_x=s_y$.
2. **Cohen–Sutherland region code** (book's exact bit order — **TOP, BOTTOM, RIGHT, LEFT**): Bit1=$\mathrm{sign}(y-y_{\max})$, Bit2=$\mathrm{sign}(y_{\min}-y)$, Bit3=$\mathrm{sign}(x-x_{\max})$, Bit4=$\mathrm{sign}(x_{\min}-x)$. Code $0000$=inside. Both codes $0000\Rightarrow$ visible; AND$\neq0000\Rightarrow$ not visible; else clip the outside endpoint against whichever boundary its set bit names, iterate.
3. **Convex polygon:** any interior-to-interior segment stays inside. **Positive orientation:** CCW vertex order. **Left/right test:** for edge $A(x_1,y_1)\to B(x_2,y_2)$, point $P(x,y)$: $C=(x_2-x_1)(y-y_1)-(y_2-y_1)(x-x_1)$; $C>0\Rightarrow$ left (inside a positively-oriented convex edge), $C<0\Rightarrow$ right.
4. **Sutherland–Hodgman:** clip subject polygon one clip-window edge at a time; per subject edge, 4-case left/right test (both left→output $P_i$; both right→nothing; exiting→output intersection; entering→output intersection then $P_i$). Weak spot: can leave spurious double-back edges on multi-part output.
5. **Weiler–Atherton:** trace subject polygon; on exiting the clip polygon, record intersection and right-turn onto the clip polygon boundary (swap roles); on re-entry, resume the subject trace. Correctly handles concave clip windows and disjoint output pieces.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | B-Q5(a,b,c)/Q6(a) | Normalization (symbolic viewport); region codes + visibility of A-B; circular clip window (related); Weiler-Atherton triangle vs rectangle |
| 2023 | A-Q4(a)/B-Q8(a) | Sutherland-Hodgman 3×3 square vs 1×1 window (fully numeric); Cohen-Sutherland (5,5)-(15,10) in (0,0)-(10,10) |
| 2022 | A-Q4(a,b,c)/B-Q7(b) | Region codes + clip AB,CD (CD grazes corner exactly); SH clip on figure (no coords); aspect-ratio-preserved normalization; convex/concave diagram |
| 2021 | A-Q4(a,b,c)/B-Q7(d) | Region codes + clip MN,PQ; SH clip on figure (no coords); convex/concave ID (3 shapes); normalization (1,1)-(2,2)→(0,0)-(1/2,1/2) |
| 2020 | B-Q5(a,b,c)/Q6(b,c) | Workstation transform (NDC→199×639 device); normalization (1,1)-(2,2)→(0,0)-(1/2,1/2); explain Cohen-Sutherland; region codes+clip AB,CD; convex/concave ID (4 shapes) |

🔁 Repeats every year: Cohen–Sutherland region codes + clip 2 lines, and a normalization/window-viewport derivation — both TIER 1 (5/5). Sutherland-Hodgman/Weiler-Atherton polygon clipping is TIER 2 (appears 2021–2024).

## Weak spots / common mistakes
- Bit order is **TOP, BOTTOM, RIGHT, LEFT** in that exact sequence — don't reorder when writing the 4-bit code.
- A point exactly on a boundary (e.g. $x=x_{\min}$) is **not** flagged by its sign bit (convention: `sign(a)=1` only if `a>0`, strictly) — this can make a line clip down to a single grazing point (2022 Q4a, segment $CD$).
- The 2022 normalization question gives **only a window**, no viewport — the "preserve aspect ratio" instruction is the cue to use the $a_w$ rule (§1 step 1), not the direct two-rectangle formula.
- Sutherland-Hodgman processes **one clip edge against the whole polygon** before moving to the next edge — don't try to test all 4 edges simultaneously per vertex.
- Weiler-Atherton is only required when the question explicitly says so, or the clip window is concave — otherwise default to Sutherland-Hodgman.

## Full solutions
[[Chapter5_Solutions.pdf]] — all 5 years (2020–2024), every sub-part answered including the Related circular-clipping bundle (2024 Q5c) and a corrected 2021/2022 year attribution for the normalization questions (previous topic-map entry had them swapped).

## Related topics
[[_Syllabus]] · [[_TopicQuestionMap]] · [[wiki/2d-transformations|2D Transformations (Ch4)]]
