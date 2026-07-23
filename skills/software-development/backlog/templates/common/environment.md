# Playbook: Environment

> Project playbook for this repo — the verification-environment contract. Read by any session that
> builds, runs, or proves the app: build threads, `verify-your-work`, `prove-your-work`,
> `merge-changes` (cleanup), and `backlog build` (isolation and parallelism verdicts). Tailor every
> section to this codebase; `setup` fills the isolation, seed, and parallelism sections from its audit.
> A session that earns a fact this playbook should have carried — a start recipe, an auth path, an
> admin bootstrap, a deploy constraint — writes it back into the matching section as part of its change,
> so the next session reads it instead of re-deriving it.

## Branching & deploys

- Base branch: _<e.g. main, or staging>_ — create worktrees and work branches from it, and target
  change requests at it. Sync it per `platform.md` § Version control before branching. The primary
  checkout stays on this branch — work branches are born inside their worktrees, never checked out here.
- Branch naming: _<e.g. `<ticket-number>-<slug>`>_.
- What a change request produces: _<e.g. a preview deployment per PR, or nothing>_.
- What a merge produces: _<e.g. merge to staging → staging deployment; promotion path to production>_.
- Deploy-target constraints: _<the hosted-runtime facts otherwise learned by a failed deploy — runtime
  and version, packaging semantics, bundle/asset limits; accrete each as discovered>_.
- Credential preflight: _<each deploy/CI credential a gate depends on, and the cheap read that proves
  it is live — run before work that will hit that gate>_.

## Running locally

- Start the full dev stack: _<command>_.
- Services that come up: _<e.g. web, API, Postgres, redis, object store>_.
- Ports / URLs / hostnames: _<add yours; note if a shared proxy with `*.localhost` hostnames is used>_.
- The commands above serve non-interactive agents: each start command runs detached with output to a
  log, stop/restart is recorded, and teardown is audited (ports free, processes gone) — a TUI-only
  launcher gets its detached wrapper recorded here. Setup verifies this headlessly, not just in a
  terminal.

## Worktree isolation

> Set by `setup` from its audit; read by `backlog build` before dispatching parallel threads.

- Regime: _<local-isolatable | cloud-singleton | none>_ — whether one worktree can run its own full
  stack beside another's.
- How to bring up an **isolated** stack for one worktree: _<the derived-env command / hook, or "main
  checkout only">_.
- Teardown for a worktree's stack (read by `merge-changes` cleanup): _<command, or "nothing to tear
  down">_.
- **Shared-singleton list** — every resource two concurrent worktrees would contend for. One row each;
  the parallelism verdict below derives from it.

  | Singleton | Collision mode | Locally isolatable? |
  |-----------|----------------|---------------------|
  | _<e.g. Postgres `app_dev`>_ | _<shared data across worktrees>_ | _<yes — per-worktree DB / no>_ |
  | _<e.g. host port 3000>_ | _<second stack fails to bind>_ | _<yes — derived port>_ |
  | _<e.g. one managed deployment / auth tenant>_ | _<one backend behind every worktree>_ | _<no — cloud singleton>_ |

## Seed data

- Seed regime: _<real seed command | load-from-dataset | none — drive the app>_.
- Command (if any): _<e.g. `pnpm dev:seed`, or the dataset-load command>_.
- What a freshly seeded stack contains: _<add yours>_.
- **Drive-to-feature path** — from a running, seeded stack, how to reach a state that exercises a
  feature: the entry command/route, the navigation steps, and any precondition state a criterion needs
  (a logged-in role, a created record, a selected workspace). _<add yours, or "n/a — no app surface">_.

## Authenticating for testing

- Auth model: _<e.g. email magic-link/OTP, OAuth, username+password, API token>_.
- How an agent mints a session: _<e.g. trigger an OTP → read it from the test inbox → complete login in
  the browser driver>_.
- **Session reuse:** mint once per run and persist the browser storage state
  (_<e.g. `e2e/.auth/state.json`, gitignored>_); every subsequent check loads it instead of
  re-authenticating.
- Test accounts / where credentials live: _<env vars or secrets store; never hardcode, never echo `.env`>_.

## Verification data

- Standing accounts/tenants and permissions: _<inventory what exists and the criterion classes each unlocks>_.
- Per-ticket fixture naming: `VERIFY-<ticket>-<purpose>` unless this repo records another collision-safe form.
- Scale affordances and limits: _<largest feasible real fixture; approved synthetic substitutes and the
  criterion classes where each is/is not valid>_.
- Lifetime/cleanup: provision before verification, retain through final evidence, then remove only this
  ticket's fixtures. Never share a mutable scratch entity across tickets.

## Driving the app & capturing evidence

> Read by `verify-your-work` (to exercise the app) and `prove-your-work` (to capture proof). One entry
> per surface. Verification is **code, not improvisation**: a browser check is a script whose run is
> reproducible, and the scripts accumulate into this repo's end-to-end suite.

- Form factor(s): _<CLI | web | mobile | desktop — list every surface tickets touch>_.
- Web driver: **Playwright driving Chrome** — the default for every browser-based verification; scripts
  live in _<e.g. `e2e/`>_ and run with _<e.g. `npx playwright
  test`>_. New checks are written as specs there, named for the ticket, and left in the tree: today's
  verification is tomorrow's regression suite. Evidence comes from Playwright's own artifacts — traces,
  screenshots, video — captured per run into _<artifact dir>_. Setup verifies the browser
  actually launches headless on this machine; if it cannot, record headed mode here as the fallback.
  Harness-native browser tools and `agent-browser` are not verification routes — they have proven
  unreliable; a browser check is a Playwright script or it is a recorded gap.
- Other surfaces: _<defaults: shell + the CLI entrypoint; a simulator + driver for mobile; desktop only
  behind a recorded use case AND explicit user approval — absent either, record the surface as a hard
  verification gap. A driver failure surfaces as a blocker; it never falls back to a less-isolated
  surface>_.
- Evidence capture per surface: _<e.g. Playwright trace/screenshots for web; terminal transcripts for
  CLI; screen recording → GIF for flows the driver can't script>_.
- Supporting tools: _<e.g. a test email inbox for OTP/magic links; add yours>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Presenting to the human

> Owned by the **`serve-via-tailnet`** skill (composed by name): how rendered artifacts reach a human
> who may not be at the machine. Its setup records this repo's surface config here (root path, surface
> dir, publish/proxy commands); this playbook does not install the surface.

## Staffing delta

> Written by `staffing setup` when this repo diverges from the machine roster; dispatch resolves models
> through the `to-subagent` skill. _<delta rows, or "none — machine roster as-is">_.

## Parallelism verdict

> Read by `backlog build` before dispatch.

- Verdict: _<parallel-safe | serialize-verification | sequential>_ — derived from the shared-singleton
  list above.
- If serialized, why: _<either "user preference — sequential by choice", or name the un-isolated rows
  that force it>_.
- Serialized exception lane: _<ticket classes that must serialize even when parallel-safe; or "none">_.
- **Lane mechanics** — under `serialize-verification`, parallel builds share the singleton through a
  lock: _<path, e.g. `.backlog-lane.lock` beside the primary checkout>_. Acquire by atomic directory
  create, writing ticket id and timestamp inside; hold only while the singleton is in use; release by
  removing the lock **after cleanup proof** — the singleton's ports free, env files restored, processes
  gone. Contenders wait on the lock, at the cadence the singleton actually turns over. A lock older
  than _<stale horizon, e.g. 30 min>_ with no activity on its holder's branch may be broken — the
  taker notes the takeover on the holder's ticket.
