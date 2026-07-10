**1. Checks + CI Gate**

`verifying.md` would record local checks only after setup has seen each invocation launch:

- Unit/targeted tests: `npm test` → confirms `package.json` `test` runs `jest`.
- Lint: `npm run lint` → confirms `eslint .` launches.
- Type check: `npm run typecheck` → confirms `tsc --noEmit` launches.
- Build: `npm run build` → confirms `next build` launches.
- Full / aggregate gate: none recorded unless the repo has a single aggregate script; this repo does not.

CI merge gate, recorded separately:

- Required GitHub Actions jobs from `.github/workflows/ci.yml`: `lint`, `typecheck`, `test`, `build`.
- Merge precondition: PR is not mergeable until all four required status checks are green.
- Divergence: same check families as local commands, but CI status is still a distinct merge gate.

**2. Drive-To-Feature Path**

`environment.md` would record:

- Seed regime: real seed command.
- Command: `npm run db:seed`, verified as launching `tsx scripts/seed.ts`.
- Drive-to-feature path beyond seed:
  - Start the Next.js app on its configured local URL, `http://localhost:3000`.
  - Log in with the configured email/password test account.
  - Navigate to `/dashboard/settings`.
  - Use that authenticated settings page as the baseline feature-exercising surface for verify/evidence.

**3. Shared-Singleton List + Verdict**

`environment.md` shared-singleton list:

| Singleton | Collision mode | Locally isolatable? |
|---|---|---|
| Docker container `myapp-db` | Fixed `container_name`; second worktree cannot create the same named container | Yes, by namespacing compose/container names per worktree |
| Host port `5432:5432` | Second DB stack fails to bind host port 5432 | Yes, by deriving per-worktree DB ports |
| Missing `COMPOSE_PROJECT_NAME` / compose namespace | Containers, volumes, networks are not namespaced per worktree | Yes, by setting per-worktree `COMPOSE_PROJECT_NAME` |
| `DATABASE_URL=postgres://localhost:5432/myapp` | Every worktree points at the same DB endpoint/data | Yes, by deriving per-worktree DB URL and DB name/port |
| Fixed test DB `myapp_test` | Concurrent tests truncate/reseed/read the same test database | Yes, by deriving per-worktree test DB name |
| Web app port `3000` | Second app process fails to bind, or tests hit the wrong app | Yes, by deriving per-worktree app ports |
| `node_modules` per worktree | Normal per-repo install is a filesystem singleton inside each worktree; concurrent installs/checks in the same worktree would collide, but separate worktrees do not share it | Yes, already isolated by worktree if not symlinked/hoisted/shared |
| `.next` build cache | Build/dev processes in the same worktree can interleave writes; separate worktrees have separate `.next` dirs | Yes, already isolated by worktree if not redirected to a shared cache |

Verdict:

- `serialize-verification`.
- Hard constraint, not preference.
- Reason: the team asked for parallel, but the DB container name, DB host port, compose namespace, hardcoded `DATABASE_URL`, fixed `myapp_test`, and app port `3000` are un-isolated. Parallel verification would contend for real shared resources and corrupt or misroute state.
- Serialized exception lane: not applicable beyond the hard serialization requirement until isolation is implemented.

**4. Label Mapping + Deps + Scale**

`backlog-policy.md` label roles:

- `bug` → existing Jira label `Type: Bug`.
- `enhancement` → existing Jira label `Type: Story`.
- `refactor` → existing Jira label `Type: Chore` as the closest existing maintenance/refactor work-type label.
- `blocked` → neutral unless separately chosen as a readiness/ownership role; Jira’s native blocker relation is authoritative for dependencies.
- `needs-triage` → neutral or pre-grooming marker, not `needs-info`.
- `P0`, `P1`, `P2` → neutral priority labels.
- `area/frontend`, `area/api` → neutral area labels.
- Workflow statuses → neutral/native Jira state, not duplicated as backlog labels.
- Readiness labels missing from existing taxonomy: setup would need to create or bind explicit Jira labels for `ready-for-agent`, `in-flight`, `ready-for-human`, and `needs-info` unless Jira statuses are deliberately bound instead.
- Exclusion labels `wontfix`, `duplicate`, `superseded`, `invalid`: not present in the listed labels, so setup would list them as roles to create or bind to existing Jira resolution/link/status conventions if available.
- Aliases: none from the given label set.

`platform.md` / dependency binding:

- Tracker binding: custom Jira.
- Dependency relation: Jira native issue link type `"is blocked by"`.
- Read blockers: Jira API/query that lists unresolved `"is blocked by"` links for the issue.
- Write blocker: Jira API call that creates an issue link using the `"is blocked by"` relation.
- If setup cannot reach Jira live, it records this as a prose contract flagged “verify against the live tracker at first use,” not as a fabricated verified command.
- No GitHub task-list fallback.

Groom scale behavior:

- Does not triage all ~300 open issues in one pass.
- Batches by Jira’s own signals: priority (`P0/P1/P2`), area (`area/frontend`, `area/api`), age, and recent activity.
- First pass targets the human-named near-term/high-priority slice.
- Long-tail issues remain listed but ungroomed for later.
- Dedupe collapses genuine duplicates to canonical issues without reopening settled team decisions or re-litigating already-prioritized/parked issues.

**Self-Assessment**

A1: Yes. Local checks are the package-script invocations setup must verify by launching; CI `lint/typecheck/test/build` is recorded separately as the merge precondition.

A2: Yes. Login with the email/password test account and navigation to `/dashboard/settings` is an explicit output beyond seed.

A3: Yes. The list includes `node_modules`, `.next`, `myapp_test`, container name, ports, compose namespace, and `DATABASE_URL`, each tagged for local isolation.

A4: Yes. The verdict is `serialize-verification` as a hard constraint because un-isolated DB/container/port/URL/test DB resources force serialization despite the team’s parallel preference.

A5: Yes. Existing labels are reused: `Type: Bug`→bug, `Type: Story`→enhancement, `Type: Chore`→refactor; priorities and areas stay neutral; no duplicate labels are minted.

A6: Yes. Dependencies bind to Jira’s native `"is blocked by"` issue link, not GitHub task lists.

A7: Yes. Groom batches the ~300 issues and dedupes without reopening settled decisions.

VERDICT: Yes, a real setup run would produce usable, reality-bound artifacts. Ambiguities: the exact package manager command cannot be known from the scenario alone, so `npm` here stands in for the repo’s verified runner; Jira readiness/exclusion roles may need either new labels or an explicit decision to bind them to Jira statuses/resolutions.