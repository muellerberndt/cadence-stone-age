# Cadence 0.89 memory readings (development founders)

## recall10-plain

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.500 | 0.47 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.499 | 0.49 | -0.001 [-0.005, +0.004] | 7/8 | 0 | 0 |
| founder | recall_h2 | 20 | 0.499 | 0.51 | -0.001 [-0.017, +0.016] | 6/11 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.497 | 0.51 | -0.003 [-0.020, +0.016] | 6/13 | 0 | 0 |
| random | recall | 20 | 0.498 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.498 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.498 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.498 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 20 | 0.982 | 0.99 |  |  | 1536 | 56638 |
| teach_step | recall_r0 | 20 | 0.968 | 0.97 | -0.014 [-0.043, +0.007] | 3/5 | 1536 | 56194 |
| teach_step | recall_h2 | 20 | 0.986 | 0.99 | +0.004 [-0.015, +0.021] | 4/1 | 1536 | 54237 |
| teach_step | recall_h2_r0 | 20 | 0.983 | 0.99 | +0.000 [-0.014, +0.015] | 4/3 | 1536 | 55720 |
| reward_step | recall | 20 | 0.663 | 0.67 |  |  | 0 | 0 |
| reward_step | recall_r0 | 20 | 0.624 | 0.62 | -0.040 [-0.124, +0.045] | 6/8 | 0 | 0 |
| reward_step | recall_h2 | 20 | 0.708 | 0.71 | +0.044 [-0.039, +0.135] | 7/8 | 0 | 0 |
| reward_step | recall_h2_r0 | 20 | 0.652 | 0.65 | -0.012 [-0.095, +0.070] | 7/10 | 0 | 0 |
| reward_live | recall | 20 | 0.822 | 0.89 |  |  | 0 | 0 |
| reward_live | recall_r0 | 20 | 0.773 | 0.80 | -0.049 [-0.116, +0.019] | 6/13 | 0 | 0 |
| reward_live | recall_h2 | 20 | 0.771 | 0.83 | -0.051 [-0.149, +0.045] | 9/11 | 0 | 0 |
| reward_live | recall_h2_r0 | 20 | 0.758 | 0.77 | -0.064 [-0.148, +0.023] | 5/15 | 0 | 0 |

## recall10-order

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.500 | 0.51 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.497 | 0.50 | -0.003 [-0.006, +0.000] | 5/10 | 0 | 0 |
| founder | recall_h2 | 20 | 0.497 | 0.49 | -0.003 [-0.012, +0.005] | 9/9 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.496 | 0.50 | -0.004 [-0.013, +0.005] | 7/9 | 0 | 0 |
| random | recall | 20 | 0.499 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.499 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.499 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.499 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 20 | 0.947 | 0.95 |  |  | 1536 | 68904 |
| teach_step | recall_r0 | 20 | 0.936 | 0.94 | -0.011 [-0.102, +0.075] | 4/6 | 1536 | 64531 |
| teach_step | recall_h2 | 20 | 0.971 | 0.97 | +0.025 [-0.050, +0.098] | 5/3 | 1536 | 64181 |
| teach_step | recall_h2_r0 | 20 | 0.984 | 0.99 | +0.038 [-0.012, +0.100] | 5/3 | 1536 | 60635 |
| reward_step | recall | 20 | 0.501 | 0.52 |  |  | 0 | 0 |
| reward_step | recall_r0 | 20 | 0.491 | 0.50 | -0.010 [-0.020, -0.002] | 3/10 | 0 | 0 |
| reward_step | recall_h2 | 20 | 0.497 | 0.49 | -0.004 [-0.023, +0.015] | 7/8 | 0 | 0 |
| reward_step | recall_h2_r0 | 20 | 0.499 | 0.50 | -0.002 [-0.019, +0.016] | 7/9 | 0 | 0 |
| reward_live | recall | 20 | 0.498 | 0.51 |  |  | 0 | 0 |
| reward_live | recall_r0 | 20 | 0.502 | 0.50 | +0.004 [-0.009, +0.017] | 7/3 | 0 | 0 |
| reward_live | recall_h2 | 20 | 0.508 | 0.50 | +0.010 [-0.008, +0.029] | 8/4 | 0 | 0 |
| reward_live | recall_h2_r0 | 20 | 0.499 | 0.51 | +0.001 [-0.011, +0.014] | 7/8 | 0 | 0 |

