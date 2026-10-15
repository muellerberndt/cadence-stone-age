# Sequence instrument v1

An auditable harness for the COLD chain of `benchmarks/cadence_081/v5_mochi_style.py`, for
a vanished route cue, for the chain under a weather that has nothing to do with it, and for the
chain seen three ways: progress hidden, an invisible step, progress visible. The
V4.2 to V5 scripts stay byte-for-byte as they were; this directory measures the same questions
with explicit custody, separate random streams and complete receipts.

| File | Responsibility |
| --- | --- |
| `worlds.py` | The COLD chain (V5's rules and seven inputs), the route cue, the weather chain (the COLD chain with three irrelevant weather bits, taught under four combinations and tested under the other four), and the view chain (the COLD chain's rules with the observation of each stage taken from a declared view: `hidden` A, B, A, B; `invisible` A, A, B, C; `visible` V5's own). Correctness lives here, independent of any brain. Invalid outputs raise `InvalidAction`; nothing is clamped. |
| `adapters.py` | `StepAdapter` (historical control, `Brain.step`) and `LiveAdapter` (continuing life, `Brain.live` with `decision_id`). A ledger gives every issued action one outcome, exactly once. Refusals follow the library's contracts: an answer refused after an accepted outcome is retried without the outcome; a refused outcome is offered again a bounded number of times. |
| `runner.py` | Lives, the caregiver schedule (including a random-label null teacher), frozen evaluation on reseeded checkpoint copies, per-state readings, the never-repeat searcher control, the withdrawal branch read at checkpoints, twin arms that continue from one taught brain, an arm's own lesson length, founder-paired contrasts and declared pairs, per-founder files. |
| `probes.py` | Interventions on copies only: sham, trace cleared, warm activity cleared, recall off, efference cleared, full reset; trace transplants; policy reads that issue no action and draw no random number. |
| `metrics.py` | Exact chain probabilities (dynamic programme, the closed binomial form, the never-repeat searcher), episode summaries, founder bootstrap, the sampled-sequence ceiling. |
| `receipts.py` | Manifest: every imported Cadence file by digest, wheel digest, both repositories' Git state, platform, threads, protocol digest, wall time and peak memory. |
| `protocol.json` | P1 development: fresh founders 1001 to 1005, six arms, two recipes. |
| `protocol-p1-drift.json` | The taught chain read state by state over 80 episodes alone, through `live` and, from the same taught brain, through `step`; with and without the episodic memory. |
| `protocol-p3-generalization.json` | The weather chain: taught under the even-parity weathers, read under the odd-parity ones, with and without the episodic memory. |
| `protocol-p3-content.json` | The weather chain: a correcting caregiver against a random-label twin and an untaught twin, at lessons of 40, 120 and 240 episodes, then 20 episodes alone through `live`. |
| `protocol-p1-drift-reset.json`, `protocol-p3-content-reset.json` | The same designs in V5's order (`withdrawal_reset`), as the notebook ran them; the drift protocol names EXP-47's seeds 42 to 53 for the replica check. |
| `tests/test_contracts.py` | Scorer, world rules, custody with a spy brain, probe isolation, seeded evaluation and exact save/load continuation on real brains; the searcher's exact value against enumeration, the weather chain's rules and splits, the random-label teacher's moments, the per-state reading against a direct reset-and-act read, an unchanged life when read at checkpoints, twin arms, and the three views of the chain against the notebook's own arrays. |

```sh
python -m pytest -q benchmarks/sequence_v1/tests
python benchmarks/sequence_v1/runner.py --protocol benchmarks/sequence_v1/protocol.json \
  --out benchmark_output_sequence_v1/p1-dev --wheel-sha256 <sha256 of the cadence-net wheel>
```

## Semantics that differ from V5

- **Life seams.** V5 delivers a life's last outcome with the next episode's first observation,
  discards the action that call issues and resets the brain. Here the last outcome is held in
  `*.seam.json` beside the checkpoint and delivered exactly once when the life resumes.
- **Withdrawal.** V5 resets transient state before the caregiver-free life. Here that life
  resumes from the seam with the trace, activity and pending action intact. A protocol that
  declares `withdrawal_reset: true` keeps V5's order instead: the lesson's last outcome arrives
  through the teaching interface with a fresh episode's observation, the action that call
  issues is discarded, and `Brain.reset` precedes the life alone.
- **Evaluation streams.** V5 samples evaluation actions with the checkpoint's own generator.
  Here each frozen copy gets a declared stream per founder and mode, shared by every arm of
  that founder.
- **Teaching receipts.** Every label's acceptance, exhausted free phase and sweeps are counted
  from the library's teaching report; V5 printed one deduplicated warning.

The world, the caregiver's rules, the schedule (4 guided and 8 autonomous decisions), the
budgets and the rewards are V5's.

## Tests adapted from cadence-teachers

Six tests come from Will Glynn's open lab notebook
[cadence-teachers](https://github.com/WGlynn/cadence-teachers), which rebuilt V5's chamber,
reproduced its published numbers seed for seed, and then read it with instruments a searching
brain cannot pass. They are reimplemented here on this instrument's worlds, adapters, seams and
receipts; the code credits each one where it lives.

| Test | Source | Here |
| --- | --- | --- |
| The never-repeat searcher: a policy with no chain knowledge that never repeats a failed action in the same situation succeeds with probability 190/625 = .304 on V5's chain, the chance level for a free-retry chamber | [EXP-45](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-45.md) | `metrics.never_repeat_chain_success_exact`; the `searcher` control on every chain world; contrasts against it |
| Per-state greedy accuracy: every stage read alone from a reset copy, and the founders with every stage right; optionally the sampled probability per stage and the memoryless success it predicts | [EXP-45](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-45.md), [EXP-46](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-46.md) | `runner.per_state`, on every chain-world reading; `evaluation.per_state_samples` |
| The weather split: three irrelevant bits, even-parity weathers taught, odd-parity weathers tested, so every single bit value is taught and only the combinations are new | [EXP-48](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-48.md) | `worlds.WeatherChain`, `protocol-p3-generalization.json` |
| The random-label null teacher: it speaks at the correcting caregiver's moments with a uniformly random action, so the pair measures what a label's content adds to being corrected | [EXP-52](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-52.md), [EXP-53](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-53.md) | caregiver `random_label`, `protocol-p3-content.json` |
| The life alone read over time from one taught brain, through `live` and through `step` | [EXP-47](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-47.md) | `withdrawal_checkpoints`, arms with `twin_of`, `protocol-p1-drift.json` |
| The chain seen three ways: progress hidden, the ambiguous chain Huncho reported on the Stone Age world (A, B, A, B, the two A and the two B observations byte-identical); an invisible step, where the first right action changes nothing seen (A, A, B, C); progress visible, V5's own observations | [EXP-56](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-56.md), [EXP-57](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-57.md), [EXP-59](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-59.md), [EXP-60](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-60.md) | `worlds.ViewChain`, `worlds.CHAIN_VIEWS`; the tests compare every view with the notebook's own arrays |

On a view where two stages look alike, a stage cannot be read alone from a reset copy (a reset
brain at A cannot know which A it is at), so the per-state reading runs only where every stage
shows its own observation, and the never-repeat searcher's rate there is measured, not exact.

Where this instrument departs from the notebook's scripts, its own semantics apply (below): the
life ends at seams, the withdrawal resumes from the seam, and the lesson lengths of the content
protocol are paired within a founder. A test in `tests/test_contracts.py` checks that stopping
the life alone for a checkpoint leaves every action, outcome and learning record as the
uninterrupted life has them.

```sh
python runner.py --protocol protocol-p1-drift.json --out ../../p1-drift
python runner.py --protocol protocol-p3-generalization.json --out ../../p3-generalization
python runner.py --protocol protocol-p3-content.json --out ../../p3-content
python report.py ../../p1-drift ../../p3-generalization ../../p3-content
```

## Reading the results

The COLD chain is fully observed: a memoryless stage-aware policy completes it in four
decisions, so success here measures prerequisite learning, never memory. Uniform random
succeeds with probability exactly 1180409/9765625 (0.1208738816) and the never-repeat
searcher with probability 190/625 (0.304); whole-chain success between the two can come from
searching inside an attempt, so the per-state reading stands beside it. Sampled success has a
ceiling set by the softmax temperature; greedy success is reported beside it and never
replaced by it. A decision whose motor margin is below the solve tolerance is counted as
undecided. With the episodic memory (`memory_choice=True`) the memory's vote joins the motor
readout inside the library: the recorded margins, probabilities and undecided counts are the
readout's own, without the vote, while the actions and every success reading include it. Every
checkpoint is read at its seam, before its last outcome is delivered; the notebook's scripts and
V5 read after delivering it. One outcome can change a memory brain's per-state answers, so a
comparison with them reads both points (`RESULTS.md`). The founder is the unit of every
interval.
