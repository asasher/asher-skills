# Changelog

Newest first. Each entry names the changed skills and what a reconcile must do.

## 2026-09-03 — the lifecycle restructured around GitHub, one playbook, and verb skills

The platform is fixed: GitHub issues and PRs via `gh`, git, an S3-compatible bucket. Role nouns and the platform, policy, evidence, change-description, and codebase playbooks are gone; the family reads one playbook, `docs/agents/environment.md`, and `retro` keeps its own.

- `backlog` (changed): verbs are `capture`, `groom`, `build`, `retro`, `status`, `setup`. Each sweeps, confirms, and fans one run of a verb skill per unit. Labels, claims, deadlines, and branch names are fixed in its `reference/labels.md`; `setup` writes `environment.md`, certifies against `agent-ready-codebase`, and creates the labels. Dispatch metadata, the local file tracker, and the `delivered`, `refactor`, `research`, and `draft` labels are dropped.
- `capture` (renamed from `to-backlog`), `deliver` (renamed from `build-change`), `merge` (renamed from `merge-change`, `watch-until` folded in). `retro` (new to the family, from in-progress).
- `shape` (changed): every artifact commits to one `artifact/<issue>` branch; at the close it runs `to-slices` when the approved spec's split is accepted, and marks the issue ready.
- `to-slices` (changed): children publish as `ready-for-agent` sub-issues, the parent is wired `blocked_by` each child and relabeled `spec`; stacked landing on the spec branch only.
- `deliver` (changed): four issue kinds (unshaped, shaped, child, spec issue); the spec issue's coverage check and promotion PR; the PR body outline inline; the stage ledger dropped.
- `merge` (changed): closes a child issue when its PR merges into the spec branch, deletes the closed issue's artifact branch, watches checks at their cadence.
- `verify-your-work`, `prove-your-work` (changed): guards versus throwaway verification scripts; the seed claim; evidence format and embed check inline; the package posts on the PR.
- `code-review`, `implement`, `tdd`, `worktree`, `to-web`, `to-branch`, `interview`, `adversarial-review`, `technical-writing`, `to-thread` (changed): vocabulary and playbook references only; `to-branch` gains its sidecar.
- Out of the install: `skill-loop` (authoring tooling, stays in `system`), `to-tailnet` (moved to `personal`). Removed: `watch-until`.

Reconcile: remove the mounts of `to-backlog`, `build-change`, `merge-change`, `watch-until`, and `to-tailnet`; re-run `npx skills add github:asasher/asher-skills --skill backlog capture deliver merge retro shape to-slices verify-your-work prove-your-work code-review implement tdd worktree to-web to-branch interview adversarial-review technical-writing to-thread agent-ready-codebase` (trimmed to your installed set, plus the new names). Then run `backlog setup`: fold the facts from `platform.md`, `backlog-policy.md`, `change-description.md`, `evidence.md`, and `codebase.md` into `environment.md` and delete those five files; let the label reconcile drop `delivered`, `refactor`, `research`, and `draft`. Open issues carrying a dropped work-type get `enhancement`; `delivered` children close with a comment naming their merge. Run `retro setup` once.

## 2026-09-01 — writing standard split by register

The writing-for-humans standard split into three skills:

- `unslop` (new): the AI-tell scan for any user-facing writing.
- `writing-for-humans` (changed): now conversation only — replies, questions, plans discussed in chat. Requires `unslop`.
- `technical-writing` (new): specs, tickets, change requests, reports, and documentation. Requires `unslop`.

Sibling skills re-routed to the right register (changed: `research`, `prototype`, `to-spec`, `to-slices`, `build-change`, `prove-your-work`, `verify-your-work`, `shape`, `backlog`).

Reconcile: re-run `npx skills add github:asasher/asher-skills --skill unslop writing-for-humans technical-writing research prototype to-spec to-slices build-change prove-your-work verify-your-work shape backlog` (trimmed to your installed set, plus the two new writing skills). No setups to run.
