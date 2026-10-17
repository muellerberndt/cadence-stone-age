# The recall memory's four options on the screen and P1

Declared 17 October 2026, before the first declared run, as the Stone Age part of a declaration
kept with the library's evidence (SHA-256
`7f81e80567f6bfd75bc8944c2b8a72ed2e294de7e58bc86ed0d9563ab893c2c1`). It extends the recall
witness ([RECALL_PROTOCOL.md](RECALL_PROTOCOL.md)): the same chambers, signals, schedules and
evaluation, five recipes in place of two, the screen's 48 founders in place of two and P1 on 24
founders in place of five.

## Recipes

`Brain.compose(7, 5, seed, modules=(48, 24), arousal=True, memory_choice=True, ...)`:

| Recipe | Memory |
| --- | --- |
| `founder` | recall off |
| `recall` | the recall memory at the pull request's founder genes, written out, the four options at their founder values (`recall_address_step="lms"`, `recall_write="always"`, `recall_null=None`, `recall_address_reward=0.0`) |
| `aroused` | `recall` with `recall_write="aroused"`: a moment is written only when its act was sampled (`live` samples its aroused acts; `step` follows the act's own flag) |
| `rewarded` | `recall` with `recall_address_reward=1.0` alone (by addendum 1 of the declaration, before any run) |
| `improved` | `recall` with `recall_address_step="toward"`, `recall_recency=None` (the power-law charge), `recall_null=0.5` (half the logit of a full match at heard 1), `recall_write="aroused"`, `recall_address_reward=1.0` |

## Readings and criteria

| Reading | Files | Founders |
| --- | --- | --- |
| the screen, four views | `protocol-options-screen-<view>.json` (derived from `protocol-options-screen.json` by `recall_screen.py`'s `derive`) | 202001 to 202048 |
| P1 | `protocol-options-p1.json` | 1001 to 1024 |

| Criterion | Definition |
| --- | --- |
| S1 | preservation: on every view, the mean over founders and arms of `improved - founder` in sampled success at or above -.05 |
| S2 | the P1 gate: every arm's upper end of the founder-resampled 95% interval of `improved - founder` in sampled success after teaching at or above zero |
| S3 | `improved - recall`, `aroused - recall` and `rewarded - recall` on every view, arm kind and P1 arm, with intervals |

`options_reading.py RUNS` writes every table; the intervals resample founders (10,000
resamples, seed 31012), each founder's four arms averaged on the screen.

Declared expectations: S1 met on the visible and consecutive views, a loss possible on the hidden
and invisible views; S2 met on the step arms, the live arms open; an unchanged result possible
everywhere. Under `write="aroused"` a greedy evaluation episode writes nothing, so the clean
greedy pass reads the slots empty from its reset.

## Runs

`aws_options.sh ROOT OUT WORKERS`: one runner process per view (or P1) and founder, every recipe
in each, at most `WORKERS` at a time, one BLAS thread each, the library tree on the Python path.
