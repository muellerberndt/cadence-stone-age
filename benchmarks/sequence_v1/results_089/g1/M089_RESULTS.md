# Cadence 0.89 memory readings (development founders)

## recall

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `carried` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | carried | 10 | 0.496 | 0.50 |  |  | 0 | 0 |
| founder | retained | 10 | 0.496 | 0.50 | +0.000 [-0.001, +0.003] | 1/1 | 0 | 0 |
| founder | recall | 10 | 0.479 | 0.47 | -0.017 [-0.040, +0.006] | 3/6 | 0 | 0 |
| founder | recall_nopos | 10 | 0.479 | 0.47 | -0.017 [-0.040, +0.006] | 3/6 | 0 | 0 |
| founder | recall_h2 | 10 | 0.484 | 0.45 | -0.012 [-0.026, +0.004] | 2/7 | 0 | 0 |
| founder | attention | 10 | 0.502 | 0.51 | +0.006 [-0.014, +0.030] | 4/5 | 0 | 0 |
| random | carried | 10 | 0.494 | nan |  |  | 0 | 0 |
| random | retained | 10 | 0.494 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 10 | 0.494 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.494 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 10 | 0.494 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 10 | 0.494 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | carried | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | retained | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | carried | 10 | 0.487 | 0.51 |  |  | 1536 | 147456 |
| teach_step | retained | 10 | 0.487 | 0.50 | +0.000 [+0.000, +0.000] | 0/0 | 1536 | 147456 |
| teach_step | recall | 10 | 0.988 | 0.99 | +0.501 [+0.482, +0.517] | 10/0 | 1536 | 58029 |
| teach_step | recall_nopos | 10 | 0.746 | 0.77 | +0.259 [+0.136, +0.371] | 7/1 | 1536 | 93472 |
| teach_step | recall_h2 | 10 | 0.996 | 1.00 | +0.508 [+0.497, +0.519] | 10/0 | 1536 | 54080 |
| teach_step | attention | 10 | 0.803 | 0.84 | +0.315 [+0.181, +0.439] | 9/0 | 1536 | 90285 |
| reward_step | carried | 10 | 0.485 | 0.50 |  |  | 0 | 0 |
| reward_step | retained | 10 | 0.486 | 0.50 | +0.001 [+0.000, +0.003] | 2/0 | 0 | 0 |
| reward_step | recall | 10 | 0.638 | 0.64 | +0.153 [+0.044, +0.264] | 9/1 | 0 | 0 |
| reward_step | recall_nopos | 10 | 0.638 | 0.64 | +0.153 [+0.044, +0.264] | 9/1 | 0 | 0 |
| reward_step | recall_h2 | 10 | 0.685 | 0.69 | +0.200 [+0.104, +0.299] | 10/0 | 0 | 0 |
| reward_step | attention | 10 | 0.510 | 0.51 | +0.025 [+0.009, +0.045] | 9/1 | 0 | 0 |
| reward_live | carried | 10 | 0.483 | 0.50 |  |  | 0 | 0 |
| reward_live | retained | 10 | 0.487 | 0.50 | +0.004 [-0.001, +0.010] | 5/1 | 0 | 0 |
| reward_live | recall | 10 | 0.691 | 0.78 | +0.208 [+0.125, +0.289] | 10/0 | 0 | 0 |
| reward_live | recall_nopos | 10 | 0.691 | 0.78 | +0.208 [+0.125, +0.289] | 10/0 | 0 | 0 |
| reward_live | recall_h2 | 10 | 0.845 | 0.90 | +0.361 [+0.265, +0.437] | 10/0 | 0 | 0 |
| reward_live | attention | 10 | 0.639 | 0.66 | +0.155 [+0.058, +0.266] | 9/0 | 0 | 0 |

