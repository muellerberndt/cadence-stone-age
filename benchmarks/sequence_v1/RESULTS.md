# Sequence instrument v1: development results, 12 October 2026

All readings below are development evidence: historical seeds 42 to 46 or development founders
1001 to 1005, never the confirmation founders. Raw run directories (checkpoints, event logs,
episode tables) are kept outside Git; each run's `manifest.json` binds the Cadence package files
by digest, the wheel digest, this repository's commit and the platform.

Environment: `cadence-net==0.81.0` from PyPI (wheel SHA-256 `182dcc6e590d74358dec021118bd5697025bd051f195863b391515dca918f3a6`),
NumPy 2.5.4, Python 3.13.0, macOS arm64, one BLAS thread.

## V5 reproduced with its own script

`benchmarks/cadence_081/v5_mochi_style.py`, unchanged (SHA-256 `d98b87aa…`), with the published
command (`--train 120 --eval 100 --post-life 80 --guided-span 4 --autonomous-span 8
--fingerprint-samples 300 --seeds 5`). 164 seconds, 65 MB peak.

| Arm | Immediate sampled, per seed (%) | Mean | Reported in V5_MOCHI_RESULTS | After 80 natural episodes, per seed | Mean | Reported |
| --- | --- | --- | --- | --- | --- | --- |
| Corrective teacher | 28, 24, 20, 11, 11 | 18.8 | 18.8, same per seed | 23, 18, 21, 32, 22 | 23.2 | 22.8 (seed 45: 30) |
| Natural only | 0, 10, 0, 0, 1 | 2.2 | 1.0 | 0, 1, 0, 15, 1 | 3.4 | 4.4 |
| Grade only | 0, 1, 0, 0, 0 | 0.2 | 0.2 | 0, 5, 0, 0, 0 | 1.0 | 1.0 |
| Founder | 9, 8, 14, 3, 4 | 7.6 | 7.6 | | | |
| Uniform random | 9, 11, 13, 15, 14 | 12.4 | 12.4 | | | |

Greedy success is 0 for every Cadence arm, as reported. The corrective teacher's immediate scores
reproduce seed for seed; the natural arm and one post-life seed differ, which is expected when
the platform differs from the original run's. Python prints the finite-teaching warning once per
location, so the script cannot count exhausted lessons; this instrument counts them from the
teaching reports.

## Which state the acquired V5 brains use

`p2_v5_state.py` probed the corrective-teacher and founder checkpoints above at every decision of
20 frozen sampled episodes each. At every decision the probe's intact reading equals the
distribution the brain then samples from, and the sham equals the intact reading.

| Checkpoint | Trace cleared | Warm activity cleared | Recall off | Full reset |
| --- | --- | --- | --- | --- |
| Corrective teacher, seeds 42 to 46 | 0.41, 0.41, 0.56, 0.30, 0.11 | 0.00, 0.05, 0.00, 0.00, 0.00 | 0.01, 0.03, 0.03, 0.23, 0.03 | 0.40, 0.41, 0.55, 0.30, 0.11 |
| Founder, seeds 42 to 46 | 0.37, 0.19, 0.31, 0.35, 0.31 | 0 | 0 | 0.37, 0.19, 0.31, 0.35, 0.31 |

Values are mean total-variation distances from the intact next-action distribution. Clearing the
working trace reproduces a full reset; clearing the warm activity changes nothing in nine of ten
checkpoints. Each decision's settle is a fresh equilibrium of the present drive, and the trace is
the only carrier of in-episode history. The untrained founders show the same size of trace effect,
and in the trained brains the trace raises the required action's probability in two seeds and lowers
it in three: the V5 brains use their trace without having learned to keep useful context in it.

## The route cue

Five development founders, the historical recipe, 480 training episodes, 200 frozen evaluation
episodes per mode. Uniform random completes 7.7%.

| Arm | Cue vanishes: sampled % | Cue kept visible: sampled % | Greedy, both |
| --- | --- | --- | --- |
| Natural, step | 0.0 | 0.0 | 0 |
| Grade, step | 2.2 | 0.0 | 0 |
| Natural, live | 3.4 | 1.9 | 0 |
| Guide, step | 10.9 | 11.8 | 0 |

The visible-cue control fails: even with the cue present at the decision, no arm learns the
route-dependent first collection. The graded arms answer one constant collection (first-choice
accuracy 0.50 in every founder), and the reward-only arms mostly stop collecting at the first
decision, because a wrong collection costs −1 at once while waiting defers the same failure. At
these budgets the chamber measures acquisition of the chain, not memory; its causal probe
(`p2_route_probe.py`) is ready for a chamber whose visible control passes.

## P1 development on fresh founders

`runner.py --protocol protocol.json`, development founders 1001 to 1005, 120 training episodes
(4 guided and 8 autonomous decisions), 200 frozen episodes per mode, then 80 episodes with the
caregiver gone, resumed from the life's seam. Sampled success in percent, per founder in brackets;
uniform random 11.6 [9 12 12 14 12] on the same evaluation episodes.

| Arm | Historical recipe (48, 24) | Greedy | After withdrawal | Single region (48) | Greedy | After withdrawal |
| --- | --- | --- | --- | --- | --- | --- |
| Founder | 6.3 [0 1 10 11 8] | 0 | | 4.3 [4 1 8 3 6] | 0 | |
| Natural, step | 0.0 | 0 | 0.0 | 0.0 | 0 | 0.0 |
| Grade, step | 0.2 | 0 | 1.3 | 2.9 [14 0 0 0 0] | 0 | 1.7 |
| Corrective, step | 21.0 [12 0 34 27 32] | 0 | 15.5 | 17.1 [13 26 17 16 14] | 20 [0 100 0 0 0] | 14.9 |
| Corrective, step, qualified teaching | 21.8 [20 20 16 35 18] | 0 | 16.3 | 22.1 [20 26 18 28 18] | 0 | 17.3 |
| Natural, live | 0.3 | 0 | 0.3 | 0.1 | 0 | 0.1 |
| Grade, live | 2.6 | 0 | 2.6 | 6.0 [0 1 14 0 16] | 0 | 6.0 |

Founder-paired differences from uniform random (sampled, percentage points, bootstrap 95% over
founders): corrective +9.4 [−2.3, +18.8] (historical recipe, four founders up) and +5.5 [+2.6, +9.9]
(single region, five up); corrective with qualified teaching +10.2 [+5.7, +16.3] and +10.5
[+7.2, +13.9], five founders up in both recipes. The reward-only and graded arms are below random
in 36 of their 40 founder readings (3 above, 1 equal): under end pay most brains learn to stop
acting on the chain. Qualified teaching refused 12 and 3 of about 1,400 lessons; no finite free
phase ran out of budget.

Reading: the selective caregiver's benefit to the sampled policy replicates on fresh founders;
greedy competence does not (one corrective founder of ten reaches it and keeps it after withdrawal;
one graded founder reaches it only after withdrawal). After the caregiver leaves, continued
natural learning lowers the sampled success in both recipes, and two founders of the historical
recipe fall to zero. V5's own script on its own seeds does reproduce its gain after withdrawal
(above); this instrument differs in its founders and in resuming the life from its seam instead
of a reset, and the two are not yet separated. The live arms learn nothing useful under end pay at
this budget.
