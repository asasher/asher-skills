# Playbook: Backlog Policy

> Project playbook for this repo. Read by `groom` (to triage the backlog), `run` (to select ready work), and the issue loop (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: **software** — step playbooks scaffolded from `templates/software/` (the shipped default). Recorded 2026-07-11 (issue #32).

## Label roles

Two independent axes, plus exclusions. Readiness decides *whether and who* picks an issue up; work-type decides *how* the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type and complete dispatch metadata (§ Dispatch metadata). Label: **`ready-for-agent`** (identity).
- `in-flight` — dispatched: an issue thread owns it, so `run` never selects it. Set by `run` at dispatch, replacing `ready-for-agent`; records what's flying via a GitHub comment alongside the label (branch name and dispatch date). Cleared by the run thread on abort, superseded by closure when the change merges, or reset by `groom`'s human-confirmed orphan sweep (§ In-flight hygiene). Label: **`in-flight`** (identity).
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Label: **`ready-for-human`** (identity).
- `needs-info` — parked, waiting on the reporter. Label: **`needs-info`** (identity).
- *(no readiness label)* — not yet groomed; a target for `backlog groom`, not for `run`.

Two further lifecycle values appear only where the tracker has no native equivalent, written by the loop, never by grooming: `in-review` and `closed`. This repo is on GitHub, which expresses both natively — an open PR is `in-review`, native issue closure (via `Closes #<n>` at merge) is `closed`. No extra labels for these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Label: **`bug`** (identity).
- `enhancement` — plan → implement branch. Label: **`enhancement`** (identity).
- `refactor` — refactor branch. Label: **`refactor`** (identity).
- `research` — source-audit branch for epistemic-terminal work. The kept dossier records supported facts, traceable inferences, contradictions, and unknowns under `research/<slug>/`. Label: **`research`** (identity).
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a narrative synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — there is **no mechanical `verify` pass/fail**. The artifact is **kept** (committed and merged): that is the line against `prototype`, which is throwaway — keep the answer, delete the artifact. Label: **`draft`** (identity).

> If the terminal question is what sources establish, use `research`. If sources feed prose judged by voice,
> persuasion, or fit, use `draft`. If behavior must change, keep the applicable code work-type and invoke
> research as a substage.

**Exclusion** — terminal; removed from grooming and from the run queue:

- Labels: **`wontfix`**, **`duplicate`**, **`superseded`**, **`invalid`** (all identity; `documentation`, `question`, `good first issue`, `help wanted` are neutral).

**Neutral** — every other label (priority, area, size, etc.); ignored for selection and routing. The default is **neutral**: a label maps to a role only when `setup` explicitly bound it — here every binding above is the identity mapping; everything else stays neutral.

**Aliases** — when several existing labels fill one role, one is canonical and the loop treats the others as that role too: **none** — every role label here is a single identity mapping. Setup reuses existing labels rather than minting duplicates.

## Dispatch metadata

Every `ready-for-agent` issue carries a stable `Dispatch:` block in its body or latest grooming comment:

- `surface`: `backend`, `ui`, `mixed`, or `non-code`, plus any required capability.
- `coordination`: `routine` or `orchestrator-required`.
- `reason`: one sentence naming why the class applies and any known uncertainty. Routine means the issue is
  settled enough for a normal coordinator; orchestrator-required is reserved for product judgment, design,
  hard diagnosis, or another named uncertainty.

`run` passes these fields to staffing before creating a worktree or child. Missing fields are a grooming gap,
never permission to infer them or default to the orchestrator.

## Dependencies

- How this repo records that one issue is blocked by another: GitHub's native `blocked_by` relation, read and written with the verified verbs in `platform.md`. `run` defers the issue while the native unresolved count is positive and releases it into the next wave after the edge clears. Duplicate/supersede links remain a `duplicate of #N` / `superseded by #N` body line plus the exclusion label.

## Readiness decision

- The agent proposes work-type, dispatch metadata, and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. The agent may apply `ready-for-human`, `needs-info`, and exclusion roles on its own.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## In-flight hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `in-flight` is the claim marker, applied optimistically — the loop accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock. `run` re-reads each issue immediately before marking it and skips any that changed.
- **Orphan sweep** — an `in-flight` issue whose recorded branch no longer exists, or has gone quiet past **7 days**, is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