## route-hidden

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 10 | 0.105 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 10 | 0.105 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 10 | 0.071 | 0.05 | -0.034 [-0.059, -0.013] | 2/7 | 0 | 0 |
| founder | recall_nopos | 10 | 0.071 | 0.05 | -0.034 [-0.059, -0.013] | 2/7 | 0 | 0 |
| founder | recall_h2 | 10 | 0.072 | 0.00 | -0.033 [-0.051, -0.013] | 1/9 | 0 | 0 |
| founder | recall_w2 | 10 | 0.075 | 0.00 | -0.030 [-0.054, -0.009] | 2/8 | 0 | 0 |
| founder | attention | 10 | 0.069 | 0.00 | -0.036 [-0.076, +0.008] | 3/7 | 0 | 0 |
| founder | episodic_recall | 10 | 0.071 | 0.05 | -0.034 [-0.059, -0.013] | 2/7 | 0 | 0 |
| random | defaults | 10 | 0.086 | nan |  |  | 0 | 0 |
| random | episodic | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step | defaults | 10 | 0.175 | 0.00 |  |  | 922 | 16386 |
| guide_step | episodic | 10 | 0.453 | 0.50 | +0.277 [+0.162, +0.376] | 9/1 | 732 | 17800 |
| guide_step | recall | 10 | 0.368 | 0.20 | +0.193 [-0.010, +0.421] | 7/3 | 916 | 14248 |
| guide_step | recall_nopos | 10 | 0.284 | 0.15 | +0.109 [-0.042, +0.287] | 6/4 | 917 | 13028 |
| guide_step | recall_h2 | 10 | 0.418 | 0.30 | +0.243 [+0.061, +0.451] | 7/2 | 912 | 12979 |
| guide_step | recall_w2 | 10 | 0.253 | 0.15 | +0.078 [-0.006, +0.193] | 4/6 | 877 | 12872 |
| guide_step | attention | 10 | 0.136 | 0.00 | -0.039 [-0.095, +0.023] | 4/6 | 907 | 14035 |
| guide_step | episodic_recall | 10 | 0.596 | 0.50 | +0.421 [+0.237, +0.626] | 10/0 | 706 | 10974 |
| grade_step | defaults | 10 | 0.077 | 0.05 |  |  | 0 | 0 |
| grade_step | episodic | 10 | 0.368 | 0.25 | +0.291 [+0.140, +0.420] | 9/1 | 0 | 0 |
| grade_step | recall | 10 | 0.006 | 0.00 | -0.072 [-0.138, -0.014] | 1/4 | 0 | 0 |
| grade_step | recall_nopos | 10 | 0.006 | 0.00 | -0.072 [-0.138, -0.014] | 1/4 | 0 | 0 |
| grade_step | recall_h2 | 10 | 0.015 | 0.00 | -0.062 [-0.136, +0.007] | 1/4 | 0 | 0 |
| grade_step | recall_w2 | 10 | 0.001 | 0.00 | -0.076 [-0.143, -0.017] | 0/4 | 0 | 0 |
| grade_step | attention | 10 | 0.001 | 0.00 | -0.076 [-0.142, -0.017] | 0/4 | 0 | 0 |
| grade_step | episodic_recall | 10 | 0.274 | 0.20 | +0.198 [+0.030, +0.355] | 8/2 | 0 | 0 |
| natural_live | defaults | 10 | 0.000 | 0.00 |  |  | 0 | 0 |
| natural_live | episodic | 10 | 0.108 | 0.05 | +0.108 [+0.036, +0.203] | 8/0 | 0 | 0 |
| natural_live | recall | 10 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live | recall_nopos | 10 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live | recall_h2 | 10 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live | recall_w2 | 10 | 0.003 | 0.00 | +0.003 [+0.000, +0.008] | 1/0 | 0 | 0 |
| natural_live | attention | 10 | 0.000 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_live | episodic_recall | 10 | 0.071 | 0.05 | +0.071 [+0.013, +0.161] | 7/0 | 0 | 0 |

