# CSE 711 — Compiler · Past-Paper Question Map
> Source: `Compilers Previous Year Questions(2024-2016).pdf` — 8 years (2024, 2023, 2022, 2021, 2020, 2018, 2017, 2016). 2019/2015 not in file.
> Read once during 2026-06-18 reset. Do not re-OCR — this file is the cache.

## Topic 1 — Lexical Analysis
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q2c, Q2d | token/pattern/lexeme relation; scanning vs parsing + lexer/parser tools | 2+2 |
| 2024 | Q2b | RE→CFG: `(a\|b)*abb` | 3 |
| 2023 | A-1a | regular definitions for unsigned numbers, vowel-ordered strings | 2 |
| 2023 | A-1c | symbol table role + components + C hash-table impl | 4 |
| 2023 | A-4a, A-4c | scanning vs parsing tools; RE→CFG `(a\|b)*abb` | 2+2 |
| 2022 | A-2 | error recovery in syntax analysis; token/pattern/lexeme; RE→transition diagram `(a\|b)*abb(a\|b)` | 3+3+3 |
| 2021 | Q3a | token, pattern, lexeme intro | 3 |
| 2020 | — | (none directly — error recovery is parsing-adjacent) | — |
| 2018 | Q2a | token/pattern/lexeme | — |
| 2017 | Q1b | token vs lexeme, input buffers | 3 |
| 2016 | Q2a | token/pattern/lexeme w/ examples | 2.25 |

## Topic 2 — Top-Down Parsing
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q3b,c,d | syntax tree construction; leftmost/rightmost derivation; ambiguity demo | 2+4+1 |
| 2024 | Q4a,b,c,d | top-down vs bottom-up compare; recursive-descent + error recovery; left recursion elim; terminals/nonterminals/start-symbol | 2.5+2.5+3+1.5 |
| 2023 | A-2a,b | left factor + left-recursion elim + suitability for top-down; recursive-descent parser construction | 4+5 |
| 2023 | A-3a,b | FIRST/FOLLOW + LL(1) table; error recovery in predictive parsing | 6+3 |
| 2023 | A-4b | **dangling-else** — show `matched_stmt` grammar still ambiguous | 5 |
| 2022 | A-3 | derive `aabbabbba` LMD+RMD; left recursion not a problem for bottom-up (why); eliminate left recursion; left factoring | 2+1+4+2 |
| 2022 | A-4 | recursive-descent how it works; FIRST/FOLLOW; partial LL(1) table fill-in | 3+3+3 |
| 2021 | Q2 | left-factor rexpr grammar; eliminate left recursion (4-step) | full Q |
| 2021 | B-1a,b,c | LR vs LL parser diff; verify LL(1); stack/input trace on `(id)*id` | 2+4+3 |
| 2020 | Q1b,c | left-recursion elimination (multi-step); error-recovery strategies | 3+1.75 |
| 2020 | Q2 | FIRST/FOLLOW; predictive parsing table; LL(1) check | 3+4+1.75 |
| 2018 | Q1a | error recovery strategies | — |
| 2017 | Q3 | predictive parsing transform; LL(1) table; trace `abab` | 2+3+3.75 |
| 2016 | Q3a | recursive-descent issue + write parser w/ scan()/err() | 3+2.75 |

## Topic 3 — Bottom-Up Parsing
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q6a,b | compare LR(0)/SLR/LR(1)/LALR; shift-reduce parse trace `(id+id)*id` | 1+3 |
| 2023 | B-1a,b | shift-reduce conflict types; semantic-action grammar w/ inherited/synth attrs + parse tree + yacc program | 2+2+2+3 |
| 2022 | (LL(1) table fill only — no full LR construction this year) | — | — |
| 2021 | B-2a | construct LR table for `S→AA, A→aA\|b` | 5+2+2 |
| 2020 | Q3a | LR(0) items + states for `S→(L)\|id, L→L,S\|S` | 1.75+5 |
| 2020 | Q4a | yacc/bison boolean-expr program | 5 |
| 2018 | Q4 | SLR sets of items + PDA/transition table + GOTO function | 2.75+3+3 |
| 2017 | Q5a,b | which parsers can parse a grammar; FIRST/FOLLOW + SLR(1)? | 2+3+3.75 |
| 2017 | Q6b | quad/triple/indirect-triple (cross-listed, see Topic 5) | 3.75 |
| 2016 | Q4 | CYK algorithm membership test (one-off, light) | 6 |
| 2016 | Q6b | canonical LR(1) DFA + Action/Goto table for `S'→S, S→0S1\|0` | 3.5+1.5 |

