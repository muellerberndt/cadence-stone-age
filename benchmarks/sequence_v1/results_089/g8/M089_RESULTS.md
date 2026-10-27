# Cadence 0.89 memory readings (development founders)

## route8-delay16

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.068 | 0.03 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 20 | 0.068 | 0.03 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.073 | 0.03 | +0.005 [-0.002, +0.013] | 10/6 | 0 | 0 |
| founder | recall_nopos_r0 | 20 | 0.073 | 0.03 | +0.005 [-0.002, +0.013] | 10/6 | 0 | 0 |
| founder | recall_h2 | 20 | 0.083 | 0.00 | +0.015 [+0.002, +0.028] | 13/6 | 0 | 0 |
| founder | episodic | 20 | 0.093 | 0.00 | +0.025 [+0.008, +0.040] | 14/5 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.073 | 0.03 | +0.005 [-0.002, +0.013] | 10/6 | 0 | 0 |
| random | recall | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.102 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | recall | 20 | 0.410 | 0.30 | +0.050 [-0.067, +0.179] | 10/10 | 2991 | 54301 |
| guide_step_1920 | recall_nopos | 20 | 0.360 | 0.20 |  |  | 2973 | 50144 |
| guide_step_1920 | recall_r0 | 20 | 0.566 | 0.47 | +0.206 [+0.045, +0.370] | 15/5 | 3269 | 61191 |
| guide_step_1920 | recall_nopos_r0 | 20 | 0.345 | 0.25 | -0.015 [-0.104, +0.079] | 10/10 | 3145 | 55637 |
| guide_step_1920 | recall_h2 | 20 | 0.406 | 0.30 | +0.046 [-0.108, +0.221] | 10/10 | 3042 | 49078 |
| guide_step_1920 | episodic | 20 | 0.430 | 0.35 | +0.071 [-0.017, +0.158] | 14/6 | 2850 | 71234 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.443 | 0.42 | +0.083 [+0.004, +0.165] | 14/6 | 2861 | 44388 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_nopos | 20 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live_1920 | recall_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.001] | 1/0 | 0 | 0 |
| natural_live_1920 | recall_nopos_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.001] | 1/0 | 0 | 0 |
| natural_live_1920 | recall_h2 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | episodic | 20 | 0.168 | 0.03 | +0.168 [+0.105, +0.236] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.235 | 0.12 | +0.235 [+0.155, +0.319] | 20/0 | 0 | 0 |

## route8-delay8

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.069 | 0.03 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 20 | 0.069 | 0.03 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.067 | 0.03 | -0.002 [-0.013, +0.010] | 9/8 | 0 | 0 |
| founder | recall_nopos_r0 | 20 | 0.067 | 0.03 | -0.002 [-0.013, +0.010] | 9/8 | 0 | 0 |
| founder | recall_h2 | 20 | 0.081 | 0.00 | +0.012 [-0.006, +0.030] | 10/10 | 0 | 0 |
| founder | episodic | 20 | 0.105 | 0.00 | +0.037 [+0.018, +0.055] | 15/4 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.067 | 0.03 | -0.002 [-0.013, +0.010] | 9/8 | 0 | 0 |
| random | recall | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.090 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | recall | 20 | 0.587 | 0.47 | +0.274 [+0.121, +0.438] | 13/7 | 3132 | 59514 |
| guide_step_1920 | recall_nopos | 20 | 0.313 | 0.17 |  |  | 3132 | 53170 |
| guide_step_1920 | recall_r0 | 20 | 0.543 | 0.47 | +0.230 [+0.026, +0.428] | 13/7 | 3290 | 62318 |
| guide_step_1920 | recall_nopos_r0 | 20 | 0.521 | 0.45 | +0.208 [+0.062, +0.359] | 10/8 | 3176 | 63292 |
| guide_step_1920 | recall_h2 | 20 | 0.533 | 0.42 | +0.220 [+0.057, +0.386] | 15/5 | 3244 | 50587 |
| guide_step_1920 | episodic | 20 | 0.467 | 0.42 | +0.153 [+0.069, +0.238] | 15/5 | 2750 | 48871 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.510 | 0.42 | +0.197 [+0.110, +0.291] | 17/2 | 2809 | 46381 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_nopos | 20 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live_1920 | recall_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_nopos_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_h2 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | episodic | 20 | 0.213 | 0.05 | +0.213 [+0.139, +0.287] | 18/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.225 | 0.07 | +0.225 [+0.149, +0.302] | 20/0 | 0 | 0 |