## route-visible

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 10 | 0.111 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 10 | 0.111 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 10 | 0.068 | 0.00 | -0.043 [-0.074, -0.009] | 2/8 | 0 | 0 |
| founder | recall_nopos | 10 | 0.068 | 0.00 | -0.043 [-0.074, -0.009] | 2/8 | 0 | 0 |
| founder | recall_h2 | 10 | 0.062 | 0.00 | -0.048 [-0.071, -0.028] | 0/9 | 0 | 0 |
| founder | recall_w2 | 10 | 0.057 | 0.00 | -0.054 [-0.078, -0.028] | 1/9 | 0 | 0 |
| founder | attention | 10 | 0.058 | 0.00 | -0.053 [-0.092, -0.014] | 3/7 | 0 | 0 |
| founder | episodic_recall | 10 | 0.068 | 0.00 | -0.043 [-0.074, -0.009] | 2/8 | 0 | 0 |
| random | defaults | 10 | 0.086 | nan |  |  | 0 | 0 |
| random | episodic | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 10 | 0.086 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| guide_step | defaults | 10 | 0.239 | 0.05 |  |  | 1014 | 36929 |
| guide_step | episodic | 10 | 0.948 | 0.90 | +0.709 [+0.585, +0.827] | 10/0 | 890 | 32186 |
| guide_step | recall | 10 | 0.502 | 0.45 | +0.263 [+0.039, +0.487] | 7/3 | 991 | 17523 |
| guide_step | recall_nopos | 10 | 0.344 | 0.20 | +0.106 [-0.089, +0.300] | 5/5 | 955 | 14314 |
| guide_step | recall_h2 | 10 | 0.430 | 0.35 | +0.192 [+0.023, +0.361] | 9/1 | 962 | 15136 |
| guide_step | recall_w2 | 10 | 0.391 | 0.25 | +0.153 [-0.046, +0.381] | 6/4 | 958 | 15513 |
| guide_step | attention | 10 | 0.218 | 0.05 | -0.020 [-0.132, +0.095] | 4/6 | 1096 | 16226 |
| guide_step | episodic_recall | 10 | 0.980 | 1.00 | +0.741 [+0.633, +0.841] | 10/0 | 835 | 15838 |
| grade_step | defaults | 10 | 0.000 | 0.00 |  |  | 0 | 0 |
| grade_step | episodic | 10 | 0.901 | 0.90 | +0.901 [+0.807, +0.976] | 10/0 | 0 | 0 |
| grade_step | recall | 10 | 0.001 | 0.00 | +0.001 [+0.000, +0.002] | 1/0 | 0 | 0 |
| grade_step | recall_nopos | 10 | 0.001 | 0.00 | +0.001 [+0.000, +0.002] | 1/0 | 0 | 0 |
| grade_step | recall_h2 | 10 | 0.079 | 0.05 | +0.079 [+0.000, +0.195] | 3/0 | 0 | 0 |
| grade_step | recall_w2 | 10 | 0.019 | 0.00 | +0.019 [+0.000, +0.056] | 2/0 | 0 | 0 |
| grade_step | attention | 10 | 0.037 | 0.00 | +0.037 [+0.000, +0.076] | 3/0 | 0 | 0 |
| grade_step | episodic_recall | 10 | 0.845 | 0.80 | +0.845 [+0.642, +0.971] | 9/0 | 0 | 0 |
| natural_live | defaults | 10 | 0.029 | 0.00 |  |  | 0 | 0 |
| natural_live | episodic | 10 | 0.924 | 1.00 | +0.895 [+0.832, +0.945] | 10/0 | 0 | 0 |
| natural_live | recall | 10 | 0.020 | 0.00 | -0.009 [-0.087, +0.060] | 1/1 | 0 | 0 |
| natural_live | recall_nopos | 10 | 0.020 | 0.00 | -0.009 [-0.087, +0.060] | 1/1 | 0 | 0 |
| natural_live | recall_h2 | 10 | 0.001 | 0.00 | -0.028 [-0.087, +0.002] | 1/1 | 0 | 0 |
| natural_live | recall_w2 | 10 | 0.000 | 0.00 | -0.029 [-0.087, +0.000] | 0/1 | 0 | 0 |
| natural_live | attention | 10 | 0.001 | 0.00 | -0.028 [-0.086, +0.002] | 2/1 | 0 | 0 |
| natural_live | episodic_recall | 10 | 0.923 | 1.00 | +0.894 [+0.833, +0.945] | 10/0 | 0 | 0 |

