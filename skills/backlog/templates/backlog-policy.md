# Playbook: Backlog Policy

> Project playbook for this repo. Read by `groom` (to triage the backlog), `run` (to select ready work), and the issue loop (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Label roles

Two independent axes, plus exclusions. Readiness decides *whether and who* picks an issue up; work-type decides *how* the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type. Default label `ready-for-agent` — _<your label>_.
- `in-flight` — dispatched: an issue thread owns it, so `run` never selects it. Set by `run` at dispatch, replacing `ready-for-agent`; records what's flying (branch name and dispatch date — local: frontmatter; GitHub: a comment alongside the label). Cleared by the run thread on abort, superseded by closure when the change merges, or reset by `groom`'s human-confirmed orphan sweep (§ In-flight hygiene). Default `in-flight` — _<your label>_.
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Default `ready-for-human` — _<your label>_.
- `needs-info` — parked, waiting on the reporter. Default `needs-info` — _<your label>_.
- *(no readiness label)* — not yet groomed; a target for `backlog groom`, not for `run`.

Two further lifecycle values appear only where the tracker has no native equivalent (the local binding's `state:` field), written by the loop, never by grooming: `in-review` (a PR is open for it — set on the work branch at PR-open) and `closed` (set on the work branch once review converges; the merge carries it to main). On trackers with native state (GitHub), an open PR and native closure express these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Default `bug` — _<your label>_.
- `enhancement` — plan → implement branch. Default `enhancement` — _<your label>_.
- `refactor` — refactor branch. Default `refactor` — _<your label>_.

**Exclusion** — terminal; removed from grooming and from the run queue:

- `wontfix`, `duplicate`, `superseded`, `invalid` — _<your labels>_.

**Neutral** — every other label (priority, area, size, etc.); ignored for selection and routing.

## Dependencies

- How this repo records that one issue is blocked by another, so `run` can skip blocked work: _<e.g. a `- [ ] depends on #123` task-list line in the body, a `blocked` label plus the linked issue, native issue dependencies where the tracker has them; local: the `deps:` frontmatter list>_.

## Readiness decision

- The agent proposes a work-type and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. The agent may apply `ready-for-human`, `needs-info`, and exclusion roles on its own.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## In-flight hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `in-flight` is the claim marker, applied optimistically — the loop accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock. `run` re-reads each issue immediately before marking it and skips any that changed.
- **Orphan sweep** — an `in-flight` issue whose recorded branch no longer exists, or has gone quiet past _<horizon, e.g. 7 days>_, is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
