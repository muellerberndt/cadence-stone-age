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

### Under the delayed-credit live regime (14 October 2026)

`protocol-p2-route-visible-live.json`, development founders 1001 to 1005, the published
`cadence-net==0.83.0` wheel (SHA-256 `6ea5eb6b…`), NumPy 2.5.4, Python 3.13.7, macOS arm64, one BLAS
thread, instrument commit `376b8c4`. The regime is the one the recall world validated through `live`:
the composed trace (amplitude 3.0, scale 1.2, retention 0) with the delayed-credit actor point (lam
0.95, gamma 0.95, critic rate 5) at actor step 0.1 (`delayed`) or 0.03 (`arena`), the body's need 0.2
per moment and a youth of 300 moments, passed to `Brain.compose` as `arousal={"need": 0.2, "youth":
300}`; V5's brain (`historical`: modules (48, 24), compose actor step 1.0, the founder arousal) is the
paired contrast. Arms through `live` with and without the grade (the grade carries no label, so
`live` takes it), 1920 training episodes with a 480-episode reading as an arm of its own length (the
same founder through the first 480 episodes of the same schedule) and a `step` control for the
`delayed` recipe; 200 frozen episodes per mode, `Brain.reset` per episode. Whole-route success and
first-choice accuracy in %, per founder in brackets. Uniform random completes 7.7% and takes the
right first collection in 20% of episodes; a constant first collection reads 50 at the first choice.
A founder passes the control when its greedy first choice is right on both routes and its greedy
whole-route success is above the founder and random controls.

| Recipe | Arm | Episodes | Success, sampled | Success, greedy | First choice, sampled | First choice, greedy | Greedy first choice right on both routes | Passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | Founder | 0 | 9.5 [14 10 4 9 10] | 0 | 21.9 [22 24 16 25 22] | 30.0 [50 0 0 50 50] | none | none |
| delayed | Natural, live | 480 | 15.2 [28 22 3 9 14] | 0 | 22.2 [32 26 2 31 21] | 20.0 [0 0 0 50 50] | none | none |
| delayed | Natural, live | 1920 | 42.1 [86 30 0 64 30] | 20.0 [100 0 0 0 0] | 52.0 [78 28 52 50 52] | 80.0 [100 50 50 100 100] | 1001, 1004, 1005 | 1001 |
| delayed | Grade, live | 480 | 26.3 [35 22 18 22 34] | 0 | 28.5 [36 19 16 31 40] | 70.0 [100 50 0 100 100] | 1001, 1004, 1005 | none |
| delayed | Grade, live | 1920 | 59.5 [24 96 0 96 82] | 60.0 [0 100 0 100 100] | 62.1 [38 72 50 81 68] | 80.0 [50 100 50 100 100] | 1002, 1004, 1005 | 1002, 1004, 1005 |
| delayed | Natural, step | 1920 | 40.8 [0 96 4 100 4] | 40.0 [0 100 0 100 0] | 52.9 [0 88 35 92 49] | 60.0 [0 100 50 100 50] | 1002, 1004 | 1002, 1004 |
| arena | Founder | 0 | 9.5 [14 10 4 9 10] | 0 | 21.9 [22 24 16 25 22] | 30.0 [50 0 0 50 50] | none | none |
| arena | Natural, live | 480 | 21.8 [29 18 18 23 22] | 0 | 26.8 [30 24 22 28 29] | 30.0 [50 0 0 50 50] | none | none |
| arena | Natural, live | 1920 | 26.5 [41 16 20 28 28] | 0 | 29.0 [44 16 21 34 30] | 50.0 [50 0 0 100 100] | 1004, 1005 | none |
| arena | Grade, live | 480 | 29.4 [36 22 32 32 25] | 0 | 29.4 [36 18 23 42 28] | 60.0 [50 50 0 100 100] | 1004, 1005 | none |
| arena | Grade, live | 1920 | 65.0 [74 40 84 69 57] | 50.0 [100 0 100 50 0] | 46.6 [64 42 48 41 38] | 90.0 [100 50 100 100 100] | 1001, 1003, 1004, 1005 | 1001, 1003, 1004 |
| historical | Founder | 0 | 12.2 [10 13 10 10 18] | 0 | 20.2 [18 23 26 15 19] | 10.0 [0 0 50 0 0] | none | none |
| historical | Natural, live | 480 and 1920 | 5.5 [0 0 16 11 0] | 0 | 10.9 [2 0 23 16 14] | 10.0 [0 0 50 0 0] | none | none |
| historical | Grade, live | 480 and 1920 | 8.9 [0 15 9 8 12] | 0 | 17.6 [2 25 24 14 23] | 30.0 [0 100 0 0 50] | 1002 | none |

Founder-paired differences from uniform random at 1920 episodes (sampled, percentage points,
bootstrap 95% over founders): `delayed` natural live +34.4 [+9.9, +63.2] (four founders up), grade
live +51.8 [+15.7, +85.1] (four up), step +33.1 [−5.2, +71.9] (two up); `arena` natural live +18.8
[+10.7, +26.9] and grade live +57.3 [+42.7, +69.2] (five up each); `historical` natural live −2.2
[−7.5, +4.0] and grade live +1.2 [−2.9, +5.1]. At 480 episodes the greedy policy of every arm and
recipe times out in all 1,000 episodes: where its first collection is right, on both routes in three
founders of the graded `delayed` arm, a later stage fails. The sampled policy of the `arena` arms and
of the graded `delayed` arm is above random at 480 episodes in five founders of five. The
`historical` readings at 480 and 1920 episodes are identical in every founder.

The training lives at 1920 episodes: the life's own success over all episodes and over its last
480, and the share of decisions answered in the aroused mode (%, per founder):

| Recipe, arm | Life success, all | Last 480 | Aroused decisions, all | Last 480 |
| --- | --- | --- | --- | --- |
| delayed, natural live | 21.2 [47 16 11 16 17] | 32.5 [100 16 6 19 21] | 94.0 [70 100 100 100 100] | 79.9 [0 100 100 100 100] |
| delayed, grade live | 27.3 [16 27 8 42 43] | 52.9 [15 59 5 86 100] | 88.6 [100 92 100 78 72] | 59.3 [100 66 100 31 0] |
| delayed, natural step | 45.3 [2 51 59 64 51] | 73.0 [0 96 87 98 84] | | |
| arena, natural live | 16.4 [20 14 18 14 16] | 18.6 [25 13 20 15 20] | 100 | 100 |
| arena, grade live | 30.4 [44 16 53 22 17] | 53.6 [100 18 100 30 20] | 89.6 [81 100 68 100 100] | 59.8 [0 99 0 99 100] |
| historical, natural live | 0.1 [0 0 0 0 0] | 0.0 | 0.4 [0 0 0 0 0] | 0.0 |
| historical, grade live | 0.0 [0 0 0 0 0] | 0.0 | 0.3 [0 0 0 0 0] | 0.0 |

Reading: the visible-cue control passes under the delayed-credit live regime on four founders of
five with the `delayed` recipe (1001 with reward alone, 1002, 1004 and 1005 with the grade) and on
three of five with `arena` (1001, 1003 and 1004 with the grade; 1004 completes one route), where
V5's brain fails on every founder as it did in the earlier reading. Through `live`, V5's brain is
calm after its youth and learns nothing, so its two budget readings are one reading; the regime's
brains stay aroused through most of their lives and the ones that pass settle into a calm routine
that completes the route in every one of their last 480 episodes. The passing founders differ by
arm: the grade carries 1002, 1004 and 1005, reward alone carries 1001, and founder 1003 learns the
route in no arm of the `delayed` recipe. The `step` control passes on 1002 and 1004; its lives on
1003 and 1005 reach 95 to 98% success in a 120-episode block and fall to 12 and 46% over their last
24 episodes, so their seam readings are of a policy that moved late. Every greedy whole-route
failure of the regime's arms at 1920 episodes is a timeout or a lock at the first collection; no
arm answers with the founder's constant.

**The vanished cue on the passing founders.** `protocol-p2-route-live.json` (the same regime, arms
and budgets, the cue at event 0 only), instrument commit `9a39834`, run on the founders whose
visible control passed: `delayed` on 1001, 1002, 1004 and 1005 and `arena` on 1001, 1003 and 1004.
Uniform random completes 7.5 and 7.8%.

| Recipe | Arm | Episodes | Success, sampled | Success, greedy | First choice, sampled | First choice, greedy | Greedy first choice per founder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | Founder | 0 | 8.8 [12 10 6 8] | 0 | 19.6 [21 18 18 22] | 12.5 [0 0 50 0] | craft fire; warm up; stone; stone on A and wood on B |
| delayed | Natural, live | 480 | 18.1 [14 22 17 20] | 0 | 16.9 [11 20 16 20] | 0 | craft fire or warm up in every founder |
| delayed | Natural, live | 1920 | 20.2 [28 20 14 20] | 0 | 17.5 [18 18 14 20] | 0 | craft fire or warm up in every founder |
| delayed | Grade, live | 480 | 24.5 [34 20 28 17] | 0 | 20.4 [20 21 20 22] | 25.0 [0 50 50 0] | craft fire; wood; wood on A and craft fire on B; warm up |
| delayed | Grade, live | 1920 | 27.0 [1 42 24 40] | 25.0 [0 50 0 50] | 34.0 [42 24 32 38] | 50.0 [50 50 50 50] | wood in every founder |
| delayed | Natural, step | 1920 | 35.1 [34 44 34 30] | 12.5 [0 50 0 0] | 18.8 [19 20 17 20] | 12.5 [0 50 0 0] | craft fire; stone; warm up; craft fire |
| arena | Founder | 0 | 8.0 [12 6 6] | 0 | 18.2 [21 16 18] | 16.7 [0 0 50] | craft fire; craft fire; stone |
| arena | Natural, live | 480 | 21.3 [23 22 20] | 0 | 17.0 [18 18 15] | 0 | craft fire; craft fire; wait |
| arena | Natural, live | 1920 | 16.0 [16 20 12] | 0 | 12.7 [14 11 12] | 0 | craft fire; craft fire; warm up |
| arena | Grade, live | 480 | 28.8 [39 26 22] | 16.7 [50 0 0] | 20.2 [27 14 19] | 16.7 [50 0 0] | stone; craft fire; wait |
| arena | Grade, live | 1920 | 29.7 [29 37 23] | 0 | 14.3 [18 12 13] | 0 | craft fire in every founder |