## p1

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 10 | 0.138 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 10 | 0.138 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 10 | 0.115 | 0.00 | -0.024 [-0.044, -0.004] | 3/6 | 0 | 0 |
| founder | recall_nopos | 10 | 0.115 | 0.00 | -0.024 [-0.044, -0.004] | 3/6 | 0 | 0 |
| founder | recall_h2 | 10 | 0.092 | 0.00 | -0.046 [-0.077, -0.015] | 2/8 | 0 | 0 |
| founder | recall_w2 | 10 | 0.122 | 0.00 | -0.015 [-0.035, +0.006] | 3/7 | 0 | 0 |
| founder | attention | 10 | 0.117 | 0.00 | -0.021 [-0.071, +0.036] | 3/6 | 0 | 0 |
| founder | episodic_recall | 10 | 0.115 | 0.00 | -0.024 [-0.044, -0.004] | 3/6 | 0 | 0 |
| random | defaults | 10 | 0.121 | nan |  |  | 0 | 0 |
| random | episodic | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 10 | 0.121 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 10 | 0.299 | nan |  |  | 0 | 0 |
| searcher | episodic | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_w2 | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | attention | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 10 | 0.299 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step | defaults | 10 | 0.071 | 0.00 |  |  | 0 | 0 |
| natural_step | episodic | 10 | 0.798 | 0.50 | +0.727 [+0.493, +0.923] | 9/0 | 0 | 0 |
| natural_step | recall | 10 | 0.002 | 0.00 | -0.069 [-0.142, +0.000] | 1/3 | 0 | 0 |
| natural_step | recall_nopos | 10 | 0.002 | 0.00 | -0.069 [-0.142, +0.000] | 1/3 | 0 | 0 |
| natural_step | recall_h2 | 10 | 0.000 | 0.00 | -0.071 [-0.142, +0.000] | 0/3 | 0 | 0 |
| natural_step | recall_w2 | 10 | 0.018 | 0.00 | -0.053 [-0.138, +0.026] | 2/3 | 0 | 0 |
| natural_step | attention | 10 | 0.003 | 0.00 | -0.068 [-0.142, +0.002] | 2/3 | 0 | 0 |
| natural_step | episodic_recall | 10 | 0.771 | 0.70 | +0.700 [+0.444, +0.900] | 9/0 | 0 | 0 |
| grade_step | defaults | 10 | 0.001 | 0.00 |  |  | 0 | 0 |
| grade_step | episodic | 10 | 0.965 | 0.80 | +0.965 [+0.917, +0.998] | 10/0 | 0 | 0 |
| grade_step | recall | 10 | 0.001 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| grade_step | recall_nopos | 10 | 0.001 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| grade_step | recall_h2 | 10 | 0.096 | 0.10 | +0.095 [+0.002, +0.279] | 5/0 | 0 | 0 |
| grade_step | recall_w2 | 10 | 0.176 | 0.00 | +0.176 [+0.000, +0.390] | 3/1 | 0 | 0 |
| grade_step | attention | 10 | 0.046 | 0.10 | +0.045 [+0.000, +0.131] | 3/0 | 0 | 0 |
| grade_step | episodic_recall | 10 | 0.973 | 0.70 | +0.972 [+0.935, +0.997] | 10/0 | 0 | 0 |
| correct_step | defaults | 10 | 0.395 | 0.10 |  |  | 262 | 4854 |
| correct_step | episodic | 10 | 0.931 | 0.90 | +0.536 [+0.363, +0.701] | 9/1 | 55 | 1159 |
| correct_step | recall | 10 | 0.553 | 0.40 | +0.158 [-0.106, +0.440] | 5/5 | 240 | 4086 |
| correct_step | recall_nopos | 10 | 0.695 | 0.20 | +0.300 [+0.142, +0.424] | 9/1 | 239 | 4067 |
| correct_step | recall_h2 | 10 | 0.658 | 0.60 | +0.264 [+0.020, +0.515] | 7/2 | 228 | 3550 |
| correct_step | recall_w2 | 10 | 0.470 | 0.60 | +0.075 [-0.146, +0.298] | 6/4 | 247 | 3920 |
| correct_step | attention | 10 | 0.571 | 0.40 | +0.176 [-0.109, +0.436] | 7/3 | 242 | 4430 |
| correct_step | episodic_recall | 10 | 0.918 | 0.80 | +0.523 [+0.409, +0.635] | 10/0 | 43 | 686 |
| correct_step_qualified | defaults | 10 | 0.362 | 0.00 |  |  | 268 | 11265 |
| correct_step_qualified | episodic | 10 | 0.966 | 0.90 | +0.605 [+0.514, +0.715] | 10/0 | 54 | 2192 |
| correct_step_qualified | recall | 10 | 0.606 | 0.40 | +0.244 [+0.060, +0.424] | 7/3 | 250 | 10185 |
| correct_step_qualified | recall_nopos | 10 | 0.387 | 0.20 | +0.025 [-0.141, +0.201] | 4/6 | 247 | 9921 |
| correct_step_qualified | recall_h2 | 10 | 0.692 | 0.60 | +0.331 [+0.101, +0.551] | 7/3 | 236 | 9462 |
| correct_step_qualified | recall_w2 | 10 | 0.688 | 0.60 | +0.326 [+0.055, +0.585] | 8/2 | 244 | 9863 |
| correct_step_qualified | attention | 10 | 0.529 | 0.32 | +0.168 [-0.066, +0.398] | 8/2 | 245 | 9968 |
| correct_step_qualified | episodic_recall | 10 | 0.981 | 1.00 | +0.620 [+0.523, +0.731] | 10/0 | 41 | 1648 |

