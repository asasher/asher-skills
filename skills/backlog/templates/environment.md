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
- Shared singletons that cannot be isolated locally: _<e.g. one managed deployment, one auth tenant, one inbox; or "none">_.

## Seed data

- Seed regime: _<real seed command | load-from-dataset | none — drive the app>_.
- Command (if any): _<e.g. `pnpm dev:seed`, or the dataset-load command>_.
- What a freshly seeded stack contains, and how to reach a feature-exercising state when there is no seed: _<add yours>_.

## Authenticating for testing

- Auth model: _<e.g. email magic-link/OTP, OAuth, username+password, API token>_.
- How an agent mints a session: _<e.g. trigger an OTP → read it from the agentmail inbox → open the link with agent-browser>_.
- Test accounts / where credentials live: _<env vars or secrets store; never hardcode, never echo `.env`>_.

## Driving the app & capturing evidence

> Set by `setup`'s app-access audit; read by `verify` (to exercise the app) and `evidence` (to capture proof). One entry per surface the loop verifies.

- Form factor(s): _<CLI | web | mobile | desktop — list every surface issues touch>_.
- Driver per surface: _<defaults: shell + the CLI entrypoint; agent-browser for the web app; a simulator + driver for mobile; computer-use tooling for desktop. Adjust to this repo>_.
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

- Verdict: _<parallel-safe | serialize-verification>_.
- If serialized, the shared resource that forces it: _<add yours>_.
- Serialized exception lane: _<issue classes that must serialize even when parallel-safe — destructive shared-tenant operations, real third-party endpoints, deliberately distinct users; or "none">_.
