---
name: triage
description: Grooms the GitHub backlog (classify, clarify, resolve dependencies, label readiness) then runs each ready-for-agent issue through a per-issue development loop (fix/plan/implement/refactor, a build⇆verify loop against acceptance criteria, evidence capture, PR, adversarial review); subcommands also run standalone.
argument-hint: "[command] [issue, PR, or target]"
user-invocable: true
disable-model-invocation: true
---

# Triage

Triage works the backlog in two phases: **groom** sorts and clarifies open issues with the human and labels which are ready, then **run** takes each ready-for-agent issue through the matching development loop, one at a time, ending at a reviewed PR. This file is the command surface; each subcommand loads its own contract from `reference/` only when it runs.

## File locations

This skill's files fall into two kinds, by where they live:

- **Bundled reference** — files under this skill's own `reference/` and `templates/`. They ship with the skill and are present wherever it is installed. Do not look for them in the target repo.
- **Project playbook** — files under `docs/agents/` in the target repo. They hold how this codebase does each step, and are created by `triage setup`.

A subcommand's contract is a bundled reference; the conventions it needs are a project playbook. If a required playbook is missing, stop and tell the user to run `triage setup`; do not improvise the step or substitute a bundled file.

## Commands

| Command | Role | Bundled reference | Project playbook |
|---|---|---|---|
| `groom` | Triage the backlog with the human: classify work-type, clarify, resolve dependencies/supersession, label readiness | `reference/groom.md` | `docs/agents/triage-policy.md` |
| `run` | Queue every ready-for-agent, unblocked issue, dispatch one issue thread per issue, report handoff | `reference/run.md`, `reference/issue-loop.md` | `docs/agents/triage-policy.md` |
| `setup` | Scaffold playbooks, provision GitHub role labels, choose parallel/sequential and scaffold worktree isolation on approval, identify seed/checks, verify readiness | `reference/setup.md`, `reference/worktree-isolation.md`, `templates/` | writes them |
| `diagnose` | Bug branch: reproduce, fix, confirm the failing path passes | `reference/diagnose.md` | `docs/agents/diagnosing-bugs.md` + `environment.md` |
| `plan` | Enhancement branch: produce a reviewable plan with testable acceptance criteria, stop at the approval gate | `reference/plan.md` | `docs/agents/planning.md` |
| `implement` | Build an approved plan | `reference/implement.md` | `docs/agents/implementing.md` + `environment.md` |
| `refactor` | Behavior-preserving change locked by tests | `reference/refactor.md` | `docs/agents/refactoring.md` |
| `verify` | Behavioral loop: run checks, verify against acceptance criteria, hand failures back to the builder until they pass or cap | `reference/verify.md` | `docs/agents/verifying.md` + `environment.md` |
| `evidence` | Capture human-facing proof once, after verify converges, indexed by the PR body | `reference/evidence.md` | `docs/agents/verifying.md` + `environment.md` |
| `adversarial-review` | Reviewer ⇆ fixer subagents on a PR until LGTM or cap | `reference/adversarial-review.md` | `docs/agents/pr-reviewer.md`, `docs/agents/pr-fixer.md` + `environment.md` |

`docs/agents/environment.md` is the shared playbook: branch model, base branch, where and how to run, isolate, seed, authenticate, and test the app, the tools available, and the parallelism verdict. Any subcommand that builds a branch, runs, or tests the app reads it alongside its own step playbook; `run` reads its parallelism verdict before dispatch.

## Routing

1. **No argument** → follow `reference/groom.md`, then offer to run the resulting ready-for-agent issues via `reference/run.md`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that bundled reference and follow it. Everything after the command name is the target (an issue number/URL, PR, branch, or path).
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed.

Every subcommand works the same whether a human types it or the loop reaches it: it resolves to the same bundled reference.

## Core rules

- Grooming is human-in-the-loop and classifies; running is autonomous and executes. The agent proposes labels but applies `ready-for-agent` only to issues the human confirms.
- Labels carry two independent roles: **readiness/ownership** (`ready-for-agent`, `ready-for-human`, `needs-info`) decides whether and who picks an issue up; **work-type** (`bug`, `enhancement`, `refactor`) decides how the agent works it. `ready-for-agent` requires a work-type. The skill reasons in roles; `docs/agents/triage-policy.md` maps them to this repo's label names.
- The `run` thread orchestrates only. It queues `ready-for-agent`, unblocked issues and dispatches; it does not solve or re-triage issues. Solving happens inside issue threads.
- A subcommand reads exactly one playbook path. The playbook decides whether to defer to an installed skill — the subcommand never branches on skill availability itself.

## Glossary

- **Groom phase**: the interactive triage pass — classify, clarify, resolve dependencies, label readiness — that releases issues to the agent.
- **Run thread**: the orchestrator thread where the ready-for-agent queue is built and dispatched.
- **Issue thread**: one thread created to take a single ready-for-agent issue through the loop to a PR.
