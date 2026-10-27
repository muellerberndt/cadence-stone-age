# Cadence 0.89 memory readings (development founders)

## recall-order

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `carried` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | carried | 20 | 0.498 | 0.50 |  |  | 0 | 0 |
| founder | retained | 20 | 0.498 | 0.50 | +0.000 [-0.001, +0.001] | 4/3 | 0 | 0 |
| founder | recall | 20 | 0.492 | 0.51 | -0.006 [-0.016, +0.004] | 5/11 | 0 | 0 |
| founder | recall_nopos | 20 | 0.492 | 0.51 | -0.006 [-0.016, +0.004] | 5/11 | 0 | 0 |
| founder | recall_r0 | 20 | 0.494 | 0.50 | -0.004 [-0.015, +0.008] | 7/11 | 0 | 0 |
| founder | recall_nopos_r0 | 20 | 0.494 | 0.50 | -0.004 [-0.015, +0.008] | 7/11 | 0 | 0 |
| founder | recall_h2 | 20 | 0.494 | 0.49 | -0.004 [-0.013, +0.003] | 6/10 | 0 | 0 |
| founder | recall_h2_nopos | 20 | 0.494 | 0.49 | -0.004 [-0.013, +0.003] | 6/10 | 0 | 0 |
| founder | attention | 20 | 0.503 | 0.52 | +0.006 [-0.003, +0.015] | 11/5 | 0 | 0 |
| random | carried | 20 | 0.493 | nan |  |  | 0 | 0 |
| random | retained | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_r0 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_h2_nopos | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | attention | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | carried | 20 | 1.000 | nan |  |  | 0 | 0 |
| oracle | retained | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_h2_nopos | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | attention | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | carried | 20 | 0.499 | 0.50 |  |  | 1536 | 147366 |
| teach_step | retained | 20 | 0.498 | 0.50 | -0.000 [-0.002, +0.000] | 1/2 | 1536 | 147370 |
| teach_step | recall | 20 | 0.972 | 0.96 | +0.473 [+0.437, +0.504] | 20/0 | 1536 | 65928 |
| teach_step | recall_nopos | 20 | 0.671 | 0.72 | +0.172 [+0.114, +0.241] | 16/3 | 1536 | 127298 |
| teach_step | recall_r0 | 20 | 0.981 | 0.97 | +0.483 [+0.449, +0.511] | 20/0 | 1536 | 65928 |
| teach_step | recall_nopos_r0 | 20 | 0.644 | 0.70 | +0.146 [+0.088, +0.210] | 17/1 | 1536 | 130336 |
| teach_step | recall_h2 | 20 | 0.967 | 0.97 | +0.469 [+0.411, +0.506] | 20/0 | 1536 | 63486 |
| teach_step | recall_h2_nopos | 20 | 0.720 | 0.75 | +0.221 [+0.159, +0.288] | 20/0 | 1536 | 121814 |
| teach_step | attention | 20 | 0.497 | 0.50 | -0.001 [-0.005, +0.002] | 7/8 | 1536 | 143162 |
| reward_step | carried | 20 | 0.496 | 0.50 |  |  | 0 | 0 |
| reward_step | retained | 20 | 0.495 | 0.50 | -0.002 [-0.008, +0.004] | 3/3 | 0 | 0 |
| reward_step | recall | 20 | 0.492 | 0.51 | -0.004 [-0.013, +0.004] | 8/10 | 0 | 0 |
| reward_step | recall_nopos | 20 | 0.492 | 0.51 | -0.004 [-0.013, +0.004] | 8/10 | 0 | 0 |
| reward_step | recall_r0 | 20 | 0.494 | 0.50 | -0.002 [-0.009, +0.004] | 6/7 | 0 | 0 |
| reward_step | recall_nopos_r0 | 20 | 0.494 | 0.50 | -0.002 [-0.009, +0.004] | 6/7 | 0 | 0 |
| reward_step | recall_h2 | 20 | 0.499 | 0.51 | +0.003 [-0.011, +0.019] | 4/9 | 0 | 0 |
| reward_step | recall_h2_nopos | 20 | 0.499 | 0.51 | +0.003 [-0.011, +0.019] | 4/9 | 0 | 0 |
| reward_step | attention | 20 | 0.501 | 0.50 | +0.004 [-0.008, +0.020] | 6/8 | 0 | 0 |
| reward_live | carried | 20 | 0.497 | 0.50 |  |  | 0 | 0 |
| reward_live | retained | 20 | 0.499 | 0.50 | +0.002 [-0.013, +0.016] | 8/6 | 0 | 0 |
| reward_live | recall | 20 | 0.498 | 0.51 | +0.001 [-0.014, +0.014] | 7/6 | 0 | 0 |
| reward_live | recall_nopos | 20 | 0.498 | 0.51 | +0.001 [-0.014, +0.014] | 7/6 | 0 | 0 |
| reward_live | recall_r0 | 20 | 0.498 | 0.51 | +0.001 [-0.008, +0.010] | 6/7 | 0 | 0 |
| reward_live | recall_nopos_r0 | 20 | 0.498 | 0.51 | +0.001 [-0.008, +0.010] | 6/7 | 0 | 0 |
| reward_live | recall_h2 | 20 | 0.493 | 0.51 | -0.004 [-0.019, +0.009] | 5/10 | 0 | 0 |
| reward_live | recall_h2_nopos | 20 | 0.493 | 0.51 | -0.004 [-0.019, +0.009] | 5/10 | 0 | 0 |
| reward_live | attention | 20 | 0.500 | 0.50 | +0.002 [-0.015, +0.018] | 9/7 | 0 | 0 |

