---
name: triage
description: Routes open GitHub issues through a per-issue development loop (classify, then fix/plan/implement/refactor, verify, PR, adversarial review); subcommands also run standalone.
argument-hint: "[command] [issue, PR, or target]"
user-invocable: true
disable-model-invocation: true
---

# Triage

Triage sorts each open issue by type and routes it through the matching development loop, one issue at a time, ending at a reviewed PR. This file is the command surface; each subcommand loads its own contract from `reference/` only when it runs.

## File locations

This skill's files fall into two kinds, by where they live:

- **Bundled reference** — files under this skill's own `reference/` and `templates/`. They ship with the skill and are present wherever it is installed. Do not look for them in the target repo.
- **Project playbook** — files under `docs/agents/` in the target repo. They hold how this codebase does each step, and are created by `triage setup`.

A subcommand's contract is a bundled reference; the conventions it needs are a project playbook. If a required playbook is missing, stop and tell the user to run `triage setup`; do not improvise the step or substitute a bundled file.

## Commands

| Command | Role | Bundled reference | Project playbook |
|---|---|---|---|
| `run` (default) | Build the issue queue, dispatch one issue thread per issue, report handoff | `reference/run.md`, `reference/issue-loop.md` | — |
| `setup` | Scaffold playbooks into `docs/agents/`; offer matching external skills | `reference/setup.md`, `templates/` | writes them |
| `diagnose` | Bug branch: reproduce, fix, confirm the failing path passes | `reference/diagnose.md` | `docs/agents/diagnosing-bugs.md` + `environment.md` |
| `plan` | Enhancement branch: produce a reviewable plan, stop at the approval gate | `reference/plan.md` | `docs/agents/planning.md` |
| `implement` | Build an approved plan | `reference/implement.md` | `docs/agents/implementing.md` + `environment.md` |
| `refactor` | Behavior-preserving change locked by tests | `reference/refactor.md` | `docs/agents/refactoring.md` |
| `verify` | Run the repo's checks and capture evidence | `reference/verify.md` | `docs/agents/verifying.md` + `environment.md` |
| `adversarial-review` | Reviewer ⇆ fixer subagents on a PR until LGTM or cap | `reference/adversarial-review.md` | `docs/agents/pr-reviewer.md`, `docs/agents/pr-fixer.md` + `environment.md` |

`docs/agents/environment.md` is the shared playbook: branch model, base branch, where and how to run, authenticate, and test the app, and which tools are available. Any subcommand that builds a branch, runs, or tests the app reads it alongside its own step playbook.

## Routing

1. **No argument** → run the orchestration in `reference/run.md`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that bundled reference and follow it. Everything after the command name is the target (an issue number/URL, PR, branch, or path).
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed.

Every subcommand works the same whether a human types it or the loop reaches it: it resolves to the same bundled reference.

## Core rules

- The `run` thread orchestrates only. It discovers the queue and dispatches; it does not solve issues. Solving happens inside issue threads.
- Apply exactly one primary classification per issue: `bug`, `enhancement`, `refactor`, or `needs-info`.
- A subcommand reads exactly one playbook path. The playbook decides whether to defer to an installed skill — the subcommand never branches on skill availability itself.

## Glossary

- **Run thread**: the orchestrator thread where the queue is discovered and dispatched.
- **Issue thread**: one thread created to take a single issue through the loop to a PR.
