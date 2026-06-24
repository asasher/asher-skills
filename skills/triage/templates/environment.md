# Playbook: Environment

> Project playbook for this repo. Shared — read by any triage subskill that builds a branch, runs, or tests the app (`implement`, `verify`, `diagnose`, the PR step, the review fixer). Tailor every section to this codebase.

## Branching & deploys

- Base branch: _<e.g. main, or staging>_ — create worktrees and work branches from it, and target PRs at it. Pull its latest remote state before branching.
- Branch naming: _<e.g. `<issue-number>-<slug>`>_.
- What a PR produces: _<e.g. a preview deployment per PR, or nothing>_.
- What a merge produces: _<e.g. merge to staging → staging deployment; promotion path to production>_.

## Where to test

- _<e.g. test locally only; do not test against the preview>_ / _<e.g. manual testing on staging after merge>_.

## Running locally

- Start the app: _<command>_.
- Ports / URLs: _<add yours>_.

## Authenticating for testing

- Auth model: _<e.g. email magic-link, OAuth, username+password, API token>_.
- How an agent gets a session: _<e.g. trigger a magic link → read it from the agentmail inbox → open the link with agent-browser>_.
- Test accounts / where credentials live: _<env vars or secrets store; never hardcode>_.

## Tools available

- _<e.g. agent-browser for driving the UI; agentmail for email/inbox flows; others>_.
