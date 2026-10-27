# Cadence 0.89 memory readings (development founders)

## view17-hidden

Uniform random 0.121. Sampled and greedy frozen success, mean over founders; the difference from `recall_nopos` is founder-paired, bootstrap 95%.

| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| founder | recall | 160 | 0.089 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | recall_nopos | 160 | 0.089 | 0.00 |  |  | 0 | 0 |
| founder | episodic_recall | 160 | 0.089 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| founder | episodic_recall_nopos | 160 | 0.089 | 0.00 | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall | 160 | 0.120 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | recall_nopos | 160 | 0.120 | nan |  |  | 0 | 0 |
| random | episodic_recall | 160 | 0.120 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| random | episodic_recall_nopos | 160 | 0.120 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall | 160 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | recall_nopos | 160 | 1.000 | nan |  |  | 0 | 0 |
| oracle | episodic_recall | 160 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| oracle | episodic_recall_nopos | 160 | 1.000 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall | 160 | 0.228 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | recall_nopos | 160 | 0.228 | nan |  |  | 0 | 0 |
| searcher | episodic_recall | 160 | 0.228 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| searcher | episodic_recall_nopos | 160 | 0.228 | nan | +0.000 [+0.000, +0.000] | 0/0 | 0 | 0 |
| corrective_step_120 | recall | 160 | 0.341 | 0.25 | -0.024 [-0.079, +0.028] | 77/75 | 264 | 4109 |
| corrective_step_120 | recall_nopos | 160 | 0.365 | 0.24 |  |  | 267 | 4020 |
| corrective_step_120 | episodic_recall | 160 | 0.751 | 0.47 | +0.386 [+0.327, +0.443] | 131/28 | 161 | 2433 |
| corrective_step_120 | episodic_recall_nopos | 160 | 0.739 | 0.47 | +0.374 [+0.315, +0.433] | 131/28 | 160 | 2423 |
| corrective_step_480 | recall | 160 | 0.566 | 0.44 | +0.005 [-0.070, +0.079] | 84/69 | 835 | 13110 |
| corrective_step_480 | recall_nopos | 160 | 0.562 | 0.42 |  |  | 836 | 12914 |
| corrective_step_480 | episodic_recall | 160 | 0.916 | 0.85 | +0.354 [+0.288, +0.417] | 130/23 | 405 | 5954 |
| corrective_step_480 | episodic_recall_nopos | 160 | 0.919 | 0.83 | +0.358 [+0.291, +0.422] | 134/18 | 393 | 5760 |

