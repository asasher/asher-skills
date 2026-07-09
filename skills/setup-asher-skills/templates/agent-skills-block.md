<!-- Seed for the `## Agent skills` context block. setup writes this section into the target repo's
     AGENTS.md (preferred) or CLAUDE.md — the per-project skill map. It is a map, not a router: there is
     no `ask-asher` dispatcher skill. Fill one row per installed skill with a one-line plain-language
     purpose, note the sibling relationships, and keep the repo pointer. No version stamp. -->

## Agent skills

These skills are installed for this project from
[asher-skills](https://github.com/asasher/asher-skills). Re-run `setup-asher-skills` (audit mode) to
reconcile them against the repo.

| Skill | What it does here | Scope |
|-------|-------------------|-------|
| <skill> | <one plain-language line — what it does for someone working this repo> | project / global |

<!-- Example rows (delete and replace with the actual installed set):
| backlog | Runs issues through groom → plan → build → review to a merged PR | project |
| plan | Turns a feature into a reviewed plan held at an approval gate | project |
| review-loop | Shows a plan or design in the browser to approve or comment on | project |
| staffing | Picks which model runs which task | global |
-->

**How they fit together:** composers pull their siblings — `plan` and `prototype` use `review-loop`
(to sign off) and `staffing` (to pick the model); `backlog` uses all four. `staffing` and `review-loop`
depend on nothing.

**Source & updates:** see the repo pointer below / in this file. To add a skill, change scope, or check for
drift, re-invoke `setup-asher-skills`.
