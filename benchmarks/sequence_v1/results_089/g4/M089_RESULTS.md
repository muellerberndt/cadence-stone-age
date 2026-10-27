# Cadence 0.89 memory readings (development founders)

## route4-hidden

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults_big | 20 | 0.093 | 0.00 | -0.008 [-0.024, +0.009] | 9/10 | 0 | 0 |
| founder | episodic | 20 | 0.101 | 0.00 |  |  | 0 | 0 |
| founder | episodic_big | 20 | 0.093 | 0.00 | -0.008 [-0.024, +0.009] | 9/10 | 0 | 0 |
| founder | recall | 20 | 0.060 | 0.03 | -0.041 [-0.057, -0.026] | 2/16 | 0 | 0 |
| founder | recall_big | 20 | 0.073 | 0.03 | -0.028 [-0.043, -0.012] | 4/15 | 0 | 0 |
| founder | episodic_recall | 20 | 0.060 | 0.03 | -0.041 [-0.057, -0.026] | 2/16 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.067 | 0.00 | -0.034 [-0.053, -0.014] | 3/16 | 0 | 0 |
| founder | episodic_recall_big | 20 | 0.073 | 0.03 | -0.028 [-0.043, -0.012] | 4/15 | 0 | 0 |
| founder | episodic_recall_h2_big | 20 | 0.057 | 0.00 | -0.044 [-0.063, -0.023] | 3/16 | 0 | 0 |
| random | defaults_big | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.090 | nan |  |  | 0 | 0 |
| random | episodic_big | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_big | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_big | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2_big | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | defaults_big | 20 | 0.166 | 0.00 | -0.370 [-0.440, -0.296] | 1/19 | 3716 | 83612 |
| guide_step_1920 | episodic | 20 | 0.536 | 0.42 |  |  | 2706 | 85255 |
| guide_step_1920 | episodic_big | 20 | 0.586 | 0.55 | +0.050 [-0.054, +0.175] | 9/9 | 2723 | 60597 |
| guide_step_1920 | recall | 20 | 0.365 | 0.28 | -0.171 [-0.307, -0.027] | 4/16 | 3291 | 56625 |
| guide_step_1920 | recall_big | 20 | 0.531 | 0.50 | -0.005 [-0.193, +0.175] | 10/9 | 3279 | 53834 |
| guide_step_1920 | episodic_recall | 20 | 0.639 | 0.60 | +0.103 [-0.021, +0.243] | 12/7 | 2697 | 47454 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.720 | 0.72 | +0.184 [+0.049, +0.313] | 15/5 | 2744 | 48550 |
| guide_step_1920 | episodic_recall_big | 20 | 0.681 | 0.65 | +0.145 [+0.037, +0.256] | 11/9 | 2723 | 46494 |
| guide_step_1920 | episodic_recall_h2_big | 20 | 0.655 | 0.60 | +0.119 [+0.003, +0.256] | 13/7 | 2690 | 35988 |
| natural_live_1920 | defaults_big | 20 | 0.000 | 0.00 | -0.193 [-0.270, -0.122] | 0/20 | 0 | 0 |
| natural_live_1920 | episodic | 20 | 0.193 | 0.05 |  |  | 0 | 0 |
| natural_live_1920 | episodic_big | 20 | 0.178 | 0.03 | -0.015 [-0.121, +0.090] | 11/9 | 0 | 0 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 | -0.193 [-0.270, -0.122] | 0/20 | 0 | 0 |
| natural_live_1920 | recall_big | 20 | 0.000 | 0.00 | -0.193 [-0.270, -0.122] | 0/20 | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.328 | 0.20 | +0.136 [+0.012, +0.253] | 13/7 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.206 | 0.03 | +0.013 [-0.084, +0.109] | 12/8 | 0 | 0 |
| natural_live_1920 | episodic_recall_big | 20 | 0.225 | 0.10 | +0.032 [-0.086, +0.149] | 10/10 | 0 | 0 |
| natural_live_1920 | episodic_recall_h2_big | 20 | 0.194 | 0.12 | +0.001 [-0.117, +0.125] | 9/11 | 0 | 0 |

