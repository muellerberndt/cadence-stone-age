# The memory of Cadence 0.89.0 where context decides a later action

Declared 26 October 2026, before the first run of these readings. Development founders only;
no confirmation founder is opened. Library: the published `cadence-net==0.89.0` wheel
(SHA-256 `7b27009d0affd2235026ca5f7b4776ba545c15d5c5a14a61c75e52b6df65b786`), Python 3.12,
NumPy 2.x, Linux x86-64, one BLAS thread per runner process.

## Question

Cadence 0.89.0 gives the recall memory a position term, on by default: every head adds to each
slot's logit a learned term for the slot's age, read from the present moment, so what a moment
hears can choose how far back the read looks. 0.88.0 added several read heads, and earlier
releases the learned-code contextual recipe (`attention=True`) and the episodic vote
(`memory_choice=True`). On the chambers where the stream's history decides a later action, do
these memories raise frozen success over the base brain, and on the fully observed chain, where
memory should not matter, do they cost anything?

## Readings

| Reading | World | Founders | Arms |
| --- | --- | --- | --- |
| `view-hidden` | V5's chain seen A, B, A, B: stage 3 looks like stage 1 | 202001 to 202020 | `natural_step_120`, `corrective_step_120`, `corrective_step_480`, `natural_live_480` |
| `view-invisible` | A, A, B, C: only the brain's own right first action tells stage 2 from stage 1 | the same | the same |
| `view-consecutive` | A, A, B, B | the same | the same |
| `view-visible` | V5's own observations: the observation names the stage (control) | the same | the same |
| `route-hidden` | a route cue shown once, two neutral events, then decisions whose first needs the cue | 1001 to 1010 | `guide_step`, `grade_step`, `natural_live` (480 episodes) |
| `route-visible` | the same with the cue kept visible (control of the chamber) | the same | the same |
| `recall` | the recall world: the latest written value asked at a query | 1001 to 1010 | `teach_step`, `reward_step`, `reward_live` (1536 episodes) |
| `p1` | the observed cold chain with 80 episodes alone after teaching (control) | 1001 to 1010 | `natural_step`, `grade_step`, `correct_step`, `correct_step_qualified` |

The evaluation, schedule, caregivers, streams and controls (untrained founder, uniform random,
oracle, searcher) are each template protocol's: frozen copies read at the arm's seam, sampled
episodes and greedy episodes, `Brain.reset` before every read episode.

## Recipes

Chain, route and P1 readings: one base, `Brain.compose(7, 5, modules=(48, 24), arousal=True)`
(`defaults`), and seven recipes on it:

| Recipe | Adds |
| --- | --- |
| `episodic` | `memory_choice=True` |
| `recall` | `recall=True` (position term on: 32 exact ages, then one bucket per doubling) |
| `recall_nopos` | `recall=True, recall_position=0` |
| `recall_h2` | `recall=True, recall_heads=2` |
| `recall_w2` | `recall=True, recall_window=2` |
| `attention` | `attention=True, learned_code=8` (recall with a two-event window on a learned code) |
| `episodic_recall` | `memory_choice=True, recall=True` |

Recall world: its own base (`carried`: one region of 32, no lateral, no episodic store, arousal,
qualified teaching with free and nudged budgets of 1024 and tolerance 0.003, a working trace of
decay 0 and amplitude 0.3) in the 0.89 form, since the library no longer takes the step sizes or
the homeostasis rate as genes: the founder teaching point sets the steps (0.5 and 0.05, momentum
0.9). Recipes: `carried`, `retained` (working trace decay 0.8), `recall`, `recall_nopos`,
`recall_h2`, `attention`.

## Readings and comparisons

Per reading, recipe and arm: the mean frozen success over founders (sampled and greedy), the
founder-paired difference from the base with a percentile 95% interval (10,000 founder resamples,
seed 31012) and the founders up and down, the first-try accuracy per stage, and the teaching
labels and sweeps the arm spent. The position term's own effect is `recall` against
`recall_nopos`, read from the same tables. `memory_089.py analyze` writes `M089_RESULTS.md` and
`m089-summary.json`.

## Expected, stated before the run

- Visible view and P1: no gain from any memory; a small loss is possible, since the memory regions
  add drive.
- Hidden, invisible and consecutive views: a gain is possible where lessons teach the read
  (corrective arms, especially at 480 episodes). Under reward alone the address and position maps
  learn nothing, so only the projections from the read regions can learn.
- Route cue: the cue is two moments back at the first decision. A memory that reads by position
  can find it, but the earlier readings found that the visible-cue control fails under this base
  recipe. When the visible control fails, the hidden reading says nothing about memory.
- Recall world: the latest written value is the most recent slot of its kind, so the recency charge
  alone may serve; the position term may add little.
- An unchanged result is possible on every reading.
