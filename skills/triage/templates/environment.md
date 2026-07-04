# Playbook: Environment

> Project playbook for this repo. Shared — read by any triage subskill that builds a branch, runs, or tests the app (`implement`, `verify`, `evidence`, `diagnose`, the PR step, the review fixer) and by `run` for the parallelism verdict. Tailor every section to this codebase. `setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: _<e.g. main, or staging>_ — create worktrees and work branches from it, and target PRs at it. Pull its latest remote state before branching.
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
- Driver per surface: _<e.g. shell + the CLI entrypoint; agent-browser / Playwright MCP for the web app; iOS simulator + driver for mobile; computer-use tooling for desktop>_.
- Evidence capture per surface: _<e.g. driver screenshots for static states; screen recording → GIF for flows; terminal transcripts for CLI>_.
- Supporting tools: _<e.g. agentmail for OTP/magic-link inboxes; others>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Model staffing

> Read by `run` at dispatch and by `verify`, `evidence`, and `adversarial-review` when they staff the delegate role. The skill defines the roles (lead / delegate / floor); this section maps them to models **per harness** — list only models each harness can actually reach, since one harness usually cannot spawn another vendor's models.

- Floor: _<minimum capability class; nothing staffs below it>_.
- From _<harness, e.g. Claude Code>_: lead = _<model>_; delegate = _<model + how to spawn it, e.g. subagent model override>_; external CLI delegate = _<e.g. codex CLI model+effort for backend-only work, or "none">_.
- From _<other harness, e.g. Codex>_: _<mapping; if no lower tier is reachable above the floor, the delegate role collapses onto the lead — still delegated into separate threads>_.
- Reviewer constraint: _<which delegate options may fill Reviewer; it must handle the full review criteria, frontend included>_.

## Parallelism verdict

> Read by `run` before dispatch.

- Verdict: _<parallel-safe | serialize-verification>_.
- If serialized, the shared resource that forces it: _<add yours>_.
- Serialized exception lane: _<issue classes that must serialize even when parallel-safe — destructive shared-tenant operations, real third-party endpoints, deliberately distinct users; or "none">_.
