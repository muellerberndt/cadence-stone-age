# Cadence 0.89 memory readings (development founders)

## view3-hidden

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 40 | 0.100 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 40 | 0.100 | 0.00 |  |  | 0 | 0 |
| founder | recall_quiet | 40 | 0.120 | 0.00 | +0.020 [+0.007, +0.033] | 26/10 | 0 | 0 |
| founder | recall_h2 | 40 | 0.066 | 0.00 | -0.034 [-0.046, -0.022] | 7/29 | 0 | 0 |
| founder | episodic | 40 | 0.112 | 0.00 | +0.012 [-0.002, +0.026] | 24/14 | 0 | 0 |
| founder | episodic_recall | 40 | 0.100 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_nopos | 40 | 0.100 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_h2 | 40 | 0.066 | 0.00 | -0.034 [-0.046, -0.022] | 7/29 | 0 | 0 |
| random | recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 40 | 0.118 | nan |  |  | 0 | 0 |
| random | recall_quiet | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_nopos | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 40 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_quiet | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_nopos | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 40 | 0.225 | nan |  |  | 0 | 0 |
| searcher | recall_quiet | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_nopos | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_h2 | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 40 | 0.452 | 0.38 | +0.040 [-0.091, +0.172] | 19/19 | 256 | 4311 |
| corrective_step_120 | recall_nopos | 40 | 0.412 | 0.28 |  |  | 255 | 4129 |
| corrective_step_120 | recall_quiet | 40 | 0.236 | 0.07 | -0.175 [-0.277, -0.075] | 12/27 | 274 | 4893 |
| corrective_step_120 | recall_h2 | 40 | 0.362 | 0.23 | -0.049 [-0.160, +0.060] | 20/17 | 261 | 3761 |
| corrective_step_120 | episodic | 40 | 0.647 | 0.28 | +0.235 [+0.084, +0.370] | 29/10 | 183 | 3259 |
| corrective_step_120 | episodic_recall | 40 | 0.757 | 0.50 | +0.345 [+0.190, +0.487] | 30/9 | 150 | 2321 |
| corrective_step_120 | episodic_recall_nopos | 40 | 0.710 | 0.55 | +0.298 [+0.170, +0.424] | 29/10 | 143 | 2238 |
| corrective_step_120 | episodic_recall_h2 | 40 | 0.794 | 0.53 | +0.383 [+0.247, +0.508] | 33/7 | 142 | 2114 |
| corrective_step_480 | recall | 40 | 0.606 | 0.53 | +0.077 [-0.079, +0.235] | 20/18 | 754 | 11606 |
| corrective_step_480 | recall_nopos | 40 | 0.529 | 0.42 |  |  | 807 | 12661 |
| corrective_step_480 | recall_quiet | 40 | 0.342 | 0.20 | -0.187 [-0.336, -0.033] | 11/29 | 961 | 18897 |
| corrective_step_480 | recall_h2 | 40 | 0.558 | 0.40 | +0.030 [-0.110, +0.168] | 19/18 | 795 | 11937 |
| corrective_step_480 | episodic | 40 | 0.829 | 0.72 | +0.299 [+0.160, +0.438] | 30/9 | 574 | 13472 |
| corrective_step_480 | episodic_recall | 40 | 0.936 | 0.82 | +0.407 [+0.298, +0.516] | 37/3 | 380 | 5939 |
| corrective_step_480 | episodic_recall_nopos | 40 | 0.938 | 0.90 | +0.409 [+0.276, +0.536] | 35/4 | 387 | 5793 |
| corrective_step_480 | episodic_recall_h2 | 40 | 0.941 | 0.88 | +0.412 [+0.287, +0.530] | 34/4 | 342 | 5007 |
| natural_live_480 | recall | 40 | 0.026 | 0.03 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_480 | recall_nopos | 40 | 0.026 | 0.03 |  |  | 0 | 0 |
| natural_live_480 | recall_quiet | 40 | 0.012 | 0.00 | -0.014 [-0.041, +0.007] | 10/10 | 0 | 0 |
| natural_live_480 | recall_h2 | 40 | 0.023 | 0.00 | -0.003 [-0.033, +0.025] | 12/10 | 0 | 0 |
| natural_live_480 | episodic | 40 | 0.843 | 0.90 | +0.817 [+0.757, +0.866] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall | 40 | 0.910 | 1.00 | +0.884 [+0.843, +0.918] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall_nopos | 40 | 0.910 | 1.00 | +0.884 [+0.843, +0.918] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall_h2 | 40 | 0.909 | 1.00 | +0.883 [+0.848, +0.913] | 40/0 | 0 | 0 |