## route10-delay16

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.061 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.057 | 0.00 | -0.004 [-0.010, +0.001] | 6/12 | 0 | 0 |
| founder | episodic_recall | 20 | 0.061 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.057 | 0.00 | -0.004 [-0.010, +0.001] | 6/12 | 0 | 0 |
| founder | recall_h2 | 20 | 0.069 | 0.00 | +0.007 [-0.008, +0.024] | 11/8 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.071 | 0.00 | +0.010 [-0.006, +0.025] | 11/7 | 0 | 0 |
| random | recall | 20 | 0.094 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.094 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | recall | 20 | 0.397 | 0.15 |  |  | 2932 | 51466 |
| guide_step_1920 | recall_r0 | 20 | 0.581 | 0.47 | +0.183 [+0.011, +0.349] | 12/7 | 3242 | 69557 |
| guide_step_1920 | episodic_recall | 20 | 0.471 | 0.50 | +0.074 [+0.019, +0.130] | 13/6 | 2818 | 39804 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.520 | 0.47 | +0.123 [+0.071, +0.184] | 20/0 | 2803 | 46269 |
| guide_step_1920 | recall_h2 | 20 | 0.579 | 0.57 | +0.182 [+0.038, +0.332] | 13/7 | 2885 | 46287 |
| guide_step_1920 | recall_h2_r0 | 20 | 0.657 | 0.57 | +0.260 [+0.103, +0.414] | 13/7 | 3164 | 49763 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live_1920 | recall_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.273 | 0.12 | +0.273 [+0.193, +0.353] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.246 | 0.12 | +0.246 [+0.162, +0.333] | 20/0 | 0 | 0 |
| natural_live_1920 | recall_h2 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_h2_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |

## route10-delay2

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.054 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 20 | 0.061 | 0.00 | +0.008 [+0.000, +0.016] | 11/6 | 0 | 0 |
| founder | episodic_recall | 20 | 0.054 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_r0 | 20 | 0.061 | 0.00 | +0.008 [+0.000, +0.016] | 11/6 | 0 | 0 |
| founder | recall_h2 | 20 | 0.069 | 0.00 | +0.016 [+0.003, +0.029] | 14/6 | 0 | 0 |
| founder | recall_h2_r0 | 20 | 0.066 | 0.00 | +0.012 [+0.001, +0.023] | 12/7 | 0 | 0 |
| random | recall | 20 | 0.092 | nan |  |  | 0 | 0 |
| random | recall_r0 | 20 | 0.092 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.092 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 20 | 0.092 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.092 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 20 | 0.092 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step_1920 | recall | 20 | 0.408 | 0.20 |  |  | 3258 | 54289 |
| guide_step_1920 | recall_r0 | 20 | 0.645 | 0.55 | +0.236 [+0.030, +0.446] | 13/7 | 3215 | 58885 |
| guide_step_1920 | episodic_recall | 20 | 0.680 | 0.60 | +0.271 [+0.086, +0.453] | 14/6 | 2659 | 51194 |
| guide_step_1920 | episodic_recall_r0 | 20 | 0.706 | 0.72 | +0.298 [+0.142, +0.453] | 18/2 | 2631 | 52028 |
| guide_step_1920 | recall_h2 | 20 | 0.629 | 0.53 | +0.221 [-0.023, +0.442] | 13/5 | 3259 | 53485 |
| guide_step_1920 | recall_h2_r0 | 20 | 0.555 | 0.50 | +0.147 [-0.049, +0.340] | 14/6 | 3220 | 63359 |
| natural_live_1920 | recall | 20 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live_1920 | recall_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | episodic_recall | 20 | 0.208 | 0.07 | +0.208 [+0.135, +0.287] | 20/0 | 0 | 0 |
| natural_live_1920 | episodic_recall_r0 | 20 | 0.207 | 0.05 | +0.207 [+0.136, +0.281] | 20/0 | 0 | 0 |
| natural_live_1920 | recall_h2 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live_1920 | recall_h2_r0 | 20 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |

