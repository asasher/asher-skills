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

## Parallelism verdict

> Read by `run` before dispatch.

- Verdict: _<parallel-safe | serialize-verification>_.
- If serialized, the shared resource that forces it: _<add yours>_.

## Tools available

- _<e.g. agent-browser for driving the UI; agentmail for email/inbox flows; others>_.