## view-hidden

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.125 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.125 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 20 | 0.073 | 0.00 | -0.053 [-0.075, -0.028] | 2/18 | 0 | 0 |
| founder | recall_nopos | 20 | 0.073 | 0.00 | -0.053 [-0.075, -0.028] | 2/18 | 0 | 0 |
| founder | recall_h2 | 20 | 0.088 | 0.00 | -0.038 [-0.058, -0.017] | 4/15 | 0 | 0 |
| founder | recall_w2 | 20 | 0.070 | 0.00 | -0.056 [-0.073, -0.039] | 0/17 | 0 | 0 |
| founder | attention | 20 | 0.078 | 0.00 | -0.048 [-0.075, -0.022] | 2/17 | 0 | 0 |
| founder | episodic_recall | 20 | 0.073 | 0.00 | -0.053 [-0.075, -0.028] | 2/18 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.224 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_w2 | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | attention | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.224 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.029 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.416 | 0.25 | +0.386 [+0.234, +0.541] | 17/1 | 0 | 0 |
| natural_step_120 | recall | 20 | 0.013 | 0.00 | -0.017 [-0.048, +0.011] | 3/4 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.013 | 0.00 | -0.017 [-0.048, +0.011] | 3/4 | 0 | 0 |
| natural_step_120 | recall_h2 | 20 | 0.028 | 0.00 | -0.002 [-0.037, +0.037] | 3/4 | 0 | 0 |
| natural_step_120 | recall_w2 | 20 | 0.029 | 0.00 | -0.001 [-0.034, +0.030] | 7/4 | 0 | 0 |
| natural_step_120 | attention | 20 | 0.044 | 0.00 | +0.015 [-0.028, +0.056] | 7/3 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.413 | 0.25 | +0.384 [+0.203, +0.569] | 17/3 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.193 | 0.05 |  |  | 281 | 4631 |
| corrective_step_120 | episodic | 20 | 0.546 | 0.25 | +0.354 [+0.179, +0.522] | 15/5 | 184 | 3168 |
| corrective_step_120 | recall | 20 | 0.475 | 0.35 | +0.283 [+0.119, +0.449] | 14/5 | 256 | 4280 |
| corrective_step_120 | recall_nopos | 20 | 0.343 | 0.10 | +0.150 [+0.043, +0.254] | 12/7 | 271 | 4195 |
| corrective_step_120 | recall_h2 | 20 | 0.368 | 0.25 | +0.175 [+0.025, +0.328] | 13/7 | 252 | 3803 |
| corrective_step_120 | recall_w2 | 20 | 0.488 | 0.35 | +0.295 [+0.171, +0.429] | 17/2 | 252 | 4255 |
| corrective_step_120 | attention | 20 | 0.412 | 0.40 | +0.220 [+0.086, +0.347] | 16/4 | 256 | 4488 |
| corrective_step_120 | episodic_recall | 20 | 0.724 | 0.40 | +0.531 [+0.381, +0.666] | 18/2 | 162 | 2504 |
| corrective_step_480 | defaults | 20 | 0.227 | 0.05 |  |  | 1065 | 34855 |
| corrective_step_480 | episodic | 20 | 0.867 | 0.65 | +0.640 [+0.540, +0.727] | 20/0 | 617 | 23116 |
| corrective_step_480 | recall | 20 | 0.584 | 0.50 | +0.358 [+0.178, +0.538] | 14/6 | 765 | 12399 |
| corrective_step_480 | recall_nopos | 20 | 0.507 | 0.45 | +0.281 [+0.068, +0.486] | 16/3 | 778 | 12403 |
| corrective_step_480 | recall_h2 | 20 | 0.689 | 0.60 | +0.463 [+0.267, +0.634] | 18/2 | 772 | 11064 |
| corrective_step_480 | recall_w2 | 20 | 0.544 | 0.50 | +0.318 [+0.110, +0.514] | 15/5 | 709 | 12573 |
| corrective_step_480 | attention | 20 | 0.713 | 0.60 | +0.486 [+0.324, +0.643] | 18/1 | 761 | 18485 |
| corrective_step_480 | episodic_recall | 20 | 0.901 | 0.85 | +0.675 [+0.532, +0.791] | 19/1 | 394 | 6556 |
| natural_live_480 | defaults | 20 | 0.033 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.857 | 1.00 | +0.823 [+0.766, +0.876] | 20/0 | 0 | 0 |
| natural_live_480 | recall | 20 | 0.019 | 0.00 | -0.015 [-0.050, +0.016] | 8/3 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.019 | 0.00 | -0.015 [-0.050, +0.016] | 8/3 | 0 | 0 |
| natural_live_480 | recall_h2 | 20 | 0.028 | 0.00 | -0.006 [-0.040, +0.026] | 6/4 | 0 | 0 |
| natural_live_480 | recall_w2 | 20 | 0.020 | 0.00 | -0.013 [-0.056, +0.029] | 5/4 | 0 | 0 |
| natural_live_480 | attention | 20 | 0.008 | 0.00 | -0.026 [-0.062, +0.005] | 4/4 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.879 | 1.00 | +0.846 [+0.786, +0.897] | 20/0 | 0 | 0 |