## view10-hidden

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 40 | 0.100 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 40 | 0.099 | 0.00 | -0.001 [-0.008, +0.006] | 15/16 | 0 | 0 |
| founder | episodic_recall | 40 | 0.100 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_r0 | 40 | 0.099 | 0.00 | -0.001 [-0.008, +0.006] | 15/16 | 0 | 0 |
| founder | recall_h2 | 40 | 0.066 | 0.00 | -0.034 [-0.046, -0.022] | 7/29 | 0 | 0 |
| founder | recall_h2_r0 | 40 | 0.067 | 0.00 | -0.033 [-0.046, -0.020] | 11/27 | 0 | 0 |
| random | recall | 40 | 0.118 | nan |  |  | 0 | 0 |
| random | recall_r0 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 40 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 40 | 0.225 | nan |  |  | 0 | 0 |
| searcher | recall_r0 | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_r0 | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2_r0 | 40 | 0.225 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 40 | 0.452 | 0.38 |  |  | 256 | 4311 |
| corrective_step_120 | recall_r0 | 40 | 0.433 | 0.45 | -0.019 [-0.159, +0.123] | 23/16 | 252 | 4490 |
| corrective_step_120 | episodic_recall | 40 | 0.757 | 0.50 | +0.305 [+0.159, +0.446] | 29/10 | 150 | 2321 |
| corrective_step_120 | episodic_recall_r0 | 40 | 0.765 | 0.57 | +0.313 [+0.188, +0.439] | 31/8 | 153 | 2394 |
| corrective_step_120 | recall_h2 | 40 | 0.362 | 0.23 | -0.089 [-0.220, +0.035] | 21/18 | 261 | 3761 |
| corrective_step_120 | recall_h2_r0 | 40 | 0.381 | 0.25 | -0.071 [-0.206, +0.064] | 17/22 | 258 | 3854 |
| corrective_step_480 | recall | 40 | 0.606 | 0.53 |  |  | 754 | 11606 |
| corrective_step_480 | recall_r0 | 40 | 0.423 | 0.28 | -0.183 [-0.330, -0.036] | 14/24 | 854 | 13292 |
| corrective_step_480 | episodic_recall | 40 | 0.936 | 0.82 | +0.330 [+0.189, +0.464] | 26/9 | 380 | 5939 |
| corrective_step_480 | episodic_recall_r0 | 40 | 0.890 | 0.78 | +0.284 [+0.142, +0.418] | 26/9 | 434 | 6251 |
| corrective_step_480 | recall_h2 | 40 | 0.558 | 0.40 | -0.048 [-0.198, +0.103] | 19/19 | 795 | 11937 |
| corrective_step_480 | recall_h2_r0 | 40 | 0.589 | 0.45 | -0.017 [-0.169, +0.133] | 21/17 | 811 | 12261 |
| natural_live_480 | recall | 40 | 0.026 | 0.03 |  |  | 0 | 0 |
| natural_live_480 | recall_r0 | 40 | 0.015 | 0.00 | -0.012 [-0.038, +0.012] | 6/9 | 0 | 0 |
| natural_live_480 | episodic_recall | 40 | 0.910 | 1.00 | +0.884 [+0.843, +0.918] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall_r0 | 40 | 0.853 | 0.95 | +0.827 [+0.771, +0.877] | 40/0 | 0 | 0 |
| natural_live_480 | recall_h2 | 40 | 0.023 | 0.00 | -0.003 [-0.033, +0.025] | 12/10 | 0 | 0 |
| natural_live_480 | recall_h2_r0 | 40 | 0.021 | 0.00 | -0.005 [-0.032, +0.018] | 10/7 | 0 | 0 |

