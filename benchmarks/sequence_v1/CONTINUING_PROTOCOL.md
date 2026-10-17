# The recall memory kept across episodes and keyed by its predecessor

Declared 17 October 2026, before the first declared run; it extends the options reading
([OPTIONS_PROTOCOL.md](OPTIONS_PROTOCOL.md)) with two options of the recall memory. Chambers,
signals, schedules and evaluation are the screen's and P1's, except where a recipe keeps its
memory.

## Question

Today every episode's end empties the recall memory, in the library (a `done` row starts a
fresh stream) and in this instrument (`Brain.reset` before every read episode), so a stage the
brain met in an earlier episode is never recalled. On the aliased views the observation alone
also cannot tell stage 1 from stage 3. Does a memory whose slots outlive an episode
(`recall_episodes="keep"`), keyed by the event heard together with the previous moment's event
and the last command (`recall_key="predecessor"`), raise sampled success on these chambers?

## Recipes

`Brain.compose(7, 5, seed, modules=(48, 24), arousal=True, memory_choice=True, ...)`:

| Recipe | Memory | Read episodes start with |
| --- | --- | --- |
| `founder` | recall off | `Brain.reset()` |
| `recall` | the recall memory at the pull request's founder genes | `Brain.reset()` |
| `base` | `recall` with `recall_recency=None` (the power-law charge) and `recall_capacity=256` | `Brain.reset()` |
| `keep` | `base` with `recall_episodes="keep"` | `Brain.reset(keep_memory=True)` |
| `pred` | `base` with `recall_key="predecessor"` | `Brain.reset()` |
| `keep_pred` | `base` with both | `Brain.reset(keep_memory=True)` |

Under `keep` the slots of the life's episodes travel into the frozen copy that is read, every read
episode keeps them and adds its own, and the per-state reading loads the copy afresh for every
situation with its memory kept (no situation's act is read by the next).

## Readings and criteria

Founders: the screen's 202001 to 202024 on the four views; P1's 1001 to 1012. One runner process
per view (or P1) and founder, every recipe in each (`run_continuing.sh`). `continuing_reading.py`
reads them, with founder-resampled 95% intervals (10,000 resamples, seed 31012), each founder's four
arms averaged on the screen.

| Criterion | Definition |
| --- | --- |
| C1 | `keep_pred - base` per view and P1 arm |
| C2 | `keep - base` and `pred - base`: the two options alone |
| C3 | preservation: `keep_pred - founder` at or above -.05 on every view; the P1 gate: every arm's upper interval end of `keep_pred - founder` in sampled success after teaching at or above zero |
| reference | `base - recall` and `recall - founder` |

Declared expectations: `keep` alone changes little on the aliased views (stage 1 and stage 3 store
the same event and successor); `pred` separates them within an episode where the previous moment
differs; `keep_pred` gains most on the hidden and invisible views. An unchanged result is possible.

## Library

Cadence on a local branch at 710f792 (the pull request's head e17711d plus the two options), frozen
for the runs.
