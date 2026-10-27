# The Cadence 0.90.0 candidate against 0.89.0: ordered recall and the hidden route (27 October 2026)

## Question

The 0.90.0 candidate changes the founders of the recall memory:

- every head's position term adds a learned slope over age beside its bucket table, so one number per
  moment leans the read toward old or recent slots at every length;
- the table is exact to 64 ages and taught at the address rate, 0.01 (0.89.0: 32 exact ages at 0.1);
- the founder recency charge is 0 (0.89.0: 0.25);
- a composed recall brain is taught by surprise: a lesson moves only the rows the brain's own answer
  gets wrong (0.89.0: every row).

The 0.89.0 readings found two Stone Age worlds where the recall memory decides the result: the ordered
recall world, where a lesson teaches the read to look back to the first or the latest of two written
values, and the route cue shown once and then hidden. Does the candidate keep what 0.89.0 reached there?

## Setup

| | |
| --- | --- |
| Readings | the ordered recall world, taught (`teach_step`: 1536 episodes, 224 evaluation episodes), as grid 5; the route cue hidden behind two neutral events, guided (`guide_step`: 480 episodes, 200 evaluation episodes), as grid 2 |
| Protocols | `protocol-m090-recall-order.json` and `protocol-m090-route-hidden.json`: grid 5's and grid 2's protocols with new founders; the route protocol also carries grid 1's `recall` recipe |
| Recipes | `recall` and `recall_h2` (two heads); the same compose call under both libraries, each library bringing its own founders |
| Founders | 1101 to 1120, which no earlier reading used |
| R089 | the published `cadence-net==0.89.0` wheel (SHA-256 `7b27009d0affd2235026ca5f7b4776ba545c15d5c5a14a61c75e52b6df65b786`); package digest `53a9fcd2…` in every run's manifest |
| C090 | the 0.90.0 candidate, cadence source at commit `838bb49` (branch `recall-slope`), version 0.90.0; package digest `c4d184a2…` |
| Environment | Linux x86-64, Python 3.12.3, NumPy 2.5.4, one BLAS thread per runner process, 16 processes at once |
| Decision rule, stated before the run | the founder-paired mean difference C090 - R089 of sampled frozen success at least -0.03 for each recipe on each world |

160 runs, every one exited 0, in 17.5 minutes (about 100 seconds a run).

## Result

Sampled frozen success (greedy in brackets), mean over 20 founders; the difference is founder-paired,
bootstrap 95% (10,000 resamples, seed 31012). Uniform random answers the ordered recall query at 0.50.

| World | Recipe | R089 | C090 | C090 - R089 [95%] | Founders up / down |
| --- | --- | --- | --- | --- | --- |
| ordered recall, taught | `recall` | 0.990 (0.99) | 0.819 (0.93) | **-0.171 [-0.267, -0.080]** | 0 / 13 |
| ordered recall, taught | `recall_h2` | 0.986 (1.00) | 0.784 (0.89) | **-0.202 [-0.307, -0.095]** | 1 / 14 |
| route cue hidden, guided | `recall` | 0.473 (0.38) | 0.277 (0.30) | **-0.197 [-0.347, -0.050]** | 8 / 12 |
| route cue hidden, guided | `recall_h2` | 0.474 (0.40) | 0.248 (0.28) | **-0.226 [-0.370, -0.089]** | 7 / 13 |

**Verdict: the candidate falls short of 0.89.0 on both worlds and both recipes**, by 0.17 to 0.23; the
decision rule fails four times of four. On the ordered recall world the candidate's founders split: 11
of 20 answer at 0.95 to 1.00 with either recipe, 6 (`recall`) and 8 (`recall_h2`) stay at 0.48 to 0.55,
chance, and the rest lie between; the per-condition means are alike (0.78 to 0.83 for the first or the
latest value, adjacent writes or one event between). Every 0.89.0 founder but one answers at 0.98 or
above. Tables: [readings/M090_RESULTS.md](readings/M090_RESULTS.md), per founder in
[readings/m090-summary.json](readings/m090-summary.json).

