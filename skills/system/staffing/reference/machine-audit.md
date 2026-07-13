# Machine audit — compile the roster, don't hardcode it

The roster is **compiled from the current machine, never shipped fixed.** Native models and effect-verified
sibling harness routes differ by machine, person, and direction. Setup audits them and writes rankings,
capabilities, coordinator eligibility, and CLI mechanics from observed results—not from an example. This is
an agent-driven procedure; **it ships no scripts.**

## The audit procedure

Run these probes and record the results:

1. **Which routes work in each direction?** Enumerate native models, then probe installed sibling harness
   CLIs. Claude→Codex uses a bounded `codex exec`; Codex→Claude uses a bounded `claude -p` and must not add
   `--bare`. Record the command shape, timestamp, return/failure class, and fallback successor per direction.
   A failed direction is unavailable without making the healthy direction unavailable. Do not poll vendor
   policy or credit notices; real invocation behavior is the operational signal.
2. **Which sibling harness CLIs are installed?** Probe `codex --version` and `claude --version`, then retain
   only the routes step 1 actually exercised. Presence alone is not reachability. The result decides which
   mechanics the base includes (see [install-and-reconcile](install-and-reconcile.md) § CLI and tools mechanics).
3. **Which harness memory layer exists?** Detect which global memory file the harness uses
   (`~/.claude/CLAUDE.md` for Claude Code, `~/.codex/AGENTS.md` for Codex) so the base is written to the
   right place. This also feeds the scope-decision flow.
4. **Do global staffing rules already exist?** Read the detected memory layer for an existing staffing
   roster. Its presence or absence chooses the scope-decision branch (see install-and-reconcile).

From (1) you have the **rows** of the rankings table and capability matrix. From (2) you have the **sibling harness
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
| model         | cost | intelligence | taste |
|---------------|------|--------------|-------|
| gpt-5.6-sol   | 4    | 9            | 5     |
| gpt-5.6-terra | 6    | 5            | 3     |
| sonnet-5      | 5    | 5            | 5     |
| opus-4.8      | 3    | 7            | 7     |
| fable-5       | 1    | 9            | 9     |

# Capabilities (booleans) — separate matrix, one row per model
| model    | browser-use | computer-use |
|----------|-------------|--------------|
| ...      | (probe/fill)| (probe/fill) |

# Capability pins — resolve at step 1, before ranking; the matrix gates only unpinned capabilities
| capability   | pinned model  |
|--------------|---------------|
| browser-use  | gpt-5.6-terra |
| computer-use | gpt-5.6-terra |

# Task-pins
| task type         | pinned model |
|-------------------|--------------|
| mechanical / bulk | gpt-5.6-sol  |

# Floor: sonnet-5 (Claude-side) / gpt-5.6-terra (Codex-side). Watcher/cron duty runs at the Floor per
# harness — a Floor assignment, not a pin (review-loop reads the Floor directly for its watcher).

# Reachability (illustrative): Claude→Codex works via `codex exec`; Codex→Claude works via `claude -p`
# without `--bare`. Each direction has its own timestamp, failure class, and successor.
```

Everything above is **audit output for one environment**. On a machine with, say, no Codex CLI and a
different model lineup, the audit produces a different table, different pins, and different CLI mechanics.
Never present the five-model rows as the canonical staffing roster; they are a labeled example of what step
(1) plus the seed produces here.

## Writing the roster from the audit

1. Reachable models → rows of the rankings table, each seeded with cost/intelligence/taste and flagged
   "tune these".
2. Same models → rows of the capability matrix; set booleans per what you can determine (a model's
   browser/computer use is often known from its documented tooling).
3. Task-pins → the named pin list; carry the mechanical/bulk pin if the pinned model is reachable, else leave
   it for the user to set.
4. CLI mechanics → include only effect-verified directions; never infer symmetry from one working route.
5. Coordinator eligibility → among the reachable routes, record which can own a durable issue child and
   dispatch/escalate its worker stages. Presence or low cost alone does not qualify a route.
6. Floor → set to the lowest capability class the user wants staffed; default it and tell the user to
   confirm.

Then hand the seeded numbers to the user to tune — the deliberately-untested part of this skill is the
subjective quality of those seed numbers.
