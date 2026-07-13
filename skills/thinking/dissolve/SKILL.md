---
name: dissolve
description: Dissolve a malformed question via two-agent debate — taboo the loaded word, unbundle the sub-questions — instead of answering it.
argument-hint: "[debate \"<question>\"] | [new \"<question>\"] | [resume] | [list]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: []
  optional: []
---

# Dissolve

Some questions can't be *answered* — they must be **dissolved**. "Is free will real?" "Is addiction a disease?"
"Is a hotdog a sandwich?" You can argue either side forever because the question is malformed: a loaded word is
doing work no fact can settle. Dissolving means refusing to pick a side and instead **deconstructing the
cognitive algorithm that makes it feel like a question** — until the itch is gone, not merely out-argued. As Yudkowsky
puts it, you write *a stack trace of the internal algorithm*, not a verdict.

This skill runs that process as a **debate between two minds** — because a lone reasoner smuggles in its own
assumptions. By default you dissolve *with a second agent* (a different model or CLI, or a spawned subagent):
you share one `dissolution.html` and challenge each other's cuts, turn by turn, in a `discussion.md` log. Debate
isn't decoration — a second agent reliably catches a strand you assumed as a premise and a resolution leaning on
desert, sharpenings a single pass misses. Optionally a **human joins the loop** — posing the question, owning the
itch, weighing in each turn. Either way completion stays subjective; who owns the gate is a Core rule below. The
whole state lives in **one self-contained HTML page** that doubles as the shareable artifact; `discussion.md` is
working scratch, and the HTML is what's true.

## The five moves

The heart of the skill. Each move maps to a section of `dissolution.html` and ends on a checkable signal.
Depth, worked examples (free will, disease), and failure patterns are in `reference/method.md` — read it when
starting a dissolution or when a move stalls.

1. **Pose the question & find the itch.** Record it in the human's own words. Then name *why it feels like a
   hanging question* — the confusion is in the map, not the territory, so the itch is the real target.
   *Done when:* the itch is named as a sensation, not restated as a fact.
2. **Taboo the word.** Ban the loaded term (*real, disease, fair, conscious, really*) and re-ask using only what
   it stands for. Where substitution flows, the word was cheap; where you **can't** substitute without smuggling
   it back, you've *located* the confusion. *Done when:* every load-bearing word is either replaced or flagged as
   irreplaceable.
3. **Stack-trace & unbundle.** Trace the mental algorithm that *generates the feeling of a question*. A disguised
   question is usually several separate questions wearing one word (Scott Alexander: "disease" bundles *is it
   bad? · is it their fault? · does treating it medically help?*). Diagram the decomposition — and pull out the
   strand you were about to **assume**: if a sub-question shows up anywhere in your own prose as a background fact
   ("drinks *despite harm*"), it isn't unbundled yet — give it its own yes/no.
   *Done when:* every strand is a distinct sub-question, including any that felt like a premise.
4. **Reduce to anticipated experience.** Turn each sub-question into what you'd actually *expect to observe* each
   way. A sub-question whose answers predict the *same* experience is **empty** — dissolved on contact. The rest
   are real (empirical or moral) and named as such. *Done when:* each sub-question is marked empty, empirical, or
   value-laden.
