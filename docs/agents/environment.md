# Playbook: Environment

> Project playbook for this repo. Shared — read by any stage that builds a branch, runs, or tests the app (`implement`, `verify-your-work`, `prove-your-work`, `diagnosing-bugs`, the change-request step, the `adversarial-review` fixer) and by `backlog build` for the parallelism verdict. Tailor every section to this codebase. `backlog setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: **main** — create work branches (and any worktrees) from it, and target PRs at it. Sync it per `platform.md` § Version control before branching.
- Branch naming: `<issue-number>-<slug>` (e.g. `6-slim-backlog-composer`).
- What a PR produces: nothing automated — no CI, no preview deploy. Review is human + `adversarial-review`.
- What a merge produces: nothing automated. Skills are consumed elsewhere via `npx skills add <repo-url> --skill <name>`; a merge just updates `main`. No deploy step, no promotion path.
- Deploy-target constraints: **n/a** — skills are consumed via `npx skills add`; there is no deploy target.
- Credential preflight (run before work that will hit either gate): `gh auth status` proves the tracker/PR credential is live; a cheap `codex exec -s read-only --skip-git-repo-check "reply OK"` proves the second-executor route. This is what `backlog build`'s per-run preflight uses.

## Running locally

> This is a **skills repository**, not a running product. "The app" is the skills themselves; there is no dev stack, no services, no ports.

- Start the full dev stack: **n/a** — nothing to boot.
- To exercise a skill (the equivalent of "running the app"): invoke it in a harness against a scenario. From Claude Code, the `Skill` tool or a subagent that reads the skill's `SKILL.md`; from Codex, per the skill's `agents/openai.yaml`. A "run" is a probe scenario driven through an executor model — see § Driving behavior.
- Scripts the skills ship (e.g. `scripts/review-server.py`) are stdlib-only Python 3 — run directly with `python3`, no install.
- Services / ports / URLs: **none** — the loop stands up no servers (the retired review surface's residual port note lives in § Presenting), only whatever transient port a probe or driven script briefly binds.
- Headless contract: **no dev stack — nothing to detach.** The loop runs no long-lived processes; a script driven for verification stops with its check. (Retired-surface leftovers, if any turn up, are reaped per § Presenting.)

## Worktree isolation

> Set by `setup`'s isolation audit; fan-out mechanics recorded 2026-07-26 (asher-skills#116).

- Regime: **local-isolatable** — skills are files + stdlib-Python scripts with no shared runtime state, so a `git worktree` is a complete isolated copy. No derived env, no ports to remap.
- How to bring up an **isolated** stack for one worktree: worktree creation goes through the **harness's native isolation mechanism** (from Claude Code, the Agent tool with `isolation: "worktree"`, or `EnterWorktree`) — never hand-rolled `git worktree add` in loop dispatch; there is nothing else to stand up. Manual, out-of-loop work may still use `git worktree add <path> -b <branch> main` directly.
- **Enumeration**: the lifecycle discovers live worktrees via `git worktree list` plus branch/change-request state — never a directory scan — so harness-placed trees cannot become an invisible accumulation surface.
- **Teardown**: nothing to tear down beyond removing the worktree — no derived env, ports, or services to reap. `git worktree remove <path>` (plus `git worktree prune` for stale registrations) completes it. The skill-common teardown lifecycle — abort path, sweep, ownership per path — is asher-skills#83's deliverable.
- **Shared-singleton list** — there is no code-level shared runtime (no DB, no ports, no shared build cache; each skill is files + stdlib scripts), so the code isolates completely. The only remaining singleton is loop infrastructure, handled without serializing code work:

  | Singleton | Collision mode | Locally isolatable? |
  |-----------|----------------|---------------------|
  | GitHub tracker | one issue graph | no — but serialized main-branch writes handle it |

  (There is no review-surface singleton: review is tracker-native, on each change request — per-ticket by construction, so concurrent reviews share nothing. The tailnet surface that once held this role is retired; § Presenting, asher-skills#116.)

  The tracker does not collide with worktrees editing skill files, so it does not force serialized *verification* of the code.

  One row is standing in every multi-worktree repo: the parent `.git` itself. Concurrent git operations from parallel worktrees can collide on its locks (`index.lock`, ref locks) — a lock error is contention, so wait and retry briefly; a lock that outlives the retry with no live git process behind it is a crashed operation's leftover, and only then safe to remove.

## Seed data

- Seed regime: **none — drive the skill.** There is no data store to seed.
- Command (if any): n/a.
- **Drive-to-feature path:** the "state" a skill needs is a **probe scenario** — a situated dry-run prompt plus an answer key, per `docs/agents/probe-evals.md`. A skill's own `evals/` directory holds its scenarios; verification drives those scenarios through an executor model (§ Driving behavior) rather than seeding a database and navigating a UI. This is the **primary** proof for skill behavior, not a substitute for one — the runtime surface of a skill genuinely is an executor harness loading it and responding to a probe, so a graded transcript is the direct observation, not a stand-in for a screenshot nobody could have taken.

## Authenticating for testing

- Auth model: **none for exercising skills** — running a skill against a scenario needs no login. Two credentials support the loop's infrastructure, both already provisioned on this machine:
  - GitHub tracker/PRs: `gh` CLI, authed as `asasher` (keyring). Mints nothing per-run.
  - Codex executor (gpt-5.6-sol / gpt-5.6-terra): the Codex CLI, authed to its own subscription (`codex --version` → 0.144.1). Billed separately from the session.
- How an agent mints a session: n/a — no app session to mint.
- Test accounts / where credentials live: `gh` keyring and `~/.codex/`; never hardcode, never echo them.

## Verification data

- Standing accounts/tenants and permissions: local filesystem fixtures plus the authenticated GitHub repo
  with issue/PR read-write access; no product test tenant or second application user is required here.
- Per-issue fixture naming: `VERIFY-<issue>-<purpose>` under a temporary directory or the owning
  `<skill>-workspace/`; never share a mutable fixture across issue runs.
- Scale: use generated temporary skill trees for catalog/closure tests and temporary state/surface roots for
  review lifecycle tests.
- Approved synthetic substitutes: situated prompt fixtures may exercise skill decisions because this repo has
  no product runtime; they do not substitute for live GitHub API behavior or script lifecycle/process checks.
- Lifetime/cleanup: the owning test retains fixtures through its final assertion/evidence capture, then
  removes only its own temporary root.
- **Per-ticket-disposable stores** — what a single ticket may reset or wipe wholesale: the ticket's own
  worktree, and its `VERIFY-<issue>-*` fixtures and temporary roots. (A leftover
  `~/.backlog/surface/asher-skills/<issue>/` entry from the retired review surface is also the ticket's to
  remove.) Everything else is shared, and destructive verbs stop at this line.

## Driving behavior & capturing evidence

> Set by `backlog setup`'s access audit; read by `verify-your-work` (to exercise the skill) and `prove-your-work` (to capture proof). One entry per surface the loop verifies. Renamed from "Driving the app" 2026-07-27 with the switch to the `skill-authoring` pack (`backlog-policy.md` § Work domain) — there is no app here, and the old name made the honest answer read like a gap.

- Form factor(s): **skill** — a Claude Code / Codex skill (SKILL.md + references/scripts). Not CLI/web/mobile/desktop. The thing under test is a prompt-driven procedure, so "driving the app" means running the skill against a scenario and judging the transcript.
- Web driver: the v2 **Playwright-driving-Chrome** default is **n/a here** — there is no browser-driven app surface; probe executors are the drivers. The rule stays visible for the one browser-shaped case this repo has: judging **rendered HTML artifacts** (plans, prototypes, maquettes) covers happy/empty/error states in both color schemes, with screenshots as evidence; harness-native browser tools and `agent-browser` remain non-verification routes.
- Driver per surface:
  - **In-session executor (Claude):** spawn a subagent (Agent tool, `subagent_type: claude` or `general-purpose`) that reads the target skill's `SKILL.md` and works a probe scenario. This is the primary driver — Opus/Fable in-session.
  - **Independent executor (gpt-5.6-sol):** `codex exec -s read-only --skip-git-repo-check` (or `-s workspace-write` when the run must edit) with a self-contained prompt that points at the skill and scenario. A second, differently-modeled executor per `docs/agents/probe-evals.md`.
  - Any stdlib script a skill ships (e.g. `review-server.py`) is driven directly with `python3`.
- Independent runtime verification: delegate a scenario to `codex exec` for a second executor outside the orchestrator's context (dispatch mechanics in the `staffing` skill's compiled harness-mechanics reference; the roster and this machine's verified routes in `staffing.md`). Reading skill files, grading transcripts against an answer key, and running a skill's `scripts/` stay local.
- Evidence capture per surface: the **eval transcript** (the executor's run) plus a **pass/fail verdict table** mapping each probe to its answer-key criterion. For a skill that produces a visual artifact (e.g. `maquette`, a rendered plan), also a screenshot of the rendered HTML. Terminal transcripts for script behavior.
- Supporting tools: `docs/agents/probe-evals.md` (the eval harness) and the skill's own `evals/` dir; an artifact a human should eyeball rides the change request (committed and screenshotted per `evidence.md`) or is opened locally (§ Presenting).
- Gaps: no automated CI — every check is agent-driven on demand. A skill whose value is subjective (taste of copy, feel of a flow) can't be fully graded mechanically; the fallback is a human review pass on the change request.

## Presenting to the human

> **The tailnet HTML review surface is retired** (Asher, 2026-07-26, asher-skills#116). Review is
> **tracker-native**: each build's review happens on its own change request — the PR thread bound in
> `platform.md` § Change review — which is per-ticket by construction, so concurrent reviews need no shared
> surface, no cap, and nothing to keep alive. Spec sign-off lives on the ticket; prototype feedback arrives
> in chat. Do not publish reviews to the tailnet, stand up review servers, or proxy review ports for the loop.

- Artifacts that genuinely need rendering (a plan or prototype HTML a human should eyeball) are a separate
  concern with **no standing surface bound here**: open them locally with `open <file>`, or commit and
  screenshot them onto the change request per `evidence.md`. The `serve-via-tailnet` skill remains installed
  and may be invoked explicitly on demand, but it is not the review path and has no standing config in this
  playbook.
- Residual machine facts from the retired surface: the LaunchAgent `com.asher.backlog-surface` still serves
  `~/.backlog/surface` on port 8377 locally (the port remains taken); any leftover `tailscale serve` handler
  under `/asher-skills/...` is an orphan — `tailscale serve status` lists live handlers, and
  `tailscale serve --set-path <path> off` reaps one.
- Keep-awake: **none** (setup choice, reconfirmed at retirement) — harnesses hold sleep assertions during
  active runs, and with review on the tracker the loop leaves nothing AFK depending on this machine being
  awake. The one exception is an explicitly-invoked `serve-via-tailnet` session, which serves from this
  machine — an AFK review over it may find the machine asleep; revisit if that bites.

## Model staffing

Read `staffing.md` — the sole authority for this repo's roster, carrying the model rows, per-harness
eligibility and capability bindings, pins, floor, succession, and the probed reachability rows with the
machine and CLI versions behind them. Its § Repo deltas holds this repo's only two overrides: skill design
remains orchestration-grade, and probe evals use the dual-executor contract in `docs/agents/probe-evals.md`.
There is no project floor, capability-provider, or succession override.

There is no machine-level staffing module to resolve first. A playbook whose probe record names a different
machine is stale — re-run `staffing setup` rather than dispatching on it.

## Parallelism verdict

> Read by `backlog build` before dispatch.

- Verdict: **parallel-safe** — re-derived 2026-07-24 under v2 semantics (asher-skills#95): the v1 record said `serialize-verification` but justified it as "user chose sequential", and the shared-singleton audit above shows **no code-level collision** — nothing environmental forces serialization. v2 distinguishes constraint from preference, so the honest verdict is parallel-safe.
- Standing dispatch preference: **parallel, uncapped** — every ready, unblocked ticket fans out by default (recorded 2026-07-26, asher-skills#116; supersedes the earlier sequential preference). The fleet is bounded by the ready queue and the harness's own concurrency limits, not by policy — the queue-on-refused-spawn rule absorbs whatever the harness declines to run at once. A **per-run override** may narrow a run to a width limit or to fully sequential; changing the day's working mode never requires a playbook edit. This is policy, not environment: the parallel-safe verdict stands on its own, and the preference can change per-run without re-auditing. (Deferred: introduce a width cap only if uncapped fan-out proves noisy in practice — review pile-up, machine load.)
- **No mid-flight rebases**: each build targets the base branch as of its fork; drift between in-flight builds is absorbed at review and merge time, never pushed into running builds.
- **Merge posture: batch via the `merge-changes` skill** — the human authorizes a batch of review-ready change requests; the skill computes dependency order, merges, and reconciles mechanically; a conflict needing judgment stops the run. The human authorization gate itself is unchanged.
- **Review posture: tracker-native** — each build's review happens on its own change request, per-ticket by construction, so concurrent reviews serialize nothing (§ Presenting records the surface retirement). The tracker handles concurrency by serializing its own writes, never by serializing code verification. (Keep-awake stays **none** — the note lives in § Presenting.)
