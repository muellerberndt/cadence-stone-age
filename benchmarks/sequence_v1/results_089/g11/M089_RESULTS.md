# Cadence 0.89 memory readings (development founders)

## view11-hidden

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.121 | 0.00 |  |  | 0 | 0 |
| founder | recall | 20 | 0.080 | 0.05 | -0.041 [-0.056, -0.027] | 0/18 | 0 | 0 |
| founder | recall_nopos | 20 | 0.080 | 0.05 | -0.041 [-0.056, -0.027] | 0/18 | 0 | 0 |
| founder | episodic | 20 | 0.121 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall | 20 | 0.080 | 0.05 | -0.041 [-0.056, -0.027] | 0/18 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.134 | nan |  |  | 0 | 0 |
| searcher | recall | 20 | 0.134 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.134 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 20 | 0.134 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.134 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.062 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | recall | 20 | 0.030 | 0.05 | -0.032 [-0.073, +0.009] | 2/8 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.030 | 0.05 | -0.032 [-0.073, +0.009] | 2/8 | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.202 | 0.15 | +0.140 [+0.013, +0.295] | 14/4 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.257 | 0.25 | +0.195 [+0.053, +0.354] | 15/4 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.235 | 0.05 |  |  | 275 | 4485 |
| corrective_step_120 | recall | 20 | 0.471 | 0.45 | +0.235 [+0.088, +0.388] | 14/5 | 251 | 3984 |
| corrective_step_120 | recall_nopos | 20 | 0.658 | 0.70 | +0.423 [+0.265, +0.575] | 15/4 | 246 | 3933 |
| corrective_step_120 | episodic | 20 | 0.893 | 0.90 | +0.657 [+0.567, +0.737] | 20/0 | 144 | 3204 |
| corrective_step_120 | episodic_recall | 20 | 0.926 | 0.90 | +0.691 [+0.610, +0.758] | 20/0 | 110 | 1796 |
| corrective_step_480 | defaults | 20 | 0.269 | 0.10 |  |  | 977 | 24646 |
| corrective_step_480 | recall | 20 | 0.554 | 0.45 | +0.286 [+0.123, +0.460] | 15/4 | 748 | 11939 |
| corrective_step_480 | recall_nopos | 20 | 0.703 | 0.65 | +0.434 [+0.238, +0.632] | 14/6 | 643 | 9972 |
| corrective_step_480 | episodic | 20 | 0.950 | 0.90 | +0.682 [+0.546, +0.801] | 19/0 | 349 | 10664 |
| corrective_step_480 | episodic_recall | 20 | 0.988 | 1.00 | +0.720 [+0.595, +0.823] | 19/0 | 222 | 3893 |
| natural_live_480 | defaults | 20 | 0.048 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | recall | 20 | 0.052 | 0.05 | +0.004 [-0.051, +0.059] | 5/8 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.052 | 0.05 | +0.004 [-0.051, +0.059] | 5/8 | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.623 | 0.65 | +0.576 [+0.392, +0.744] | 18/2 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.637 | 0.60 | +0.589 [+0.443, +0.734] | 19/0 | 0 | 0 |

