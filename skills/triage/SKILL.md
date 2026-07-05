---
name: triage
description: Groom the GitHub backlog; run ready-for-agent issues through the issue loop to reviewed PRs; subcommands run standalone.
argument-hint: "[command] [issue, PR, or target]"
user-invocable: true
disable-model-invocation: true
---

# Triage

This file is the command surface; each subcommand loads its own contract from `reference/` only when it runs.

## References

`reference/` and `templates/` are bundled with this skill; `docs/agents/` is the target repo's playbook, created by `triage setup`. A subcommand's bundled reference is the **orchestration contract** — target, gates, staffing, handoffs. Its playbook carries the **working instructions** — the technique (shipped inlined via the template baseline) plus this repo's conventions — so a repo changes how a step works by editing its playbooks, never the skill. If a required playbook is missing, stop and tell the user to run `triage setup`; do not improvise or substitute bundled files.

## Commands

| Command | Role | Bundled reference | Project playbook |
|---|---|---|---|
| `groom` | With the human: classify work-type, clarify, resolve relationships, label readiness | `reference/groom.md` | `docs/agents/triage-policy.md` |
| `run` | Queue ready-for-agent, unblocked issues; dispatch one issue thread each | `reference/run.md`, `reference/issue-loop.md` | `docs/agents/triage-policy.md`; threads read `pr.md` + their step playbooks |
| `setup` | Scaffold or reconcile playbooks/labels; set isolation, app access, presentation surface, seed/checks, readiness | `reference/setup.md`, `reference/worktree-isolation.md`, `reference/migrations.md`, `templates/` | writes them |
| `diagnose` | Bug: reproduce, fix, confirm the failing path passes | `reference/diagnose.md` | `docs/agents/diagnosing-bugs.md` + `environment.md` |
| `plan` | Enhancement: plan or skip; HTML plan, approval gate, commit before build | `reference/plan.md` | `docs/agents/planning.md` |
| `prototype` | Throwaway code that answers a design question (logic or UI shape) | `reference/prototype.md` | `docs/agents/prototyping.md` + `environment.md` |
| `implement` | Build an approved plan | `reference/implement.md` | `docs/agents/implementing.md` + `environment.md` |
| `refactor` | Behavior-preserving change locked by tests | `reference/refactor.md` | `docs/agents/refactoring.md` |
| `verify` | Verdict loop: checks plus pass/fail against acceptance criteria | `reference/verify.md` | `docs/agents/verifying.md` + `environment.md` |
| `evidence` | Capture and present proof once review converges; fill the PR's evidence block | `reference/evidence.md` | `docs/agents/evidence.md` + `environment.md` |
| `adversarial-review` | Reviewer ⇆ fixer subagents on a PR until LGTM or cap | `reference/adversarial-review.md` | `docs/agents/pr-reviewer.md`, `docs/agents/pr-fixer.md` + `environment.md` |

`docs/agents/environment.md` is the shared playbook (run/isolate/seed/auth + the parallelism verdict `run` reads); references that touch the app read it alongside their step playbook. Model staffing — the **orchestrator**/**builder**/**checker** roles, the work-surface routing, and the fallback ladder — is defined in `reference/staffing.md`, loaded by the references that spawn work; the roster lives in the Model staffing section of `environment.md`. The **presentation surface** — how plans and prototypes reach a human who may not be at the machine — is defined in `reference/presenting.md`; its contract lives in the Presenting section of `environment.md`.

## Routing

1. **No argument** → follow `reference/groom.md`, then offer to run the resulting ready-for-agent issues via `reference/run.md`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that bundled reference and follow it. Everything after the command name is the target (an issue number/URL, PR, branch, or path).
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed.
