# Neural Networks + Learning
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
An Artificial Neural Network (ANN) is a computational model of simple processing units (nodes) connected by weighted links, loosely inspired by biological neurons (soma↔node, dendrite↔input, axon↔output, synapse↔weight); it computes outputs as an activation function (typically sigmoid $\sigma(z)=\frac{1}{1+e^{-z}}$) of weighted input sums, and *learns* by adjusting those weights from examples — most commonly via **backpropagation** (gradient descent + chain rule).

## Key steps / algorithm
**Backpropagation Algorithm (Han & Kamber, the canonical exam template — Example 9.1):**
1. Initialise weights $w_{ij}$ and biases $\theta_j$ to small random values.
2. **Forward pass:** $I_j = \sum_i w_{ij}O_i + \theta_j$, then $O_j = \sigma(I_j) = \frac{1}{1+e^{-I_j}}$ — propagate input → hidden → output.
3. **Backward pass — error computation:**
   - Output unit: $Err_j = O_j(1-O_j)(T_j - O_j)$
   - Hidden unit: $Err_j = O_j(1-O_j)\sum_k Err_k\, w_{jk}$ (error flows backward along the same weighted connections)
4. **Update:** $\Delta w_{ij} = l \cdot Err_j \cdot O_i$, $w_{ij}^{new}=w_{ij}+\Delta w_{ij}$ (and $\Delta\theta_j = l\cdot Err_j$ for biases).
5. **Sanity-check:** re-run the forward pass with new weights — output should move closer to target $T$. (This final check is *exactly* what 2023 Q8b asks for.)
6. Repeat per-case or per-epoch until a termination condition (small $\Delta w$, low misclassification %, or epoch limit).

**Perceptron Training Rule** (single-layer, simpler exam variant): $\Delta_i = \eta(t(E)-o(E))\cdot x_i$, with a bias unit (constant input "1", weight $w_0$) representing the threshold: $S = w_0 + \sum w_i x_i$.

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | B-Q8 (9 marks) | a) Inductive learning + example, b) ANN-vs-biological comparison, c) Fuzzy/Uncertainty short notes |
| 2023 | B-Q8 (9 marks) | a) Associative memory + multilayer architecture, b) **sigmoid forward/backward-pass numerical + weight update** |
| 2022 | B-1 (9 marks) | a) ANN definition+comparison, b) learning, c) supervised/unsupervised/reinforcement, d) Fuzzy/Uncertainty short notes |
| 2021 | — | **Not asked** — that year's "Q8" is a pure Bayesian Network question (Burglary/Alarm/Earthquake CPTs). Corrected 2026-06-07. |
| 2020 | — | **Not asked** — no NN question anywhere in the paper (that year's Q8 = Bayes + meningitis). Corrected 2026-06-07. |

🔁 **Corrected yield: 3/5 years (2024, 2023, 2022)** — NOT 5/5 as the map previously claimed. Still high-value (9 marks, Section B) when it appears, always paired with a Fuzzy Logic/Uncertainty short-notes sub-part (2024, 2022) or a numerical (2023). The only numerical asked so far (2023 Q8b) is structurally identical to the **Han & Kamber Example 9.1** worked example — see `NeuralNet_Solutions.tex` for the full step-by-step reproduction.

## Weak spots / common mistakes
- Computing hidden-unit error *before* the output-unit error exists — backprop must go output→hidden, in that order.
- Forgetting that if an input $x_i = 0$, then $\Delta w$ for weights *leaving* that unit is exactly $0$ (don't recompute as nonzero).
- Generic "ANN = artificial brain" definitions score low — name the structural mapping (soma/dendrite/axon/synapse ↔ node/input/output/weight) explicitly.
- Conflating supervised (has labelled targets) / unsupervised (finds structure, no targets) / reinforcement (delayed reward signal) — always give one concrete example per type.
- Treating this as a guaranteed-every-year topic (it's 3/5) — don't let it crowd out Bayes/BN, FOL, or Planning (all 5/5).

## Related topics
[[wiki/bayes_networks|Bayes + Bayesian Networks]] · [[wiki/fuzzy_logic|Fuzzy Logic + Uncertainty]]
