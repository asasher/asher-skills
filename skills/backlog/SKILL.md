---
name: backlog
description: Groom the backlog; run ready-for-agent issues through the issue loop to reviewed changes; subcommands run standalone. Works against GitHub, a local on-disk tracker, or any bound platform.
argument-hint: "[command] [issue, PR, or target]"
user-invocable: true
disable-model-invocation: true
---

# Backlog

This file is the command surface; each subcommand loads its own contract from `reference/` only when it runs.

## References

`reference/` and `templates/` are bundled with this skill; `docs/agents/` is the target repo's playbook, created by `backlog setup`. A subcommand's bundled reference is the **orchestration contract** — target, gates, staffing, handoffs. Its playbook carries the **working instructions** — the technique (shipped inlined via the template baseline) plus this repo's conventions — so a repo changes how a step works by editing its playbooks, never the skill. If a required playbook is missing, stop and tell the user to run `backlog setup`; do not improvise or substitute bundled files.

**Nouns are roles.** The references speak in a fixed vocabulary — *issue*, *label*, *PR*, *branch*, *worktree*, *push* — but each is a role, not a platform feature. `docs/agents/platform.md` binds every role to this repo's real tracker, review surface, version control, and harness, with verified commands per verb. On GitHub the bindings match the words; on other platforms (a local on-disk tracker, GitLab, jj) the words stay and the mechanics change. A reference never assumes a platform beyond what the binding records.

## Commands

| Command | Role | Bundled reference | Project playbook |
|---|---|---|---|
| `groom` | With the human: classify work-type, clarify, resolve relationships, label readiness | `reference/groom.md` | `docs/agents/backlog-policy.md` + `platform.md` |
| `run` | Queue ready-for-agent, unblocked issues; dispatch one issue thread each | `reference/run.md`, `reference/issue-loop.md` | `docs/agents/backlog-policy.md` + `platform.md`; threads read `pr.md` + their step playbooks |
| `setup` | Scaffold or reconcile playbooks; bind the platforms; set isolation, app access, seed/checks, readiness; ensure the siblings | `reference/setup.md`, `reference/worktree-isolation.md`, `reference/migrations.md`, `templates/` | writes them |
| `diagnose` | Bug: reproduce, fix, confirm the failing path passes | `reference/diagnose.md` | `docs/agents/diagnosing-bugs.md` + `environment.md` |
| `plan` | Enhancement: plan or skip; HTML plan, approval gate (backlog keeps the commit-and-implement dev-tail) | the `plan` skill (composed by name) | — |
| `prototype` | Throwaway code that answers a design question (logic or UI shape) | the `prototype` skill (composed by name) | — |
| `implement` | Build an approved plan | `reference/implement.md` | `docs/agents/implementing.md` + `environment.md` |
| `refactor` | Behavior-preserving change locked by tests | `reference/refactor.md` | `docs/agents/refactoring.md` |
| `verify` | Verdict loop: checks plus pass/fail against acceptance criteria | `reference/verify.md` | `docs/agents/verifying.md` + `environment.md` |
| `evidence` | Capture and present proof once review converges; fill the PR's evidence block | `reference/evidence.md` | `docs/agents/evidence.md` + `environment.md` + `platform.md` |
| `adversarial-review` | Reviewer ⇆ fixer subagents on a PR until LGTM or cap | `reference/adversarial-review.md` | `docs/agents/change-reviewer.md`, `docs/agents/change-fixer.md` + `environment.md` |

`docs/agents/environment.md` is the shared playbook (run/isolate/seed/auth + the parallelism verdict `run` reads); references that touch the app read it alongside their step playbook. `docs/agents/platform.md` is the other shared playbook — the platform bindings above; references that touch the tracker, open or edit a PR, or create worktrees read it. Four capabilities are **composed by plain name from sibling skills**, never imported: `staffing` owns the roster/roles/fallback (the **orchestrator**/**builder**/**checker**/**floor** vocabulary; its roster resolves in `environment.md` § Model staffing); `review-loop` owns the presentation surface and interactive review (its config in `environment.md` § Presenting); `plan` owns planning and the approval gate; `prototype` owns throwaway design questions.

## Dependency surface

Three kinds of dependency, per `AGENTS.md` § Conventions:

1. **Bundled references** — backlog's own dev contract under `reference/` plus the dev playbooks it ships under `templates/`. These ship with the skill and are not looked for in the target repo.
2. **Project playbooks** — `docs/agents/*.md`, installed into the target repo by `setup`. A repo changes how a step works by editing its playbooks, never the skill.
3. **Sibling skills** — `staffing`, `review-loop`, `plan`, `prototype`, composed by plain name (never imported; what each owns is under the command table). `setup` ensures they are present; absent a sibling, backlog states the requirement rather than failing silently.

## Routing

1. **No argument** → follow `reference/groom.md`, then offer to run the resulting ready-for-agent issues via `reference/run.md`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that bundled reference and follow it. Everything after the command name is the target (an issue number/URL, PR, branch, or path). A first word of `plan` or `prototype` (and any staffing or presentation concern) delegates to the named sibling skill rather than a bundled reference.
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed.
