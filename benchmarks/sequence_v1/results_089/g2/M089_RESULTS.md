# Cadence 0.89 memory readings (development founders)

## recall2

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `carried` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | carried | 20 | 0.495 | 0.50 |  |  | 0 | 0 |
| founder | recall | 20 | 0.496 | 0.47 | +0.001 [-0.015, +0.016] | 11/8 | 0 | 0 |
| founder | recall_nopos | 20 | 0.496 | 0.47 | +0.001 [-0.015, +0.016] | 11/8 | 0 | 0 |
| founder | recall_p4 | 20 | 0.496 | 0.47 | +0.001 [-0.015, +0.016] | 11/8 | 0 | 0 |
| founder | recall_rate03 | 20 | 0.496 | 0.47 | +0.001 [-0.015, +0.016] | 11/8 | 0 | 0 |
| founder | recall_h2 | 20 | 0.496 | 0.48 | +0.001 [-0.018, +0.021] | 11/8 | 0 | 0 |
| founder | recall_h2_nopos | 20 | 0.496 | 0.48 | +0.001 [-0.018, +0.021] | 11/8 | 0 | 0 |
| founder | recall_h4 | 20 | 0.488 | 0.49 | -0.006 [-0.032, +0.019] | 10/9 | 0 | 0 |
| founder | recall_areward | 20 | 0.496 | 0.47 | +0.001 [-0.015, +0.016] | 11/8 | 0 | 0 |
| founder | recall_h2_areward | 20 | 0.496 | 0.48 | +0.001 [-0.018, +0.021] | 11/8 | 0 | 0 |
| random | carried | 20 | 0.496 | nan |  |  | 0 | 0 |
| random | recall | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_p4 | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_rate03 | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_nopos | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h4 | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_areward | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_areward | 20 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | carried | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_p4 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_rate03 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h4 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | carried | 20 | 0.490 | 0.50 |  |  | 1536 | 147374 |
| teach_step | recall | 20 | 0.969 | 0.97 | +0.480 [+0.451, +0.505] | 20/0 | 1536 | 55378 |
| teach_step | recall_nopos | 20 | 0.912 | 0.94 | +0.422 [+0.359, +0.473] | 19/1 | 1536 | 73514 |
| teach_step | recall_p4 | 20 | 0.969 | 0.97 | +0.480 [+0.451, +0.505] | 20/0 | 1536 | 55378 |
| teach_step | recall_rate03 | 20 | 0.984 | 0.99 | +0.494 [+0.472, +0.512] | 20/0 | 1536 | 55000 |
| teach_step | recall_h2 | 20 | 0.994 | 1.00 | +0.505 [+0.492, +0.518] | 20/0 | 1536 | 53642 |
| teach_step | recall_h2_nopos | 20 | 0.960 | 0.96 | +0.471 [+0.425, +0.506] | 20/0 | 1536 | 60722 |
| teach_step | recall_h4 | 20 | 0.995 | 1.00 | +0.505 [+0.492, +0.518] | 20/0 | 1536 | 52690 |
| teach_step | recall_areward | 20 | 0.980 | 0.99 | +0.490 [+0.466, +0.511] | 20/0 | 1536 | 57590 |
| teach_step | recall_h2_areward | 20 | 0.991 | 1.00 | +0.502 [+0.490, +0.514] | 20/0 | 1536 | 52514 |
| reward_step | carried | 20 | 0.491 | 0.50 |  |  | 0 | 0 |
| reward_step | recall | 20 | 0.704 | 0.71 | +0.212 [+0.126, +0.298] | 14/3 | 0 | 0 |
| reward_step | recall_nopos | 20 | 0.704 | 0.71 | +0.212 [+0.126, +0.298] | 14/3 | 0 | 0 |
| reward_step | recall_p4 | 20 | 0.704 | 0.71 | +0.212 [+0.126, +0.298] | 14/3 | 0 | 0 |
| reward_step | recall_rate03 | 20 | 0.704 | 0.71 | +0.212 [+0.126, +0.298] | 14/3 | 0 | 0 |
| reward_step | recall_h2 | 20 | 0.627 | 0.63 | +0.136 [+0.061, +0.214] | 13/4 | 0 | 0 |
| reward_step | recall_h2_nopos | 20 | 0.627 | 0.63 | +0.136 [+0.061, +0.214] | 13/4 | 0 | 0 |
| reward_step | recall_h4 | 20 | 0.755 | 0.76 | +0.264 [+0.188, +0.335] | 19/1 | 0 | 0 |
| reward_step | recall_areward | 20 | 0.681 | 0.68 | +0.190 [+0.106, +0.276] | 14/4 | 0 | 0 |
| reward_step | recall_h2_areward | 20 | 0.647 | 0.65 | +0.155 [+0.072, +0.246] | 13/5 | 0 | 0 |
| reward_live | carried | 20 | 0.488 | 0.50 |  |  | 0 | 0 |
| reward_live | recall | 20 | 0.843 | 0.91 | +0.355 [+0.295, +0.404] | 19/1 | 0 | 0 |
| reward_live | recall_nopos | 20 | 0.843 | 0.91 | +0.355 [+0.295, +0.404] | 19/1 | 0 | 0 |
| reward_live | recall_p4 | 20 | 0.843 | 0.91 | +0.355 [+0.295, +0.404] | 19/1 | 0 | 0 |
| reward_live | recall_rate03 | 20 | 0.843 | 0.91 | +0.355 [+0.295, +0.404] | 19/1 | 0 | 0 |
| reward_live | recall_h2 | 20 | 0.804 | 0.87 | +0.316 [+0.244, +0.380] | 19/1 | 0 | 0 |
| reward_live | recall_h2_nopos | 20 | 0.804 | 0.87 | +0.316 [+0.244, +0.380] | 19/1 | 0 | 0 |
| reward_live | recall_h4 | 20 | 0.839 | 0.91 | +0.351 [+0.273, +0.417] | 19/1 | 0 | 0 |
| reward_live | recall_areward | 20 | 0.820 | 0.93 | +0.332 [+0.274, +0.384] | 19/1 | 0 | 0 |
| reward_live | recall_h2_areward | 20 | 0.834 | 0.90 | +0.346 [+0.291, +0.395] | 20/0 | 0 | 0 |