## view4-hidden

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults_big | 20 | 0.113 | 0.00 | -0.012 [-0.033, +0.008] | 7/11 | 0 | 0 |
| founder | episodic | 20 | 0.125 | 0.00 |  |  | 0 | 0 |
| founder | episodic_big | 20 | 0.113 | 0.00 | -0.012 [-0.033, +0.008] | 7/11 | 0 | 0 |
| founder | recall | 20 | 0.073 | 0.00 | -0.053 [-0.075, -0.028] | 2/18 | 0 | 0 |
| founder | recall_big | 20 | 0.083 | 0.00 | -0.042 [-0.072, -0.014] | 6/13 | 0 | 0 |
| founder | episodic_recall | 20 | 0.073 | 0.00 | -0.053 [-0.075, -0.028] | 2/18 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.074 | 0.00 | -0.052 [-0.074, -0.030] | 3/16 | 0 | 0 |
| founder | episodic_recall_big | 20 | 0.083 | 0.00 | -0.042 [-0.072, -0.014] | 6/13 | 0 | 0 |
| founder | episodic_recall_h2_big | 20 | 0.076 | 0.00 | -0.049 [-0.083, -0.018] | 6/14 | 0 | 0 |
| random | defaults_big | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | episodic_big | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_big | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_big | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2_big | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2_big | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults_big | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic | 20 | 0.224 | nan |  |  | 0 | 0 |
| searcher | episodic_big | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_big | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_r0 | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_big | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_h2_big | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_480 | defaults_big | 20 | 0.235 | 0.00 | -0.632 [-0.693, -0.569] | 0/20 | 1079 | 27226 |
| corrective_step_480 | episodic | 20 | 0.867 | 0.65 |  |  | 617 | 23116 |
| corrective_step_480 | episodic_big | 20 | 0.723 | 0.60 | -0.144 [-0.327, +0.029] | 8/11 | 595 | 10906 |
| corrective_step_480 | recall | 20 | 0.584 | 0.50 | -0.282 [-0.492, -0.075] | 7/12 | 765 | 12399 |
| corrective_step_480 | recall_big | 20 | 0.451 | 0.25 | -0.415 [-0.589, -0.227] | 3/15 | 898 | 13363 |
| corrective_step_480 | episodic_recall | 20 | 0.901 | 0.85 | +0.035 [-0.100, +0.138] | 14/2 | 394 | 6556 |
| corrective_step_480 | episodic_recall_r0 | 20 | 0.913 | 0.85 | +0.046 [-0.093, +0.163] | 14/2 | 396 | 6016 |
| corrective_step_480 | episodic_recall_big | 20 | 0.925 | 0.70 | +0.058 [-0.026, +0.145] | 12/7 | 438 | 6270 |
| corrective_step_480 | episodic_recall_h2_big | 20 | 0.916 | 0.65 | +0.050 [-0.034, +0.135] | 12/5 | 487 | 6443 |
| corrective_step_1920 | defaults_big | 20 | 0.202 | 0.00 | -0.754 [-0.812, -0.696] | 0/20 | 4209 | 76989 |
| corrective_step_1920 | episodic | 20 | 0.957 | 0.95 |  |  | 1543 | 69892 |
| corrective_step_1920 | episodic_big | 20 | 0.924 | 0.85 | -0.033 [-0.128, +0.038] | 6/8 | 1480 | 26139 |
| corrective_step_1920 | recall | 20 | 0.647 | 0.60 | -0.310 [-0.497, -0.134] | 5/12 | 2498 | 38497 |
| corrective_step_1920 | recall_big | 20 | 0.494 | 0.35 | -0.463 [-0.613, -0.303] | 2/16 | 3217 | 42442 |
| corrective_step_1920 | episodic_recall | 20 | 0.984 | 1.00 | +0.027 [-0.012, +0.072] | 7/6 | 741 | 11501 |
| corrective_step_1920 | episodic_recall_r0 | 20 | 0.994 | 1.00 | +0.036 [+0.003, +0.079] | 9/4 | 740 | 11021 |
| corrective_step_1920 | episodic_recall_big | 20 | 0.988 | 0.95 | +0.030 [+0.005, +0.068] | 9/2 | 1041 | 14204 |
| corrective_step_1920 | episodic_recall_h2_big | 20 | 0.948 | 0.95 | -0.009 [-0.113, +0.065] | 8/5 | 1244 | 15708 |
| natural_live_1920 | defaults_big | 20 | 0.029 | 0.00 | -0.831 [-0.887, -0.766] | 0/20 | 0 | 0 |
| natural_live_1920 | episodic | 20 | 0.860 | 1.00 |  |  | 0 | 0 |
| natural_live_1920 | episodic_big | 20 | 0.868 | 1.00 | +0.008 [-0.058, +0.084] | 6/14 | 0 | 0 |
| natural_live_1920 | recall | 20 | 0.045 | 0.05 | -0.815 [-0.886, -0.731] | 0/20 | 0 | 0 |
| natural_live_1920 | recall_big | 20 | 0.017 | 0.00 | -0.844 [-0.897, -0.780] | 0/20 | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.879 | 1.00 | +0.019 [-0.060, +0.102] | 10/10 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.830 | 1.00 | -0.030 [-0.126, +0.064] | 8/12 | 0 | 0 |
| natural_live_1920 | episodic_recall_big | 20 | 0.886 | 1.00 | +0.026 [-0.054, +0.105] | 12/8 | 0 | 0 |
| natural_live_1920 | episodic_recall_h2_big | 20 | 0.921 | 1.00 | +0.061 [+0.001, +0.130] | 11/8 | 0 | 0 |