## Diagnostic: which change moves the result (after the readings, same founders)

The candidate's `recall` recipe with one 0.89.0 setting restored at a time (`protocol-m090d-*.json`,
`memory_090.py jobs-diagnostic`), against `recall` under each library; founder-paired, bootstrap 95%.

| Recipe under the candidate | Ordered recall | - candidate | - 0.89.0 | Route hidden | - candidate | - 0.89.0 |
| --- | --- | --- | --- | --- | --- | --- |
| `recall`, as composed | 0.819 | | -0.171 | 0.277 | | -0.197 |
| lessons on every row | 0.867 | +0.048 [-0.106, +0.199] | -0.122 | **0.420** | **+0.143 [+0.042, +0.251]** | -0.053 [-0.241, +0.133] |
| recency 0.25 | 0.765 | -0.054 [-0.189, +0.085] | -0.225 | 0.291 | +0.014 [-0.070, +0.100] | -0.182 |
| 0.89.0's position term (32 exact ages at 0.1, no slope) | **0.935** | **+0.116 [+0.008, +0.223]** | -0.055 | 0.302 | +0.026 [-0.054, +0.121] | -0.171 |
| the table at 0.1, the slope kept | **0.931** | **+0.112 [+0.001, +0.220]** | -0.059 | 0.276 | -0.001 [-0.080, +0.084] | -0.197 |
| no slope, the table exact to 64 at 0.01 kept | 0.817 | -0.002 [-0.122, +0.117] | -0.173 | 0.248 | -0.028 [-0.114, +0.049] | -0.225 |
| every 0.89.0 setting | 0.990 | +0.171 [+0.080, +0.267] | +0.000 [+0.000, +0.000] | 0.473 | +0.197 [+0.050, +0.347] | +0.000 [+0.000, +0.000] |

**Reading.**
- With every 0.89.0 setting restored, the candidate reads exactly as 0.89.0 on each of the 40
  founder-worlds (every founder's difference is 0.000): the new code changes nothing but its founders.
- **Ordered recall: the table's rate.** Teaching the table at 0.1 with the slope kept recovers the
  candidate to 0.93, as 0.89.0's whole position term does; the slope itself neither helps nor harms here
  (0.82 with and without it). The slower table, 0.01, is where the candidate's loss on this world comes
  from; the remaining 0.06 to 0.89.0 goes with the other settings together.
- **Route cue: the lessons.** Lessons on every row recover the guided route from 0.28 to 0.42 (0.89.0:
  0.47). Under surprise lessons a guided brain is taught only where it errs, and the recall memory learns
  less from the guide in 480 episodes. The position term's changes do not move this world.
- The recency charge moves neither world.

Tables: [diagnostic/M090_DIAGNOSTIC.md](diagnostic/M090_DIAGNOSTIC.md),
[diagnostic/m090d-summary.json](diagnostic/m090d-summary.json). The two recipes that split the position
term were added to the diagnostic protocols after its first 160 runs; the other recipes are unchanged.
240 diagnostic runs, every one exited 0, in 25 minutes.

## Reproduce

From `benchmarks/sequence_v1/`, with each library in a directory of its own:

```bash
python memory_090.py derive && mkdir -p OUT && python memory_090.py jobs OUT
LIB_R089=<0.89.0 wheel install> LIB_C090=<candidate source>/src PY=python bash run_m090.sh OUT 16
python memory_090.py analyze OUT
python memory_090.py derive-diagnostic && mkdir -p DIAG && python memory_090.py jobs-diagnostic DIAG
LIB_R089=<...> LIB_C090=<...> PY=python bash run_m090.sh DIAG 16
python memory_090.py analyze-diagnostic OUT DIAG
```