## route2-hidden

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.090 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.090 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall | 20 | 0.048 | 0.00 | -0.043 [-0.055, -0.031] | 1/18 | 0 | 0 |
| founder | episodic_recall_nopos | 20 | 0.048 | 0.00 | -0.043 [-0.055, -0.031] | 1/18 | 0 | 0 |
| founder | episodic_recall_h2 | 20 | 0.066 | 0.00 | -0.024 [-0.040, -0.007] | 5/14 | 0 | 0 |
| founder | episodic_recall_areward | 20 | 0.048 | 0.00 | -0.043 [-0.055, -0.031] | 1/18 | 0 | 0 |
| founder | recall_h2 | 20 | 0.066 | 0.00 | -0.024 [-0.040, -0.007] | 5/14 | 0 | 0 |
| founder | recall_h2_areward | 20 | 0.066 | 0.00 | -0.024 [-0.040, -0.007] | 5/14 | 0 | 0 |
| random | defaults | 20 | 0.091 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_nopos | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_areward | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_areward | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step | defaults | 20 | 0.215 | 0.00 |  |  | 922 | 14406 |
| guide_step | episodic | 20 | 0.488 | 0.42 | +0.273 [+0.230, +0.313] | 20/0 | 730 | 19036 |
| guide_step | episodic_recall | 20 | 0.613 | 0.60 | +0.399 [+0.306, +0.501] | 20/0 | 715 | 13538 |
| guide_step | episodic_recall_nopos | 20 | 0.659 | 0.60 | +0.444 [+0.330, +0.561] | 19/1 | 691 | 12617 |
| guide_step | episodic_recall_h2 | 20 | 0.619 | 0.60 | +0.404 [+0.282, +0.531] | 19/1 | 709 | 11224 |
| guide_step | episodic_recall_areward | 20 | 0.688 | 0.68 | +0.473 [+0.348, +0.597] | 19/1 | 701 | 13698 |
| guide_step | recall_h2 | 20 | 0.565 | 0.47 | +0.350 [+0.196, +0.506] | 14/6 | 917 | 14925 |
| guide_step | recall_h2_areward | 20 | 0.525 | 0.53 | +0.310 [+0.125, +0.497] | 13/7 | 944 | 14345 |
| grade_step | defaults | 20 | 0.119 | 0.03 |  |  | 0 | 0 |
| grade_step | episodic | 20 | 0.338 | 0.25 | +0.219 [+0.120, +0.309] | 17/3 | 0 | 0 |
| grade_step | episodic_recall | 20 | 0.274 | 0.23 | +0.155 [+0.031, +0.277] | 14/5 | 0 | 0 |
| grade_step | episodic_recall_nopos | 20 | 0.274 | 0.23 | +0.155 [+0.031, +0.277] | 14/5 | 0 | 0 |
| grade_step | episodic_recall_h2 | 20 | 0.359 | 0.30 | +0.240 [+0.115, +0.360] | 15/5 | 0 | 0 |
| grade_step | episodic_recall_areward | 20 | 0.279 | 0.15 | +0.161 [+0.045, +0.272] | 14/4 | 0 | 0 |
| grade_step | recall_h2 | 20 | 0.011 | 0.00 | -0.108 [-0.160, -0.059] | 1/11 | 0 | 0 |
| grade_step | recall_h2_areward | 20 | 0.031 | 0.03 | -0.088 [-0.157, -0.018] | 3/10 | 0 | 0 |
| natural_live | defaults | 20 | 0.017 | 0.00 |  |  | 0 | 0 |
| natural_live | episodic | 20 | 0.088 | 0.03 | +0.072 [+0.017, +0.137] | 14/1 | 0 | 0 |
| natural_live | episodic_recall | 20 | 0.051 | 0.00 | +0.035 [-0.009, +0.082] | 14/3 | 0 | 0 |
| natural_live | episodic_recall_nopos | 20 | 0.051 | 0.00 | +0.035 [-0.009, +0.082] | 14/3 | 0 | 0 |
| natural_live | episodic_recall_h2 | 20 | 0.074 | 0.00 | +0.058 [+0.009, +0.110] | 14/2 | 0 | 0 |
| natural_live | episodic_recall_areward | 20 | 0.051 | 0.00 | +0.035 [-0.008, +0.082] | 14/2 | 0 | 0 |
| natural_live | recall_h2 | 20 | 0.000 | 0.00 | -0.017 [-0.041, +0.000] | 0/3 | 0 | 0 |
| natural_live | recall_h2_areward | 20 | 0.000 | 0.00 | -0.016 [-0.041, +0.000] | 0/2 | 0 | 0 |
| guide_step_1920 | defaults | 20 | 0.192 | 0.03 |  |  | 3636 | 83881 |
| guide_step_1920 | episodic | 20 | 0.569 | 0.53 | +0.377 [+0.340, +0.419] | 20/0 | 2727 | 91962 |
| guide_step_1920 | episodic_recall | 20 | 0.647 | 0.55 | +0.455 [+0.343, +0.558] | 19/1 | 2648 | 48857 |
| guide_step_1920 | episodic_recall_nopos | 20 | 0.613 | 0.55 | +0.422 [+0.288, +0.554] | 17/3 | 2629 | 48599 |
| guide_step_1920 | episodic_recall_h2 | 20 | 0.774 | 0.78 | +0.582 [+0.473, +0.691] | 20/0 | 2673 | 40134 |
| guide_step_1920 | episodic_recall_areward | 20 | 0.737 | 0.72 | +0.545 [+0.447, +0.641] | 20/0 | 2741 | 53979 |
| guide_step_1920 | recall_h2 | 20 | 0.512 | 0.35 | +0.320 [+0.158, +0.486] | 15/5 | 3283 | 49264 |
| guide_step_1920 | recall_h2_areward | 20 | 0.643 | 0.55 | +0.451 [+0.294, +0.603] | 17/3 | 3286 | 50251 |
| natural_live_1920 | defaults | 20 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live_1920 | episodic | 20 | 0.167 | 0.07 | +0.167 [+0.088, +0.257] | 19/0 | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.269 | 0.12 | +0.269 [+0.185, +0.350] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_nopos | 20 | 0.269 | 0.12 | +0.269 [+0.185, +0.350] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_h2 | 20 | 0.319 | 0.25 | +0.319 [+0.229, +0.405] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_areward | 20 | 0.233 | 0.10 | +0.233 [+0.149, +0.320] | 19/0 | 0 | 0 |
| natural_live_1920 | recall_h2 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_h2_areward | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |

## route2-visible

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.090 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.090 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall | 20 | 0.049 | 0.00 | -0.041 [-0.055, -0.026] | 3/17 | 0 | 0 |
| founder | episodic_recall_nopos | 20 | 0.049 | 0.00 | -0.041 [-0.055, -0.026] | 3/17 | 0 | 0 |
| founder | episodic_recall_h2 | 20 | 0.045 | 0.00 | -0.045 [-0.056, -0.033] | 2/18 | 0 | 0 |
| founder | episodic_recall_areward | 20 | 0.049 | 0.00 | -0.041 [-0.055, -0.026] | 3/17 | 0 | 0 |
| founder | recall_h2 | 20 | 0.045 | 0.00 | -0.045 [-0.056, -0.033] | 2/18 | 0 | 0 |
| founder | recall_h2_areward | 20 | 0.045 | 0.00 | -0.045 [-0.056, -0.033] | 2/18 | 0 | 0 |
| random | defaults | 20 | 0.091 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_nopos | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_h2 | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_areward | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_areward | 20 | 0.091 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step | defaults | 20 | 0.162 | 0.03 |  |  | 1024 | 37556 |
| guide_step | episodic | 20 | 0.959 | 0.90 | +0.797 [+0.730, +0.857] | 20/0 | 883 | 32171 |
| guide_step | episodic_recall | 20 | 0.895 | 0.88 | +0.733 [+0.616, +0.837] | 20/0 | 817 | 15806 |
| guide_step | episodic_recall_nopos | 20 | 0.876 | 0.82 | +0.715 [+0.625, +0.802] | 20/0 | 840 | 16444 |
| guide_step | episodic_recall_h2 | 20 | 0.972 | 1.00 | +0.810 [+0.744, +0.869] | 20/0 | 807 | 14180 |
| guide_step | episodic_recall_areward | 20 | 0.901 | 0.82 | +0.739 [+0.644, +0.827] | 20/0 | 828 | 16958 |
| guide_step | recall_h2 | 20 | 0.584 | 0.55 | +0.422 [+0.254, +0.583] | 16/3 | 967 | 14758 |
| guide_step | recall_h2_areward | 20 | 0.506 | 0.47 | +0.344 [+0.199, +0.485] | 16/4 | 952 | 14289 |
| grade_step | defaults | 20 | 0.059 | 0.03 |  |  | 0 | 0 |
| grade_step | episodic | 20 | 0.867 | 0.80 | +0.808 [+0.710, +0.892] | 20/0 | 0 | 0 |
| grade_step | episodic_recall | 20 | 0.939 | 0.85 | +0.879 [+0.821, +0.930] | 20/0 | 0 | 0 |
| grade_step | episodic_recall_nopos | 20 | 0.939 | 0.85 | +0.879 [+0.821, +0.930] | 20/0 | 0 | 0 |
| grade_step | episodic_recall_h2 | 20 | 0.906 | 0.85 | +0.847 [+0.732, +0.934] | 20/0 | 0 | 0 |
| grade_step | episodic_recall_areward | 20 | 0.901 | 0.88 | +0.841 [+0.760, +0.911] | 20/0 | 0 | 0 |
| grade_step | recall_h2 | 20 | 0.013 | 0.05 | -0.047 [-0.109, +0.004] | 4/3 | 0 | 0 |
| grade_step | recall_h2_areward | 20 | 0.017 | 0.00 | -0.043 [-0.109, +0.013] | 4/4 | 0 | 0 |
| natural_live | defaults | 20 | 0.012 | 0.00 |  |  | 0 | 0 |
| natural_live | episodic | 20 | 0.931 | 1.00 | +0.919 [+0.889, +0.946] | 20/0 | 0 | 0 |
| natural_live | episodic_recall | 20 | 0.948 | 1.00 | +0.935 [+0.911, +0.955] | 20/0 | 0 | 0 |
| natural_live | episodic_recall_nopos | 20 | 0.948 | 1.00 | +0.935 [+0.911, +0.955] | 20/0 | 0 | 0 |
| natural_live | episodic_recall_h2 | 20 | 0.922 | 1.00 | +0.910 [+0.872, +0.944] | 20/0 | 0 | 0 |
| natural_live | episodic_recall_areward | 20 | 0.941 | 1.00 | +0.929 [+0.905, +0.950] | 20/0 | 0 | 0 |
| natural_live | recall_h2 | 20 | 0.000 | 0.00 | -0.012 [-0.031, +0.000] | 0/3 | 0 | 0 |
| natural_live | recall_h2_areward | 20 | 0.000 | 0.00 | -0.012 [-0.030, +0.000] | 1/3 | 0 | 0 |
| guide_step_1920 | defaults | 20 | 0.211 | 0.03 |  |  | 3819 | 145926 |
| guide_step_1920 | episodic | 20 | 0.988 | 0.97 | +0.777 [+0.734, +0.816] | 20/0 | 3286 | 150136 |
| guide_step_1920 | episodic_recall | 20 | 0.968 | 0.90 | +0.757 [+0.701, +0.808] | 20/0 | 3100 | 59889 |
| guide_step_1920 | episodic_recall_nopos | 20 | 0.977 | 0.97 | +0.766 [+0.711, +0.816] | 20/0 | 3074 | 61186 |
| guide_step_1920 | episodic_recall_h2 | 20 | 0.939 | 0.90 | +0.727 [+0.653, +0.798] | 20/0 | 3022 | 52536 |
| guide_step_1920 | episodic_recall_areward | 20 | 0.963 | 0.88 | +0.752 [+0.688, +0.809] | 20/0 | 3082 | 64284 |
| guide_step_1920 | recall_h2 | 20 | 0.635 | 0.55 | +0.424 [+0.263, +0.583] | 17/2 | 3342 | 53225 |
| guide_step_1920 | recall_h2_areward | 20 | 0.413 | 0.30 | +0.202 [+0.030, +0.389] | 13/6 | 3489 | 52385 |
| natural_live_1920 | defaults | 20 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live_1920 | episodic | 20 | 0.932 | 1.00 | +0.932 [+0.916, +0.948] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.946 | 1.00 | +0.946 [+0.931, +0.960] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_nopos | 20 | 0.946 | 1.00 | +0.946 [+0.931, +0.960] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_h2 | 20 | 0.922 | 1.00 | +0.922 [+0.890, +0.950] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_areward | 20 | 0.941 | 1.00 | +0.941 [+0.924, +0.955] | 20/0 | 0 | 0 |
| natural_live_1920 | recall_h2 | 20 | 0.001 | 0.00 | +0.001 [+0.000, +0.003] | 1/0 | 0 | 0 |
| natural_live_1920 | recall_h2_areward | 20 | 0.001 | 0.00 | +0.001 [+0.000, +0.002] | 1/0 | 0 | 0 |

