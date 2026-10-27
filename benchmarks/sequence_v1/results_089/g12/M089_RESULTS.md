# Cadence 0.89 memory readings (development founders)

## route12-16-hidden

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.093 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.073 | 0.03 | -0.019 [-0.036, -0.002] | 8/11 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.069 | 0.00 | -0.024 [-0.042, -0.005] | 6/13 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.073 | 0.03 | -0.019 [-0.036, -0.002] | 8/11 | 0 | 0 |
| random | episodic | 20 | 0.102 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_3840 | episodic | 20 | 0.479 | 0.50 |  |  | 5487 | 149387 |
| guide_step_3840 | recall_r0 | 20 | 0.382 | 0.30 | -0.098 [-0.265, +0.081] | 7/13 | 6501 | 118738 |
| guide_step_3840 | recall_h2_r0 | 20 | 0.488 | 0.35 | +0.008 [-0.157, +0.183] | 7/13 | 6559 | 96267 |
| guide_step_3840 | episodic_recall_r0 | 20 | 0.485 | 0.45 | +0.006 [-0.034, +0.044] | 9/10 | 5539 | 83502 |

## route12-16-visible

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.102 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 19 | 0.061 | 0.00 | -0.041 [-0.061, -0.020] | 4/15 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.067 | 0.00 | -0.035 [-0.055, -0.015] | 5/14 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.059 | 0.00 | -0.043 [-0.062, -0.023] | 4/16 | 0 | 0 |
| random | episodic | 20 | 0.102 | nan |  |  | 0 | 0 |
| random | recall_r0 | 19 | 0.100 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.102 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 19 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_3840 | episodic | 20 | 0.988 | 1.00 |  |  | 7009 | 458653 |
| guide_step_3840 | recall_r0 | 19 | 0.435 | 0.32 | -0.553 [-0.705, -0.389] | 2/17 | 6460 | 132941 |
| guide_step_3840 | recall_h2_r0 | 20 | 0.447 | 0.30 | -0.542 [-0.685, -0.389] | 2/17 | 6454 | 99397 |
| guide_step_3840 | episodic_recall_r0 | 20 | 0.986 | 1.00 | -0.002 [-0.014, +0.008] | 9/8 | 6599 | 106063 |

## route12-8-hidden

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.105 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.067 | 0.03 | -0.038 [-0.055, -0.020] | 1/18 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.080 | 0.00 | -0.026 [-0.044, -0.007] | 3/16 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.067 | 0.03 | -0.038 [-0.055, -0.020] | 1/18 | 0 | 0 |
| random | episodic | 20 | 0.090 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_3840 | episodic | 20 | 0.459 | 0.45 |  |  | 5352 | 98907 |
| guide_step_3840 | recall_r0 | 20 | 0.593 | 0.42 | +0.134 [-0.011, +0.286] | 10/10 | 6268 | 115296 |
| guide_step_3840 | recall_h2_r0 | 20 | 0.479 | 0.40 | +0.020 [-0.162, +0.212] | 8/12 | 6492 | 91272 |
| guide_step_3840 | episodic_recall_r0 | 20 | 0.530 | 0.57 | +0.071 [+0.013, +0.159] | 15/5 | 5453 | 78815 |

## route12-8-visible

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `episodic` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | episodic | 20 | 0.103 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.063 | 0.00 | -0.040 [-0.057, -0.022] | 4/16 | 0 | 0 |
| founder | recall_h2_r0 | 19 | 0.058 | 0.00 | -0.046 [-0.063, -0.030] | 1/18 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.063 | 0.00 | -0.040 [-0.057, -0.022] | 4/16 | 0 | 0 |
| random | episodic | 20 | 0.090 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 19 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.090 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 19 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_3840 | episodic | 20 | 0.976 | 0.97 |  |  | 6806 | 283262 |
| guide_step_3840 | recall_r0 | 20 | 0.476 | 0.28 | -0.500 [-0.642, -0.346] | 3/17 | 6404 | 130524 |
| guide_step_3840 | recall_h2_r0 | 19 | 0.355 | 0.24 | -0.622 [-0.783, -0.448] | 2/17 | 6681 | 103342 |
| guide_step_3840 | episodic_recall_r0 | 20 | 0.984 | 0.97 | +0.007 [-0.024, +0.035] | 13/5 | 6513 | 140576 |