## Topic 4 — Syntax-Directed Translation
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q6c,d | synth/inherited def + S/L-attributed; build SDD + annotated parse tree for `3*5+4n` | 2+3 |
| 2023 | B-1b | non-terminal attribute inherited/synth table; annotated parse tree for `¬(A∧(A⇒B))`; yacc program | 2+2+3 |
| 2023 | B-2b | dependency graph for `3*5*2` | 2 |
| 2023 | B-3a | L-attributed vs S-attributed; classify given grammar | 5 |
| 2023 | B-3c | DAG for `-(a*b)+(c+d)-(a+b+c+d)` (cross-listed Topic 5/7) | 3 |
| 2022 | B-1b,c | LR table for `S→AA,A→aA|b`; synth/inherited def; dependency graph for `3·5·2` | 5+2+2 |
| 2021 | Q5 | synth/inherited def; SDT postfix→infix; annotated parse trees for `9-5+2`, `9-5*2` | 2+2.75+2.5 |
| 2020 | Q3b | differentiate synth vs inherited | 2 |
| 2018 | Q2c | synth/inherited + S/L-attributed | 2.75 |
| 2017 | Q4c | attribute grammar — list inherited/synth, L-attributed check (binary-number example) | 3.75 |
| 2016 | Q2c | SDD attributes inherited/synth + L-attributed determination | 2+2 |

## Topic 5 — Intermediate Code (TAC / quad / triple / array addressing)
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q8a,b | expr → TAC/quad/triple/indirect-triple; dot-product program → TAC (array addressing) | 4+3 |
| 2023 | B-2a,b | `-(a+b)*(c+d)+(a+b+c)` → quad/triple/indirect-triple; sieve-of-primes → TAC (array) | 3+4 |
| 2021 | B-3b,c | code-gen from TAC w/ arrays `x=a[i],y=b[i],z=x*y`; quad/triple/indirect-triple for `-(a*b)+(c+d)-(a+b+c+d)` | 3+3 |
| 2020 | Q7c | triples/quad/SSA differences | 3.75 |
| 2018 | Q6a | `a=b[i]+c[i]` → syntax tree + quad/triple/indirect-triple | 4+4 |
| 2017 | Q6b | `a*-(b+c)` → syntax tree + TAC | 3.75 |
| 2016 | B-2a | TAC for `-(a*b)+(c+d)-(a+b+c+d)`-style + DAG | (see also Topic 4) |

⚠️ No backpatching / truelist / falselist question found in any of the 8 years.

## Topic 6 — Runtime Environments
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | B-4a | Fibonacci `f(5)` recursive — full activation tree + stack snapshot at first `f(1)` return | 3+3 |
| 2023 | B-4 | Fibonacci recursive activation record order; activation tree; stack-frame diagrams; static vs dynamic storage + garbage collector | full Q |
| 2020 | Q8 | **mergesort** activation tree + activation records (exact match to professor's callout) | 2+3.75 |
| 2018 | Q7c, Q8b | runtime-stack/activation-record role; activation-record diagrams at point-one/point-two in nested C functions | 3+3 |
| 2017 | Q1a | environment/state mappings, static bindings | 2 |

## Topic 7 — Code Optimisation (Lc#8 in slide filename)
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q7c | basic block + flow graph definitions | 2 |
| 2024 | B-3a,b | CFG from 30-line TAC listing; objectives of optimization + apply all valid transforms to the flow graph | 2.5+5 |
| 2023 | B-2c | define copy propagation + advantage | 2 |
| 2023 | B-3a,b | CFG from TAC; apply optimizations in stages | 2.5+5 |
| 2021 | B-3a | basic blocks start-points from numbered TAC; name B1,B2…, draw CFG | 3+3.75 |
| 2020 | Q6a,b | basic-block start points + names + CFG; DAG for given basic block | 3+3.75+2 |
| 2018 | Q8b | basic blocks construct + flow graph (10-line TAC) | full Q |
| 2017 | Q8c | basic blocks construct + flow graph | 3 |
| 2016 | Q8 | bubble-sort TAC → flow graph + apply ALL optimization techniques in stages | full Q |

## Topic 8 — Code Generation (source slides pending — Lc#7 missing)
| Year | Q# | Ask | Marks |
|---|---|---|---|
| 2024 | Q8c | instruction-cost calc: `MOV b,R0 / ADD c,R0 / MOV R0,a` | 2 |
| 2021 | Q7b,c | reconstruct C function from x86-64 assembly (reverse codegen, one-off); stack frames/caller-vs-callee-saved registers | 3+3 |
| 2020 | Q5c | instruction-cost calc (same MOV/ADD pattern) | — |
| 2017 | Q6c | instruction-cost calc (same pattern) | — |

⚠️ No liveness-interval / interference-graph / loop-invariant-hoisting / strength-reduction question found in any of the 8 years. Re-check once Lc#7 slides are uploaded — may be new-syllabus content.
