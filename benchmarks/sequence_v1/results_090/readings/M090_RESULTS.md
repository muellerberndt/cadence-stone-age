# Cadence 0.90 candidate against 0.89.0 (founders 1101 to 1120)

Frozen success, sampled (greedy), mean over founders; the difference C090 - R089 is founder-paired, bootstrap 95% (10,000 resamples, seed 31012).

## recall-order (teach_step)

| Recipe | Founders | R089 | C090 | C090 - R089 [95%] | Up/down | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| recall | 20 | 0.990 (0.99) | 0.819 (0.93) | -0.171 [-0.267, -0.080] | 0/13 | fails |
| recall_h2 | 20 | 0.986 (1.00) | 0.784 (0.89) | -0.202 [-0.307, -0.095] | 1/14 | fails |

Per condition, sampled (the first or the latest written value asked; adjacent writes or one neutral event between them):

| Recipe | Library | ask-first | ask-first-gap | ask-latest | ask-latest-gap |
| --- | --- | --- | --- | --- | --- |
| recall | R089 | 1.00 | 0.97 | 0.99 | 1.00 |
| recall | C090 | 0.80 | 0.83 | 0.83 | 0.82 |
| recall_h2 | R089 | 0.99 | 0.99 | 0.98 | 0.99 |
| recall_h2 | C090 | 0.79 | 0.78 | 0.79 | 0.78 |

## route-hidden (guide_step)

| Recipe | Founders | R089 | C090 | C090 - R089 [95%] | Up/down | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| recall | 20 | 0.473 (0.38) | 0.277 (0.30) | -0.197 [-0.347, -0.050] | 8/12 | fails |
| recall_h2 | 20 | 0.474 (0.40) | 0.248 (0.28) | -0.226 [-0.370, -0.089] | 7/13 | fails |

Libraries as the runs' manifests record them (version, package digest):

- R089: 0.89.0, `53a9fcd26333a4219c8f31bb64ef171a70c5e581f16df20e4edc2a3ede718d13`
- C090: 0.90.0, `c4d184a2f4aa3b1db27ab84f5c834973be5b0ffeb60ed8c5cb73ad7c3ea0c0f2`

Gate: the paired mean difference at least -0.03 for each recipe on each world: **fails**.