The causal probe (`p2_route_probe.py`) on every trained checkpoint: two copies of the frozen brain
live the cue phase of route A and of route B and face the byte-identical first decision. The
probability of the route's required first collection, A / B per founder, intact and after a trace
erase; the sham round trip equals the intact reading in all 24 and 15 checkpoints, and
`Brain.reset` reads as the trace erase in all 78 readings:

| Recipe, arm, 1920 episodes | Intact, A / B per founder | After a trace erase | Both routes right, greedy |
| --- | --- | --- | --- |
| delayed, natural live | 0.19/0.19, 0.17/0.18, 0.16/0.16, 0.19/0.19 | 0.19/0.20, 0.16/0.17, 0.16/0.16, 0.19/0.19 | 0 of 4 |
| delayed, grade live | 0.69/0.13, 0.35/0.15, 0.68/0.02, 0.38/0.30 | 0.74/0.07, 0.33/0.15, 0.58/0.04, 0.26/0.30 | 0 of 4 |
| delayed, natural step | 0.18/0.20, 0.20/0.21, 0.14/0.23, 0.19/0.20 | 0.18/0.20, 0.20/0.21, 0.13/0.28, 0.19/0.20 | 0 of 4 |
| arena, natural live | 0.13/0.15, 0.10/0.09, 0.16/0.16 | 0.16/0.17, 0.14/0.14, 0.16/0.16 | 0 of 3 |
| arena, grade live | 0.18/0.19, 0.16/0.14, 0.16/0.17 | 0.18/0.19, 0.17/0.18, 0.16/0.17 | 0 of 3 |