## view-invisible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.120 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.120 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 20 | 0.067 | 0.00 | -0.053 [-0.072, -0.034] | 2/17 | 0 | 0 |
| founder | recall_nopos | 20 | 0.067 | 0.00 | -0.053 [-0.072, -0.034] | 2/17 | 0 | 0 |
| founder | recall_h2 | 20 | 0.076 | 0.00 | -0.043 [-0.063, -0.022] | 5/15 | 0 | 0 |
| founder | recall_w2 | 20 | 0.072 | 0.00 | -0.048 [-0.070, -0.027] | 3/16 | 0 | 0 |
| founder | attention | 20 | 0.069 | 0.00 | -0.051 [-0.071, -0.029] | 2/16 | 0 | 0 |
| founder | episodic_recall | 20 | 0.067 | 0.00 | -0.053 [-0.072, -0.034] | 2/17 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.328 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_w2 | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | attention | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.328 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.137 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.102 | 0.00 | -0.035 [-0.120, +0.073] | 8/11 | 0 | 0 |
| natural_step_120 | recall | 20 | 0.081 | 0.00 | -0.056 [-0.104, -0.014] | 4/9 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.081 | 0.00 | -0.056 [-0.104, -0.014] | 4/9 | 0 | 0 |
| natural_step_120 | recall_h2 | 20 | 0.031 | 0.00 | -0.106 [-0.157, -0.058] | 2/12 | 0 | 0 |
| natural_step_120 | recall_w2 | 20 | 0.075 | 0.00 | -0.062 [-0.136, +0.014] | 6/10 | 0 | 0 |
| natural_step_120 | attention | 20 | 0.071 | 0.05 | -0.066 [-0.130, +0.001] | 4/12 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.156 | 0.00 | +0.018 [-0.078, +0.126] | 8/11 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.334 | 0.05 |  |  | 265 | 4154 |
| corrective_step_120 | episodic | 20 | 0.835 | 0.40 | +0.501 [+0.393, +0.601] | 19/1 | 157 | 3132 |
| corrective_step_120 | recall | 20 | 0.507 | 0.25 | +0.173 [+0.016, +0.332] | 11/7 | 255 | 3976 |
| corrective_step_120 | recall_nopos | 20 | 0.504 | 0.20 | +0.171 [+0.024, +0.322] | 13/6 | 256 | 3910 |
| corrective_step_120 | recall_h2 | 20 | 0.516 | 0.40 | +0.183 [+0.060, +0.312] | 14/3 | 262 | 3678 |
| corrective_step_120 | recall_w2 | 20 | 0.357 | 0.30 | +0.024 [-0.126, +0.177] | 10/10 | 259 | 4062 |
| corrective_step_120 | attention | 20 | 0.505 | 0.35 | +0.171 [+0.034, +0.315] | 13/7 | 267 | 4107 |
| corrective_step_120 | episodic_recall | 20 | 0.788 | 0.50 | +0.455 [+0.358, +0.547] | 20/0 | 168 | 2839 |
| corrective_step_480 | defaults | 20 | 0.309 | 0.00 |  |  | 992 | 17211 |
| corrective_step_480 | episodic | 20 | 0.885 | 0.45 | +0.575 [+0.477, +0.660] | 19/1 | 464 | 9005 |
| corrective_step_480 | recall | 20 | 0.666 | 0.40 | +0.357 [+0.179, +0.528] | 15/5 | 768 | 12563 |
| corrective_step_480 | recall_nopos | 20 | 0.734 | 0.45 | +0.424 [+0.271, +0.565] | 17/2 | 757 | 12181 |
| corrective_step_480 | recall_h2 | 20 | 0.768 | 0.60 | +0.459 [+0.303, +0.597] | 17/3 | 766 | 10807 |
| corrective_step_480 | recall_w2 | 20 | 0.730 | 0.60 | +0.420 [+0.273, +0.553] | 17/3 | 807 | 13925 |
| corrective_step_480 | attention | 20 | 0.799 | 0.40 | +0.490 [+0.368, +0.599] | 17/3 | 759 | 16159 |
| corrective_step_480 | episodic_recall | 20 | 0.945 | 0.90 | +0.635 [+0.567, +0.698] | 20/0 | 367 | 6688 |
| natural_live_480 | defaults | 20 | 0.231 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.263 | 0.00 | +0.032 [-0.090, +0.159] | 9/11 | 0 | 0 |
| natural_live_480 | recall | 20 | 0.187 | 0.20 | -0.044 [-0.140, +0.055] | 9/10 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.187 | 0.20 | -0.044 [-0.140, +0.055] | 9/10 | 0 | 0 |
| natural_live_480 | recall_h2 | 20 | 0.139 | 0.05 | -0.092 [-0.170, -0.011] | 7/12 | 0 | 0 |
| natural_live_480 | recall_w2 | 20 | 0.159 | 0.15 | -0.071 [-0.148, +0.008] | 7/13 | 0 | 0 |
| natural_live_480 | attention | 20 | 0.162 | 0.10 | -0.068 [-0.139, +0.004] | 5/13 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.194 | 0.00 | -0.037 [-0.123, +0.059] | 7/12 | 0 | 0 |

