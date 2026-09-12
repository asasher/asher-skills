# Changelog

Newest first. Each entry names the changed skills and what a reconcile must do.

## 2026-09-13 — simplify instructions and retire Relay

- `backlog`: trim the environment template to project facts and demonstrated capability results; simplify certification instructions.
- `to-thread`: shorten the T3 reference while retaining launch verification, provider traps, and recovery. The helper stays.
- `diagram-design`: shorten the discovery description and replace the routine planning pause with reasonable defaults and material clarifications.
- `verify-your-work`, `agent-ready-codebase`, `prove-your-work`, `to-spec`, `staffing`: default UI checks to headless Playwright. Alternatives must demonstrate isolated control and capture on the execution host. Concurrent runs use separate browser sessions, auth state, fixtures, and output paths. A headed fallback needs an isolated display or explicit approval to use the user's session. Temporary scripts are conditional; reproducible actions and evidence remain required.
- `writing-for-humans`: quote the description so its colon parses as YAML text; wording and invocation are unchanged.
- Retire `relay`: remove its entire package and catalog entry. Historical source and authoring records remain in Git.

Reconcile: refresh these skills in the installed set and remove Relay mounts. Reconcile existing environment playbooks to project facts, preserving operational knowledge; demonstrate browser isolation before certifying UI work. Staffing now declares `verify-your-work`, already in the unchanged 36-skill family install set. Preserve consumer-owned Relay records for deliberate cleanup. No behavioral skill evals were added.

## 2026-09-12 — label setup from a table

`backlog`: replace the 102-line label reconciler with nine rows in `reference/labels.md`. Setup compares repository labels, presents changes, applies the approved plan, and reads back the result. Label names, colors, and workflow meanings remain; descriptions are shorter.

Reconcile: refresh backlog and remove its retired `scripts/reconcile-labels.py`. No live tracker changes are part of this authoring change. `diagram-design` also drops a stale checker docstring pointing to unshipped repository tools. The family review lists 381 package files and distinguishes further simplification recommendations from applied changes.

## 2026-09-10 — mobile review reader

Authoring tooling: `bun review:serve` serves the family guide and renders linked Markdown at its original path. The reader preserves relative links and heading anchors, links named skills in the presentation, and provides previous/next navigation, metadata disclosure, and raw source. It binds to loopback for sharing through Tailscale Serve.

`diagram-design`: correct the internal quadrant-variant heading link. Reconcile this skill for that link fix; the reader and its development dependencies stay in the authoring repo. Validation covered the mobile reading journey, all 382 indexed package files, 2,021 local links and anchors, raw-source fidelity, and access from another tailnet machine.

## 2026-09-10 — respect skill package boundaries

Removed five cross-skill file links from `capture` and `to-slices`. Their steps now carry the required publication outcomes without reaching into backlog's internal files. Native blockers, milestone inheritance, conflict approval, and migration readback remain explicit.

Reconcile: refresh `capture` and `to-slices`. No setup or dependency changes. The audit covered all 47 authored skill packages; internal package references, named sibling composition, and provenance citations remain. Authoring rules and review documents now make this boundary explicit.

## 2026-09-10 — group testing batches with milestones

`capture` groups requested batches in GitHub milestones, keeping one ticket per finding. Spec parents remain the integration mechanism for approved implementation splits. `backlog groom` preserves batch membership through consolidation and proposes completed milestone closures; `status` reports progress and closure candidates. `to-slices` inherits and reads back milestone assignments.

The shared milestone contract covers conflicting assignments, cross-batch duplicates, and deliberate migration from organizational parent issues. Milestone membership supplies neither readiness nor branching dependencies.

Reconcile: refresh `capture`, `backlog`, and `to-slices`. Existing organizational parents migrate only when selected by the user; preserve their context and real dependencies. No labels, setup, or install-set changes are required. The family guide and manual review order now include testing batches. Validation is structural and editorial; no behavioral evals were added.

## 2026-09-06 — retro proposes project issues from recent sessions

`retro` now reviews a bounded batch of local build and shaping transcripts, compares findings with open and closed project issues, and offers issue or comment drafts for user selection. Every tracker write follows that selection. Accepted findings stay in the current project; upstream escalation belongs to whoever resolves them.

The first sweep covers the latest three completed sessions; subsequent batches resume from an ignored `.retro/checkpoint.json` in the primary checkout. Worktrees share the checkpoint; machines keep separate copies. Dismissed findings count as reviewed. Pending discussion, failed writes, and unread sessions keep their coverage pending.

Reconcile: refresh `retro` and `backlog`, include `capture` with retro, and retire the old retro setup from installation instructions. The ledger, playbook, denylists, note verb, upstream workflow, scrub helper, and its obsolete dry-run are removed from the skill. Preserve existing consumer records for deliberate cleanup; the new workflow initializes on first use. Update family documentation. No new behavioral evals were added.

