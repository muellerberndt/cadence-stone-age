# Cadence 0.89 memory readings (development founders)

## route14-delay16

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.092 | 0.00 |  |  | 0 | 0 |
| founder | episodic_recall | 20 | 0.061 | 0.00 | -0.031 [-0.050, -0.012] | 5/15 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.060 | 0.00 | -0.032 [-0.052, -0.011] | 5/15 | 0 | 0 |
| founder | episodic_recall_h2 | 20 | 0.048 | 0.00 | -0.044 [-0.057, -0.031] | 2/17 | 0 | 0 |
| founder | recall_r0 | 20 | 0.060 | 0.00 | -0.032 [-0.052, -0.011] | 5/15 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.048 | 0.00 | -0.044 [-0.057, -0.031] | 2/18 | 0 | 0 |
| random | episodic | 20 | 0.094 | nan |  |  | 0 | 0 |
| random | episodic_recall | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | episodic | 20 | 0.450 | 0.38 |  |  | 2900 | 118078 |
| guide_step_1920 | episodic_recall | 20 | 0.433 | 0.42 | -0.017 [-0.093, +0.046] | 12/7 | 2699 | 48964 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.485 | 0.53 | +0.035 [-0.019, +0.096] | 13/7 | 2748 | 42184 |
| guide_step_1920 | episodic_recall_h2 | 20 | 0.486 | 0.38 | +0.036 [-0.046, +0.124] | 12/8 | 2725 | 38318 |
| guide_step_1920 | recall_r0 | 20 | 0.652 | 0.57 | +0.202 [+0.040, +0.353] | 14/6 | 3221 | 62916 |
| guide_step_1920 | recall_h2_r0 | 20 | 0.592 | 0.53 | +0.142 [-0.006, +0.288] | 13/7 | 3158 | 55517 |
| natural_live_1920 | episodic | 20 | 0.254 | 0.12 |  |  | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.246 | 0.07 | -0.008 [-0.108, +0.089] | 11/9 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.228 | 0.07 | -0.026 [-0.142, +0.089] | 10/9 | 0 | 0 |
| natural_live_1920 | episodic_recall_h2 | 20 | 0.258 | 0.12 | +0.004 [-0.133, +0.139] | 11/9 | 0 | 0 |
| natural_live_1920 | recall_r0 | 20 | 0.000 | 0.00 | -0.254 [-0.342, -0.167] | 0/20 | 0 | 0 |
| natural_live_1920 | recall_h2_r0 | 20 | 0.000 | 0.00 | -0.254 [-0.342, -0.167] | 0/20 | 0 | 0 |

## route14-delay2

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.093 | 0.00 |  |  | 0 | 0 |
| founder | episodic_recall | 20 | 0.058 | 0.00 | -0.036 [-0.050, -0.022] | 2/18 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.060 | 0.00 | -0.033 [-0.049, -0.017] | 3/15 | 0 | 0 |
| founder | episodic_recall_h2 | 20 | 0.050 | 0.00 | -0.043 [-0.059, -0.026] | 2/17 | 0 | 0 |
| founder | recall_r0 | 20 | 0.060 | 0.00 | -0.033 [-0.049, -0.017] | 3/15 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.052 | 0.00 | -0.041 [-0.057, -0.024] | 2/17 | 0 | 0 |
| random | episodic | 20 | 0.097 | nan |  |  | 0 | 0 |
| random | episodic_recall | 20 | 0.097 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.097 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 20 | 0.097 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_r0 | 20 | 0.097 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.097 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | episodic | 20 | 0.548 | 0.50 |  |  | 2806 | 109445 |
| guide_step_1920 | episodic_recall | 20 | 0.724 | 0.68 | +0.176 [+0.044, +0.313] | 14/6 | 2707 | 53106 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.781 | 0.75 | +0.233 [+0.099, +0.359] | 16/4 | 2683 | 55178 |
| guide_step_1920 | episodic_recall_h2 | 20 | 0.681 | 0.65 | +0.133 [+0.026, +0.236] | 12/8 | 2658 | 41395 |
| guide_step_1920 | recall_r0 | 20 | 0.565 | 0.42 | +0.017 [-0.147, +0.183] | 9/10 | 3245 | 64989 |
| guide_step_1920 | recall_h2_r0 | 20 | 0.628 | 0.53 | +0.080 [-0.103, +0.257] | 13/7 | 3181 | 49894 |
| natural_live_1920 | episodic | 20 | 0.281 | 0.15 |  |  | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.220 | 0.12 | -0.061 [-0.184, +0.064] | 8/12 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.126 | 0.05 | -0.156 [-0.265, -0.039] | 7/13 | 0 | 0 |
| natural_live_1920 | episodic_recall_h2 | 20 | 0.275 | 0.15 | -0.007 [-0.128, +0.116] | 9/11 | 0 | 0 |
| natural_live_1920 | recall_r0 | 20 | 0.000 | 0.00 | -0.281 [-0.359, -0.202] | 0/19 | 0 | 0 |
| natural_live_1920 | recall_h2_r0 | 20 | 0.000 | 0.00 | -0.281 [-0.359, -0.202] | 0/19 | 0 | 0 |

