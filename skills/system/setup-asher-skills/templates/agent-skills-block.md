<!-- Seed for the `## Agent skills` context block. On a greenfield project setup creates canonical
     AGENTS.md and, when Claude Code is used, a minimal CLAUDE.md that begins with @AGENTS.md. Existing
     deliberate one- or two-file layouts are reconciled in place. It is a map, not a router: there is
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

**How they fit together:** render this summary from the installed skills' canonical sibling declarations;
do not maintain a second dependency list in this template.

**Source & updates:** see the repo pointer below / in this file. To add a skill, change scope, or check for
drift, re-invoke `setup-asher-skills`.
