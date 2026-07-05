# Task: Make the goodwork skill self-contained — ship server/await assets + runnable eval gates

The goodwork skill (`skills/goodwork/`) will be deployed by copying the skill folder into a fresh project. Everything setup/execution need must live INSIDE the skill folder. The authoritative contract: `goodwork-workspace/v2/SPEC.md` (server contract, event/approval schemas, await semantics, security rules) and `SCHEMAS.md`. Do not weaken anything in them.

## Part A — Shippable assets in `skills/goodwork/scripts/`

1. `server.py` — Python 3 stdlib ONLY, no pip deps. Implements the SPEC contract: serves projection pages from `goodwork/` JSON state (read-only), single POST `/event` endpoint appending to `events.jsonl`, binds 127.0.0.1 on a random free port, per-session token required on EVERY request (path or header per SPEC), token + port printed as one JSON line on stdout at startup, stays up while pending approvals exist then idle-timeout, never writes any state file. Keep it lean (~150-250 lines); log requests to stderr.
2. `await.py` — the blocking bridge per SPEC: `--ids`, `--timeout`, cursor file handling, drains events that arrived before start, exits with matched events as JSON on stdout; distinct exit codes for matched / timeout / error.
3. `pages/` — minimal HTML/JS templates for approval flow (mobile-first, per-item + batch checkboxes, reject-with-reason), CV diff (a `@pierre/diffs` mount point with graceful fallback to a plain inline diff when the vendored lib is absent), kanban (list view on mobile). Templates read JSON the server injects/serves; no external network requests anywhere.
4. `init_workspace.py` — creates the `goodwork/` state files empty-but-valid per SCHEMAS.md, checks `.env` is gitignored (creates/extends `.gitignore` if needed).

Wire the skill docs: `reference/setup.md` and `reference/execution.md` point to these scripts as THE implementation (run them, don't rewrite them); state.md mentions init. Keep pointers one line each — no restating contracts. SKILL.md stays ≤ 85 lines.

## Part B — Runnable eval gates in `goodwork-workspace/eval/gates/`

Deterministic tests, no LLM calls, plain pytest or bash+python, runnable via a single `run-gates.sh`:
- `no-unauthenticated-post`: POST /event without/with-wrong token → rejected, nothing appended.
- `event-append-only`: valid POST appends exactly one well-formed line; server never modifies other files (fs snapshot before/after).
- `hash-mismatch-blocks`: simulate approve event with stale content_hash → validation helper (write a small `scripts/validate_approval.py` used by both agent guidance and tests) refuses to mint an approval record.
- `await-drains-offline-clicks`: write events, then start await → returns them; cursor advances; second await gets nothing.
- `await-timeout-and-partial`: exit codes and partial-match output per SPEC.
- `env-gitignored`: init_workspace on a dir where .env would be tracked → fails loudly.
- `sole-writer`: after a full server session with posts, only events.jsonl changed.
- `init-schema-valid`: init_workspace output validates against SCHEMAS.md examples' shapes.

RUN the gates (`run-gates.sh`) until green. These are local-only tests — no tokens, no network beyond 127.0.0.1.

## Rules

- Stdlib only, macOS-friendly, no daemons left running after tests (kill server processes you start).
- Don't touch the persona/pair-harness files in `goodwork-workspace/eval/` beyond adding the `gates/` dir and a pointer line in eval's README.
- If SPEC is ambiguous somewhere you must implement, implement the safer reading and list it in the final summary.

Finish by printing: files written, gate results (pass/fail each), and ambiguities resolved.
