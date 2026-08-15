# Playbook: Environment

> Project playbook for this repo — the verification-environment contract. Read by any session that builds, runs, or proves the app: build threads, `verify-your-work`, `prove-your-work`, `merge-change` (cleanup), `backlog build` (the agent-readiness gate), and `backlog status` (the teardown sweep). Tailor every section to this codebase; `setup` fills the agent-readiness section from its certification. A session that earns a fact this playbook should have carried — a start recipe, an auth path, an admin bootstrap, a deploy constraint — writes it back into the matching section as part of its change, so the next session reads it instead of re-deriving it. Repo facts accrete here; machine state is never recorded — a capability is checked at use, and a failed check warns and names its fallback.

## Branching & deploys

- Base branch: _<e.g. main, or staging>_ — create worktrees and work branches from it, and target change requests at it. Sync it per `platform.md` § Version control before branching. The primary checkout stays on this branch — work branches are born inside their worktrees, never checked out here.
- Branch naming: _<e.g. `<ticket-number>-<slug>`>_; feature branches and `artifact/` branches per `platform.md` § Version control.
- What a change request produces: _<e.g. a preview deployment per PR, or nothing>_.
- What a merge produces: _<e.g. merge to staging → staging deployment; promotion path to production>_.
- Deploy-target constraints: _<the hosted-runtime facts otherwise learned by a failed deploy — runtime and version, packaging semantics, bundle/asset limits; accrete each as discovered>_.
- Credential preflight: _<each deploy/CI credential a gate depends on, and the cheap read that proves it is live — run before work that will hit that gate>_.

## Running locally

- Start the full dev stack: _<command>_.
- Services that come up: _<e.g. web, API, Postgres, redis, object store>_.
- Ports / URLs / hostnames: _<add yours; note if a shared proxy with `*.localhost` hostnames is used>_.
- The commands above serve non-interactive agents: each start command runs detached with output to a log, stop/restart is recorded, and teardown is audited (ports free, processes gone) — a TUI-only launcher gets its detached wrapper recorded here. Setup verifies this headlessly, not just in a terminal.

## Agent-readiness

> The standard lives in the `agent-ready-codebase` reference skill; this section records this repo's **answers**. `backlog setup` certifies against the checklist — pass, or a punch list of gaps — and `backlog build` dispatches only on a full pass. Working copies always go through the project-owned `worktree` skill. Parallel-safety is upkeep, not a one-time audit: re-certify on demand, and a build that breaks an answer fixes the answer.

The four checklist items — status and the working recipe for each:

1. **Worktrees** — the `worktree` skill can create, inspect, and remove working copies here: _<pass | gap — what blocks it>_.
2. **Stack per worktree** — each working copy brings up its own dev stack beside the others: _<pass — the bring-up command/hook | gap>_. Teardown: _<command, or "nothing to tear down">_ — it must resolve the **same environment-wrapped compose project** the bring-up resolved (same env files, same project-name derivation, run from inside the worktree) and remove its volumes; a hardcoded compose project or `container_name` fails this item twice — concurrent stacks collide, and the survivor stays label-pinned to whichever directory ran it last. Containers whose compose working-dir label points at a path that no longer exists are orphans of exactly that failure; the teardown sweep surfaces them.
3. **Auth per worktree** — an agent can mint a session in each copy independently: _<pass — how | gap>_.
4. **Seed** — seed data exists and exercises everything the app offers, including new features: _<pass | gap>_. Details in § Seed data below.

**Shared singletons — use ≠ change.** Every genuinely shared resource, one row each. Twenty parallel builds may _use_ a singleton; a ticket that _changes_ it is marked at the tracker (slice differently first; a dependency edge only for true residue). Most rows collide only on change.

| Singleton | Collides on | Notes |
| --- | --- | --- |
| _<e.g. one managed auth deployment>_ | _<change only>_ | _<changer tickets marked at the tracker>_ |
| _<e.g. a shared staging target>_ | _<change only>_ | _<add yours>_ |
| the parent `.git` | use (locks) | concurrent git operations can collide on `index.lock`/ref locks — a lock error is contention: wait and retry briefly; a lock outliving the retry with no live git process behind it is a crashed operation's leftover, only then safe to remove |