## view-visible

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.126 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.126 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 20 | 0.076 | 0.00 | -0.050 [-0.068, -0.032] | 2/18 | 0 | 0 |
| founder | recall_nopos | 20 | 0.076 | 0.00 | -0.050 [-0.068, -0.032] | 2/18 | 0 | 0 |
| founder | recall_h2 | 20 | 0.082 | 0.00 | -0.044 [-0.068, -0.015] | 3/17 | 0 | 0 |
| founder | recall_w2 | 20 | 0.071 | 0.00 | -0.055 [-0.077, -0.032] | 3/17 | 0 | 0 |
| founder | attention | 20 | 0.090 | 0.00 | -0.036 [-0.056, -0.016] | 4/15 | 0 | 0 |
| founder | episodic_recall | 20 | 0.076 | 0.00 | -0.050 [-0.068, -0.032] | 2/18 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.291 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_w2 | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | attention | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.291 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.149 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.863 | 0.80 | +0.714 [+0.572, +0.821] | 18/1 | 0 | 0 |
| natural_step_120 | recall | 20 | 0.017 | 0.00 | -0.133 [-0.175, -0.089] | 2/16 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.017 | 0.00 | -0.133 [-0.175, -0.089] | 2/16 | 0 | 0 |
| natural_step_120 | recall_h2 | 20 | 0.012 | 0.00 | -0.137 [-0.178, -0.095] | 0/16 | 0 | 0 |
| natural_step_120 | recall_w2 | 20 | 0.051 | 0.00 | -0.098 [-0.155, -0.039] | 3/13 | 0 | 0 |
| natural_step_120 | attention | 20 | 0.063 | 0.00 | -0.086 [-0.143, -0.027] | 5/13 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.806 | 0.75 | +0.657 [+0.501, +0.790] | 18/1 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.327 | 0.00 |  |  | 264 | 4902 |
| corrective_step_120 | episodic | 20 | 0.935 | 0.90 | +0.609 [+0.472, +0.718] | 19/1 | 49 | 1055 |
| corrective_step_120 | recall | 20 | 0.539 | 0.40 | +0.212 [+0.031, +0.394] | 13/7 | 234 | 3845 |
| corrective_step_120 | recall_nopos | 20 | 0.616 | 0.35 | +0.288 [+0.108, +0.470] | 14/6 | 224 | 3731 |
| corrective_step_120 | recall_h2 | 20 | 0.600 | 0.55 | +0.273 [+0.097, +0.442] | 14/6 | 237 | 3530 |
| corrective_step_120 | recall_w2 | 20 | 0.571 | 0.50 | +0.244 [+0.032, +0.457] | 12/8 | 226 | 3757 |
| corrective_step_120 | attention | 20 | 0.516 | 0.40 | +0.189 [+0.009, +0.369] | 11/8 | 246 | 4061 |
| corrective_step_120 | episodic_recall | 20 | 0.917 | 0.85 | +0.590 [+0.432, +0.718] | 19/1 | 36 | 649 |
| corrective_step_480 | defaults | 20 | 0.473 | 0.25 |  |  | 885 | 17124 |
| corrective_step_480 | episodic | 20 | 0.972 | 0.95 | +0.499 [+0.363, +0.620] | 18/0 | 127 | 3246 |
| corrective_step_480 | recall | 20 | 0.669 | 0.55 | +0.197 [-0.027, +0.404] | 12/7 | 663 | 10959 |
| corrective_step_480 | recall_nopos | 20 | 0.783 | 0.70 | +0.310 [+0.122, +0.488] | 14/5 | 658 | 11241 |
| corrective_step_480 | recall_h2 | 20 | 0.746 | 0.70 | +0.273 [+0.062, +0.460] | 12/7 | 603 | 8735 |
| corrective_step_480 | recall_w2 | 20 | 0.674 | 0.60 | +0.201 [-0.083, +0.459] | 12/8 | 652 | 10608 |
| corrective_step_480 | attention | 20 | 0.803 | 0.75 | +0.331 [+0.134, +0.514] | 15/5 | 657 | 12066 |
| corrective_step_480 | episodic_recall | 20 | 0.999 | 1.00 | +0.526 [+0.387, +0.643] | 18/0 | 74 | 1279 |
| natural_live_480 | defaults | 20 | 0.213 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.986 | 1.00 | +0.772 [+0.716, +0.836] | 20/0 | 0 | 0 |
| natural_live_480 | recall | 20 | 0.081 | 0.05 | -0.133 [-0.221, -0.031] | 4/14 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.081 | 0.05 | -0.133 [-0.221, -0.031] | 4/14 | 0 | 0 |
| natural_live_480 | recall_h2 | 20 | 0.116 | 0.10 | -0.098 [-0.177, -0.013] | 5/13 | 0 | 0 |
| natural_live_480 | recall_w2 | 20 | 0.161 | 0.10 | -0.053 [-0.162, +0.066] | 7/12 | 0 | 0 |
| natural_live_480 | attention | 20 | 0.071 | 0.05 | -0.143 [-0.241, -0.017] | 3/15 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.984 | 1.00 | +0.770 [+0.713, +0.834] | 20/0 | 0 | 0 |

