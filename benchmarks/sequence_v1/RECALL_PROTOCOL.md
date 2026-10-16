# The recall memory on the Stone Age chambers: a declared witness

Declared 2026-10-16, before any run of this reading. Nothing below changes after the first run
starts. This reading is a witness of the memory in a world, not a gate of the library branch:
it says what the memory does on these chambers on two founders, and nothing about whether the
branch merges.

## Question

`Brain.compose(..., recall=True)` adds the recall memory: each stream's recent moments as slots,
addressed by the present observation before each settle, written after each act, and read into
the association region through two source regions (`recall` and `next`). On the context-key
screen's chambers, the chain seen four ways, do the `place` and `ctx5` arms keep their sampled
success and clean greedy passes with the memory on, and on which views does the memory raise them?

## Code under test

| Part | Where | Commit |
| --- | --- | --- |
| Library | Cadence worktree `lanes/r3lib`, branch `r3-library` | `a7c6c14` |
| Instrument | Stone Age fork worktree `lanes/check-sa-recall`, branch `recall-reading` from `r2-cortex-chambers` | `5c43eda` plus this declaration |
| Protocols | `protocol-recall-screen.json` (master, four views), `protocol-recall-screen-{hidden,invisible,visible,consecutive}.json` (derived by `recall_screen.py derive`), `protocol-recall-p1.json` | this branch |

The runner passes a recipe's `compose` entries to `Brain.compose` unchanged (unknown names
reach the library), so no instrument code changes for the option; the Stone Age observation is
7 inputs wide, and the memory keys and stores it as it is (`recall_code` 0).

## Recipes

| Recipe | `Brain.compose(7, 5, seed, ...)` |
| --- | --- |
| `founder` | `modules=(48, 24), arousal=True, memory_choice=True`: the screen's sensory recipe, the recall memory off; byte-identical to the brain before the option (verified on these chambers earlier today, and `recall=False` equals the option absent) |
| `recall` | the same plus `recall=True, recall_scale=1.2` and the founder genes written out: amplitude 3.0, temperature 0.25, heard 1.0, recency 0.25, address 0.01, address_temperature 0.1, address_prior 1.0, context 0.0, context_decay 0.5, capacity 64, value `"event"`, next `True`, code 0 |

Construction check before the declaration (no lives, no readings): the recall recipe builds
under the library; its checkpoint digest equals the one built with the defaults alone; the
`place` arms' `memory_context=0.0` override and the `learning_qualified=True` override keep
the founder's efficacy and bias under the recall recipe (the runner's own arm check); the
recall recipe has 3,812 synapses against the founder's 3,476 and 13,141 parameters against
12,567 (the two regions' projections and the 7 by 7 address map).

## Witnesses, founders, arms, readings

The context-key screen's four views of V5's chain (`hidden` A, B, A, B; `invisible` A, A, B, C;
`visible` V5's own; `consecutive` A, A, B, B), its arms `place_natural_120`,
`place_corrective_120`, `ctx5_natural_120`, `ctx5_corrective_120` (120 episodes, the corrective
teacher's schedule 4 guided and 8 autonomous decisions), its controls, streams and evaluation
(100 sampled episodes and one greedy episode from a frozen copy at the arm's seam, `Brain.reset`
before each episode, which empties the slots and keeps the address map). Screen founders 202001
and 202025, the control subset of the earlier lanes, both recipes on each: 8 founder-arm pairs
per view, 4 per arm kind.

| Reading | Definition |
| --- | --- |
| Sampled success | the share of the 100 sampled episodes completed within 10 decisions |
| Clean pass | the one greedy episode completed in four decisions (`exact_minimal_completions == episodes`) |
| First-try accuracy | per stage, the share of sampled episodes reaching it whose first decision there was right (reported beside the two readings above) |

P1 (`protocol-recall-p1.json`, the cold chain, six arms, 120 episodes taught and 80 alone, 200
sampled episodes) runs on founder 1001 after the screen if time allows; founders 1002 to 1005
only if time allows after that.

## Criteria

| Name | Rule |
| --- | --- |
| Preservation | per view, recall minus founder in sampled success, paired by founder and arm, the mean over the 8 pairs at or above -.05; the memory preserves the screen when every view meets it. The same difference per arm kind (4 pairs) and the clean passes as counts with their discordant pairs are reported beside it |
| Benefit | the views where that paired mean is above zero, with the sign count over the pairs. Hidden and invisible are the views where the stream's history has to tell a stage; visible is the view where the observation alone does; consecutive the view where only the brain's own actions do |
| Control check | the founder recipe's readings, trained-state digests and event digests on 202001 and 202025 (and on 1001 for P1) must equal the dense founder's earlier control runs (`lanes/r2g-runs/sk-control-<view>`, `sk-control-p1`, sensory recipe, library `c231f5c`) arm for arm; a difference is reported, not repaired |

On two founders no interval is claimed; paired means are given with their SEM over the pairs.
P1 on one founder gives point differences per arm; the founder-paired bootstrap of the earlier
lane applies only with the extension founders.

## Expected outcome, stated before the run

The memory is written at every accepted observation (after each act) and read by the present
observation (the address is the event heard, the map starting at zero), and the stream's slots
are emptied at an episode's end. So within an episode the slots hold that episode's moments only.
At an episode's first moment the regions read silence. At a later moment showing an observation
seen before, the address finds the earlier like moments: the `recall` region shows that
observation again (a like moment exists), and the `next` region shows what followed it. On the
hidden view the second A (stage 3) finds the first A whose next is B when the first action was
right, while the first A finds nothing: the memory offers, at the founder address, a signal
that tells the second occurrence from the first, and the arm's plastic synapses from the two
regions have to learn to read it. Wrong actions blur the signal: a wrong action at stage 1
leaves A and writes an A moment whose next is A. The address lesson runs only where lessons
run, under the corrective teacher; under reward alone the map stays at zero and only the
projections learn. On the hidden view the address lesson therefore has to learn to look back
through what the corrective lessons name; the natural arms get no address lesson at all.

Expected: no change or a small change on the visible view, where the observation names the
stage; a possible gain in the corrective arms on the hidden and invisible views; a loss is
possible on any view, since the two regions add drive (amplitude 3.0 through projections at
scale 1.2) that the founder's settle did not have. An unchanged result on every view is possible
and would say that 120 episodes on these founders do not teach the projections to read the
regions, not that the memory holds nothing.

## Runs

`run_recall.sh`, two queues, at most two runner processes, single BLAS thread, the shared venv
with `PYTHONPATH` at the library worktree's `src`:

| Queue | Order |
| --- | --- |
| 1 | hidden, invisible (`--seeds 202001 202025 --recipes founder recall`), then P1 founder 1001, then the P1 extension founders if time allows |
| 2 | visible, consecutive (the same seeds and recipes) |

Wall times from each run's `manifest.json`; `uptime` before and after. Analysis:
`recall_screen.py analyze <runs> <control runs>` writes `RECALL_RESULTS.md` and
`recall-summary.json` beside the runs.
