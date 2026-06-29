# Playbook: Triage Policy

> Project playbook for this repo. Read by `groom` (to triage the backlog), `run` (to select ready work), and the issue loop (to route on work-type). The skill reasons in **roles**; map this repo's actual GitHub label names to each role below so the wording can differ per repo.

## Label roles

Two independent axes, plus exclusions. Readiness decides *whether and who* picks an issue up; work-type decides *how* the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — the agent may work it. Requires a work-type. Default label `ready-for-agent` — _<your label>_.
- `ready-for-human` — only a human; the agent skips it entirely. Default `ready-for-human` — _<your label>_.
- `needs-info` — parked, waiting on the reporter. Default `needs-info` — _<your label>_.
- *(no readiness label)* — not yet groomed; a target for `triage groom`, not for `run`.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Default `bug` — _<your label>_.
- `enhancement` — plan → implement branch. Default `enhancement` — _<your label>_.
- `refactor` — refactor branch. Default `refactor` — _<your label>_.

**Exclusion** — terminal; removed from grooming and from the run queue:

- `wontfix`, `duplicate`, `superseded`, `invalid` — _<your labels>_.

**Neutral** — every other label (priority, area, size, etc.); ignored for selection and routing.

## Dependencies

- How this repo records that one issue is blocked by another, so `run` can skip blocked work: _<e.g. a `- [ ] depends on #123` task-list line in the body, a `blocked` label plus the linked issue, or GitHub's native issue dependencies>_.

## Readiness decision

- The agent proposes a work-type and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. The agent may apply `ready-for-human`, `needs-info`, and exclusion roles on its own.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).
