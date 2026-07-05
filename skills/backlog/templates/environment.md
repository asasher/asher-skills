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
- Driver per surface: _<e.g. shell + the CLI entrypoint; agent-browser / Playwright MCP for the web app; iOS simulator + driver for mobile; computer-use tooling for desktop>_.
- Evidence capture per surface: _<e.g. driver screenshots for static states; screen recording → GIF for flows; terminal transcripts for CLI>_.
- Supporting tools: _<e.g. agentmail for OTP/magic-link inboxes; others>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Presenting to the human

> Read by `plan` and `prototype` when they pause for review; contract in the skill's `reference/presenting.md`. Set by `setup` — the shipped default is a singular tailnet surface; local-only and custom channels are legitimate alternates.

- Surface: _<tailnet | local-only | custom>_.
- Root URL: _<e.g. `https://<machine>.<tailnet>.ts.net/review`; "n/a" for local-only>_.
- Document server: _<e.g. a static server rooted at `~/.backlog/surface`, kept alive by the OS (LaunchAgent), proxied once via `tailscale serve --bg --set-path /review http://localhost:<port>` — the sandboxed macOS tailscale app cannot serve file paths directly>_.
- Publish a document: _<e.g. `ln -sfn <absolute path to the committed file> ~/.backlog/surface/<repo>/<issue>/<name>.html`>_.
- Expose a live prototype: _<e.g. `tailscale serve --bg --set-path /<repo>/<issue>/proto http://localhost:<port>`>_.
- Reap rule: _<e.g. remove the worktree's symlinks under the surface directory and `tailscale serve --set-path <path> off` for its proxies; `tailscale serve status` lists handlers for the orphan sweep>_.
- Keep-awake: _<the user's setup choice. Default: none — the surface is up when the machine is awake (harnesses hold sleep assertions during active runs). If the user wants planned AFK reviews to survive long pauses or lid-closed on battery, record their chosen mechanism here.>_.

## Model staffing

> Read by `run` at dispatch and by every reference that spawns work. The skill defines the roles (`reference/staffing.md`: orchestrator, builder by surface, checker, floor); this section maps them to models **per harness** — list only models each harness can actually reach, since one harness usually cannot spawn another vendor's models. One model may fill several roles.

- Floor: _<minimum capability class; nothing staffs below it in any role>_.
- From _<harness, e.g. Claude Code>_:
  - Orchestrator: _<model, usually the session model>_.
  - Builder (backend): _<model + how to spawn it, e.g. an external CLI + effort>_.
  - Builder (ui): _<model + how to spawn it, e.g. subagent model override>_.
  - Checker: _<model per surface; the Reviewer must handle the full review criteria, frontend included>_.
- From _<other harness, e.g. Codex>_: _<mapping; when no other tier is reachable above the floor, every role collapses onto the session model — still delegated into separate threads>_.
- Succession: _<who steps up to orchestrate when the orchestrator's model is unreachable, and which roles they keep>_.

## Parallelism verdict

> Read by `run` before dispatch.

- Verdict: _<parallel-safe | serialize-verification>_.
- If serialized, the shared resource that forces it: _<add yours>_.
- Serialized exception lane: _<issue classes that must serialize even when parallel-safe — destructive shared-tenant operations, real third-party endpoints, deliberately distinct users; or "none">_.
