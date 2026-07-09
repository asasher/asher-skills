# Machine audit — compile the roster, don't hardcode it

The roster is **compiled from the current machine, never shipped fixed.** Which models a harness can reach,
and whether the Codex CLI is installed, differ per machine and per person. So at install time the agent runs
this audit and writes the rankings table, capability matrix, and CLI mechanics **from what it finds** — not
from any example. This is an agent-driven, prompt-level procedure; **it ships no scripts.**

## The audit procedure

Run these probes and record the results:

1. **Which models can this harness reach?** Enumerate the models the current harness/session can actually
   dispatch work to (in Claude Code, the models the Agent/Workflow `model` parameter accepts; in Codex, the
   models the session and its config can run). List each reachable model by name. A model the harness cannot
   reach is **not** a roster candidate — record only reachable ones.
2. **Is the Codex CLI installed?** Probe for it (e.g. `codex --version`). Codex is the path some harnesses
   use to reach a model they can't call natively (e.g. Claude Code reaching gpt-5.5 only via `codex exec`).
   Record present/absent — it decides which CLI mechanics the base includes (see
   [install-and-reconcile](install-and-reconcile.md) § CLI and tools mechanics).
3. **Which harness memory layer exists?** Detect which global memory file the harness uses
   (`~/.claude/CLAUDE.md` for Claude Code, `~/.codex/AGENTS.md` for Codex) so the base is written to the
   right place. This also feeds the scope-decision flow.
4. **Do global staffing rules already exist?** Read the detected memory layer for an existing staffing
   roster. Its presence or absence chooses the scope-decision branch (see install-and-reconcile).

From (1) you have the **rows** of the rankings table and capability matrix. From (2) you have the **CLI
mechanics** the base needs. What the audit **cannot** probe is the *judgment numbers* — cost, intelligence,
and taste are human assessments, not machine-detectable — so seed them, then let the user tune.

## The default seed (numbers the user tunes)

Cost/intelligence/taste can't be probed, so the audit seeds them from a documented default and states plainly
that **the user edits these to fit their own machine and pricing.** Seed only rows for models the audit found
reachable; drop any example row whose model this machine can't reach, and add a seeded row for any reachable
model the example omits.

### Example of audit output (illustrative only — NOT the shipped roster)

The following is **one machine's audit result**, shown so you know the shape to write. It is an *example of
output*, never the authoritative table — a different machine produces a different set of rows. Reproduce the
*shape*, not these values:

```
# Rankings (higher = better) — SEED VALUES, tune to your machine
| model    | cost | intelligence | taste |
|----------|------|--------------|-------|
| gpt-5.5  | 7    | 8            | 5     |
| sonnet-5 | 5    | 5            | 7     |
| opus-4.8 | 4    | 7            | 8     |
| fable-5  | 2    | 9            | 9     |

# Capabilities (booleans) — separate matrix, one row per model
| model    | browser-use | computer-use |
|----------|-------------|--------------|
| ...      | (probe/fill)| (probe/fill) |

# Task-pins
| task type            | pinned model |
|----------------------|--------------|
| mechanical / bulk    | gpt-5.5      |

# Reachability / Codex: gpt-5.5 reachable only via the Codex CLI (installed).
```

Everything above is **audit output for one environment**. On a machine with, say, no Codex CLI and a
different model lineup, the audit produces a different table, different pins, and different CLI mechanics.
Never present the four-model rows as the canonical staffing roster; they are a labeled example of what step
(1) plus the seed produces here.

## Writing the roster from the audit

1. Reachable models → rows of the rankings table, each seeded with cost/intelligence/taste and flagged
   "tune these".
2. Same models → rows of the capability matrix; set booleans per what you can determine (a model's
   browser/computer use is often known from its documented tooling).
3. Task-pins → the named pin list; carry the mechanical/bulk pin if the pinned model is reachable, else leave
   it for the user to set.
4. CLI mechanics → include only the mechanics for tools the audit found present (Codex block only if Codex is
   installed).
5. Floor → set to the lowest capability class the user wants staffed; default it and tell the user to
   confirm.

Then hand the seeded numbers to the user to tune — the deliberately-untested part of this skill is the
subjective quality of those seed numbers.
