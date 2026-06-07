# Fuzzy Logic + Uncertainty
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
Fuzzy Logic (Zadeh, 1960s) is a problem-solving methodology that simulates human reasoning under *uncertainty* using fuzzy sets, where membership grades range continuously over [0,1] instead of the strict 0/1 of Boolean logic.

## Key steps / algorithm
**Crisp vs fuzzy sets:** Boolean = instantaneous transition (in/out); Fuzzy = gradual transition via a *membership function* $m_A(x) \in [0,1]$ — an object can be partially in multiple sets at once.

**Fuzzy Decision Process — 3 steps:**
1. **Fuzzification:** crisp input → fuzzy input. Assign linguistic labels (cold/cool/normal/warm/hot) via membership functions (trapezoidal/triangular most common). E.g. T=66°F → T_cool=0.2, T_normal=0.6.
2. **Fuzzy reasoning (Rule Evaluation, min-max inference):** evaluate IF-THEN rules. Rule strength = **min** of antecedents (fuzzy AND = intersection); fuzzy output for shared consequents = **max** of rule strengths (fuzzy OR = union). Fuzzy NOT: $m_{\bar A}(x)=1-m_A(x)$.
3. **Defuzzification:** fuzzy output → crisp output, via **Centre of Gravity (COG)**: $COG = \dfrac{\sum x \cdot m(x)}{\sum m(x)}$ (worked slide example → COG = 34.5).

**Soft Computing context:** Fuzzy Logic + Neural Networks + Genetic Algorithms = Soft Computing. Combining FL+NN → *neuro-fuzzy systems* (cooperative: NN tunes FL params; hybrid: FL rules built as fuzzy-neuron network).

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | B-Q8c (3 marks) | "Write short notes on: i) Fuzzy logic ii) Uncertainty" — inside NN question |
| 2022 | B-1d (2 marks) | "Write short notes on: i) Fuzzy logic ii) Uncertainty" — inside NN question |
🔁 Only 2/5 years (2020–2024) ask it — lowest yield topic. Always a 2–3 mark "short notes" sub-part bundled inside the Neural Networks question, always paired with Uncertainty. 2021/2020 do NOT ask it (verified — corrected a prior map error claiming "combined with NN").

**Uncertainty short note:** see [[wiki/bayes_networks|Bayes + BN]] for the full doorbell example, sources of uncertainty list, and Bayes' Theorem worked solutions — that page is authoritative for any Uncertainty numerical.

## Weak spots / common mistakes
- Confusing fuzzification (crisp→fuzzy, step 1) with defuzzification (fuzzy→crisp, step 3)
- Min-max is for rule evaluation/reasoning (step 2), NOT defuzzification (which uses COG)
- Writing a generic "what is uncertainty" answer without the doorbell example — examiners reward the named example
- Don't over-invest revision time here — low yield (2/5 years) vs Bayes/NN/FOL which appear every year

## Related topics
[[wiki/bayes_networks|Bayes + Bayesian Networks]] · [[wiki/neural_networks|Neural Networks + Learning]]
