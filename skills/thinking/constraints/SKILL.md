---
name: constraints
description: Find and work the one constraint limiting a system, Theory-of-Constraints style, on a shared visual HTML page.
argument-hint: "[new \"<system>\"] | [resume] | [list] | [map|find|dig|cloud|plan|experiment|review]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: []
---

# Constraints

Every system has, at any moment, **one thing** that limits it — the constraint. Improving anything else is a
mirage: *an hour saved at a non-bottleneck is an hour saved for nothing*. This skill runs the Theory of
Constraints as a facilitated, visual investigation **with** the user: map how work flows toward the goal, hunt
the constraint down with evidence rather than opinion, then squeeze it (exploit), align everything else to it
(subordinate), and only then consider spending money on it (elevate) — each move framed as a falsifiable
experiment. When the constraint breaks, it moves; the loop starts again.

The whole state lives in **one self-contained HTML page**, `constraint.html` — flow map, suspect board, logic
trees, conflict clouds, experiment cards, constraint history — which doubles as the shareable artifact. The page
is the deliverable *and* the memory: every session updates it, every resume reads it. If you haven't read
[reference/framework.md](reference/framework.md) this session, read it before running any command — it holds the
synthesized theory, the evidence rules, and the workspace convention.

## Core rules

- **No goal, no constraint.** A constraint only exists relative to a goal with a countable throughput unit.
  If the goal is vague, every annoyance looks like a constraint — pin the goal before hunting.
- **The constraint is a hypothesis, not a verdict.** Every claim carries a confidence mark — *suspected /
  evidenced / validated* — and the mark only moves rightward on observables: queue sizes, wait times, aging
  work, expedite frequency, calendar load, a moved system metric. Convert opinions to observables before
  recording them ("review is slow" → median review wait, count of PRs older than SLA).
- **One question at a time, anchored with a hypothesis.** Offer your working read and let the user correct it —
  corrections are denser than free recall. Never fire a questionnaire.
- **Exploit before elevate.** Never recommend hiring, buying, or reorganizing until the exploit checklist is
  visibly exhausted and subordination has been tried. Free capacity is almost always hiding in misuse.
- **Name the dependency, never the person.** Not "Brent is the bottleneck" but "the system routes everything
  through one person's knowledge." Not "the founder can't delegate" but "no decision rules exist that let
  non-founder work move safely." The user's own self-blame gets the same reframe.
- **The system, not the parts.** Refuse local-efficiency wins that don't move system throughput. Before any
  fix: *if this improves 50%, which system-level number changes?*
- **Don't let analysis become the constraint.** Timebox the hunt; the aim is the next highest-leverage
  experiment, not certainty. A suspected-grade constraint with a cheap reversible experiment beats a
  validated-grade one three sessions from now.
- **Know when ToC is the wrong lens.** Contested goal, exploratory work with no repeatable flow, unknown
  product-market fit, safety/ethics/trust issues — say so, point to a better framing, and stop.
- **The page stays current.** After every working session: update the affected sections and their
  `data-status`, the dashboard, the `Updated` date, and prepend a session-log entry. Diagrams re-render on
  save — keep them true. Mechanics: [reference/artifact.md](reference/artifact.md).
- **Evidence files go in `sources/`.** Exports, screenshots, metrics snapshots — saved next to the page and
  cited `[n]`; never pasted as walls of text.

## Commands

| Command | Step | Does | Reference |
|---|---|---|---|
| `new "<system>"` | — | Scaffold a system folder + `constraint.html`, then open with the goal conversation | [artifact.md](reference/artifact.md), [map.md](reference/map.md) |
| `map` | Goal & flow | Pin the goal and throughput unit; draw the flow map; run the queue / scarcity / policy scans | [map.md](reference/map.md) |
| `find` | Identify | Run the hunt: suspects board, question banks, doubling tests, validation — ends with one named, typed, confidence-marked constraint | [find.md](reference/find.md) |
| `dig` | Identify | Deep dive when symptoms are scattered or the constraint smells like policy/paradigm: UDEs → three-cloud / Current Reality Tree → core conflict | [trees.md](reference/trees.md) |
| `cloud` | Change | Evaporating Cloud for a specific conflict blocking action — surface assumptions, find the injection | [trees.md](reference/trees.md) |
| `plan` | Exploit & subordinate | Squeeze the constraint without spending; write the subordination rules; stage elevate options behind a gate | [act.md](reference/act.md) |
| `experiment` | Cause the change | Turn plan moves into falsifiable cards: hypothesis, prediction, metric, review date | [act.md](reference/act.md) |
| `review` | Repeat | Score experiments against predictions, run the has-it-moved check, sweep for inertia, close or continue the cycle | [review.md](reference/review.md) |
| `resume` | — | Inside a system folder: read `constraint.html`, report where things stand, continue | — |
| `list` | — | At the workspace root: every system folder with its current constraint, step, and next review date | — |

## Routing

1. **`new "<system>"`** → scaffold per [reference/artifact.md](reference/artifact.md), then run `map`.
2. **No argument, inside a system folder** (a `constraint.html` is here) → `resume`: read the page's
   `data-status` rail and dashboard, say where the work stands, and continue the active step. If a review date
   has passed, lead with `review`.
3. **No argument, at the workspace root** → `list`, then ask which system to resume.
4. **First word matches a command** → load its reference and run it. Everything after is the detail.
5. **Aliases**: `goal` → `map`; `hunt`, `bottleneck` → `find`; `crt`, `udes`, `why` → `dig`; `conflict`,
   `stuck` → `cloud`; `exploit`, `subordinate`, `elevate` → `plan`; `test`, `hypothesis` → `experiment`;
   `moved`, `check` → `review`.
6. **First word doesn't match** → infer the step from the request, state the inference, and proceed.
   "Why aren't we shipping more"-shaped requests infer `find` (via `map` if the page has no flow map yet);
   "should we hire" infers `plan` (the exploit gate); "did it work" infers `review`.
7. **Step guards**: `find` needs a goal and flow map — run `map` first if the Goal section is empty. `plan`
   needs a named constraint. `experiment` needs at least one plan move. Guards are one sentence, then do the
   prerequisite, not a lecture.

## The arc

**Goal → Map → Find → Plan → Experiments → Loop.** Sections of the page, in order; each ends on a checkable
signal (its *done-when*, defined in the references). The Loop section never closes — when a review shows the
constraint has moved, the old cycle is archived as a history entry and Find/Plan/Experiments reopen for the new
constraint. Expect the second cycle to be faster than the first: the map survives, only the hunt reruns.

## Output standards

- Every session ends with the page updated and **one concrete next action with a date** — usually an
  experiment's next measurement or its review.
- The named constraint is always stated with its **type** (physical / policy / paradigm / market / attention),
  its **confidence mark**, and the evidence behind the mark — in the dashboard, not buried in prose.
- Plans show the exploit moves *before* any elevate option, and every elevate option carries its throughput-
  accounting test (ΔT vs ΔI + ΔOE).
- Experiment cards state a numeric-or-observable prediction and a review date. "Try it and see" is not a card.
- Diagrams carry the evidence: queue counts annotated on the flow map, confidence chips on suspects, red
  highlight on the constraint node. Someone opening the page cold should find the constraint in ten seconds.