## view10-visible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 40 | 0.092 | 0.00 |  |  | 0 | 0 |
| founder | recall_r0 | 40 | 0.096 | 0.00 | +0.004 [-0.003, +0.010] | 15/13 | 0 | 0 |
| founder | episodic_recall | 40 | 0.092 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_r0 | 40 | 0.096 | 0.00 | +0.004 [-0.003, +0.010] | 15/13 | 0 | 0 |
| founder | recall_h2 | 40 | 0.079 | 0.00 | -0.014 [-0.027, +0.000] | 10/27 | 0 | 0 |
| founder | recall_h2_r0 | 40 | 0.079 | 0.00 | -0.013 [-0.027, +0.001] | 11/25 | 0 | 0 |
| random | recall | 40 | 0.118 | nan |  |  | 0 | 0 |
| random | recall_r0 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_r0 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_r0 | 40 | 0.118 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 40 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_r0 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_r0 | 40 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 40 | 0.297 | nan |  |  | 0 | 0 |
| searcher | recall_r0 | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_r0 | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2_r0 | 40 | 0.297 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 40 | 0.667 | 0.50 |  |  | 225 | 3660 |
| corrective_step_120 | recall_r0 | 40 | 0.707 | 0.62 | +0.040 [-0.091, +0.171] | 19/17 | 225 | 3733 |
| corrective_step_120 | episodic_recall | 40 | 0.947 | 0.93 | +0.280 [+0.153, +0.405] | 33/4 | 29 | 537 |
| corrective_step_120 | episodic_recall_r0 | 40 | 0.989 | 0.97 | +0.322 [+0.210, +0.438] | 35/3 | 30 | 538 |
| corrective_step_120 | recall_h2 | 40 | 0.676 | 0.53 | +0.010 [-0.127, +0.143] | 18/19 | 227 | 3519 |
| corrective_step_120 | recall_h2_r0 | 40 | 0.668 | 0.55 | +0.001 [-0.118, +0.122] | 17/20 | 226 | 3535 |
| corrective_step_480 | recall | 40 | 0.800 | 0.62 |  |  | 643 | 10427 |
| corrective_step_480 | recall_r0 | 40 | 0.737 | 0.65 | -0.064 [-0.205, +0.072] | 18/17 | 617 | 10454 |
| corrective_step_480 | episodic_recall | 40 | 0.999 | 1.00 | +0.199 [+0.113, +0.292] | 30/2 | 62 | 1094 |
| corrective_step_480 | episodic_recall_r0 | 40 | 0.999 | 1.00 | +0.199 [+0.112, +0.291] | 29/3 | 58 | 1086 |
| corrective_step_480 | recall_h2 | 40 | 0.839 | 0.78 | +0.038 [-0.092, +0.165] | 22/17 | 602 | 9075 |
| corrective_step_480 | recall_h2_r0 | 40 | 0.834 | 0.72 | +0.034 [-0.085, +0.155] | 17/17 | 622 | 9190 |
| natural_live_480 | recall | 40 | 0.152 | 0.07 |  |  | 0 | 0 |
| natural_live_480 | recall_r0 | 40 | 0.103 | 0.05 | -0.050 [-0.115, +0.013] | 15/17 | 0 | 0 |
| natural_live_480 | episodic_recall | 40 | 0.989 | 1.00 | +0.836 [+0.761, +0.902] | 40/0 | 0 | 0 |
| natural_live_480 | episodic_recall_r0 | 40 | 0.988 | 1.00 | +0.835 [+0.758, +0.901] | 40/0 | 0 | 0 |
| natural_live_480 | recall_h2 | 40 | 0.130 | 0.07 | -0.023 [-0.111, +0.069] | 10/20 | 0 | 0 |
| natural_live_480 | recall_h2_r0 | 40 | 0.137 | 0.07 | -0.016 [-0.095, +0.062] | 16/17 | 0 | 0 |