## 2026-09-06 — outcome instructions, new staffing, and CLIProxyAPI images

- `staffing`: use GPT-6 Astra for planning, orchestration, implementation, research synthesis, and independent verification; Claude Fable 5.1 for taste and frontend work; Terra for bounded collection and browser capture. Fresh context establishes review independence. Retire Fable 5 and the Sol/Opus default assignments.
- `codex-imagegen`: implement issue #208 with configured CLIProxyAPI → native Codex → explicitly authorized direct OpenAI API. Shared routing covers flat, batch, layered, and generated spritesheet modes. Preserve actual dimensions, immutable outputs, and partial evidence. Bind inferred credentials to their endpoint and remove the external system-skill dependency.
- Replace routine command recipes with outcomes in `backlog`, `capture`, `code-review`, `merge`, `prove-your-work`, `retro`, `tdd`, `to-branch`, `to-slices`, `to-thread`, `skill-loop`, `diagram-design`, `maquette`, `shadixfy`, `watch-video`, `bayes`, `constraints`, `dissolve`, `learn-anything`, `relay`, and `to-tailnet`. Preserve exact helper interfaces and operational invariants. Diagram checks now use shipped helpers and available browser tooling; label appearance lives in the reconciler.

Reconcile: refresh these skills in your installed set and include `codex-imagegen` wherever `staffing` is installed. The README install set now contains 36 family/support skills. Existing playbooks remain valid; newly authored playbooks link canonical project commands and record additional invocation requirements. Review the updated family guide and manual review order.

Validation: 22 local image-backend tests pass; a visually inspected live proxy smoke preserved and reported its 1254 × 1254 result against a 1024 × 1024 request. Structural, formatting, and rendered-guide checks pass. No new behavioral skill evals were added.

## 2026-09-06 — remove redundant negations from skill instructions

Reviewed all 47 authored skills, removing speculative prohibitions, repeated exclusions, and instructions already expressed by adjacent positive requirements. Concrete approval, evidence, privacy, and recovery contracts remain. Supporting references and templates use the same wording discipline.

Changed: `adversarial-review`, `agent-ready-codebase`, `backlog`, `bare-minimum-design`, `bayes`, `capture`, `code-review`, `codex-imagegen`, `constraints`, `deliver`, `diagnosing-bugs`, `diagram-design`, `dissolve`, `domain-modeling`, `goodwork`, `handoff`, `implement`, `interview`, `learn-anything`, `maquette`, `merge`, `principle-experience-first`, `prototype`, `prove-your-work`, `relay`, `research`, `retro`, `shadixfy`, `shape`, `skill-loop`, `staffing`, `tdd`, `technical-writing`, `to-branch`, `to-slices`, `to-spec`, `to-subagent`, `to-tailnet`, `to-thread`, `to-web`, `unslop`, `verify-your-work`, `watch-video`.

Reconcile: refresh the changed skills in your installed set. Invocation policies, dependency declarations, and the README install set are unchanged. Existing playbooks remain valid. The instruction-review document records this editorial pass, a separate command-recipe audit, and a staffing proposal; the latter two are not implemented in this entry. No behavioral evals were added.

## 2026-09-05 — ticket-based shaping and a simpler build owner

Groom reads all open tickets before consolidation and routing. Shape works on one ticket and records an **approved spec**. Shaping and builds preserve the primary checkout, attach existing local or remote branches in secondary worktrees, and push coherent progress for recovery on another machine.

- Rewritten: `backlog`, `shape`, `deliver`, `implement`, `adversarial-review`, `agent-ready-codebase`, `merge`, `retro`, `capture`, `to-slices`, `verify-your-work`, `prove-your-work`, `to-web`, and `to-thread`.
- Supporting contracts aligned: `code-review`, `to-spec`, `to-branch`, `to-subagent`, and `staffing`. Routine stages run inline with the owner; code review is independent, and high-risk work gets independent behavioral verification. Ordinary PRs open after implementation checks, never as drafts. `merge review` shortlists open PRs without merging.
- Removed: `worktree`. Native Git preparation lives in `to-thread`; merge owns safe cleanup. Published HTML and evidence remain after temporary branches are deleted. `to-web` and a demonstrated artifact bucket are required; evidence media never enters Git.
- Added human documentation: the visual family guide and ordered source review. Skill evals have not been added or run for this rewrite.

Reconcile: refresh the lifecycle family and its supporting skills together using the current README install command. Remove the installed `worktree` mount and harness links; preserve actual working copies and branches. Re-run `backlog setup` to certify artifact uploads and reconcile ordinary PR creation, branch recovery, and worktree conventions. Existing approved specs keep their recorded revisions; only a newer spec needs new approval. Preserve ongoing claims and review budgets.

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