5. **Resolve & run the gate.** State what's left of the original once the word is tabooed and the parts
   separated. Where a surviving part is a value/decision question, settle it by **consequences** — which stance
   produces better outcomes (blame by what *helps*, not what's deserved) — not by hunting a hidden fact; showing
   it's *a decision, not a discovery* is the dissolution, not a verdict you impose. Then the **gate**: ask
   whoever owns the itch — the human when present, else the two agents' explicit agreement (Core rules) —
   whether *any lingering feeling of a hanging question* remains. Any
   residual "but still…" means it is **not** dissolved — record where the pull is and loop back.
   *Done when:* the gate's owner reports no lingering confusion. A logged open thread is a paused, resumable state — not completion.

The moves are a loop, not a staircase — tabooing often exposes a new sub-question that sends you back to move 2.

## Operating model

- **One workspace, one folder per question.** The skill is installed once at a **dissolve workspace** root. Each
  question is its own folder — the *dissolution* — holding `dissolution.html` (state + artifact) and `sources/`.
  Folders are siblings; a question is self-contained, shareable, and deletable on its own.
- **The HTML is the state.** There is no separate state file. `dissolution.html` *is* the single source of
  truth: its five sections carry the thinking and each carries a `data-status` (`empty`/`active`/`done`) that
  tells you, on resume, exactly where the work stands. Edit it directly. Mechanics — section markers, precise
  edits, diagrams, the session log, and citations — are in `reference/artifact.md`.
- **Two agents, one page.** Dissolving defaults to a debate: this agent plus a second (a different model/CLI, or
  a spawned subagent) work the *same* `dissolution.html`, alternating and challenging each other's taboo-rewrites,
  cuts, and verdicts. Each turn: read the partner's last move, push on its weakest point (a strand assumed as a
  premise, a "value" that's really empirical, a resolution leaning on desert), then update the page. Converge when
  neither can sharpen the cut further **and** the gate passes. The turn log is a sibling `discussion.md` —
  **scratch, not state**; the HTML stays the single source of truth. Full protocol: `reference/debate.md`.
- **Sources go in `sources/`.** Anything that can't sit inline (a PDF, a saved article, a long quote) is copied
  into the dissolution's `sources/` folder and cited in the page as a numbered reference `[n]`. External URLs may
  be cited directly. Never paste a wall of source text into a section.

## Commands

| Command | Does |
|---|---|
| `debate "<question>"` | **Default for a fresh question.** Scaffold like `new`, then bring in a second agent and dissolve as a two-agent debate over one `dissolution.html` + a `discussion.md` turn log; add the human to the loop when present. See `reference/debate.md`. |
| `new "<question>"` | Solo fallback when no second agent is available: create the dissolution and dissolve it single-handed. Otherwise prefer `debate`. |
| `resume` | Inside a dissolution folder: read `dissolution.html`, report which move is active from the `data-status` rail, and continue it. This is the default inside a folder. |
| `list` | At the workspace root: list every dissolution folder with its current move and overall status. The default at the root. |

## Routing

1. **`debate "<question>"`** (or **`new`** for the solo fallback) → scaffold the folder and begin (see
   `reference/artifact.md` for the copy/fill steps, `reference/debate.md` for the two-agent protocol).
2. **No argument, inside a dissolution folder** (a `dissolution.html` is here) → `resume`.
3. **No argument, at the workspace root** (sibling dissolution folders, no `dissolution.html` here) → `list`, then
   ask which to resume.
4. **First word doesn't match** → treat the whole argument as a question to dissolve; confirm, then `debate`
   (or `new` if no second agent is available).

## Core rules

- **Dissolve, don't answer.** Your job is to remove the question, not win it. If you catch yourself defending a
  position, stop — you've slipped from dissolving to arguing. Proving a question *meaningless* is also not
  dissolving; you must show *why the mind generated it*.
- **Whoever owns the itch owns the gate.** Completion is subjective. When a human is in the loop, the confusion
  is in *their* map — never declare it dissolved on your own authority; the gate is a question you ask them, every
  time. In an unattended debate, the gate is the two agents' *explicit* agreement that the original has stopped
  being a question — not one agent's say-so.
- **The page stays current.** After every working session, update the affected sections, their `data-status`, the
  `Updated` date, and prepend a session-log entry. The page is only useful as state if it always reflects reality.
- **Keep the artifact shareable.** `dissolution.html` must stay a clean, self-contained one-pager anyone can open
  — no external state, no build step, diagrams rendered inline. Follow `reference/artifact.md`.