Reading: with the cue vanished, no founder of either recipe passes. The reward-only lives stay
aroused to the end and their greedy first choice is to craft or to warm up, with nothing collected;
the graded `delayed` lives settle on wood first, the context-blind constant that reads 50 at the
first choice and completes route A alone (greedy 50 on 1002 and 1005), and the graded `arena` lives
craft first. The probe finds the first-decision policy the same after cue A
and after cue B in every checkpoint, within 0.12 of itself after a trace erase, and unmoved by the
other branch's trace, so the working trace of this regime carries nothing of the cue across the two
neutral events at the decision, and the lives' first choices over their last 480 episodes are at
chance and independent of the previous episode's route. The same probe on the brains trained with
the cue visible finds the cue carried in two checkpoints of 30 in the `delayed` recipe, both
`step`-trained (founders 1002 and 1004: both routes right intact, 0.85/0.66 and 0.87/0.87; route B
lost after a trace erase, 0.79/0.03 and 0.80/0.05, and lost with the other branch's trace), and in
none of 25 in `arena`. The chamber measures memory on these founders under this regime: the visible
control passes and the vanished cue fails, on the reward path and on the graded path, at 480 and at
1920 episodes.

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

## Cadence 0.82.0 against 0.81.0, published wheels

Cadence 0.82.0 carries the composed brain's context differently: the prefrontal copy of the last
interpretation keeps amplitude 3.0 but is read back through a projection that starts at scale 1.2
instead of 12, and the trace carries exactly the last interpretation (retention 0 instead of 0.2).
Both releases ran in one interpreter (Python 3.13.7, NumPy 2.5.4, macOS arm64, one BLAS thread):
the PyPI 0.81.0 wheel (SHA-256 `182dcc6e…`) and the 0.82.0 wheel as published (`716b7008…`).

**V5's own script**, published command, seeds 42 to 46. On 0.82.0 the script's version guard
(`if version != "0.81.0":`) accepts 0.82.0 as well; nothing else differs. Frozen full-chain success
in %, sampled, per seed, then the mean:

| Arm | 0.81.0 immediate | 0.82.0 immediate | 0.81.0 after 80 natural episodes | 0.82.0 after 80 natural episodes |
| --- | --- | --- | --- | --- |
| Corrective teacher | 28, 24, 20, 11, 11 (18.8) | 28, 33, 38, 9, 24 (**26.4**) | 23, 18, 21, 32, 22 (23.2) | 31, 69, 0, 4, 24 (**25.6**) |
| Natural only | 0, 10, 0, 0, 1 (2.2) | 0, 1, 0, 1, 15 (3.4) | 0, 1, 0, 15, 1 (3.4) | 1, 0, 0, 11, 19 (6.2) |
| Grade only | 0, 1, 0, 0, 0 (0.2) | 0, 0, 7, 0, 0 (1.4) | 0, 5, 0, 0, 0 (1.0) | 0, 0, 83, 0, 0 (16.6) |
| Founder / uniform random | 7.6 / 12.4 | 9.2 / 12.4 | | |

**P1 on fresh founders 1001 to 1005** (`protocol-p1-library-defaults.json`: V5's layout at the
library's own trace defaults, 120 training episodes, 200 frozen episodes, then 80 natural episodes).
Sampled %, per founder, immediately → after the caregiver leaves:

| Arm | 0.81.0 | 0.82.0 |
| --- | --- | --- |
| Correcting executed mistakes | 12 0 34 27 32 (21.0) → 14 0 12 27 24 (15.5) | 96 26 33 54 16 (**44.8**) → 86 26 53 1 0 (33.2) |
| The same, qualified | 20 20 16 35 18 (21.8) → 20 0 30 0 32 (16.3) | 66 36 52 54 12 (**44.3**) → 20 0 66 0 0 (17.2) |
| Reward only (`natural_step`) | 0 0 0 0 0 → 0 0 0 0 0 | 20 0 0 16 32 (13.4) → 30 0 19 29 31 (21.7) |
| Graded only | 0 0 0 0 0 → 0 0 0 6 0 | 0 0 0 0 0 → 0 60 0 0 0 |
| Untrained founder (uniform random 11.6) | 0 1 10 11 8 (6.3) | 6 10 14 18 14 (12.3) |

Reading: with 0.82.0 an untrained brain is no longer worse than random on the observed chain,
correcting executed mistakes doubles the frozen success, reward alone lifts three founders above
random where 0.81.0 lifted none, and single founders reach full greedy competence (1001 under
correction, greedy 100% before and after withdrawal). The chain is not mastered: after the
caregiver leaves, skills still erode in some founders (V5 seeds 44 and 45, P1 founders 1004 and
1005), and the route task with a vanished cue is not addressed by this release.

Reproduce:

```sh
python -m pip install cadence-net==0.82.0
sed -i.bak 's/    if version != "0.81.0":/    if version not in ("0.81.0", "0.82.0"):/' \
  benchmarks/cadence_081/v5_mochi_style.py
python benchmarks/cadence_081/v5_mochi_style.py --train 120 --eval 100 --post-life 80 \
  --guided-span 4 --autonomous-span 8 --fingerprint-samples 300 --seeds 5
cd benchmarks/sequence_v1
python runner.py --protocol protocol-p1-library-defaults.json --out ../../p1-082 \
  --seeds 1001 1002 1003 1004 1005
```

## After the caregiver leaves: `step` against `live`, and a motor bias at birth (0.82.0)

`protocol-p1-next.json`, the published 0.82.0 wheel, fresh founders 1001 to 1005, V5's layout,
120 training episodes, 200 frozen episodes, then 80 episodes alone. Two new instrument options: an
arm's life after the caregiver may continue through another interface (`withdrawal_adapter`), and a
recipe may set every motor bias once at birth (`motor_bias`; zero in every released composition).
Sampled %, per founder, immediately → after the life alone:

| Arm | 0.82.0 composition | Motor bias 0.3 at birth |
| --- | --- | --- |
| Corrected while taught, then alone through `step` | 96 25.5 33 54 15.5 (44.8) → 86 26 53 1 0 (33.2) | 0.5 60 87 0.5 74.5 (44.5) → 1.5 28 0.5 20.5 1 (10.3) |
| Corrected while taught, then alone through `live` | same → 85.5 28.5 37.5 47 14 (**42.5**) | same → 0.5 31.5 0 2.5 1.5 (7.2) |
| Reward only through `step` | 19.5 0 0 16 31.5 (13.4) → 29.5 0 19 29 31 (21.7) | 1.5 0.5 0.5 0 0 (0.5) → 1.5 0 0 0 0 (0.3) |
| Reward only through `live` | 2 3.5 0 17 16 (7.7) → unchanged | 5 0 0 3.5 9 (3.5) → 5 0 0 3.5 20 (5.7) |
| Untrained founder | 5.5 10 14 18 14 (12.3) | 4 5 17 13 12.5 (10.3) |

Reading: a brain that continues alone through `live` keeps what the caregiver taught. Calm moments
do not learn, and the two collapses of the `step` continuation (founders 1004 and 1005) do not
happen; the price is less further improvement (founder 1003: 37.5 against 53). `live` from birth
with reward only learns little at this budget. A motor bias of 0.3 at birth, which makes a taught
recall chamber recall far better, harms this chain: two founders learn nothing while taught,
reward alone learns nothing, and even `live` does not keep what was taught.

## Tests adapted from cadence-teachers, Cadence 0.83.0 (14 October 2026)

The tests this instrument adapts from Will Glynn's
[cadence-teachers](https://github.com/WGlynn/cadence-teachers) (README, "Tests adapted from
cadence-teachers"), run with their declared protocols on development founders from 1001 on and,
for the replica check, on the notebook's seeds 42 to 53. Environment: the published
`cadence-net==0.83.0` wheel (SHA-256 `6ea5eb6b…`), NumPy 2.5.4, Python 3.13.7, macOS arm64,
one BLAS thread, instrument commits `f42305d` and `4bb77c4`.

**The port is exact.** The chamber rules and observations (2,000 random episodes, plain and
weather), the weather splits, the memoryless formula, the searcher's value and the per-state
reads of three checkpoints equal the notebook's code on identical inputs. The drift design run
in V5's order on EXP-47's seeds equals EXP-47's own script run on this machine in all 240
readings (per-state answers and greedy success; taught and after 10, 20, 40 and 80 episodes
alone; both paths, both signals), when both are read at the same point. That script on this
machine matches its published Windows readings in 48 of 48 taught readings and 44 to 48 of 48
at each checkpoint.

**Where a reading is taken matters for a memory brain.** This instrument reads a checkpoint at
its seam, before the last outcome is delivered; the notebook reads after delivering it. One
outcome changes the memory brain's per-state answers often: on EXP-47's seeds 7 founders have
every stage right after teaching at the seam and 9 after the delivery. Every result below holds
at both reading points; the tables give the seam reading unless they say otherwise.

### Generalization under an unseen weather (EXP-48)

`protocol-p3-generalization.json`, twelve founders, 120 training episodes under the four taught
weathers. Per-state greedy accuracy over the 16 taught and the 16 unseen situations (%),
founders with every unseen situation right, and whole-chain success under the unseen weathers
(%). Uniform random 12.4, never-repeat searcher 30.0 (exact 30.4), untaught founder 12.5.

| Arm | Taught weathers | Unseen weathers | Gap, founder-paired | Every unseen situation right | Sampled | Greedy |
| --- | --- | --- | --- | --- | --- | --- |
| Untaught founder | 20 | 18 | +2.1 [−0.5, +4.7] | 0 | 12.5 | 0.0 |
| Corrected, without memory | 54 | 54 | +0.0 [−3.1, +2.6] | 0 | 32.1 | 0.0 |
| Reward only, without memory | 30 | 29 | +1.0 [+0.0, +3.1] | 0 | 6.2 | 2.1 |
| Corrected, episodic memory | 87 | 86 | +1.0 [−2.1, +4.2] | 6 | 90.7 | 89.6 |
| Reward only, episodic memory | 72 | 69 | +3.6 [+0.5, +7.3] | 4 | 56.1 | 39.6 |

Under the unseen weathers the memory adds 32.3 points per state to correction (bootstrap 95%
[+13.5, +46.9], ten founders up, one down; +43.8 read after the delivery) and 40.1 to reward
alone ([+21.9, +58.3]).

Reading: what the memory brain learns carries to situations it never met. The gap between
taught and unseen weathers stays within four points at both reading points, and under unseen
weathers the corrected memory brain completes the chain three times as often as the searcher.
Corrected without the memory, the brain reads half the situations right and completes the chain
as often as the searcher. EXP-48 read 89 and 84 per state and +31 over the plain brain on its
seeds; the two agree.

### The content of a label (EXP-52, EXP-53)

`protocol-p3-content.json`, twenty-four founders with the episodic memory. Each founder is taught
three ways at each lesson length: by the correcting caregiver, by its random-label twin (a
uniformly random action at the same kind of moment) and not at all; every arm then lives 20
episodes alone through `live`. Per-state greedy accuracy under the unseen weathers (%), with
founder-paired differences (points, bootstrap 95%, founders up/down):

| Lesson | Reading | Corrected | Random label | Untaught | Content: corrected − random | Corrected − untaught | Random − untaught |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 40 | end of the lesson | 71.1 | 66.7 | 29.9 | +4.4 [−12.8, +21.9], 12/9 | +41.1 [+27.6, +54.4], 20/3 | +36.7 [+22.7, +50.0], 18/5 |
| 40 | after 20 alone | 72.9 | 56.0 | 38.5 | **+16.9** [+6.2, +28.4], 14/6 | +34.4 [+21.1, +47.7], 20/4 | +17.4 [+2.3, +32.6], 15/6 |
| 120 | end of the lesson | 83.6 | 68.5 | 58.1 | +15.1 [+4.2, +27.1], 13/7 | +25.5 [+9.6, +40.6], 17/4 | +10.4 [−5.7, +26.8], 11/12 |
| 120 | after 20 alone | 79.4 | 58.1 | 58.3 | **+21.4** [+9.6, +32.6], 19/4 | +21.1 [+6.2, +36.5], 13/6 | −0.3 [−17.4, +16.9], 12/12 |
| 240 | end of the lesson | 81.2 | 85.9 | 72.9 | −4.7 [−14.8, +4.9], 11/9 | +8.3 [−5.7, +23.2], 14/10 | +13.0 [+3.1, +23.7], 14/7 |
| 240 | after 20 alone | 76.8 | 70.6 | 69.0 | +6.2 [−5.7, +18.2], 14/8 | +7.8 [−7.0, +22.9], 13/9 | +1.6 [−9.6, +12.8], 13/9 |

The content after 20 episodes alone, by reading point and order:

| Lesson | Seam order, at the seam | Seam order, after delivery | V5's order (`protocol-p3-content-reset.json`), at the seam | V5's order, after delivery |
| --- | --- | --- | --- | --- |
| 40 | +16.9 [+6.2, +28.4] | +16.7 [+5.5, +28.1] | +23.2 [+8.9, +37.5] | +23.7 [+12.5, +34.9] |
| 120 | +21.4 [+9.6, +32.6] | +22.1 [+9.4, +34.6] | +16.4 [+7.0, +25.8] | +20.8 [+12.0, +29.7] |
| 240 | +6.2 [−5.7, +18.2] | +2.6 [−8.1, +13.5] | +8.3 [−0.5, +17.4] | +5.7 [−3.9, +15.6] |

Labels given over all founders: corrected 1,149, 2,441 and 3,840; random 1,920, 4,199 and
6,028 at the three lengths (a randomly labelled student makes more mistakes in guided windows).

Reading: the content of a label reaches the memory brain at 40- and 120-episode lessons, in both
orders and at both reading points. Being corrected at all lifts a 40-episode student far above
an untaught one, whatever the label says (+36.7 at the end of the lesson); 20 episodes alone
through `live` keep what the right labels taught and lose half of what random labels gave. At
120 episodes the right labels lead at the end of the lesson too. At 240 episodes reward alone
has taught the untaught brain most of the chain and the three arms lie within noise of one
another. EXP-53 read the content as +1.3, +10.7 and +6.8 points with standard errors near six.
EXP-53's own script, run on this machine, reproduces its published 40-episode readings student for
student (24 of 24; at 120 and 240 episodes the platforms part, 19 and 3 of 24 identical). With 48
more students it reads +12.5 and +9.9 for the next two groups of 24, and +7.9 (SEM 4.5) over all
72. The instrument on EXP-53's 24 students' own seeds reads +8.6 [−7.3, +24.2] in V5's order.
EXP-53's 40-episode null sits at the low end of what samples of 24 students give; across these
samples the right label adds between 8 and 24 points at 40-episode lessons.

### The life alone, read over time (EXP-46, EXP-47)

`protocol-p1-drift.json` (resumed from the seam) and `protocol-p1-drift-reset.json` (V5's order),
twelve founders each, 120 training episodes, then 80 episodes alone through `live` and, from the
same taught brain, through `step`. Corrected memory brain, read after the held outcome is
delivered (EXP-47's reading point): founders with every stage right after teaching and after 10,
20, 40 and 80 episodes alone; founders whose greedy policy completes the chain after 80; mean
per-state accuracy after 80 (%).

| Founders and order | Path | Every stage right | Greedy completes at 80 | Per-state at 80 |
| --- | --- | --- | --- | --- |
| 42 to 53, V5's order | `live` | 9, 8, 7, 6, 6 | 12 | 88 |
| 42 to 53, V5's order | `step` | 9, 8, 8, 6, 9 | 11 | 92 |
| 1001 to 1012, V5's order | `live` | 9, 8, 9, 9, 9 | 12 | 90 |
| 1001 to 1012, V5's order | `step` | 9, 9, 9, 9, 6 | 8 | 85 |
| 1001 to 1012, from the seam | `live` | 9, 10, 10, 10, 10 | 12 | 92 |
| 1001 to 1012, from the seam | `step` | 9, 10, 10, 9, 5 | 10 | 79 |
| EXP-47 as published, 42 to 53 | `live` | 9, 8, 6, 5, 5 | 12 | 85 |
| EXP-47 as published, 42 to 53 | `step` | 9, 8, 8, 6, 9 | 12 | 94 |

Without the memory the same corrections leave 56% per state and whole-chain success at 40.0%
(EXP-46: 58% and 19.3%); with it, 92% and 99.1% (EXP-46: 94% and 96.3%). Reward-only learners
with the memory end the 80 episodes alone between 2 points below and 15 points above their
per-state accuracy after teaching, on either path and at either reading point.

Reading: EXP-47's drift through `live` reproduces on its own seeds, and on twelve fresh founders
the two paths trade places: `live` keeps all nine fully right founders and `step` loses three.
Pooled over the 24 founders run in V5's order, both paths end with 15 of 18 fully right founders.
The greedy policy completes the chain in 22 of 24 after teaching, and after 80 episodes alone in
24 of 24 through `live` and 19 of 24 through `step`. At this sample size, which stage drifts and
on which path depends on the founder; the greedy stall through `step` that the episodic memory
guide describes appears, and through `live` it does not.

## The memory of Cadence 0.89.0 where context decides a later action (26 October 2026)

[M089_PROTOCOL.md](M089_PROTOCOL.md) declares the readings, and `memory_089.py` writes their protocols, jobs and tables.

**Setup.**
- Library: the published `cadence-net==0.89.0` wheel (SHA-256 `7b27009d…`). NumPy 2.5.4, Python 3.12.3, Linux x86-64, one BLAS thread per runner.
- Founders: development founders only, 202001-202020 on the chain views and 1001-1010 elsewhere.
- Frozen copies are read at the arm's seam: 100 sampled and 1 greedy episode on the views, 200 on the route and P1, 224 on the recall world.
- Each cell below is the mean over founders. The full tables are in [results_089/g1/M089_RESULTS.md](results_089/g1/M089_RESULTS.md); the founder-paired contrasts between recipes are in [results_089/g1/M089_CONTRASTS.md](results_089/g1/M089_CONTRASTS.md).

### Grid 1: sampled frozen success (greedy in brackets)

| Reading, arm | Base | Episodic vote | Recall (position on) | Recall, no position | Recall, 2 heads | Episodic + recall |
| --- | --- | --- | --- | --- | --- | --- |
| Recall world, taught (`teach_step`) | 0.49 | | **0.99** (0.99) | 0.75 (0.77) | **1.00** (1.00) | |
| Recall world, reward through `live` | 0.48 | | 0.69 (0.78) | 0.69 (0.78) | **0.84** (0.90) | |
| Route cue hidden, guided | 0.17 | 0.45 (0.50) | 0.37 (0.20) | 0.28 (0.15) | 0.42 (0.30) | **0.60** (0.50) |
| Route cue visible, guided (chamber control) | 0.24 | 0.95 (0.90) | 0.50 (0.45) | 0.34 (0.20) | 0.43 (0.35) | **0.98** (1.00) |
| Hidden view (A B A B), corrected, 120 | 0.19 | 0.55 (0.25) | 0.48 (0.35) | 0.34 (0.10) | 0.37 (0.25) | **0.72** (0.40) |
| Hidden view, corrected, 480 | 0.23 | 0.87 (0.65) | 0.58 (0.50) | 0.51 (0.45) | 0.69 (0.60) | **0.90** (0.85) |
| Hidden view, reward through `live`, 480 | 0.03 | 0.86 (1.00) | 0.02 | 0.02 | 0.03 | **0.88** (1.00) |
| Invisible view (A A B C), corrected, 480 | 0.31 | 0.89 (0.45) | 0.67 (0.40) | 0.73 (0.45) | 0.77 (0.60) | **0.94** (0.90) |
| Consecutive view (A A B B), corrected, 480 | 0.23 | 0.66 (0.20) | 0.48 (0.20) | 0.49 (0.20) | 0.54 (0.45) | **0.79** (0.60) |
| Visible view (control), reward through `live`, 480 | 0.21 | **0.99** (1.00) | 0.08 (0.05) | 0.08 (0.05) | 0.12 (0.10) | 0.98 (1.00) |
| P1 (control), corrected | 0.39 | **0.93** (0.90) | 0.55 (0.40) | 0.69 (0.20) | 0.66 (0.60) | 0.92 (0.80) |

**Chance:**
- Uniform random completes the chain views and P1 in 0.121 of episodes. The untrained founder brains read 0.12-0.14.
- On the route and the recall world, the `random` control reads 0.09 and 0.49.

**Founder-paired contrasts (sampled, 95% bootstrap over founders):**
- **The position term alone** (recall minus recall without it):
  - recall world, taught: +0.24 [+0.12, +0.37], 9 founders up and 1 down;
  - hidden view, corrected, 120 episodes: +0.13 [−0.03, +0.30];
  - route cue, guided: +0.08 (hidden) and +0.16 (visible), neither interval clear of zero;
  - visible view, corrected: −0.08 and −0.11; P1, corrected: −0.14 and +0.22; no interval is clear of zero;
  - every reward-only arm: 0 exactly.
- **The recall memory with the episodic vote**, against the vote alone: hidden view, corrected, 120 episodes, +0.18 [+0.01, +0.34] (16 up, 4 down); route cue hidden, guided, +0.14 [−0.03, +0.31].
- **The learned-code recipe** (`attention=True`) against plain recall:
  - recall world, taught: −0.19 [−0.31, −0.07];
  - route cue, guided: −0.23 and −0.28.

### Reading

1. **The episodic vote carries most of the gain on every chamber and under every signal.** That includes reward alone through `live`: on the hidden view, 0.03 for the base against 0.86 with the vote, greedy 1.00 on all 20 founders. It also makes the route chamber's visible control pass (0.90-0.95 under each signal), so the route cue now measures memory. With the cue hidden, the guided vote reaches 0.45 against 0.95 visible.
2. **The recall memory helps only where lessons teach it.**
   - Under corrections and the guide it adds +0.15 to +0.46 to the base.
   - Under reward alone and through `live` it adds nothing or costs. On the visible view the base learns 0.21 through `live` and the recall brains 0.08. Every untrained recall founder reads about 0.05 below the base.
   - The address map and the position term are taught by lessons only. The read's extra drive is there from birth.
3. **The position term helps where order is the question and lessons teach it.**
   - Recall world (the latest written value), taught: 0.99 against 0.75 without it.
   - On the aliased chains and the route its effect is small and within the noise of 10 to 20 founders: positive on the hidden view and the route, negative on the visible view and P1.
4. **The recall memory adds to the vote under corrections on the aliased views.** Greedy passes at 480 episodes:

   | View | Episodic + recall | Episodic alone |
   | --- | --- | --- |
   | invisible | 0.90 | 0.45 |
   | consecutive | 0.60 | 0.20 |
   | hidden | 0.85 | 0.65 |

   Under reward alone the combination equals the vote.
5. **Two heads are the best plain recall recipe at 480 corrected episodes and under reward in the recall world** (0.84 against 0.69 through `live`). The paired intervals touch zero.

### Grid 2: the recall world and the route cue on 20 new founders (1011 to 1030)

Tables: [results_089/g2/M089_RESULTS.md](results_089/g2/M089_RESULTS.md) and [contrasts](results_089/g2/M089_CONTRASTS.md).

| Reading, arm | Base | Episodic vote | Episodic + recall | Episodic + recall, no position | Episodic + recall, 2 heads | Recall, 2 heads |
| --- | --- | --- | --- | --- | --- | --- |
| Route cue hidden, guided, 480 | 0.21 | 0.49 (0.42) | 0.61 (0.60) | 0.66 (0.60) | 0.62 (0.60) | 0.56 (0.47) |
| Route cue hidden, guided, 1920 | 0.19 | 0.57 (0.53) | 0.65 (0.55) | 0.61 (0.55) | **0.77** (0.78) | 0.51 (0.35) |
| Route cue hidden, reward through `live`, 1920 | 0.00 | 0.17 (0.07) | 0.27 (0.12) | 0.27 (0.12) | **0.32** (0.25) | 0.00 |
| Route cue visible, guided, 1920 (control) | 0.21 | **0.99** (0.97) | 0.97 (0.90) | 0.98 (0.97) | 0.94 (0.90) | 0.64 (0.55) |
| Route cue visible, reward through `live`, 1920 (control) | 0.00 | 0.93 (1.00) | **0.95** (1.00) | 0.95 (1.00) | 0.92 (1.00) | 0.00 |

Recall world, taught, sampled (greedy):

| Base | Recall | Recall, no position | Position 4 | Position rate 0.3 | 2 heads | 2 heads, no position | 4 heads | Address reward |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.49 | 0.97 (0.97) | 0.91 (0.94) | 0.97 | 0.98 | 0.99 (1.00) | 0.96 | 0.99 | 0.98 |

Under reward through `live`:
- recall 0.84 (0.91);
- two heads 0.80;
- four heads 0.84.

Contrasts, sampled, 95% over founders:

| Contrast | Reading, arm | Difference | Founders up / down |
| --- | --- | --- | --- |
| Position term | recall world, taught | +0.06 [+0.01, +0.12] | 10 / 4 |
| Position term | recall world, 2 heads, taught | +0.03 [+0.00, +0.08] | |
| Position term | route cue, with the episodic vote | −0.05 and +0.03 (within noise) | |
| Recall with the vote, against the vote alone | route cue hidden, guided | +0.13 [+0.04, +0.22] | 13 / 6 |
| Four heads against two | recall world, reward through `step` | +0.13 [+0.05, +0.21] | |

Reward training of the address map (`recall_address_reward=1.0`) changed nothing measurable. Four exact ages behave like 32 in the recall world, whose episodes are short.

**Reading.** In both grids, the position term helps the taught recall world, the reading where order decides the answer: over the 30 founders of the two grids, recall answers 0.97-0.99 and the memory without the term 0.75-0.91. It does not help the route cue, whose answer is found by content. With the cue hidden, the best memory recipe, the episodic vote with two recall heads at 1920 guided episodes, reaches 0.77. With the cue visible the same recipes reach 0.94-0.99, so the cue is still not carried reliably across the two neutral events.

### Grid 3: the chain views on 40 new founders (202021 to 202060)

Tables: [results_089/g3/M089_RESULTS.md](results_089/g3/M089_RESULTS.md) and [contrasts](results_089/g3/M089_CONTRASTS.md). Sampled (greedy):

| View, arm | Recall | Recall, no position | Recall at amplitude 1 | Episodic vote | Episodic + recall | Episodic + recall, no position | Episodic + 2 heads |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hidden, corrected, 120 | 0.45 (0.38) | 0.41 (0.28) | 0.24 (0.07) | 0.65 (0.28) | 0.76 (0.50) | 0.71 (0.55) | **0.79** (0.53) |
| Hidden, corrected, 480 | 0.61 (0.53) | 0.53 (0.42) | 0.34 (0.20) | 0.83 (0.72) | **0.94** (0.82) | 0.94 (0.90) | 0.94 (0.88) |
| Hidden, reward through `live`, 480 | 0.03 | 0.03 | 0.01 | 0.84 (0.90) | **0.91** (1.00) | 0.91 (1.00) | 0.91 (1.00) |
| Invisible, corrected, 120 | 0.46 (0.15) | 0.46 (0.28) | 0.36 (0.07) | **0.89** (0.47) | 0.77 (0.50) | 0.89 (0.65) | 0.84 (0.47) |
| Invisible, corrected, 480 | 0.73 (0.30) | 0.59 (0.25) | 0.34 (0.05) | 0.95 (0.85) | **0.96** (1.00) | 0.96 (0.97) | 0.95 (0.97) |
| Invisible, reward through `live`, 480 | 0.12 | 0.12 | 0.12 | **0.31** (0.12) | 0.21 (0.12) | 0.21 (0.12) | 0.24 (0.15) |
| Visible, corrected, 480 (control) | 0.80 (0.62) | 0.80 (0.72) | 0.62 (0.47) | 0.98 (0.93) | **1.00** (1.00) | 1.00 (1.00) | 1.00 (1.00) |

Contrasts, sampled, 95% over the 40 founders:

| Contrast | Reading | Difference | Founders up / down |
| --- | --- | --- | --- |
| The recall memory with the vote, against the vote alone | hidden, corrected, 480 | +0.11 [+0.02, +0.20] | 26 / 10 |
| The same | hidden, reward through `live` | +0.07 [+0.01, +0.13] | 23 / 14 |
| The same | invisible, corrected, 120 | −0.12 [−0.23, −0.01] | |
| The position term | hidden, 120 / 480 | +0.04 / +0.08 | 19/19 and 20/18 |
| The position term | invisible, 480 | +0.14 [−0.00, +0.29] | |
| The position term with the vote | any view | within ±0.05, except invisible at 120: −0.12 [−0.22, −0.03] | |
| The read at amplitude 1, against 3 | hidden, invisible, visible | −0.18 to −0.39 | |

The quieter read loses what lessons teach and does not remove the cost under reward alone.

**Reading.**
- Over 60 founders, the position term is a small positive effect on the aliased chains that the noise does not resolve.
- On the hidden view, where history (A after B) tells the stage, the recall memory adds to the vote under both corrections and reward. On the invisible view, where only the brain's own previous action tells the stage, it costs the vote early in teaching. The recall memory keys and stores observations, never the brain's own actions.

### The recall world per condition

From the episode tables (sampled, taught). [results_089/g1/M089_CONDITIONS.md](results_089/g1/M089_CONDITIONS.md), [g2](results_089/g2/M089_CONDITIONS.md):

| Condition | Base | Recall, grid 1 / grid 2 | Recall without position, grid 1 / grid 2 | Two heads, grid 1 / grid 2 |
| --- | --- | --- | --- | --- |
| one write, 0-2 neutral events | 0.47-0.51 | 0.99-1.00 / 0.99-1.00 | 0.75-0.82 / 0.95-0.96 | 0.99-1.00 / 0.99-1.00 |
| one write, 1-2 distractors | 0.50-0.52 | 0.99-1.00 / 0.99-1.00 | 0.82-0.83 / 0.94 | 0.99-1.00 / 0.99-1.00 |
| two writes, the latest asked (`order-latest`) | 0.48-0.53 | 1.00 / 0.90 | 0.70 / 0.90 | 1.00 / 1.00 |
| two writes with gaps (`replacement`) | 0.45-0.48 | **0.95 / 0.92** | **0.53 / 0.74** | 1.00 / 1.00 |

Under reward through `live` the position term is untrained and the two-write conditions stay the hardest:
- `order-latest`: 0.52-0.69;
- `replacement`: 0.61-0.84;
- one write: 0.69-0.95.

### Grid 4: longer lives, a wider brain, no recency charge (hidden view 202001 to 202020, hidden route 1001 to 1020)

Tables: [results_089/g4/M089_RESULTS.md](results_089/g4/M089_RESULTS.md) and [contrasts](results_089/g4/M089_CONTRASTS.md). Sampled (greedy):

| Reading, arm | Episodic vote | Vote at (96, 48) | Episodic + recall | Episodic + recall, recency 0 | Episodic + recall at (96, 48) | Recall | Recall at (96, 48) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hidden view, corrected, 1920 | 0.96 (0.95) | 0.92 (0.85) | 0.98 (1.00) | **0.99** (1.00) | 0.99 (0.95) | 0.65 (0.60) | 0.49 (0.35) |
| Hidden view, reward through `live`, 1920 | 0.86 (1.00) | 0.87 (1.00) | 0.88 (1.00) | 0.83 (1.00) | 0.89 (1.00) | 0.05 | 0.02 |
| Hidden route, guided, 1920 | 0.54 (0.42) | 0.59 (0.55) | 0.64 (0.60) | **0.72** (0.72) | 0.68 (0.65) | 0.37 (0.28) | 0.53 (0.50) |
| Hidden route, reward through `live`, 1920 | 0.19 (0.05) | 0.18 (0.03) | **0.33** (0.20) | 0.21 (0.03) | 0.22 (0.10) | 0.00 | 0.00 |

Contrasts, sampled, 95% over founders:

| Contrast | Reading | Difference | Founders up / down |
| --- | --- | --- | --- |
| The recall memory with the vote, against the vote alone | hidden route, reward through `live` | +0.14 [+0.01, +0.25] | 13 / 7 |
| The same | hidden route, guided | +0.10 [−0.02, +0.24] | |
| Twice the width | hidden view, corrected, 480 | −0.14 [−0.33, +0.03] | |
| Twice the width, recall alone | hidden view, corrected, 480 and 1920 | −0.13 and −0.15 | |
| No recency charge | hidden route, reward through `live` | −0.12 [−0.24, −0.00] | |

Twice the width otherwise changes nothing measurable. No recency charge otherwise changes nothing measurable either.

**Reading.**
- The hidden view is solved by the episodic vote with the recall memory once lessons are long (0.98-0.99 at 1920 corrected episodes, greedy 1.00), and nearly so through `live` (0.88-0.92, greedy 1.00).
- The hidden route is not solved. With the cue gone after one event and two neutral events before the decision, the best recipe reaches 0.72 guided and 0.33 through `live`, against 0.94-0.99 with the cue kept visible.
- Width does not close the gap.

### Grid 5: the ordered recall world, the first or the latest written value (founders 1001 to 1020)

The recall world with a query of its own for the first value (`"ask": "order"` in the world entry, `ORDER_CONDITIONS` in `worlds.py`, rules tested in `tests/test_recall_order.py`). Each episode writes two values and then asks for one of them:
- the first value, at a new query marker;
- the latest value, at the old query marker.

The writes are adjacent or one neutral event apart, and one neutral event precedes the query. Only one input bit says which write is asked, so content alone cannot choose: the read has to look back by order. The base, its arms (1536 episodes) and the evaluation (224 episodes) are the recall world's.

Tables: [results_089/g5/M089_RESULTS.md](results_089/g5/M089_RESULTS.md), [contrasts](results_089/g5/M089_CONTRASTS.md) and [per condition](results_089/g5/M089_CONDITIONS.md).

Sampled frozen success (greedy). Uniform random 0.50.

| Recipe | Taught (`teach_step`) | Reward through `step` | Reward through `live` |
| --- | --- | --- | --- |
| Base (`carried`) | 0.50 (0.50) | 0.50 | 0.50 |
| Retained working trace | 0.50 (0.50) | 0.49 | 0.50 |
| Recall, position term | **0.97** (0.96) | 0.49 | 0.50 |
| Recall, no position term | 0.67 (0.72) | 0.49 | 0.50 |
| Recall, position term, recency 0 | **0.98** (0.97) | 0.49 | 0.50 |
| Recall, no position term, recency 0 | 0.64 (0.70) | 0.49 | 0.50 |
| Two heads, position term | **0.97** (0.97) | 0.50 | 0.49 |
| Two heads, no position term | 0.72 (0.75) | 0.50 | 0.49 |
| Learned-code recipe (`attention=True`, 8 units) | 0.50 (0.50) | 0.50 | 0.50 |

Per condition, taught:

| Condition | Position term | No position term |
| --- | --- | --- |
| Adjacent writes, first or latest asked | 0.96-0.98 | 0.73-0.85 |
| One neutral event between the writes | 0.96-0.98 | 0.53-0.64, near chance |

The position term, founder-paired, taught, 95% over 20 founders:

| Recipe | Difference | Founders up / down |
| --- | --- | --- |
| Recall | **+0.30 [+0.23, +0.37]** | 19 / 1 |
| Recall, recency 0 | +0.34 [+0.27, +0.40] | 19 / 0 |
| Two heads | +0.25 [+0.17, +0.32] | 18 / 1 |

**Reading.**
- A lesson teaches the read to look back to the first or the latest write only with the position term. Without it, the read still separates adjacent writes partly, through the successor read, but loses them once one event lies between.
- No recipe learns the ordered question from reward alone, in 1536 episodes through `step` or `live`. The position term and the address map are taught by lessons only, so a rewarded brain never learns where to look.
- The learned-code recipe with 8 units learns neither recall world even when taught.

### Grid 6: the vanished route cue at longer delays (founders 1001 to 1020, 1920 episodes)

The route cue world with 2, 4 or 8 neutral events between the cue and the first decision. Tables: [results_089/g6/M089_RESULTS.md](results_089/g6/M089_RESULTS.md) and [contrasts](results_089/g6/M089_CONTRASTS.md).

Sampled (greedy), guided:

| Neutral events | Episodic vote | Episodic + recall | Episodic + recall, no position | Episodic + 2 heads | Recall | Recall, no position |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.54 (0.42) | 0.64 (0.60) | 0.63 (0.55) | **0.71** (0.75) | 0.37 (0.28) | 0.38 (0.23) |
| 4 | 0.47 (0.42) | 0.53 (0.47) | 0.57 (0.53) | **0.59** (0.55) | 0.47 (0.38) | 0.37 (0.30) |
| 8 | 0.47 (0.42) | 0.47 (0.40) | 0.46 (0.42) | 0.49 (0.40) | **0.59** (0.47) | 0.31 (0.17) |

Reward through `live`, sampled, by neutral events:

| Recipe | 2 | 4 | 8 |
| --- | --- | --- | --- |
| Episodic vote | 0.19 | 0.18 | 0.21 |
| Vote and recall | 0.33 | 0.28 | 0.13 |
| Recall alone | 0.00 | 0.00 | 0.00 |

Contrasts, sampled, 95% over 20 founders:

| Contrast | Reading | Difference | Founders up / down |
| --- | --- | --- | --- |
| The vote with the recall memory, against the vote alone | 2 events, guided / through `live` | +0.10 / +0.14 | |
| The same | 4 events, guided / through `live` | +0.07 / +0.10 | |
| The same | 8 events, guided / through `live` | +0.01 / −0.08 | |
| The position term, recall alone | 8 events, guided | **+0.27 [+0.12, +0.44]** | 13 / 7 |
| The position term, recall alone | 2 and 4 events, guided | −0.01 and +0.10 | |
| The position term, with the vote | any delay | within ±0.03 | |

**Reading.**
- As the cue recedes, the recall memory's help to the vote shrinks, and at 8 events it is gone.
- Alone, recall needs its position term more the further back the cue lies: at 8 events it reaches 0.59 with the term against 0.31 without it, and beats the vote (0.47).
- With the vote in the choice, the position term's effect disappears at every delay. The vote decides where both are present, and the read's look-back does not reach the choice.

### Grid 7: the ordered recall world with learned codes, reward-trained addresses, and a life alone (founders 1001 to 1020)

The ordered recall world as in grid 5. The taught arm then lives 512 episodes alone through `live`. Tables: [results_089/g7/M089_RESULTS.md](results_089/g7/M089_RESULTS.md) and [contrasts](results_089/g7/M089_CONTRASTS.md).

Sampled (greedy), and after 512 episodes alone:

| Recipe | Taught | After 512 alone through `live` | Reward through `live` |
| --- | --- | --- | --- |
| Recall | **0.97** (0.96) | 0.96 | 0.50 |
| Recall, no position term | 0.67 (0.72) | 0.71 | 0.50 |
| Recall on a learned code of 8 units | 0.50 (0.50) | 0.50 | 0.50 |
| Recall on a learned code of 16 units | 0.88 (0.89) | 0.89 | 0.51 |
| Contextual recipe, 8 units | 0.50 (0.50) | 0.50 | 0.50 |
| Contextual recipe, 16 units | 0.93 (0.94) | 0.94 | 0.50 |
| Contextual recipe, 16 units, address lesson on | 0.82 (0.85) | 0.83 | 0.50 |
| Recall, reward trains the address map | 0.96 (0.96) | 0.96 | 0.55 (0.56) |
| Two heads, reward trains the address maps | 0.95 (0.94) | 0.95 | 0.51 |

Contrasts, sampled, 95% over 20 founders:

| Contrast | Reading | Difference | Founders up / down |
| --- | --- | --- | --- |
| A 16-unit code against 8 units | contextual recipe, taught | +0.44 [+0.37, +0.49] | 19 / 1 |
| Recall on a 16-unit code against recall on the observation | taught | −0.09 [−0.19, +0.00] | |
| The address lesson on | contextual recipe | −0.11 [−0.22, −0.00] | |
| Reward training of the address map | reward through `live` | +0.05 [−0.01, +0.13] | |

**Reading.**
- An 8-unit code cannot hold these observations: 10 inputs, two value tokens and two query markers. Every memory keyed on it fails, so the width of a learned code is a capacity limit. At 16 units the contextual recipe answers 0.93.
- A taught memory brain keeps the ordered recall through 512 episodes alone. Calm moments of `live` change nothing.
- Reward training of the address map does not teach the ordered question.

### Grid 8: the recall memory alone at 8 and 16 neutral events, recency on and off (founders 1001 to 1020)

Tables: [results_089/g8/M089_RESULTS.md](results_089/g8/M089_RESULTS.md) and [contrasts](results_089/g8/M089_CONTRASTS.md). The recall runs at 8 events repeat grid 6's on the same founders, and their readings are identical.

Guided, 1920 episodes, sampled (greedy):

| Neutral events | Recall | Recall, no position | Recall, recency 0 | Recall, no position, recency 0 | Recall, 2 heads | Episodic vote | Vote and recall, recency 0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | **0.59** (0.47) | 0.31 (0.17) | 0.54 (0.47) | 0.52 (0.45) | 0.53 (0.42) | 0.47 (0.42) | 0.51 (0.42) |
| 16 | 0.41 (0.30) | 0.36 (0.20) | **0.57** (0.47) | 0.34 (0.25) | 0.41 (0.30) | 0.43 (0.35) | 0.44 (0.42) |

Reward through `live` at both delays:
- every recall recipe without the vote: 0.00;
- the vote: 0.17-0.21;
- the vote and recall at recency 0: 0.22-0.23.

Contrasts, sampled, 95% over 20 founders:

| Contrast | Neutral events | Difference | Founders up / down |
| --- | --- | --- | --- |
| The position term, recency 0 | 16 | **+0.22 [+0.09, +0.35]** | 14 / 6 |
| The position term, recency 0 | 8 | +0.02 | |
| The position term, founder recency 0.25 | 8 | +0.27 [+0.12, +0.44] | |
| The position term, founder recency 0.25 | 16 | +0.05 | |
| Recency 0 against 0.25, with the position term | 16 | +0.16 [+0.02, +0.30] | 16 / 4 |

**Reading.**
- The founder recency charge (0.25 per moment) works against the position term at long delays. At 8 events, without the charge, content alone finds the cue, and the term matters only where the charge has to be overcome. At 16 events the charge (4 logits at the cue's slot) defeats what the term learns. Without it, the term carries the cue across 16 events: 0.57 against 0.34.
- The position term's per-bucket offset can itself learn a recency profile where one helps.
- Reward alone still teaches no recall recipe to use the cue at these delays.

### Grid 9: the episodic vote's context and weight at 8 and 16 neutral events (founders 1001 to 1020)

Tables: [results_089/g9/M089_RESULTS.md](results_089/g9/M089_RESULTS.md) and [contrasts](results_089/g9/M089_CONTRASTS.md).

Sampled, 1920 episodes. Each cell is guided / reward through `live`:

| Neutral events | Vote, context 0.5 | Context 0.8 | Context 0.9 | Context 0.9 and recall | Vote at half weight | Half weight and recall | Recall alone |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 0.47 / 0.21 | 0.43 / 0.11 | 0.48 / 0.22 | 0.54 / 0.18 | 0.48 / 0.02 | 0.52 / 0.02 | **0.59** / 0.00 |
| 16 | 0.43 / 0.17 | 0.46 / 0.24 | 0.43 / 0.18 | **0.47** / **0.29** | 0.47 / 0.04 | 0.39 / 0.03 | 0.41 / 0.00 |

**Reading.**
- Keeping more of the past in the vote's context key (0.8 or 0.9 per moment against 0.5) changes nothing under guidance: within ±0.03.
- Halving the vote's weight costs the reward-only arm 0.13-0.19 and does not let the recall read through.
- After 8 or 16 identical neutral events the context trace is dominated by them: at 0.9 the cue keeps about 2% of the trace at 16 events. The vote's context records cannot carry a cue across such a delay, whatever the decay.
- In these grids only the recall memory's position term carries the cue across the longest delays, and only where lessons teach it: grid 8, recency 0.

### Grid 10: recency 0 against the founder 0.25 with the position term, on new founders across worlds

Founders:
- 1021 to 1040 on the recall worlds and the route;
- 202021 to 202060 on the views.

Tables: [results_089/g10/M089_RESULTS.md](results_089/g10/M089_RESULTS.md), [contrasts](results_089/g10/M089_CONTRASTS.md) and [per condition](results_089/g10/M089_CONDITIONS.md).

Recency 0 minus recency 0.25, sampled, 95% over founders:

| Reading, arm | Recall | Episodic + recall | Recall, 2 heads |
| --- | --- | --- | --- |
| Route, 2 neutral events, guided | **+0.24 [+0.03, +0.45]** (0.41 → 0.64) | +0.03 | −0.07 |
| Route, 16 neutral events, guided | **+0.18 [+0.01, +0.35]** (0.40 → 0.58) | +0.05 [+0.01, +0.09] | +0.08 (0.58 → **0.66**) |
| Hidden view, corrected, 480 | **−0.18 [−0.33, −0.04]** (0.61 → 0.42) | −0.05 | +0.03 |
| Hidden view, reward through `live`, 480 | −0.01 | −0.06 [−0.11, −0.01] | −0.00 |
| Visible view, corrected, 120 and 480 | +0.04 and −0.06 | +0.04 and 0.00 | −0.01 and 0.00 |
| Recall world, taught / reward through `live` | −0.01 / −0.05 | | −0.00 / −0.01 |
| Ordered recall world, taught | −0.01 | | +0.01 |

**Reading.**
- The recency charge helps where the newest record should win: the hidden chain, where the second A has to be read against the B just before it.
- The charge hurts where an old record has to win: the route cue across neutral events. There the read without the charge and with the position term does best, two heads at 16 events reaching 0.66.
- Neither founder value suits both.
- A recency profile the lessons can change would serve both. One way is to start the position term's per-bucket offset at the charge and drop the fixed charge, so that a new brain reads as today.

### Grid 11: the chain views with the brain's last executed action shown (founders 202001 to 202020)

The view chain with `"efference": true`: the observation also shows the brain's last executed action, five inputs, all zero before an episode's first decision. The world and rules are otherwise unchanged; the test is in `tests/test_recall_order.py`. Recipes, arms and founders are grid 1's, so every comparison is founder-paired across the two grids (`efference_vs_g1.py`). Tables: [results_089/g11/M089_RESULTS.md](results_089/g11/M089_RESULTS.md) and [the paired effects](results_089/g11/efference-vs-g1.json).

Sampled, with grid 1's reading without the action in brackets:

| View, arm | Base | Recall | Recall, no position | Episodic vote | Episodic + recall |
| --- | --- | --- | --- | --- | --- |
| Consecutive, corrected, 480 | 0.37 (0.23) | 0.69 (0.48) | 0.65 (0.49) | **0.98** (0.66) | 0.99 (0.79) |
| Consecutive, reward through `live`, 480 | 0.06 (0.05) | 0.11 (0.02) | 0.11 (0.02) | **0.75** (0.16) | 0.53 (0.10) |
| Invisible, corrected, 120 | 0.38 (0.33) | 0.61 (0.51) | 0.57 (0.50) | 0.86 (0.83) | **0.98** (0.79) |
| Invisible, reward through `live`, 480 | 0.15 (0.23) | 0.20 (0.19) | 0.20 (0.19) | **0.84** (0.26) | 0.65 (0.19) |
| Hidden, corrected, 120 | 0.24 (0.19) | 0.47 (0.48) | 0.66 (0.34) | 0.89 (0.55) | **0.93** (0.72) |
| Hidden, reward through `live`, 480 | 0.05 (0.03) | 0.05 (0.02) | 0.05 (0.02) | 0.62 (0.86) | 0.64 (0.88) |

Founder-paired effect of showing the action, 95% over 20 founders:

| Reading | Recipe | Effect | Founders up / down |
| --- | --- | --- | --- |
| Consecutive, corrected, 120 / 480 | Episodic vote | **+0.31 [+0.23, +0.38]** / **+0.33 [+0.23, +0.42]** | 20/0, 19/0 |
| Consecutive, reward through `live` | Episodic vote | **+0.60 [+0.43, +0.74]** | 18 / 2 |
| Invisible, reward through `live` | Episodic vote | **+0.58 [+0.43, +0.72]** | 18 / 2 |
| Consecutive, reward through `live` | Episodic + recall | +0.43 | |
| Invisible, reward through `live` | Episodic + recall | +0.45 | |
| Consecutive, corrected, 120 | Episodic + recall | +0.45 [+0.27, +0.61] | 19 / 1 |
| Consecutive, reward through `live` | Recall | +0.09 [+0.03, +0.18] | |
| Hidden, reward through `live` | Episodic vote | **−0.23 [−0.42, −0.06]** | |
| Hidden, reward through `live` | Episodic + recall | −0.24 [−0.40, −0.09] | |

**Reading.**
- Where only the brain's own previous action tells two stages apart, showing that action is worth more than any memory option, above all to a brain learning from reward alone. The episodic vote's context records already fade in what the stream did, yet they gain 0.58-0.60 when the action is in the observation.
- The recall memory, whose slots hold observations only, gains in the corrected arms.
- On the hidden view, where the observations' history tells the stage, the extra inputs cost the reward-only learners.
- An efference copy belongs in what the memories key on and store, with its weight learned, not fixed.

### Grid 12: the long-delay route with 3840 guided episodes (founders 1001 to 1020)

Tables: [results_089/g12/M089_RESULTS.md](results_089/g12/M089_RESULTS.md) and [contrasts](results_089/g12/M089_CONTRASTS.md).

Sampled (greedy):

| Neutral events, cue | Episodic vote | Recall, recency 0 | Recall, 2 heads, recency 0 | Vote and recall, recency 0 |
| --- | --- | --- | --- | --- |
| 8, hidden | 0.46 (0.45) | **0.59** (0.42) | 0.48 (0.40) | 0.53 (0.57) |
| 8, visible | **0.98** (0.97) | 0.48 (0.28) | 0.35 (0.24) | 0.98 (0.97) |
| 16, hidden | 0.48 (0.50) | 0.38 (0.30) | 0.49 (0.35) | 0.49 (0.45) |
| 16, visible | **0.99** (1.00) | 0.43 (0.32) | 0.45 (0.30) | 0.99 (1.00) |

**Two lives failed.** In one recall brain at recency 0 and one with two heads (founders 1018 and 1006, cue visible), a decision's free phase did not settle within its 1024 steps: residuals 0.028 and 0.0031 against the tolerance 0.003. `act` raised, the life ended, and those two cells hold 19 founders.

**Reading.**
- Twice the lessons leave the hidden route where 1920 left it. The vote recipes reach 0.46-0.53 with the cue gone and 0.98-0.99 with it visible.
- Without the vote, the recall memory does not learn the route's chain even with the cue visible (0.35-0.48), so its limit there is acquisition, not memory.
- Each part does half the task. The vote learns the chain but cannot carry the cue across 8 or 16 events. The recall memory's position term can carry the cue (grids 8 and 10), but without the vote the brain does not learn the chain.
- Combined, they do not join the two: what the read recalls does not reach the vote's records.

### Grid 13: the headline effects on fresh founders

Founders:
- 1041 to 1060 on the ordered recall world and the route;
- 202061 to 202080 on the views, with and without the last action shown.

Tables: [results_089/g13/M089_RESULTS.md](results_089/g13/M089_RESULTS.md), [contrasts](results_089/g13/M089_CONTRASTS.md) and [efference pairs](results_089/g13/efference-pairs.json).

Each effect is founder-paired, 95% over 20 fresh founders:

| Effect | Reading | Readings without → with | Difference | Founders up / down | Earlier grid |
| --- | --- | --- | --- | --- | --- |
| Position term | ordered recall world, taught | 0.58 → 0.94 | **+0.36 [+0.29, +0.42]** | 19 / 1 | grid 5: +0.30 |
| Position term, two heads | ordered recall world, taught | 0.69 → 1.00 | **+0.31 [+0.25, +0.37]** | 20 / 0 | grid 5: +0.25 |
| Position term | ordered recall world, reward through `step` or `live` | 0.50 → 0.50 | 0 exactly | | |
| Recency 0 against 0.25 | route, 16 neutral events, guided | 0.36 → 0.65 | **+0.29 [+0.16, +0.40]** | 16 / 4 | grids 8 and 10: +0.16 and +0.18 |
| The last action shown, episodic vote | consecutive, reward through `live` | 0.08 → 0.74 | **+0.67 [+0.49, +0.82]** | 19 / 1 | grid 11: +0.60 |
| The same, vote and recall | consecutive, reward through `live` | 0.13 → 0.82 | +0.69 [+0.53, +0.83] | | |
| The same, vote and recall | invisible, reward through `live` | 0.29 → 0.81 | +0.52 [+0.32, +0.70] | 18 / 2 | |
| The same, vote alone | invisible, reward through `live` | | +0.29 [+0.09, +0.50] | | |
| The same, vote | consecutive, corrected, 120 | | +0.39 [+0.26, +0.53] | | |
| The same, recall alone | either view | | −0.13 to +0.17 | | |

The last action does not help the recall memory alone.

## Summary of the 0.89 readings

| World | Base | Best recipe, guided or corrected | Best recipe, reward alone | Uniform random |
| --- | --- | --- | --- | --- |
| Recall world, the latest value | 0.48-0.49 | recall with 2 heads: 0.99-1.00 | recall, 2 heads: 0.80-0.84 through `live` | 0.49 |
| Ordered recall world, first or latest | 0.50 | recall or 2 heads with the position term: 0.94-1.00 | none: 0.50 | 0.50 |
| Hidden view (A B A B) | 0.19-0.27 | vote and recall: 0.98-0.99 at 1920 | vote and recall: 0.88-0.92 through `live` (greedy 1.00) | 0.121 |
| Invisible view (A A B C) | 0.31-0.49 | vote and recall: 0.96-1.00 at 480 | vote with the last action shown: 0.84 | 0.121 |
| Consecutive view (A A B B) | 0.22-0.37 | vote with the last action shown: 0.98 | vote and recall with the last action: 0.82 | 0.121 |
| Route cue, 2 events | 0.17-0.21 | vote and recall, 2 heads, 1920: 0.77 | vote and recall: 0.33 | 0.09 (`random` control) |
| Route cue, 16 events | not run | recall, 2 heads, recency 0: 0.66; recall, recency 0: 0.65 | vote and recall: 0.25-0.29 | 0.09 |
| Route cue visible (control) | 0.16-0.24 | the vote: 0.95-0.99 | the vote: 0.92-0.93 | 0.09 |
| P1 (control) | 0.39 | the vote: 0.93 (0.95 after 80 alone) | the vote: 0.97 (graded) | 0.121 |

### Grid 14: guided route brains that then live 1920 episodes alone through `live` (fresh founders 1041 to 1060)

Tables: [results_089/g14/M089_RESULTS.md](results_089/g14/M089_RESULTS.md) and [contrasts](results_089/g14/M089_CONTRASTS.md).

Sampled (greedy) after the guided life, then after 1920 episodes alone:

| Neutral events | Episodic vote | Vote and recall | Vote and recall, recency 0 | Vote, 2 recall heads | Recall, recency 0 | Recall, 2 heads, recency 0 |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.55 (0.50) → 0.59 | 0.72 (0.68) → **0.76** | **0.78** (0.75) → 0.70 | 0.68 (0.65) → 0.72 | 0.57 (0.42) → 0.50 | 0.63 (0.53) → 0.62 |
| 16 | 0.45 (0.38) → 0.33 | 0.43 (0.42) → 0.32 | 0.49 (0.53) → 0.43 | 0.49 (0.38) → 0.47 | **0.65** (0.57) → **0.64** | 0.59 (0.53) → 0.55 |

A life from reward alone through `live`, after its own 1920 episodes and then 1920 more:

| Recipe | 2 neutral events | 16 neutral events |
| --- | --- | --- |
| Episodic vote | 0.28 → 0.29 | 0.25 → 0.23 |
| Vote and recall | 0.22 → 0.39 | 0.25 → 0.27 |
| Vote and recall, recency 0 | 0.13 → 0.46 | 0.23 → 0.33 |
| Recall alone | 0.00 | 0.00 |

Contrasts, sampled, 95% over 20 fresh founders:

| Contrast | Neutral events | Difference | Founders up / down | Earlier grids |
| --- | --- | --- | --- | --- |
| Vote and recall against the vote, guided | 2 | **+0.18 [+0.04, +0.31]** | 14 / 6 | +0.13 and +0.14 in grids 1 and 2 |
| Recall at recency 0 against the vote, guided | 16 | **+0.20 [+0.04, +0.35]** | 14 / 6 | |

**Reading.**
- Taught route memories survive a long life alone: recall at recency 0 keeps 0.64 of 0.65 at 16 events, and the vote with recall 0.76 of 0.72 at 2. The vote recipes at 16 events lose 0.02-0.12 alone.
- A brain learning from reward alone keeps improving slowly with the recall memory beside the vote, 0.13-0.22 → 0.39-0.46 over the second 1920 episodes at 2 events, and the vote alone does not.

### Grid 15: the ordered recall world with the writes 4, 16 or 48 neutral events apart (founders 1001 to 1010, taught)

Conditions `ask-first-gapK` and `ask-latest-gapK` put K neutral events between the two writes (the world's `"gaps"` entry; the test is in `tests/test_recall_order.py`). Tables: [results_089/g15/M089_RESULTS.md](results_089/g15/M089_RESULTS.md), [contrasts](results_089/g15/M089_CONTRASTS.md) and [per condition](results_089/g15/M089_CONDITIONS.md).

Sampled (greedy):

| Writes apart | Recall | Recall, no position | Recall, recency 0 | Recall, no position, recency 0 |
| --- | --- | --- | --- | --- |
| 4 | **0.97** (0.95) | 0.65 (0.70) | 0.94 (0.95) | 0.64 (0.65) |
| 16 | 0.90 (0.90) | 0.78 (0.80) | **0.94** (0.95) | 0.57 (0.60) |
| 48 | 0.86 (0.90) | 0.79 (0.78) | **0.92** (0.93) | 0.55 (0.57) |

The position term at recency 0, founder-paired, 95% over 10 founders:

| Writes apart | Difference | Founders up / down |
| --- | --- | --- |
| 4 | +0.30 [+0.16, +0.43] | 9 / 0 |
| 16 | +0.37 [+0.26, +0.46] | 10 / 0 |
| 48 | +0.37 [+0.26, +0.47] | 9 / 0 |

At the founder recency the term adds +0.31, +0.12 and +0.07.

**Reading.**
- The position term lets a taught read pick the first or the latest of two writes 48 moments apart: 0.92, past the 32 exact ages, in the doubling buckets.
- Without the term and without recency the read is at chance.
- Without the term but with the recency charge the read mixes the two writes unequally, the newer one more. Lessons can learn to read that imbalance as order: 0.78-0.79 at 16 and 48 events.

### Grid 16: grid 15's gaps on ten more founders (1011 to 1020), and the writes 96 events apart with 128 slots (1001 to 1020)

Tables: [results_089/g16/M089_RESULTS.md](results_089/g16/M089_RESULTS.md), [contrasts](results_089/g16/M089_CONTRASTS.md) and [per condition](results_089/g16/M089_CONDITIONS.md).

Taught, sampled (greedy):

| Writes apart | Recall | Recall, no position | Recall, recency 0 | Recall, no position, recency 0 |
| --- | --- | --- | --- | --- |
| 4 | 0.97 (0.97) | 0.72 (0.72) | 0.97 (0.97) | 0.73 (0.75) |
| 16 | 0.94 (0.95) | 0.67 (0.68) | 0.95 (0.95) | 0.60 (0.68) |
| 48 | 0.86 (0.82) | 0.84 (0.85) | 0.89 (0.95) | 0.51 (0.53) |
| 96, 128 slots | 0.86 (0.86) | | **0.89** (0.89) | 0.52 (0.51) |

The position term at recency 0, founder-paired, 95%:

| Writes apart | Difference | Founders up / down |
| --- | --- | --- |
| 4 | +0.24 [+0.11, +0.36] | |
| 16 | +0.35 [+0.25, +0.43] | 10 / 0 |
| 48 | +0.37 [+0.27, +0.46] | 9 / 1 |
| 96, 128 slots | **+0.38 [+0.30, +0.45]** | 18 / 1, over 20 founders |

**Reading.**
- Over 20 founders, a taught recall memory with the position term answers which of two writes was first or latest at 0.89-0.97, whether they lie 4, 16, 48 or 96 moments apart.
- Without the term, and without the recency charge, it reads at chance: 0.51-0.73.
- The reach is bounded by the slots the memory keeps (64 by default): with 128 slots, 96 moments are within reach.

### Grid 17: the position term on the hidden view, 160 fresh founders (202081 to 202240)

Tables: [results_089/g17/M089_RESULTS.md](results_089/g17/M089_RESULTS.md) and [contrasts](results_089/g17/M089_CONTRASTS.md).

Sampled (greedy):

| Arm | Recall | Recall, no position | Episodic + recall | Episodic + recall, no position |
| --- | --- | --- | --- | --- |
| Corrected, 120 | 0.34 (0.25) | 0.36 (0.24) | 0.75 (0.47) | 0.74 (0.47) |
| Corrected, 480 | 0.57 (0.44) | 0.56 (0.42) | 0.92 (0.85) | 0.92 (0.83) |

The position term, founder-paired, 95% over 160 founders:

| Recipe | Corrected, 120 | Corrected, 480 |
| --- | --- | --- |
| Recall | −0.024 [−0.079, +0.028] | +0.005 [−0.070, +0.079] |
| Episodic + recall | +0.012 [−0.049, +0.071] | −0.003 [−0.046, +0.038] |

**Reading.** On the hidden chain the position term has no effect. The earlier positive readings on 20 to 60 founders (+0.04 to +0.13) were within their noise. The history that tells stage 3 from stage 1 (A after B) is read by content: the successor read and the cortex of the moment before. It is not read by how long ago it happened.

## What the 0.89 readings show

1. **The position term does what it was built for: order and distance, where a lesson teaches it.**
   - It lets a taught recall memory answer which of two writes came first or last, at 0.89-0.97 against 0.51-0.73 without it, from 4 to 96 moments apart. That is 20 founders per reading, with up to 20 of 20 founders up.
   - It carries a vanished cue across 16 neutral events: 0.57-0.65 against 0.34-0.36, at recency 0.
   - It does nothing where content already tells the moments apart: the aliased chains (160 founders), the route at 2 events and the plain recall world.
2. **Reward alone teaches neither the position term nor the address map.** No recipe answers the ordered recall world from reward, through `step` or `live`, in 1536 episodes. Under reward the recall memory adds nothing on the chains and costs the untrained founders about 0.05. On the plain recall world it helps, 0.69-0.84, through its fixed address and the projections.
3. **The episodic vote carries most behaviour on every chamber, under every signal.** It learns from reward through `live`, keeps what was taught through a long life alone, and makes the route's visible control pass.
   - The recall memory adds to it under lessons on the hidden view: +0.11 [+0.02, +0.20] at 480 corrected episodes, over 40 founders.
   - On the route at 2 events it adds +0.13 to +0.18, over three founder sets.
   - It does not join the vote across long delays. At 8 to 16 events the vote alone cannot carry the cue, the recall memory alone cannot learn the chain, and the two together reach about 0.5 against 0.99 with the cue visible.
4. **The brain's own last action is missing from what the memories see.** Showing it lifts the vote under reward alone by 0.52-0.69 on the views where only the brain's own action tells the stages apart, in two founder sets. It costs 0.23 on the view where history does that.
5. **The fixed recency charge conflicts with the position term.** It helps the hidden chain (recall alone at 480 corrected episodes: 0.61 against 0.42 without it). It defeats the term at long delays (16 events: 0.36 against 0.65 without it, in three founder sets).
6. **Limits found on the way.**
   - A learned code of 8 units cannot hold the recall world's observations: every recipe keyed on it is at chance. 16 units suffice.
   - A wider brain (96, 48) does not help.
   - In 2 of 160 long lives a free phase did not settle within its budget, and `act` raised.