## view11-invisible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.115 | 0.00 |  |  | 0 | 0 |
| founder | recall | 20 | 0.102 | 0.00 | -0.013 [-0.032, +0.007] | 5/12 | 0 | 0 |
| founder | recall_nopos | 20 | 0.102 | 0.00 | -0.013 [-0.032, +0.007] | 5/12 | 0 | 0 |
| founder | episodic | 20 | 0.115 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall | 20 | 0.102 | 0.00 | -0.013 [-0.032, +0.007] | 5/12 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.136 | nan |  |  | 0 | 0 |
| searcher | recall | 20 | 0.136 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.136 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 20 | 0.136 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.136 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.184 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | recall | 20 | 0.023 | 0.00 | -0.162 [-0.219, -0.099] | 2/14 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.023 | 0.00 | -0.162 [-0.219, -0.099] | 2/14 | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.248 | 0.15 | +0.064 [-0.055, +0.191] | 10/8 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.320 | 0.30 | +0.135 [-0.045, +0.330] | 9/10 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.378 | 0.15 |  |  | 268 | 4551 |
| corrective_step_120 | recall | 20 | 0.606 | 0.55 | +0.227 [+0.046, +0.406] | 14/6 | 252 | 3957 |
| corrective_step_120 | recall_nopos | 20 | 0.566 | 0.55 | +0.187 [+0.020, +0.361] | 12/8 | 247 | 4082 |
| corrective_step_120 | episodic | 20 | 0.862 | 0.75 | +0.483 [+0.325, +0.629] | 16/4 | 109 | 3040 |
| corrective_step_120 | episodic_recall | 20 | 0.984 | 1.00 | +0.606 [+0.501, +0.707] | 20/0 | 75 | 1462 |
| corrective_step_480 | defaults | 20 | 0.493 | 0.20 |  |  | 908 | 25305 |
| corrective_step_480 | recall | 20 | 0.739 | 0.70 | +0.245 [-0.011, +0.482] | 13/7 | 684 | 11368 |
| corrective_step_480 | recall_nopos | 20 | 0.845 | 0.80 | +0.352 [+0.120, +0.561] | 15/5 | 629 | 10394 |
| corrective_step_480 | episodic | 20 | 0.981 | 0.95 | +0.488 [+0.340, +0.625] | 18/2 | 261 | 8123 |
| corrective_step_480 | episodic_recall | 20 | 0.996 | 1.00 | +0.503 [+0.360, +0.636] | 19/0 | 119 | 2385 |
| natural_live_480 | defaults | 20 | 0.146 | 0.05 |  |  | 0 | 0 |
| natural_live_480 | recall | 20 | 0.202 | 0.25 | +0.057 [-0.064, +0.178] | 12/8 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.202 | 0.25 | +0.057 [-0.064, +0.178] | 12/8 | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.841 | 0.95 | +0.696 [+0.566, +0.815] | 19/1 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.648 | 0.70 | +0.503 [+0.323, +0.670] | 16/2 | 0 | 0 |

## view11-consecutive

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.112 | 0.00 |  |  | 0 | 0 |
| founder | recall | 20 | 0.092 | 0.00 | -0.019 [-0.038, +0.000] | 5/14 | 0 | 0 |
| founder | recall_nopos | 20 | 0.092 | 0.00 | -0.019 [-0.038, +0.000] | 5/14 | 0 | 0 |
| founder | episodic | 20 | 0.112 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall | 20 | 0.092 | 0.00 | -0.019 [-0.038, +0.000] | 5/14 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.137 | nan |  |  | 0 | 0 |
| searcher | recall | 20 | 0.137 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.137 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 20 | 0.137 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.137 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.074 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | recall | 20 | 0.028 | 0.00 | -0.047 [-0.090, -0.001] | 3/10 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.028 | 0.00 | -0.047 [-0.090, -0.001] | 3/10 | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.209 | 0.15 | +0.135 [+0.009, +0.276] | 11/7 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.221 | 0.10 | +0.147 [+0.011, +0.307] | 13/6 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.249 | 0.10 |  |  | 274 | 4958 |
| corrective_step_120 | recall | 20 | 0.381 | 0.35 | +0.132 [+0.013, +0.260] | 13/7 | 260 | 4122 |
| corrective_step_120 | recall_nopos | 20 | 0.545 | 0.55 | +0.296 [+0.122, +0.464] | 15/5 | 250 | 4040 |
| corrective_step_120 | episodic | 20 | 0.950 | 0.95 | +0.702 [+0.611, +0.784] | 20/0 | 109 | 3032 |
| corrective_step_120 | episodic_recall | 20 | 0.945 | 0.95 | +0.696 [+0.553, +0.812] | 19/1 | 84 | 1539 |
| corrective_step_480 | defaults | 20 | 0.371 | 0.20 |  |  | 971 | 21867 |
| corrective_step_480 | recall | 20 | 0.688 | 0.60 | +0.317 [+0.129, +0.490] | 15/3 | 765 | 12199 |
| corrective_step_480 | recall_nopos | 20 | 0.647 | 0.50 | +0.276 [+0.089, +0.450] | 13/6 | 719 | 11597 |
| corrective_step_480 | episodic | 20 | 0.985 | 1.00 | +0.614 [+0.496, +0.711] | 19/0 | 251 | 5766 |
| corrective_step_480 | episodic_recall | 20 | 0.987 | 0.95 | +0.616 [+0.496, +0.714] | 19/0 | 192 | 3567 |
| natural_live_480 | defaults | 20 | 0.062 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | recall | 20 | 0.108 | 0.05 | +0.046 [-0.015, +0.117] | 10/8 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.108 | 0.05 | +0.046 [-0.015, +0.117] | 10/8 | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.754 | 0.85 | +0.692 [+0.581, +0.790] | 20/0 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.528 | 0.60 | +0.467 [+0.296, +0.635] | 17/3 | 0 | 0 |

