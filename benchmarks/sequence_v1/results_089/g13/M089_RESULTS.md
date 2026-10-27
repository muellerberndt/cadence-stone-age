# Cadence 0.89 memory readings (development founders)

## route13-delay16

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.061 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.060 | 0.00 | -0.001 [-0.008, +0.006] | 7/9 | 0 | 0 |
| founder | recall_h2 | 20 | 0.048 | 0.00 | -0.013 [-0.029, +0.002] | 9/10 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.048 | 0.00 | -0.013 [-0.025, -0.002] | 8/12 | 0 | 0 |
| random | recall | 20 | 0.094 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | recall | 20 | 0.364 | 0.28 |  |  | 3033 | 54362 |
| guide_step_1920 | recall_r0 | 20 | 0.652 | 0.57 | +0.288 [+0.158, +0.405] | 16/4 | 3221 | 62916 |
| guide_step_1920 | recall_h2 | 20 | 0.437 | 0.38 | +0.073 [-0.057, +0.204] | 13/7 | 2943 | 46364 |
| guide_step_1920 | recall_h2_r0 | 20 | 0.592 | 0.53 | +0.228 [+0.056, +0.399] | 15/4 | 3158 | 55517 |

## recall13-order

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.498 | 0.50 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 20 | 0.498 | 0.50 |  |  | 0 | 0 |
| founder | recall_h2 | 20 | 0.489 | 0.49 | -0.009 [-0.018, +0.000] | 7/10 | 0 | 0 |
| founder | recall_h2_nopos | 20 | 0.489 | 0.49 | -0.009 [-0.018, +0.000] | 7/10 | 0 | 0 |
| random | recall | 20 | 0.508 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.508 | nan |  |  | 0 | 0 |
| random | recall_h2 | 20 | 0.508 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_nopos | 20 | 0.508 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 20 | 0.940 | 0.94 | +0.358 [+0.294, +0.415] | 19/1 | 1536 | 63805 |
| teach_step | recall_nopos | 20 | 0.582 | 0.65 |  |  | 1536 | 133726 |
| teach_step | recall_h2 | 20 | 0.995 | 1.00 | +0.413 [+0.371, +0.454] | 20/0 | 1536 | 60946 |
| teach_step | recall_h2_nopos | 20 | 0.688 | 0.69 | +0.105 [+0.030, +0.179] | 14/6 | 1536 | 122630 |
| reward_step | recall | 20 | 0.502 | 0.51 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| reward_step | recall_nopos | 20 | 0.502 | 0.51 |  |  | 0 | 0 |
| reward_step | recall_h2 | 20 | 0.500 | 0.50 | -0.002 [-0.013, +0.008] | 6/8 | 0 | 0 |
| reward_step | recall_h2_nopos | 20 | 0.500 | 0.50 | -0.002 [-0.013, +0.008] | 6/8 | 0 | 0 |
| reward_live | recall | 20 | 0.500 | 0.50 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| reward_live | recall_nopos | 20 | 0.500 | 0.50 |  |  | 0 | 0 |
| reward_live | recall_h2 | 20 | 0.491 | 0.50 | -0.009 [-0.017, -0.002] | 2/9 | 0 | 0 |
| reward_live | recall_h2_nopos | 20 | 0.491 | 0.50 | -0.009 [-0.017, -0.002] | 2/9 | 0 | 0 |

## view13-consecutive

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.078 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.110 | 0.00 | +0.033 [+0.011, +0.055] | 12/6 | 0 | 0 |
| founder | episodic_recall | 20 | 0.078 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.124 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.345 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.345 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.345 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 20 | 0.275 | 0.05 |  |  | 272 | 4130 |
| corrective_step_120 | episodic | 20 | 0.489 | 0.15 | +0.213 [+0.067, +0.348] | 15/5 | 205 | 3248 |
| corrective_step_120 | episodic_recall | 20 | 0.508 | 0.15 | +0.232 [+0.076, +0.383] | 15/5 | 208 | 3174 |
| natural_live_480 | recall | 20 | 0.038 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.079 | 0.00 | +0.041 [-0.009, +0.093] | 8/5 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.128 | 0.00 | +0.089 [+0.032, +0.150] | 12/4 | 0 | 0 |

## view13-consecutive-efference

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.088 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.118 | 0.05 | +0.030 [+0.011, +0.048] | 14/6 | 0 | 0 |
| founder | episodic_recall | 20 | 0.088 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.124 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.141 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.141 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.141 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 20 | 0.445 | 0.35 |  |  | 249 | 4105 |
| corrective_step_120 | episodic | 20 | 0.881 | 0.85 | +0.436 [+0.304, +0.565] | 20/0 | 115 | 2573 |
| corrective_step_120 | episodic_recall | 20 | 0.875 | 0.75 | +0.430 [+0.293, +0.571] | 20/0 | 98 | 1803 |
| natural_live_480 | recall | 20 | 0.082 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.745 | 0.75 | +0.663 [+0.508, +0.800] | 19/1 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.821 | 0.90 | +0.739 [+0.585, +0.868] | 18/2 | 0 | 0 |

## view13-invisible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.090 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.115 | 0.00 | +0.025 [+0.005, +0.045] | 12/6 | 0 | 0 |
| founder | episodic_recall | 20 | 0.090 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.124 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.322 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.322 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.322 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 20 | 0.533 | 0.25 |  |  | 258 | 4465 |
| corrective_step_120 | episodic | 20 | 0.731 | 0.25 | +0.198 [+0.007, +0.381] | 15/5 | 158 | 3208 |
| corrective_step_120 | episodic_recall | 20 | 0.796 | 0.50 | +0.262 [+0.118, +0.412] | 16/4 | 157 | 2868 |
| natural_live_480 | recall | 20 | 0.165 | 0.05 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.307 | 0.15 | +0.143 [-0.016, +0.309] | 13/7 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.289 | 0.10 | +0.124 [-0.020, +0.274] | 13/7 | 0 | 0 |

## view13-invisible-efference

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.099 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.117 | 0.05 | +0.018 [-0.003, +0.039] | 13/7 | 0 | 0 |
| founder | episodic_recall | 20 | 0.099 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.124 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.124 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.139 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.139 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.139 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 20 | 0.406 | 0.35 |  |  | 243 | 3798 |
| corrective_step_120 | episodic | 20 | 0.900 | 0.95 | +0.494 [+0.336, +0.646] | 17/1 | 102 | 2267 |
| corrective_step_120 | episodic_recall | 20 | 0.843 | 0.85 | +0.437 [+0.216, +0.628] | 17/3 | 84 | 1597 |
| natural_live_480 | recall | 20 | 0.161 | 0.15 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.599 | 0.55 | +0.439 [+0.246, +0.628] | 17/3 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.810 | 0.95 | +0.650 [+0.483, +0.780] | 19/1 | 0 | 0 |

