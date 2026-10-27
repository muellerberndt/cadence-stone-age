# Cadence 0.89 memory readings (development founders)

## recall-order-code

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 20 | 0.492 | 0.51 |  |  | 0 | 0 |
| founder | recall_nopos | 20 | 0.492 | 0.51 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | code8 | 20 | 0.506 | 0.52 | +0.014 [+0.002, +0.026] | 14/5 | 0 | 0 |
| founder | code16 | 20 | 0.498 | 0.50 | +0.006 [-0.003, +0.016] | 11/5 | 0 | 0 |
| founder | att8 | 20 | 0.503 | 0.52 | +0.011 [+0.000, +0.023] | 11/6 | 0 | 0 |
| founder | att16 | 20 | 0.492 | 0.50 | +0.000 [-0.009, +0.009] | 8/9 | 0 | 0 |
| founder | att16_addr | 20 | 0.492 | 0.50 | +0.000 [-0.009, +0.009] | 8/9 | 0 | 0 |
| founder | recall_areward | 20 | 0.492 | 0.51 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_h2_areward | 20 | 0.494 | 0.49 | +0.002 [-0.007, +0.011] | 9/9 | 0 | 0 |
| random | recall | 20 | 0.493 | nan |  |  | 0 | 0 |
| random | recall_nopos | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | code8 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | code16 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | att8 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | att16 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | att16_addr | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_areward | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_areward | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | code8 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | code16 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | att8 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | att16 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | att16_addr | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_areward | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 20 | 0.972 | 0.96 |  |  | 1536 | 65928 |
| teach_step | recall_nopos | 20 | 0.671 | 0.72 | -0.301 [-0.366, -0.229] | 1/19 | 1536 | 127298 |
| teach_step | code8 | 20 | 0.498 | 0.50 | -0.473 [-0.504, -0.437] | 0/20 | 1536 | 142904 |
| teach_step | code16 | 20 | 0.883 | 0.89 | -0.089 [-0.194, +0.001] | 4/6 | 1536 | 72378 |
| teach_step | att8 | 20 | 0.497 | 0.50 | -0.475 [-0.506, -0.438] | 0/20 | 1536 | 143162 |
| teach_step | att16 | 20 | 0.932 | 0.94 | -0.040 [-0.103, +0.009] | 2/6 | 1536 | 73678 |
| teach_step | att16_addr | 20 | 0.820 | 0.85 | -0.152 [-0.243, -0.069] | 1/12 | 1536 | 91040 |
| teach_step | recall_areward | 20 | 0.958 | 0.96 | -0.014 [-0.082, +0.040] | 3/3 | 1536 | 66278 |
| teach_step | recall_h2_areward | 20 | 0.945 | 0.94 | -0.027 [-0.101, +0.035] | 3/3 | 1536 | 64203 |
| reward_live | recall | 20 | 0.498 | 0.51 |  |  | 0 | 0 |
| reward_live | recall_nopos | 20 | 0.498 | 0.51 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| reward_live | code8 | 20 | 0.503 | 0.50 | +0.005 [-0.011, +0.023] | 9/8 | 0 | 0 |
| reward_live | code16 | 20 | 0.506 | 0.51 | +0.007 [-0.004, +0.022] | 10/8 | 0 | 0 |
| reward_live | att8 | 20 | 0.500 | 0.50 | +0.001 [-0.009, +0.013] | 7/9 | 0 | 0 |
| reward_live | att16 | 20 | 0.498 | 0.50 | +0.000 [-0.014, +0.014] | 8/10 | 0 | 0 |
| reward_live | att16_addr | 20 | 0.498 | 0.50 | +0.000 [-0.014, +0.014] | 8/10 | 0 | 0 |
| reward_live | recall_areward | 20 | 0.549 | 0.56 | +0.051 [-0.005, +0.130] | 10/8 | 0 | 0 |
| reward_live | recall_h2_areward | 20 | 0.512 | 0.53 | +0.014 [-0.015, +0.063] | 6/9 | 0 | 0 |

