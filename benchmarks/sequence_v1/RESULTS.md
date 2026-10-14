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
