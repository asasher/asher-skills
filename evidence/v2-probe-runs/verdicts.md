# v2 family probe runs — verdict table

Dual-executor Tier 1 situated probes per `docs/agents/probe-evals.md`, run 2026-07-23 on the
`sdlc-lifecycle` branch (post-review-pass state, HEAD ≈ `6602ddf`). Executors: **claude-opus** (in-session
subagent, only the probe packet in context) and **gpt-5.6-sol** (`codex exec --sandbox read-only`, same
packets). Packets contained only the files each probe header names; answer keys were written before the
runs (in each skill's `evals/probes.md`) and withheld from executors. Full answers: `transcript-claude-opus.md`,
`transcript-codex-sol.md`.

| Skill | Probes | claude-opus | gpt-5.6-sol | Verdict |
|---|---|---|---|---|
| backlog | P1, P1b, P2–P6 | 7/7 | 7/7 | **pass** |
| shape | P1–P9 | 9/9 | 9/9 | **pass** |
| to-spec | P1–P8 | 8/8 | 8/8 | **pass** |
| to-tickets | P1–P8 | 8/8 | 8/8 | **pass** |
| prototype | P1–P5 | 5/5 | 5/5 | **pass** |
| implement | P1–P4 | 4/4 | 4/4 | **pass** |
| code-review | P1–P7 | 7/7 | 7/7 | **pass** |
| watch-until | P1–P5 | 5/5 | 5/5 | **pass** |

**Total: 53/53 per executor, 106/106 combined. Every set meets its pass bar on both executors.**

## Flagged ambiguities (the valuable findings)

- **backlog P5 (opus):** the skill states "Missing playbooks: run `backlog setup` first" as a general
  rule but does not say whether `build` hard-aborts or prompts when a playbook is missing mid-command.
  Both executors reached the correct action; recorded as acceptable looseness, no change made.
- **implement P1 (both executors):** the tidy-up strand fits neither route and both executors flagged it
  rather than performing it — the designed outcome after the refactoring-route negation was removed.
- **code-review P4 (sol):** the probe's premise ("Spec found 1 severe issue") contradicted the scenario
  ("no spec can be found anywhere"). Real probe-set bug; P4 premise amended in the same change as this
  evidence. The separation rule was still answered correctly under the hypothetical.
- **shape P4 (both):** whether a settled cadence decision is ADR-worthy is left to domain-modeling's
  contract — correctly deferred by both executors, not a defect.
