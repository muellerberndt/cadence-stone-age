# Sequence instrument v1

An auditable harness for the COLD chain of `benchmarks/cadence_081/v5_mochi_style.py` and for
a vanished route cue. The V4.2 to V5 scripts stay byte-for-byte as they were; this directory
measures the same questions with explicit custody, separate random streams and complete
receipts.

| File | Responsibility |
| --- | --- |
| `worlds.py` | The COLD chain (V5's rules and seven inputs) and the route cue. Correctness lives here, independent of any brain. Invalid outputs raise `InvalidAction`; nothing is clamped. |
| `adapters.py` | `StepAdapter` (historical control, `Brain.step`) and `LiveAdapter` (continuing life, `Brain.live` with `decision_id`). A ledger gives every issued action one outcome, exactly once. Refusals follow the library's contracts: an answer refused after an accepted outcome is retried without the outcome; a refused outcome is offered again a bounded number of times. |
| `runner.py` | Lives, the caregiver schedule, frozen evaluation on reseeded checkpoint copies, the withdrawal branch, founder-paired contrasts, per-founder files. |
| `probes.py` | Interventions on copies only: sham, trace cleared, warm activity cleared, recall off, efference cleared, full reset; trace transplants; policy reads that issue no action and draw no random number. |
| `metrics.py` | Exact chain probabilities (dynamic programme and the closed binomial form), episode summaries, founder bootstrap, the sampled-sequence ceiling. |
| `receipts.py` | Manifest: every imported Cadence file by digest, wheel digest, both repositories' Git state, platform, threads, protocol digest, wall time and peak memory. |
| `protocol.json` | P1 development: fresh founders 1001 to 1005, six arms, two recipes. |
| `tests/test_contracts.py` | Scorer, world rules, custody with a spy brain, probe isolation, seeded evaluation and exact save/load continuation on real brains. |

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
  resumes from the seam with the trace, activity and pending action intact.
- **Evaluation streams.** V5 samples evaluation actions with the checkpoint's own generator.
  Here each frozen copy gets a declared stream per founder and mode, shared by every arm of
  that founder.
- **Teaching receipts.** Every label's acceptance, exhausted free phase and sweeps are counted
  from the library's teaching report; V5 printed one deduplicated warning.

The world, the caregiver's rules, the schedule (4 guided and 8 autonomous decisions), the
budgets and the rewards are V5's.

## Reading the results

The COLD chain is fully observed: a memoryless stage-aware policy completes it in four
decisions, so success here measures prerequisite learning, never memory. Uniform random
succeeds with probability exactly 1180409/9765625 (0.1208738816). Sampled success has a
ceiling set by the softmax temperature; greedy success is reported beside it and never
replaced by it. A decision whose motor margin is below the solve tolerance is counted as
undecided. The founder is the unit of every interval.