**Punch list** — the gaps certification found, each groomable as its own ticket: _<the list, or "none — certified <date>">_.

## Seed data

- Seed regime: _<real seed command | load-from-dataset | none — drive the app>_.
- Command (if any): _<e.g. `pnpm dev:seed`, or the dataset-load command>_.
- What a freshly seeded stack contains: _<add yours>_.
- **The seed is a maintained artifact**: a ticket that adds a feature extends the seed in scope; a seed that misses a feature is drift.
- **Drive-to-feature path** — from a running, seeded stack, how to reach a state that exercises a feature: the entry command/route, the navigation steps, and any precondition state a criterion needs (a logged-in role, a created record, a selected workspace). _<add yours, or "n/a — no app surface">_.

## Authenticating for testing

- Auth model: _<e.g. email magic-link/OTP, OAuth, username+password, API token>_.
- How an agent mints a session: _<e.g. trigger an OTP → read it from the test inbox → complete login in the browser driver>_.
- **Session reuse:** mint once per run and persist the browser storage state (_<e.g. `e2e/.auth/state.json`, gitignored>_); every subsequent check loads it instead of re-authenticating.
- Test accounts / where credentials live: _<env vars or secrets store; never hardcode, never echo `.env`>_.
- Record here only the liveness probe (e.g. `gh auth status`) — never an observed identity; who is authed is checked at use, not written down.

## Verification data

- Standing accounts/tenants and permissions: _<inventory what exists and the criterion classes each unlocks>_.
- Per-ticket fixture naming: `VERIFY-<ticket>-<purpose>` unless this repo records another collision-safe form.
- Scale affordances and limits: _<largest feasible real fixture; approved synthetic substitutes and the criterion classes where each is/is not valid>_.
- Lifetime/cleanup: provision before verification, retain through final evidence, then remove only this ticket's fixtures. Never share a mutable scratch entity across tickets.
- **Per-ticket-disposable stores** — the stores a single ticket may reset, drop, or wipe wholesale (e.g. its own worktree's database): _<list them; everything else is shared, and destructive verbs stop at this line>_.

## Driving the app & capturing evidence

> Read by `verify-your-work` (to exercise the app) and `prove-your-work` (to capture proof). One entry per surface. Verification is **code, not improvisation**: a browser check is a script whose run is reproducible.

- Form factor(s): _<CLI | web | mobile | desktop — list every surface tickets touch>_.
- Web driver: **Playwright driving Chrome** — the default for every browser-based verification; scripts live in _<e.g. `e2e/`>_ and run with _<e.g. `npx playwright test`>_. Evidence comes from Playwright's own artifacts — traces, screenshots, video — captured per run. Headless launch is checked at use; headed mode is the fallback when headless cannot launch. Harness-native browser tools and `agent-browser` are not verification routes — they have proven unreliable; a browser check is a Playwright script or it is a recorded gap.
- **Durable vs scaffolding is a shaping decision, executed here:** only the checks the spec declares durable join the maintained suite. One-work scaffolding scripts are dropped before merge, their runs captured as evidence via the `to-web` sibling — the run survives, the script does not.
- Other surfaces: _<defaults: shell + the CLI entrypoint; a simulator + driver for mobile; desktop only behind a recorded use case AND explicit user approval — absent either, record the surface as a hard verification gap. A driver failure surfaces as a blocker; it never falls back to a less-isolated surface>_.
- Evidence capture per surface: _<e.g. Playwright trace/screenshots for web; terminal transcripts for CLI; screen recording → GIF for flows the driver can't script>_.
- Supporting tools: _<e.g. a test email inbox for OTP/magic links; add yours>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Presenting to the human

> No standing presentation surface is bound here. Review happens on the change request bound in `platform.md` § Change review; evidence media uploads via the `to-web` sibling and embeds by URL per `evidence.md`. Where the `to-tailnet` skill is installed, it may be invoked on demand when the human needs an artifact on another device without publishing it.

## Staffing delta

> Written by `staffing setup` when this repo diverges from the roster; dispatch resolves models through the `to-subagent` skill. _<delta rows, or "none — roster as-is">_.