## view3-invisible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 40 | 0.097 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 40 | 0.097 | 0.00 |  |  | 0 | 0 |
| founder | recall_quiet | 40 | 0.115 | 0.00 | +0.018 [+0.007, +0.029] | 25/12 | 0 | 0 |
| founder | recall_h2 | 40 | 0.085 | 0.00 | -0.011 [-0.027, +0.005] | 18/21 | 0 | 0 |
| founder | episodic | 40 | 0.116 | 0.00 | +0.019 [+0.004, +0.034] | 21/12 | 0 | 0 |
| founder | episodic_recall | 40 | 0.097 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_nopos | 40 | 0.097 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_h2 | 40 | 0.085 | 0.00 | -0.011 [-0.027, +0.005] | 18/21 | 0 | 0 |
| random | recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 40 | 0.118 | nan |  |  | 0 | 0 |
| random | recall_quiet | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_nopos | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 40 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_quiet | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_nopos | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 40 | 0.308 | nan |  |  | 0 | 0 |
| searcher | recall_quiet | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_nopos | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_h2 | 40 | 0.308 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 40 | 0.462 | 0.15 | +0.003 [-0.123, +0.129] | 20/20 | 255 | 4414 |
| corrective_step_120 | recall_nopos | 40 | 0.459 | 0.28 |  |  | 257 | 3984 |
| corrective_step_120 | recall_quiet | 40 | 0.360 | 0.07 | -0.099 [-0.213, +0.012] | 14/24 | 268 | 4499 |
| corrective_step_120 | recall_h2 | 40 | 0.433 | 0.05 | -0.026 [-0.147, +0.094] | 16/24 | 262 | 3764 |
| corrective_step_120 | episodic | 40 | 0.885 | 0.47 | +0.426 [+0.320, +0.528] | 36/4 | 156 | 3142 |
| corrective_step_120 | episodic_recall | 40 | 0.769 | 0.50 | +0.309 [+0.187, +0.426] | 32/8 | 146 | 2658 |
| corrective_step_120 | episodic_recall_nopos | 40 | 0.887 | 0.65 | +0.427 [+0.324, +0.528] | 34/6 | 145 | 2480 |
| corrective_step_120 | episodic_recall_h2 | 40 | 0.838 | 0.47 | +0.379 [+0.283, +0.475] | 35/5 | 147 | 2390 |
| corrective_step_480 | recall | 40 | 0.731 | 0.30 | +0.142 [-0.005, +0.288] | 22/17 | 752 | 12404 |
| corrective_step_480 | recall_nopos | 40 | 0.590 | 0.25 |  |  | 791 | 12396 |
| corrective_step_480 | recall_quiet | 40 | 0.340 | 0.05 | -0.249 [-0.396, -0.098] | 11/27 | 956 | 17645 |
| corrective_step_480 | recall_h2 | 40 | 0.732 | 0.33 | +0.143 [+0.012, +0.279] | 24/15 | 824 | 11851 |
| corrective_step_480 | episodic | 40 | 0.950 | 0.85 | +0.360 [+0.239, +0.487] | 31/8 | 426 | 8671 |
| corrective_step_480 | episodic_recall | 40 | 0.960 | 1.00 | +0.370 [+0.253, +0.492] | 33/6 | 317 | 5966 |
| corrective_step_480 | episodic_recall_nopos | 40 | 0.961 | 0.97 | +0.371 [+0.250, +0.497] | 31/7 | 297 | 5237 |
| corrective_step_480 | episodic_recall_h2 | 40 | 0.948 | 0.97 | +0.358 [+0.226, +0.489] | 32/5 | 303 | 5085 |
| natural_live_480 | recall | 40 | 0.119 | 0.05 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_480 | recall_nopos | 40 | 0.119 | 0.05 |  |  | 0 | 0 |
| natural_live_480 | recall_quiet | 40 | 0.119 | 0.05 | +0.000 [-0.055, +0.057] | 13/19 | 0 | 0 |
| natural_live_480 | recall_h2 | 40 | 0.083 | 0.03 | -0.036 [-0.089, +0.019] | 8/19 | 0 | 0 |
| natural_live_480 | episodic | 40 | 0.311 | 0.12 | +0.192 [+0.088, +0.296] | 29/10 | 0 | 0 |
| natural_live_480 | episodic_recall | 40 | 0.212 | 0.12 | +0.092 [+0.009, +0.184] | 26/12 | 0 | 0 |
| natural_live_480 | episodic_recall_nopos | 40 | 0.212 | 0.12 | +0.092 [+0.009, +0.184] | 26/12 | 0 | 0 |
| natural_live_480 | episodic_recall_h2 | 40 | 0.242 | 0.15 | +0.123 [+0.030, +0.221] | 26/11 | 0 | 0 |

