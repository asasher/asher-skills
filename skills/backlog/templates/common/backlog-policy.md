# Playbook: Backlog Policy

> Project playbook for this repo. Read by `groom` (to triage the backlog), `run` (to select ready work), and the issue loop (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: _<software | skill-authoring | writing | research | ops | general>_.
- Chosen at `backlog setup`, this is the kind of work this repo's backlog tracks. Playbooks resolve from `templates/common/` overlaid by `templates/<domain>/`, then same-name `templates/software/` stand-ins for any required step the domain pack omits.
- Absent this section (an install from before domain packs existed), the domain is `software`.
- When the chosen domain's pack was not yet shipped at install time, or a shipped pack omitted a required step, those step playbooks are `software` baselines standing in, each flagged in its own header as a code-flavored stand-in to tailor.

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
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a research synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — no mechanical `verify` pass/fail. The artifact is **kept** (committed and merged), unlike `prototype`, which is throwaway — keep the answer, delete the artifact. Default `draft` — _<your label>_.

> Recognizing `draft`: the deliverable is an artifact judged by taste/fit — a memo, copy, a synthesis, code docs — with no testable spec to run against. When that is the shape, groom to `draft`, not `enhancement`.

**Exclusion** — terminal; removed from grooming and from the run queue:

- `wontfix`, `duplicate`, `superseded`, `invalid` — _<your labels>_.

**Neutral** — every other label; ignored for selection and routing. On an inherited tracker this is *most* labels (priority, area/component, size, team, release). The default is **neutral**: a label maps to a role only when `setup` explicitly bound it: _<list the role→label mappings here; leave everything else neutral>_.

**Aliases** — when several existing labels fill one role, one is canonical and the loop treats the others as that role too: _<e.g. `type:bug` and `defect` both → `bug`; or "none">_. Setup reuses existing labels rather than minting duplicates.

## Dependencies

- How this repo records that one issue is blocked by another, so `run` can skip blocked work: _<pick the binding — a `- [ ] depends on #123` task-list line in the body (GitHub default); the `deps:` frontmatter list (local); or the tracker's **native dependency relation** where it has one (Jira `is blocked by`, Linear `blocked-by`), read via the blocker verbs in `platform.md`>_.
- `run` treats an issue with any unresolved (open/incomplete) blocker as blocked and skips it. Duplicate/supersede links: _<the convention — a `duplicate of #N` / `superseded by #N` body line plus the exclusion label, or the tracker's native link>_.

## Readiness decision

- The agent proposes a work-type and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. The agent may apply `ready-for-human`, `needs-info`, and exclusion roles on its own.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## In-flight hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `in-flight` is the claim marker, applied optimistically — the loop accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock. `run` re-reads each issue immediately before marking it and skips any that changed.
- **Orphan sweep** — an `in-flight` issue whose recorded branch no longer exists, or has gone quiet past _<horizon, e.g. 7 days>_, is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
