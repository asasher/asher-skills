# Playbook: Backlog Policy

> Project playbook for this repo. Read by `groom` (to triage the backlog), `run` (to select ready work), and the issue loop (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: **software** — step playbooks scaffolded from `templates/software/` (the shipped default). Recorded 2026-07-11 (issue #32).

## Label roles

Two independent axes, plus exclusions. Readiness decides *whether and who* picks an issue up; work-type decides *how* the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type. Label: **`ready-for-agent`** (identity).
- `in-flight` — dispatched: an issue thread owns it, so `run` never selects it. Set by `run` at dispatch, replacing `ready-for-agent`; records what's flying via a GitHub comment alongside the label (branch name and dispatch date). Cleared by the run thread on abort, superseded by closure when the change merges, or reset by `groom`'s human-confirmed orphan sweep (§ In-flight hygiene). Label: **`in-flight`** (identity).
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Label: **`ready-for-human`** (identity).
- `needs-info` — parked, waiting on the reporter. Label: **`needs-info`** (identity).
- *(no readiness label)* — not yet groomed; a target for `backlog groom`, not for `run`.

Two further lifecycle values appear only where the tracker has no native equivalent, written by the loop, never by grooming: `in-review` and `closed`. This repo is on GitHub, which expresses both natively — an open PR is `in-review`, native issue closure (via `Closes #<n>` at merge) is `closed`. No extra labels for these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Label: **`bug`** (identity).
- `enhancement` — plan → implement branch. Label: **`enhancement`** (identity).
- `refactor` — refactor branch. Label: **`refactor`** (identity).
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a research synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — there is **no mechanical `verify` pass/fail**. The artifact is **kept** (committed and merged): that is the line against `prototype`, which is throwaway — keep the answer, delete the artifact. Label: **`draft`** (identity).

> Recognizing `draft`: the deliverable is an artifact judged by taste/fit — a memo, copy, a synthesis, code docs — with no testable spec to run against. When that is the shape, groom to `draft`, not `enhancement`.

**Exclusion** — terminal; removed from grooming and from the run queue:

- Labels: **`wontfix`**, **`duplicate`**, **`superseded`**, **`invalid`** (all identity; `documentation`, `question`, `good first issue`, `help wanted` are neutral).

**Neutral** — every other label (priority, area, size, etc.); ignored for selection and routing. The default is **neutral**: a label maps to a role only when `setup` explicitly bound it — here every binding above is the identity mapping; everything else stays neutral.

**Aliases** — when several existing labels fill one role, one is canonical and the loop treats the others as that role too: **none** — every role label here is a single identity mapping. Setup reuses existing labels rather than minting duplicates.

## Dependencies

- How this repo records that one issue is blocked by another, so `run` can skip blocked work: a `- [ ] depends on #123` task-list line in the issue body. `run` treats an issue with any unchecked, unclosed dependency as blocked and skips it. Duplicate/supersede links: a `duplicate of #N` / `superseded by #N` body line plus the exclusion label.

## Readiness decision

- The agent proposes a work-type and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. The agent may apply `ready-for-human`, `needs-info`, and exclusion roles on its own.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## In-flight hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `in-flight` is the claim marker, applied optimistically — the loop accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock. `run` re-reads each issue immediately before marking it and skips any that changed.
- **Orphan sweep** — an `in-flight` issue whose recorded branch no longer exists, or has gone quiet past **7 days**, is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
