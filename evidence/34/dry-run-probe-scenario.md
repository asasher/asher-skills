# Dry-run probe: does hardened `backlog setup` bind to a real inherited repo?

You are acting as the reasoning of the `backlog` skill's **setup** audit. Read the ACTUAL hardened
reference and template files in this worktree, then apply them to the synthetic inherited-repo scenario
below and produce exactly what setup would record. This is a dry run — do not run any commands, do not edit
anything; reason from the files and the scenario.

## Files to read first (in this worktree)
- `skills/backlog/reference/setup.md` (steps 3, 4, 5, 6, 9)
- `skills/backlog/reference/worktree-isolation.md` (audit probes + shared-singleton list + verdict)
- `skills/backlog/reference/groom.md` (steps 1, 4 — scale)
- `skills/backlog/templates/environment.md`, `verifying.md`, `evidence.md`, `platform.md`, `pr.md`,
  `backlog-policy.md`

## The synthetic inherited repo (what the audit is pointed at)
A mature Next.js + TypeScript app, adopted by a new team.
- `package.json` scripts: `"test": "jest"`, `"lint": "eslint ."`, `"typecheck": "tsc --noEmit"`,
  `"build": "next build"`, `"db:seed": "tsx scripts/seed.ts"`. No `Makefile`.
- `.github/workflows/ci.yml` runs, as required status checks on the default branch: `lint`, `typecheck`,
  `test`, `build`. Merges are blocked until these pass.
- `docker-compose.yml`: one service `db` with `container_name: myapp-db`, ports `5432:5432`, and the app
  reads a single hardcoded `DATABASE_URL=postgres://localhost:5432/myapp`. Tests run against a fixed
  `myapp_test` database. No `COMPOSE_PROJECT_NAME`. `node_modules` is a normal per-repo install; `.next` is
  the build cache. The web app runs on a fixed port 3000.
- Feature to exercise a change: the app requires logging in (email + password test account) and navigating
  to `/dashboard/settings` to reach the surface most issues touch.
- Tracker: **Jira** (not GitHub). Labels in use: `Type: Bug`, `Type: Story`, `Type: Chore`, `P0`, `P1`,
  `P2`, `area/frontend`, `area/api`, `needs-triage`, `blocked`, plus workflow statuses. Jira has a native
  **"is blocked by"** issue link type. There are ~300 open issues, most untouched for months.
- The team wants issue work to run **in parallel** across worktrees.

## Produce these four artifacts, then self-assess
1. **Checks + CI gate** (setup step 5 → `verifying.md`): which check commands setup records and how it
   confirms each; and the CI merge-gate it records as a separate merge precondition.
2. **Drive-to-feature path** (step 6 → `environment.md`): what setup records beyond seed to reach a
   feature-exercising state.
3. **Shared-singleton list + verdict** (step 4 + worktree-isolation → `environment.md`): the enumerated
   singleton list (resource · collision mode · locally-isolatable?) and the resulting parallelism verdict —
   given the team asked for parallel. State whether the verdict is a preference or a hard constraint and why.
4. **Label mapping + deps + scale** (step 3 + groom → `backlog-policy.md`/`platform.md`): the role→label
   mapping (which Jira labels map to which roles, which stay neutral, any aliases), how the non-GitHub
   dependency relation binds, and how groom handles ~300 issues.

## Self-assessment (answer each yes/no + one line)
- A1: Are the recorded checks the ones setup *verified by running*, and is the CI gate (`lint/typecheck/test/build`) recorded as a merge precondition distinct from local checks?
- A2: Is the drive-to-feature path (login + navigate to `/dashboard/settings`) recorded as an explicit output beyond seed?
- A3: Does the singleton list include the local-filesystem singletons (`node_modules`, `.next`, `myapp_test` DB) as well as the container/port/DATABASE_URL ones? Is each tagged isolatable?
- A4: Given the team asked for parallel but nothing is isolated, is the verdict `serialize-verification` as a HARD constraint naming the forcing singletons — not honored as a preference?
- A5: Does the label mapping map `Type: Bug`→bug, `Type: Story`→enhancement, `Type: Chore`→refactor (or reasoned alias), leave `P0/P1/P2` and `area/*` neutral, and reuse existing labels rather than minting duplicates?
- A6: Does the dependency binding use Jira's native "is blocked by" relation (not the GitHub task-list fallback)?
- A7: Does groom batch the ~300 issues rather than triage all at once, and dedupe without re-litigating settled ones?
- VERDICT: Would a real setup run against this repo produce usable, reality-bound artifacts? Name any place the hardened files are ambiguous, self-contradictory, or point at a slot that does not exist.
