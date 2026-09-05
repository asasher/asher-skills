# Changelog

Newest first. Each entry names the changed skills and what a reconcile must do.

## 2026-09-05 — delivery converges on one revision and resumes from durable state

Delivery opens a PR after implementation and combines behavioral verification with read-only review before one fixer acts. Fixes invalidate both verdicts. The run preserves its pass budget, deadline, and explicit stop outcome across resumption; completion checks review, verification, evidence, and CI against the current revision.

- `deliver`, `adversarial-review`, `code-review`, `verify-your-work`, `prove-your-work` (changed): combined convergence, revision-specific reports and checkpoints, risk-scaled verification and review contexts, optional suggestions that do not block, and reuse of matching evidence with reproducible dropped scripts.
- `backlog`, `to-slices` (changed): one canonical issue per shaping subject; build capacity counts live workers and unresolved reservations; failed spawns recover without discarding work. Splits persist their issue mapping and finish wiring and readback before publishing readiness.
- `shape`, `to-spec` (changed): preserve risk and required failure-path checks in the settled spec; dispatch synthesis from the persisted record; allow precise independent research questions early and preserve runtime-real prototype formats.
- `implement` (changed): declare `domain-modeling`, scale checks to actual effects, and return the implementation context needed by a fixer.
- `to-subagent`, `staffing` (changed): carry execution permissions and deadlines, confirm cancellation before allowing another writer, resume compatible fix workers, and staff behavioral verification independently from the builder.
- `merge` (changed): check head and base freshness immediately before each merge, require current verification and evidence, watch required CI, and use `--match-head-commit`. Confirm actual merge before cleanup and close issues explicitly when the configured base is not the default branch.

Reconcile: refresh these skills together. Run `backlog setup` to reconcile the initial PR state, concurrent-build limit, admission mechanism, and the expanded `shaping` label description. Existing runs recover from their issue and PR records; missing revision-specific proof is pending work, and existing stop conditions remain stops. No skills were added or removed; the README install set is unchanged.

## 2026-09-03 — diagram-design ships a dark default skin

The shipped visual system in `diagram-design` is now dark by default, with every value read off Vercel's Geist color scales: near-black paper, a gray-100 raised surface for nodes and cards, gray-alpha hairlines, gray-900/1000 text, the blue-900 text step as the one accent, and blue-700 for link arrows. The series and override palettes use the Geist 900 steps per hue with light-mode counterparts. Light is the alternate variant. Project `DESIGN.md` resolution and the resolution order are unchanged.

- `diagram-design` (changed): `references/style-guide.md` defines the dark column as the default and the light column as the variant; every type reference, primitive, and template carries the new hex values, and the "Dark mode" sections became "Light mode" sections. `assets/template-dark.html` is renamed `assets/template-light.html`; the slug suffix for the variant is `-light`. The semantic override palette lists the dark-legible hexes and light mode darkens them (`C_dark`), reversing the old `C_light` rule. The pre-baked `assets/example-*.html` files keep the upstream skin and are documented as layout references only.
- Reconcile: a diagram generated under the old skin re-renders with the new tokens; nothing else in the family reads these values.

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
