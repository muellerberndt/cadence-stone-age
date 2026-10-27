# Diagnostic of the 0.90 candidate (founders 1101 to 1120, after the readings)

The candidate's `recall` recipe with one 0.89.0 setting restored at a time. Sampled frozen success, mean over founders; differences founder-paired, bootstrap 95%.

## recall-order (teach_step)

| Recipe under the candidate | Sampled | - `recall` under the candidate [95%] | - `recall` under 0.89.0 [95%] |
| --- | --- | --- | --- |
| `recall` (the candidate as composed) | 0.819 | | |
| `recall_every`: lessons on every row (0.89.0's default) | 0.867 | +0.048 [-0.106, +0.199] | -0.122 [-0.215, -0.044] |
| `recall_r025`: the age charge of 0.25 (0.89.0's founder) | 0.765 | -0.054 [-0.189, +0.085] | -0.225 [-0.318, -0.131] |
| `recall_p32`: 0.89.0's position term: 32 exact ages at rate 0.1, no slope | 0.935 | +0.116 [+0.008, +0.223] | -0.055 [-0.125, +0.000] |
| `recall_rate01`: the table taught at 0.1 (0.89.0's rate), the slope kept | 0.931 | +0.112 [+0.001, +0.220] | -0.059 [-0.130, -0.001] |
| `recall_noslope`: no slope, the table exact to 64 at 0.01 kept | 0.817 | -0.002 [-0.122, +0.117] | -0.173 [-0.270, -0.082] |
| `recall_089`: every 0.89.0 setting | 0.990 | +0.171 [+0.080, +0.267] | +0.000 [+0.000, +0.000] |

`recall` under 0.89.0: 0.990.

## route-hidden (guide_step)

| Recipe under the candidate | Sampled | - `recall` under the candidate [95%] | - `recall` under 0.89.0 [95%] |
| --- | --- | --- | --- |
| `recall` (the candidate as composed) | 0.277 | | |
| `recall_every`: lessons on every row (0.89.0's default) | 0.420 | +0.143 [+0.042, +0.251] | -0.053 [-0.241, +0.133] |
| `recall_r025`: the age charge of 0.25 (0.89.0's founder) | 0.291 | +0.014 [-0.070, +0.100] | -0.182 [-0.345, -0.023] |
| `recall_p32`: 0.89.0's position term: 32 exact ages at rate 0.1, no slope | 0.302 | +0.026 [-0.054, +0.121] | -0.171 [-0.317, -0.030] |
| `recall_rate01`: the table taught at 0.1 (0.89.0's rate), the slope kept | 0.276 | -0.001 [-0.080, +0.084] | -0.197 [-0.362, -0.039] |
| `recall_noslope`: no slope, the table exact to 64 at 0.01 kept | 0.248 | -0.028 [-0.114, +0.049] | -0.225 [-0.392, -0.049] |
| `recall_089`: every 0.89.0 setting | 0.473 | +0.197 [+0.050, +0.347] | +0.000 [+0.000, +0.000] |

`recall` under 0.89.0: 0.473.

