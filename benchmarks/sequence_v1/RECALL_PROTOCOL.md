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

## Custody note, written after the runs

The library worktree's branch `r3-library` moved from `a7c6c14` to `ca9b124` at 18:02:27, before
the first run (18:06:18), by a commit of another session that changed two notes under
`benchmarks/binding/` and no file under `src/`. Every run's manifest records the library at
`ca9b124`, clean, with the same 56 package file digests (package digest `c022362d`), which equal
`a7c6c14`'s blobs file for file; and the instrument at `85956c4`, clean, the declaration commit.
The commits after it on this branch amend the analysis script only.

## Follow-up reading: context in the key

Declared 2026-10-16, after the first reading's results and before any run of this one. Nothing
below changes after the first run starts. The same kind of witness, not a gate.

### Question

A moment's key and address are the event heard; with `recall_context` above zero they also
carry the fading history of the events before it (`history = context_decay * history + event`
after each witnessed moment; `key = heard * x + context * history`; the address adds the learned
map's terms). Does that context keep the sampled success and clean passes of the `place` and
`ctx5` arms against the founder, and does it raise them over the plain recall recipe on the
views where the stream's history has to tell a stage?

### Recipes, witnesses, readings

| Recipe | Compose |
| --- | --- |
| `founder`, `recall` | the first reading's, retained from its runs (`rs-<view>`, `rs-p1`), not rerun |
| `recall_ctx05` | the recall recipe plus `recall_context=0.5, recall_context_decay=0.5` |
| `recall_ctx10` | the same with `recall_context=1.0` |

Construction check before the declaration: both context recipes build; their efficacy and bias
equal the recall recipe's (context is a saved setting that changes no weight); the `place` arms'
`memory_context=0.0` override keeps them; after two moments of events e0 then e1 the second slot's
key is `e1 + e0` under context 1.0 and `e1` under context 0.0; `Brain.reset` empties the slots,
the cortex of the moment before and the history.

Protocols: `protocol-recall-context.json` (master, views hidden, invisible, visible; derived files
`protocol-recall-context-<view>.json`) and `protocol-recall-context-p1.json`. Founders 202001 and
202025, the first reading's arms, controls, schedule, streams and evaluation; the context recipes
run with `--recipes recall_ctx05 recall_ctx10` into `rc-<view>`; 8 pairs per view and recipe.

| Reading | Rule |
| --- | --- |
| Per view and recipe | sampled success and clean passes per arm and founder; the paired mean against the founder with its SEM, up/down/equal, clean counts with discordant pairs |
| Preservation | per view and context recipe, the paired mean against the founder at or above -.05 |
| Benefit | per view, the context recipes above the founder, and whether each is above the plain recall recipe's paired mean on that view |
| Hidden stage 3 | first-try accuracy at stage 3 (the second A) per recipe, arm and founder, and its mean over the 8 |
| The better recipe | the context recipe with the higher mean paired difference against the founder over the three views' 24 pairs; a tie goes to more clean passes |
| P1 | if time allows: founder 1001, the better recipe alone (`rc-p1`), all six arms read as `step` and `live`: sampled, greedy and per-state after teaching and after 80 alone, against the retained founder and recall rows; point readings |

### Expected outcome, stated before the run

On the hidden view the first A's key is A; after a right action B's key is B plus context times
A; the second A's address is A plus context times (half A plus B), and an A repeated after a
wrong action at stage 1 has address A plus context times A. So with context the address itself
tells A-after-B from A-after-A and from the first A before any lesson, and the slots a moment
finds depend on the history it shares with them; with context 1.0 the history weighs as much as
the event, so at the second A the B moment is addressed more than the first A. The projections
from the recall and next regions have to learn to read that in 120 episodes, and under reward
alone no address lesson runs. Expected: on the hidden view a gain over the plain recall recipe
in the corrective arms is possible, and so is no change; a heavier history makes like moments'
keys less alike and the address less selective, so a loss against the plain recipe is possible
on every view, most likely at context 1.0; on the visible view no change or a small change. An
unchanged result is possible.

### Runs

`run_recall_context.sh`: queue 1 hidden then visible, queue 2 invisible (two runner processes);
then P1 for the better recipe on founder 1001 alone. Wall times from the manifests, `uptime`
before and after. Analysis: `recall_screen.py analyze` appends the follow-up sections to
`RECALL_RESULTS.md` and a `context` entry to `recall-summary.json`.
