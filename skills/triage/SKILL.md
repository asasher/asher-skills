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

`reference/` and `templates/` are bundled with this skill; `docs/agents/` is the target repo's playbook, created by `triage setup`. A subcommand's bundled reference is the contract; the playbook supplies repo conventions. If a required playbook is missing, stop and tell the user to run `triage setup`; do not improvise or substitute bundled files.

## Commands

| Command | Role | Bundled reference | Project playbook |
|---|---|---|---|
| `groom` | With the human: classify work-type, clarify, resolve relationships, label readiness | `reference/groom.md` | `docs/agents/triage-policy.md` |
| `run` | Queue ready-for-agent, unblocked issues; dispatch one issue thread each | `reference/run.md`, `reference/issue-loop.md` | `docs/agents/triage-policy.md` |
| `setup` | Scaffold playbooks/labels; set isolation, seed/checks, readiness | `reference/setup.md`, `reference/worktree-isolation.md`, `templates/` | writes them |
| `diagnose` | Bug: reproduce, fix, confirm the failing path passes | `reference/diagnose.md` | `docs/agents/diagnosing-bugs.md` + `environment.md` |
| `plan` | Enhancement: plan or skip; stop at the approval gate | `reference/plan.md` | `docs/agents/planning.md` |
| `implement` | Build an approved plan | `reference/implement.md` | `docs/agents/implementing.md` + `environment.md` |
| `refactor` | Behavior-preserving change locked by tests | `reference/refactor.md` | `docs/agents/refactoring.md` |
| `verify` | Verdict loop: checks plus pass/fail against acceptance criteria | `reference/verify.md` | `docs/agents/verifying.md` + `environment.md` |
| `evidence` | Capture proof after verify; index it in the PR body | `reference/evidence.md` | `docs/agents/verifying.md` + `environment.md` |
| `adversarial-review` | Reviewer ⇆ fixer subagents on a PR until LGTM or cap | `reference/adversarial-review.md` | `docs/agents/pr-reviewer.md`, `docs/agents/pr-fixer.md` + `environment.md` |

`docs/agents/environment.md` is the shared playbook (run/isolate/seed/auth + the parallelism verdict `run` reads); references that touch the app read it alongside their step playbook.

## Routing

1. **No argument** → follow `reference/groom.md`, then offer to run the resulting ready-for-agent issues via `reference/run.md`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that bundled reference and follow it. Everything after the command name is the target (an issue number/URL, PR, branch, or path).
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed.

## Model staffing

The skill defines the roles; the Model staffing section of `docs/agents/environment.md` (written by `triage setup`) records who fills them, because the roster depends on the harness the loop runs in — a harness that cannot reach another vendor's models fills every role from its own lineup.

- **Lead** — the most capable model reachable. Runs the issue thread and its thinking-heavy steps: groom, run, orient, diagnose, plan, implement, refactor.
- **Delegate** — the next most capable tier below the lead, never below the floor. Runs the capped loops: verify ⇆ fix, evidence capture, and the adversarial-review subagents. May be an external CLI for backend-only work when the harness can invoke one; the Reviewer must satisfy the full review criteria, frontend included.
- **Floor** — the minimum capability class the playbook names. Nothing staffs below it. If no model exists between the lead and the floor, the delegate role runs on the lead model itself — delegation into a separate thread still keeps the capped loops out of the lead context.

Each reference restates its staffing where it spawns, so subcommands stay standalone.

## Core rules

- Grooming is human-in-the-loop and classifies; running is autonomous and executes. The agent proposes labels but applies `ready-for-agent` only to issues the human confirms.
- Labels carry two roles — **readiness** (whether/who picks it up) and **work-type** (how it's worked); `ready-for-agent` requires a work-type. The skill reasons in roles; `docs/agents/triage-policy.md` maps them to this repo's labels.
- The `run` thread orchestrates only. It queues `ready-for-agent`, unblocked issues and dispatches; it does not solve or re-triage issues. Solving happens inside issue threads.
- A subcommand reads its own step playbook (and `environment.md` when it touches the app). The playbook decides whether to defer to an installed skill — the subcommand never branches on skill availability itself.
