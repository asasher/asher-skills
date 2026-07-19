---
name: backlog
description: Groom the backlog; run ready-for-agent issues through the build loop to reviewed changes; subcommands run standalone.
argument-hint: "[command] [issue, PR, or target]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [diagnosing-bugs, prototype, research, review-loop, staffing]
  optional: []
  setup: reference/setup.md
---

# Backlog

This file is the command surface; each subcommand loads its own contract from `reference/` only when it runs.

## References

A subcommand's bundled reference is the **orchestration contract** — target, gates, staffing, handoffs. Project playbooks carry repo-specific working instructions; reusable disciplines may instead live in a named sibling. If a required playbook is missing, stop and tell the user to run `backlog setup`; do not improvise.

**Nouns are roles.** The references speak in a fixed vocabulary — *issue*, *label*, *PR*, *branch*, *worktree*, *push* — but each is a role, not a platform feature. `docs/agents/platform.md` binds every role to this repo's real tracker, review surface, version control, and harness, with verified commands per verb. On GitHub the bindings match the words; on other platforms (a local on-disk tracker, GitLab, jj) the words stay and the mechanics change. A reference never assumes a platform beyond what the binding records.

## Commands

| Command | Role | Bundled reference | Project playbook |
|---|---|---|---|
| `groom` | With the human: classify work-type, clarify, resolve relationships, label readiness | `reference/groom.md` | `docs/agents/backlog-policy.md` + `platform.md` |
| `run` | Queue ready issues; staff each coordinator before creating its worktree/child | `reference/run.md`, `reference/run-state.md`, `reference/build-loop.md` | `docs/agents/backlog-policy.md` + `platform.md`; threads read `change-description.md` + their step playbooks |
| `setup` | Ask the work domain and install its baseline pack; reconcile playbooks; bind platforms; set isolation, app access, seed/checks, readiness; ensure siblings | `reference/setup.md`, `reference/worktree-isolation.md`, `templates/` | writes them |
| `diagnose` | Hand a bug to the `diagnosing-bugs` skill; retain issue lifecycle and downstream verify/evidence | `reference/diagnose.md` + sibling by name | optional `docs/agents/diagnosing-bugs.md` delta + `environment.md` |
| `prototype` | Throwaway code that answers a design question (logic or UI shape) | the `prototype` skill (composed by name) | — |
| `research` | Establish source-backed facts and inferences; standalone or as the research work-type branch | the `research` skill (composed by name) | `docs/agents/researching.md` |
| `implement` | Build the enhancement: just-in-time tactical plan, then test-first build | `reference/implement.md` | `docs/agents/implementing.md` + `environment.md` |
| `refactor` | Behavior-preserving change locked by tests | `reference/refactor.md` | `docs/agents/refactoring.md` |
| `verify` | Verdict loop: checks plus pass/fail against acceptance criteria | `reference/verify.md` | `docs/agents/verifying.md` + `environment.md` |
| `evidence` | Capture and present proof once review converges; fill the PR's evidence block | `reference/evidence.md` | `docs/agents/evidence.md` + `environment.md` + `platform.md` |
| `adversarial-review` | Reviewer ⇆ fixer subagents on a PR until LGTM or cap | `reference/adversarial-review.md` | `docs/agents/change-reviewer.md`, `docs/agents/change-fixer.md` + `environment.md` |

`docs/agents/environment.md` is the shared playbook (run/isolate/seed/auth + the parallelism verdict `run` reads); references that touch the app read it alongside their step playbook. `docs/agents/platform.md` is the other shared playbook — the platform bindings above. Five capabilities are **composed by plain name**, never imported: `diagnosing-bugs` owns the bug method; `research` source-backed investigation; `staffing` the roster/roles/fallback; `review-loop` presentation and review; `prototype` throwaway design questions.

## Dependency surface

Three kinds of dependency, per `AGENTS.md` § Conventions:

1. **Bundled references** — backlog's own dev contract under `reference/` plus the playbook baselines it ships under `templates/`: shared `templates/common/` plus per-domain packs `templates/<domain>/` (`software/` is the shipped default; the domain is chosen at setup). These ship with the skill and are not looked for in the target repo.
2. **Project playbooks** — `docs/agents/*.md`, installed into the target repo by `setup`. A repo changes how a step works by editing its playbooks, never the skill.
3. **Sibling skills** — the five named above, composed by plain name. `setup` ensures they are present; absent a sibling, backlog states the requirement rather than failing silently.

## Seams

Backlog is deliberately one thin skill with three named internal contracts — documented seams, not separate
skills:

- **groom = organize.** The tracker as truth: admission audit, route judgment, serialized writes. The only
  stage that stamps readiness.
- **run = schedule.** Dependency waves, parallelism, worktrees, dispatch, liveness — build-ignorant. **A
  queue of one is first-class** (`backlog run <issue>`).
- **build loop = one issue → reviewed PR.** The invariant dev tail (implement · verify · adversarial review ·
  evidence). Its *inputs* vary by entryway; the gates never do.

## Routing

1. **No argument** → follow `reference/groom.md`, then offer to run the resulting ready-for-agent issues via `reference/run.md`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that bundled reference and follow it. Everything after the command name is the target (an issue number/URL, PR, branch, or path). A first word of `prototype` or `research` delegates to that named sibling rather than a bundled reference; invoke `staffing` or `review-loop` directly for their own commands.
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed.
