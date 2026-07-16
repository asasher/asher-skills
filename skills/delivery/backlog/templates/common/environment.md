# Playbook: Environment

> Project playbook for this repo. Shared — read by any backlog subskill that builds a branch, runs, or tests the app (`implement`, `verify`, `evidence`, `diagnose`, the PR step, the review fixer) and by `run` for the parallelism verdict. Tailor every section to this codebase. `setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: _<e.g. main, or staging>_ — create worktrees and work branches from it, and target PRs at it. Sync it per `platform.md` § Version control before branching (on the local tracker binding, `run`'s claim commit is the fork point).
- Branch naming: _<e.g. `<issue-number>-<slug>`>_.
- What a PR produces: _<e.g. a preview deployment per PR, or nothing>_.
- What a merge produces: _<e.g. merge to staging → staging deployment; promotion path to production>_.

## Running locally

- Start the full dev stack: _<command>_.
- Services that come up: _<e.g. web, API, Postgres, redis, object store>_.
- Ports / URLs / hostnames: _<add yours; note if a shared proxy with `*.localhost` hostnames is used>_.

## Worktree isolation

> Set by `setup` per `reference/worktree-isolation.md`.

- Regime: _<local-isolatable | cloud-singleton>_.
- How to bring up an **isolated** stack for one worktree: _<the derived-env command / hook, or "main checkout only">_.
- **Shared-singleton list** — every resource two concurrent worktrees would contend for, from the isolation audit's probes. One row each; `setup` derives the verdict below from it, and `run` reads the recorded verdict. _<Fill the table, or "none — no runnable stack".>_

  | Singleton | Collision mode | Locally isolatable? |
  |-----------|----------------|---------------------|
  | _<e.g. Postgres `app_dev`>_ | _<shared data across worktrees>_ | _<yes — per-worktree DB / no>_ |
  | _<e.g. host port 3000>_ | _<second stack fails to bind>_ | _<yes — derived port>_ |
  | _<e.g. shared `node_modules`>_ | _<install mutates a running tree>_ | _<yes — per-worktree install>_ |
  | _<e.g. `.next` build cache>_ | _<interleaved writes corrupt artifacts>_ | _<yes — per-worktree cache dir>_ |
  | _<e.g. one managed deployment / auth tenant>_ | _<one backend behind every worktree>_ | _<no — cloud singleton>_ |

## Seed data

- Seed regime: _<real seed command | load-from-dataset | none — drive the app>_.
- Command (if any): _<e.g. `pnpm dev:seed`, or the dataset-load command>_.
- What a freshly seeded stack contains: _<add yours>_.
- **Drive-to-feature path** — from a running, seeded stack, how to reach a state that exercises a feature: the entry command/route, the navigation steps, and any precondition state a criterion needs (a logged-in role, a created record, a selected workspace). Set by `setup`'s access audit; `verify`/`evidence` drive it. _<add yours, or "n/a — no app surface">_.

## Authenticating for testing

- Auth model: _<e.g. email magic-link/OTP, OAuth, username+password, API token>_.
- How an agent mints a session: _<e.g. trigger an OTP → read it from the agentmail inbox → open the link with agent-browser>_.
- Test accounts / where credentials live: _<env vars or secrets store; never hardcode, never echo `.env`>_.

## Verification data

- Standing accounts/tenants and permissions: _<inventory what exists and the criterion classes each unlocks>_.
- Per-issue fixture naming: `VERIFY-<issue>-<purpose>` unless this repo records another collision-safe form.
- Scale affordances and limits: _<largest feasible real fixture; plan-approved synthetic substitutes and the criterion classes where each is/is not valid>_.
- Lifetime/cleanup: provision before the criteria loop, retain through final evidence, then let the named
  issue owner remove only its fixtures. Never share a mutable scratch entity across issues.

## Driving the app & capturing evidence

> Set by `setup`'s app-access audit; read by `verify` (to exercise the app) and `evidence` (to capture proof). One entry per surface the loop verifies.

- Form factor(s): _<CLI | web | mobile | desktop — list every surface issues touch>_.
- Driver per surface: _<defaults: shell + the CLI entrypoint; **agent-browser with an isolated profile** for the web app (the user's own browser only under a recorded user-session carve-out, with per-use consent); a simulator + driver for mobile; desktop requires the **Computer Use gate** — a concrete use case recorded here AND explicit user approval; absent either, record the surface as a hard verification gap. A driver failure surfaces as a blocker; it never falls back to a less-isolated surface. Adjust to this repo>_.
- Independent runtime verification: _<default: delegate to `codex exec` with a self-contained prompt when a check needs real UI interaction, screenshots, simulator state, or a second opinion outside the orchestrator's context (codex mechanics owned by the `staffing` skill); "n/a" when codex is unreachable>_.
- Evidence capture per surface: _<e.g. driver screenshots for static states; screen recording → GIF for flows; terminal transcripts for CLI>_.
- Supporting tools: _<default: agentmail for OTP/magic-link inboxes; add yours>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Presenting to the human

> Owned by the **`review-loop`** skill (composed by name): the presentation surface and interactive review — how plans and prototypes reach a human who may not be at the machine. review-loop's setup records this repo's surface config here (tailnet root, surface dir, publish/proxy commands, hub, keep-awake). backlog does not install the surface.

## Model staffing

> Owned by the **`staffing`** skill (composed by name): the model roster — roles (orchestrator, builder by surface, checker, floor), rankings, and the fallback ladder. `run` and every reference that spawns work resolve staffing questions against it; staffing's setup writes the compiled roster here (global base + this project's delta).

## Parallelism verdict

> Read by `run` before dispatch.

- Verdict: _<parallel-safe | serialize-verification>_ — gated by the shared-singleton list above, asymmetrically: `parallel-safe` requires a list with no un-isolated collision; `serialize-verification` may come from that list (a hard constraint) or from a plain preference to serialize.
- If serialized, why: _<either "user preference — sequential by choice" (the list is clear), or name the un-isolated rows from the list that force it — a hard constraint, since a parallel fan-out would corrupt that shared state>_.
- Serialized exception lane: _<issue classes that must serialize even when parallel-safe — destructive shared-tenant operations, real third-party endpoints, deliberately distinct users; or "none">_.
