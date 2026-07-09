# Rankings, capabilities, pins, and the resolution order

Three structures drive routing, and **they are deliberately separate**: a rankings table, a capability
matrix, and a task-pin list. Keeping them apart is the whole point — mixing them corrupts the tie-break
(explained below). The concrete rows come from the machine audit and any project override; this file defines
what each structure *is* and how a routing question resolves against them.

## The rankings table

Rankings, **higher = better**, three columns only:

- **cost** — reflects what this machine's owner actually pays, not list price.
- **intelligence** — how hard a problem you can hand the model unsupervised.
- **taste** — UI/UX, code quality, API design, and copy.

The table contains **only** cost, intelligence, and taste. It never contains a capability boolean. Its rows
are model names with those three numbers; nothing else belongs here. (The audit fills in *which* models
appear; the numbers come from a tunable default seed — see [machine-audit](machine-audit.md).)

## The capability matrix — a separate structure

Capabilities are **booleans keyed by model**, in their own matrix, never columns in the rankings table:

| capability     | meaning                                                    |
|----------------|------------------------------------------------------------|
| browser-use    | can drive a real browser (navigate, click, read the page)  |
| computer-use   | can operate a desktop/GUI environment                      |

Add capability rows as the environment needs them. A capability is either present or absent for a model; it
is not "better" or "worse", so it has no place on a higher-is-better axis.

**Why they must stay separate:** the rankings tie-break orders models by *degree* (more intelligence beats
less). A capability is a *kind*, not a degree — a model either drives a browser or it does not. If you fold
"browser-use" in as a numeric column, you either (a) let a browser-capable-but-dumber model outrank a
smarter one on an unrelated task, or (b) let raw intelligence override a hard capability requirement and pick
a model that physically cannot do the job. Either way the `intelligence > taste > cost` ordering stops
meaning what it says. So capabilities **gate** (filter the candidate set); they never **rank**.

## Task-pins — a separate, first-class list

A **pin** binds a task *type* to a specific model, resolved **before** any ranking. Pins are an explicit
named list, kept distinct from ranking-derived defaults:

- **mechanical / bulk work** (clear-spec implementation, migrations, data analysis, bulk edits) → the pinned
  bulk model.
- (projects add their own pins as deltas.)

A pin **short-circuits the ranking**: if the task matches a pin, you return the pinned model and do **not**
derive a choice from the table. A pin is a routing decision already made; ranking is for tasks no pin
covers. Do not "double-check" a pinned choice against the rankings — that defeats the pin.

## Resolution order

Resolve every "which model?" question in this exact order:

1. **Task-type pin?** If the task matches a pin, return the pinned model. **Stop** — skip steps 2–3.
2. **Gates — filter the candidate set before ranking.** Both gates are **hard constraints**, not
   preferences: they remove models from contention, they do not merely nudge the tie-break. Apply whichever
   the task triggers (a task may trigger both, one, or neither):
   - **Capability gate.** If the task requires a capability (e.g. a browser-driving task needs `browser-use`),
     filter the candidate models to those the capability matrix marks true for it. A task with no capability
     requirement keeps all candidates.
   - **Taste gate.** If the task is **user-facing** (UI, copy, API design), filter the candidates to those
     with **taste ≥ 7**. This is a floor, not a tie-break: a model below taste 7 is out of contention for
     user-facing work no matter how high its intelligence. A task that is not user-facing keeps all
     candidates.

   The models that survive both applicable gates are the survivor set.
3. **Rank the survivors** by `intelligence > taste > cost`: highest intelligence wins; ties broken by taste;
   remaining ties broken by cost (cheaper wins). Cost is a tie-breaker **only**. Ranking never resurrects a
   model a gate removed — a taste-5 model cannot win user-facing work on intelligence, because the taste gate
   already dropped it in step 2.
4. **Fallback ladder.** If the chosen model is unreachable from the current harness, apply the succession
   line in [roles-and-fallback](roles-and-fallback.md): the next most capable reachable survivor takes the
   role; if none is reachable, run on the current model in a subagent. A model the harness cannot reach is
   not a candidate.

### Worked example — a browser-driving task

"Who drives this browser-automation task?" First check pins (step 1): no bulk/mechanical match, so continue.
Capability gate (step 2): the task requires `browser-use`, so filter to models the **capability matrix**
marks `browser-use: true` — that is the deciding structure, cited by its matrix location. Then rank *those
survivors only* (step 3) by intelligence > taste > cost. The smartest model overall is irrelevant if it is
not in the browser-capable survivor set — that is exactly the corruption the separation prevents.

### Worked example — a bulk mechanical edit

"Who does a large mechanical find-and-replace across the codebase?" Step 1 matches the mechanical/bulk pin,
so return the **pinned** bulk model and stop. The answer is the pin, not a ranking derivation — do not walk
the table for it.

## How to apply — defaults, not limits

- **These are defaults, not limits.** Standing permission to override: if a cheaper model's output does not
  meet the bar, rerun the work with a smarter model **without asking**. Judge the output, not the price tag.
  Escalating costs less than shipping mediocre work.
- Use cheaper models to gather information and try things first, then move the work up if needed — don't let
  cost keep work off the right model.
- **Cost is a tie-breaker only.** When axes conflict for anything that ships: `intelligence > taste > cost`.
- Anything user-facing (UI, copy, API design) needs **taste ≥ 7** — and this is a **hard gate, not a soft
  default**: it is enforced in step 2 of the resolution order (the taste gate), which filters out any model
  below the floor *before* the `intelligence > taste > cost` ranking runs. Unlike cost (a soft default you
  may escalate past freely), the user-facing taste floor is never overridden by a higher-intelligence model.
- Orchestration, design, and hard diagnosis go to the most capable reachable model.
- Reviews go to a high-taste/high-intelligence model, optionally a second independent model as an extra
  perspective.
- Never staff below the floor (see [roles-and-fallback](roles-and-fallback.md)); never use a model the
  roster names as excluded.
