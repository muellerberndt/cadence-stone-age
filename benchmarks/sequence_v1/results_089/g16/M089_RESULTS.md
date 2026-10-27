# Cadence 0.89 memory readings (development founders)

## recall16-gap96

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos_r0_c128` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall_c128 | 20 | 0.504 | 0.50 | +0.000 [-0.006, +0.006] | 11/9 | 0 | 0 |
| founder | recall_r0_c128 | 20 | 0.504 | 0.50 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos_r0_c128 | 20 | 0.504 | 0.50 |  |  | 0 | 0 |
| random | recall_c128 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_r0_c128 | 20 | 0.493 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0_c128 | 20 | 0.493 | nan |  |  | 0 | 0 |
| oracle | recall_c128 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_r0_c128 | 20 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0_c128 | 20 | 1.000 | nan |  |  | 0 | 0 |
| teach_step | recall_c128 | 20 | 0.859 | 0.86 | +0.344 [+0.254, +0.425] | 19/1 | 1536 | 74504 |
| teach_step | recall_r0_c128 | 20 | 0.894 | 0.89 | +0.378 [+0.298, +0.450] | 18/1 | 1536 | 85051 |
| teach_step | recall_nopos_r0_c128 | 20 | 0.516 | 0.51 |  |  | 1536 | 146149 |

## recall16-gap48

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 10 | 0.504 | 0.47 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 10 | 0.504 | 0.47 |  |  | 0 | 0 |
| founder | recall_r0 | 10 | 0.500 | 0.50 | -0.004 [-0.012, +0.004] | 4/4 | 0 | 0 |
| founder | recall_nopos_r0 | 10 | 0.500 | 0.50 | -0.004 [-0.012, +0.004] | 4/4 | 0 | 0 |
| random | recall | 10 | 0.510 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.510 | nan |  |  | 0 | 0 |
| random | recall_r0 | 10 | 0.510 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0 | 10 | 0.510 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 10 | 0.864 | 0.82 | +0.020 [-0.124, +0.171] | 4/3 | 1536 | 86362 |
| teach_step | recall_nopos | 10 | 0.844 | 0.85 |  |  | 1536 | 92317 |
| teach_step | recall_r0 | 10 | 0.886 | 0.95 | +0.042 [-0.095, +0.188] | 4/3 | 1536 | 83901 |
| teach_step | recall_nopos_r0 | 10 | 0.512 | 0.53 | -0.331 [-0.443, -0.203] | 2/8 | 1536 | 147354 |

## recall16-gap16

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 10 | 0.496 | 0.47 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 10 | 0.496 | 0.47 |  |  | 0 | 0 |
| founder | recall_r0 | 10 | 0.503 | 0.50 | +0.007 [-0.003, +0.018] | 6/2 | 0 | 0 |
| founder | recall_nopos_r0 | 10 | 0.503 | 0.50 | +0.007 [-0.003, +0.018] | 6/2 | 0 | 0 |
| random | recall | 10 | 0.500 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.500 | nan |  |  | 0 | 0 |
| random | recall_r0 | 10 | 0.500 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0 | 10 | 0.500 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 10 | 0.944 | 0.95 | +0.273 [+0.129, +0.410] | 7/0 | 1536 | 61238 |
| teach_step | recall_nopos | 10 | 0.671 | 0.68 |  |  | 1536 | 107955 |
| teach_step | recall_r0 | 10 | 0.946 | 0.95 | +0.275 [+0.105, +0.421] | 7/1 | 1536 | 61238 |
| teach_step | recall_nopos_r0 | 10 | 0.598 | 0.68 | -0.074 [-0.205, +0.047] | 6/4 | 1536 | 138154 |

## recall16-gap4

Uniform random as in the `random` control rows. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 10 | 0.509 | 0.53 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 10 | 0.509 | 0.53 |  |  | 0 | 0 |
| founder | recall_r0 | 10 | 0.507 | 0.50 | -0.002 [-0.008, +0.003] | 4/5 | 0 | 0 |
| founder | recall_nopos_r0 | 10 | 0.507 | 0.50 | -0.002 [-0.008, +0.003] | 4/5 | 0 | 0 |
| random | recall | 10 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 10 | 0.496 | nan |  |  | 0 | 0 |
| random | recall_r0 | 10 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos_r0 | 10 | 0.496 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 10 | 1.000 | nan |  |  | 0 | 0 |
| oracle | recall_r0 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos_r0 | 10 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| teach_step | recall | 10 | 0.970 | 0.97 | +0.248 [+0.096, +0.388] | 9/1 | 1536 | 58899 |
| teach_step | recall_nopos | 10 | 0.721 | 0.72 |  |  | 1536 | 121994 |
| teach_step | recall_r0 | 10 | 0.969 | 0.97 | +0.248 [+0.096, +0.387] | 9/1 | 1536 | 59875 |
| teach_step | recall_nopos_r0 | 10 | 0.732 | 0.75 | +0.011 [-0.189, +0.207] | 7/3 | 1536 | 108109 |