## view-consecutive

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `defaults` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | defaults | 20 | 0.117 | 0.00 |  |  | 0 | 0 |
| founder | episodic | 20 | 0.117 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall | 20 | 0.069 | 0.00 | -0.048 [-0.068, -0.028] | 3/16 | 0 | 0 |
| founder | recall_nopos | 20 | 0.069 | 0.00 | -0.048 [-0.068, -0.028] | 3/16 | 0 | 0 |
| founder | recall_h2 | 20 | 0.076 | 0.00 | -0.041 [-0.057, -0.024] | 4/16 | 0 | 0 |
| founder | recall_w2 | 20 | 0.075 | 0.00 | -0.042 [-0.065, -0.019] | 4/16 | 0 | 0 |
| founder | attention | 20 | 0.074 | 0.00 | -0.044 [-0.062, -0.023] | 1/18 | 0 | 0 |
| founder | episodic_recall | 20 | 0.069 | 0.00 | -0.048 [-0.068, -0.028] | 3/16 | 0 | 0 |
| random | defaults | 20 | 0.131 | nan |  |  | 0 | 0 |
| random | episodic | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_w2 | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall | 20 | 0.131 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | defaults | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_w2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | defaults | 20 | 0.348 | nan |  |  | 0 | 0 |
| searcher | episodic | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_h2 | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_w2 | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | attention | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall | 20 | 0.348 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| natural_step_120 | defaults | 20 | 0.072 | 0.00 |  |  | 0 | 0 |
| natural_step_120 | episodic | 20 | 0.108 | 0.00 | +0.037 [-0.009, +0.087] | 12/8 | 0 | 0 |
| natural_step_120 | recall | 20 | 0.024 | 0.00 | -0.048 [-0.084, -0.013] | 3/11 | 0 | 0 |
| natural_step_120 | recall_nopos | 20 | 0.024 | 0.00 | -0.048 [-0.084, -0.013] | 3/11 | 0 | 0 |
| natural_step_120 | recall_h2 | 20 | 0.033 | 0.00 | -0.039 [-0.073, -0.004] | 4/12 | 0 | 0 |
| natural_step_120 | recall_w2 | 20 | 0.026 | 0.00 | -0.045 [-0.071, -0.022] | 3/12 | 0 | 0 |
| natural_step_120 | attention | 20 | 0.040 | 0.00 | -0.032 [-0.070, +0.007] | 6/11 | 0 | 0 |
| natural_step_120 | episodic_recall | 20 | 0.046 | 0.00 | -0.026 [-0.059, +0.010] | 6/12 | 0 | 0 |
| corrective_step_120 | defaults | 20 | 0.220 | 0.00 |  |  | 278 | 4522 |
| corrective_step_120 | episodic | 20 | 0.643 | 0.05 | +0.424 [+0.314, +0.532] | 19/1 | 209 | 3509 |
| corrective_step_120 | recall | 20 | 0.316 | 0.05 | +0.096 [-0.045, +0.248] | 11/8 | 269 | 4879 |
| corrective_step_120 | recall_nopos | 20 | 0.297 | 0.05 | +0.077 [-0.015, +0.182] | 12/8 | 275 | 4078 |
| corrective_step_120 | recall_h2 | 20 | 0.252 | 0.05 | +0.033 [-0.062, +0.137] | 8/12 | 276 | 3829 |
| corrective_step_120 | recall_w2 | 20 | 0.265 | 0.05 | +0.046 [-0.040, +0.144] | 10/9 | 271 | 4102 |
| corrective_step_120 | attention | 20 | 0.237 | 0.00 | +0.017 [-0.056, +0.086] | 12/8 | 274 | 4129 |
| corrective_step_120 | episodic_recall | 20 | 0.498 | 0.00 | +0.278 [+0.149, +0.404] | 16/4 | 203 | 3189 |
| corrective_step_480 | defaults | 20 | 0.226 | 0.00 |  |  | 1054 | 20605 |
| corrective_step_480 | episodic | 20 | 0.657 | 0.20 | +0.431 [+0.318, +0.541] | 19/1 | 749 | 16343 |
| corrective_step_480 | recall | 20 | 0.476 | 0.20 | +0.249 [+0.102, +0.397] | 14/6 | 964 | 17715 |
| corrective_step_480 | recall_nopos | 20 | 0.488 | 0.20 | +0.262 [+0.103, +0.422] | 15/5 | 908 | 15694 |
| corrective_step_480 | recall_h2 | 20 | 0.541 | 0.45 | +0.315 [+0.143, +0.479] | 15/5 | 951 | 14416 |
| corrective_step_480 | recall_w2 | 20 | 0.443 | 0.20 | +0.217 [+0.043, +0.389] | 13/7 | 953 | 14550 |
| corrective_step_480 | attention | 20 | 0.435 | 0.15 | +0.209 [+0.055, +0.366] | 14/6 | 946 | 25335 |
| corrective_step_480 | episodic_recall | 20 | 0.794 | 0.60 | +0.568 [+0.455, +0.663] | 18/2 | 703 | 12266 |
| natural_live_480 | defaults | 20 | 0.048 | 0.00 |  |  | 0 | 0 |
| natural_live_480 | episodic | 20 | 0.157 | 0.00 | +0.108 [+0.013, +0.213] | 11/6 | 0 | 0 |
| natural_live_480 | recall | 20 | 0.015 | 0.00 | -0.033 [-0.069, +0.003] | 5/7 | 0 | 0 |
| natural_live_480 | recall_nopos | 20 | 0.015 | 0.00 | -0.033 [-0.069, +0.003] | 5/7 | 0 | 0 |
| natural_live_480 | recall_h2 | 20 | 0.014 | 0.00 | -0.034 [-0.072, +0.003] | 5/9 | 0 | 0 |
| natural_live_480 | recall_w2 | 20 | 0.015 | 0.00 | -0.033 [-0.070, +0.001] | 6/8 | 0 | 0 |
| natural_live_480 | attention | 20 | 0.013 | 0.00 | -0.036 [-0.070, -0.002] | 3/9 | 0 | 0 |
| natural_live_480 | episodic_recall | 20 | 0.098 | 0.00 | +0.050 [-0.023, +0.137] | 7/5 | 0 | 0 |

