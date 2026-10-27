# Cadence 0.89 memory readings (development founders)

## route9-delay16

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.093 | 0.00 |  |  | 0 | 0 |
| founder | episodic_ctx08 | 20 | 0.093 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_ctx09 | 20 | 0.093 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_ctx09 | 20 | 0.068 | 0.03 | -0.025 [-0.040, -0.008] | 5/14 | 0 | 0 |
| founder | episodic_amp05 | 20 | 0.093 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_amp05 | 20 | 0.068 | 0.03 | -0.025 [-0.040, -0.008] | 5/14 | 0 | 0 |
| founder | recall | 20 | 0.068 | 0.03 | -0.025 [-0.040, -0.008] | 5/14 | 0 | 0 |
| random | episodic | 20 | 0.102 | nan |  |  | 0 | 0 |
| random | episodic_ctx08 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_ctx09 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_ctx09 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_amp05 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_amp05 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_ctx08 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_ctx09 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_ctx09 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_amp05 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_amp05 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | episodic | 20 | 0.430 | 0.35 |  |  | 2850 | 71234 |
| guide_step_1920 | episodic_ctx08 | 20 | 0.461 | 0.28 | +0.031 [-0.022, +0.086] | 13/6 | 2969 | 64665 |
| guide_step_1920 | episodic_ctx09 | 20 | 0.427 | 0.35 | -0.003 [-0.079, +0.071] | 11/9 | 3118 | 70777 |
| guide_step_1920 | episodic_recall_ctx09 | 20 | 0.469 | 0.42 | +0.038 [-0.015, +0.104] | 13/6 | 3078 | 46633 |
| guide_step_1920 | episodic_amp05 | 20 | 0.466 | 0.53 | +0.036 [-0.009, +0.087] | 11/8 | 2864 | 67273 |
| guide_step_1920 | episodic_recall_amp05 | 20 | 0.388 | 0.35 | -0.042 [-0.144, +0.051] | 11/9 | 2844 | 50281 |
| guide_step_1920 | recall | 20 | 0.410 | 0.30 | -0.021 [-0.134, +0.099] | 8/12 | 2991 | 54301 |
| natural_live_1920 | episodic | 20 | 0.168 | 0.03 |  |  | 0 | 0 |
| natural_live_1920 | episodic_ctx08 | 20 | 0.237 | 0.12 | +0.069 [-0.010, +0.148] | 14/6 | 0 | 0 |
| natural_live_1920 | episodic_ctx09 | 20 | 0.183 | 0.03 | +0.016 [-0.087, +0.120] | 8/12 | 0 | 0 |
| natural_live_1920 | episodic_recall_ctx09 | 20 | 0.292 | 0.23 | +0.124 [+0.021, +0.223] | 14/6 | 0 | 0 |
| natural_live_1920 | episodic_amp05 | 20 | 0.035 | 0.00 | -0.133 [-0.205, -0.064] | 2/16 | 0 | 0 |
| natural_live_1920 | episodic_recall_amp05 | 20 | 0.032 | 0.00 | -0.136 [-0.204, -0.075] | 2/18 | 0 | 0 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 | -0.168 [-0.236, -0.105] | 0/20 | 0 | 0 |

## route9-delay8

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.105 | 0.00 |  |  | 0 | 0 |
| founder | episodic_ctx08 | 20 | 0.105 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_ctx09 | 20 | 0.105 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_ctx09 | 20 | 0.069 | 0.03 | -0.037 [-0.055, -0.018] | 4/15 | 0 | 0 |
| founder | episodic_amp05 | 20 | 0.105 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_amp05 | 20 | 0.069 | 0.03 | -0.037 [-0.055, -0.018] | 4/15 | 0 | 0 |
| founder | recall | 20 | 0.069 | 0.03 | -0.037 [-0.055, -0.018] | 4/15 | 0 | 0 |
| random | episodic | 20 | 0.090 | nan |  |  | 0 | 0 |
| random | episodic_ctx08 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_ctx09 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_ctx09 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_amp05 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_amp05 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_ctx08 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_ctx09 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_ctx09 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_amp05 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_amp05 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | episodic | 20 | 0.467 | 0.42 |  |  | 2750 | 48871 |
| guide_step_1920 | episodic_ctx08 | 20 | 0.433 | 0.35 | -0.034 [-0.108, +0.036] | 8/12 | 2959 | 72703 |
| guide_step_1920 | episodic_ctx09 | 20 | 0.479 | 0.47 | +0.013 [-0.010, +0.037] | 12/8 | 3072 | 75537 |
| guide_step_1920 | episodic_recall_ctx09 | 20 | 0.544 | 0.45 | +0.077 [-0.012, +0.185] | 12/6 | 3050 | 52661 |
| guide_step_1920 | episodic_amp05 | 20 | 0.477 | 0.42 | +0.011 [-0.028, +0.053] | 13/7 | 2939 | 65095 |
| guide_step_1920 | episodic_recall_amp05 | 20 | 0.520 | 0.53 | +0.053 [-0.071, +0.178] | 12/8 | 2887 | 52980 |
| guide_step_1920 | recall | 20 | 0.587 | 0.47 | +0.120 [-0.008, +0.249] | 13/7 | 3132 | 59514 |
| natural_live_1920 | episodic | 20 | 0.213 | 0.05 |  |  | 0 | 0 |
| natural_live_1920 | episodic_ctx08 | 20 | 0.113 | 0.00 | -0.100 [-0.182, -0.016] | 7/11 | 0 | 0 |
| natural_live_1920 | episodic_ctx09 | 20 | 0.216 | 0.05 | +0.003 [-0.091, +0.098] | 11/9 | 0 | 0 |
| natural_live_1920 | episodic_recall_ctx09 | 20 | 0.181 | 0.05 | -0.032 [-0.154, +0.093] | 11/9 | 0 | 0 |
| natural_live_1920 | episodic_amp05 | 20 | 0.025 | 0.00 | -0.188 [-0.261, -0.117] | 3/17 | 0 | 0 |
| natural_live_1920 | episodic_recall_amp05 | 20 | 0.025 | 0.00 | -0.188 [-0.261, -0.116] | 4/16 | 0 | 0 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 | -0.213 [-0.287, -0.139] | 0/18 | 0 | 0 |