## view3-visible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 40 | 0.092 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 40 | 0.092 | 0.00 |  |  | 0 | 0 |
| founder | recall_quiet | 40 | 0.117 | 0.00 | +0.024 [+0.012, +0.036] | 30/7 | 0 | 0 |
| founder | recall_h2 | 40 | 0.079 | 0.00 | -0.014 [-0.027, +0.000] | 10/27 | 0 | 0 |
| founder | episodic | 40 | 0.119 | 0.00 | +0.026 [+0.009, +0.042] | 26/12 | 0 | 0 |
| founder | episodic_recall | 40 | 0.092 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_nopos | 40 | 0.092 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_h2 | 40 | 0.079 | 0.00 | -0.014 [-0.027, +0.000] | 10/27 | 0 | 0 |
| random | recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 40 | 0.118 | nan |  |  | 0 | 0 |
| random | recall_quiet | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_nopos | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 40 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_quiet | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_nopos | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 40 | 0.297 | nan |  |  | 0 | 0 |
| searcher | recall_quiet | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_nopos | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_h2 | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 40 | 0.667 | 0.50 | -0.047 [-0.164, +0.072] | 16/22 | 225 | 3660 |
| corrective_step_120 | recall_nopos | 40 | 0.714 | 0.53 |  |  | 232 | 3918 |
| corrective_step_120 | recall_quiet | 40 | 0.551 | 0.42 | -0.163 [-0.276, -0.052] | 11/28 | 245 | 4377 |
| corrective_step_120 | recall_h2 | 40 | 0.676 | 0.53 | -0.037 [-0.157, +0.081] | 16/23 | 227 | 3519 |
| corrective_step_120 | episodic | 40 | 0.987 | 0.97 | +0.273 [+0.187, +0.362] | 37/2 | 39 | 885 |
| corrective_step_120 | episodic_recall | 40 | 0.947 | 0.93 | +0.233 [+0.134, +0.329] | 36/2 | 29 | 537 |
| corrective_step_120 | episodic_recall_nopos | 40 | 0.971 | 0.97 | +0.258 [+0.151, +0.361] | 36/1 | 30 | 537 |
| corrective_step_120 | episodic_recall_h2 | 40 | 0.997 | 1.00 | +0.283 [+0.195, +0.374] | 36/1 | 30 | 505 |
| corrective_step_480 | recall | 40 | 0.800 | 0.62 | -0.001 [-0.118, +0.116] | 19/19 | 643 | 10427 |
| corrective_step_480 | recall_nopos | 40 | 0.801 | 0.72 |  |  | 624 | 10262 |
| corrective_step_480 | recall_quiet | 40 | 0.616 | 0.47 | -0.185 [-0.337, -0.038] | 15/21 | 736 | 12872 |
| corrective_step_480 | recall_h2 | 40 | 0.839 | 0.78 | +0.038 [-0.100, +0.172] | 19/15 | 602 | 9075 |
| corrective_step_480 | episodic | 40 | 0.975 | 0.93 | +0.175 [+0.084, +0.274] | 27/4 | 115 | 2651 |
| corrective_step_480 | episodic_recall | 40 | 0.999 | 1.00 | +0.199 [+0.112, +0.293] | 28/0 | 62 | 1094 |
| corrective_step_480 | episodic_recall_nopos | 40 | 0.997 | 1.00 | +0.196 [+0.109, +0.291] | 29/1 | 61 | 1056 |
| corrective_step_480 | episodic_recall_h2 | 40 | 0.998 | 1.00 | +0.198 [+0.111, +0.292] | 29/2 | 61 | 997 |
| natural_live_480 | recall | 40 | 0.152 | 0.07 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_480 | recall_nopos | 40 | 0.152 | 0.07 |  |  | 0 | 0 |
| natural_live_480 | recall_quiet | 40 | 0.150 | 0.10 | -0.003 [-0.096, +0.089] | 14/18 | 0 | 0 |
| natural_live_480 | recall_h2 | 40 | 0.130 | 0.07 | -0.023 [-0.111, +0.069] | 10/20 | 0 | 0 |
| natural_live_480 | episodic | 40 | 0.987 | 1.00 | +0.834 [+0.759, +0.899] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall | 40 | 0.989 | 1.00 | +0.836 [+0.761, +0.902] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall_nopos | 40 | 0.989 | 1.00 | +0.836 [+0.761, +0.902] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall_h2 | 40 | 0.981 | 1.00 | +0.828 [+0.754, +0.893] | 40/0 | 0 | 0 |

