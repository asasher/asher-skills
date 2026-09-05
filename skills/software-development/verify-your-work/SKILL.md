---
name: verify-your-work
description: Verify a change against its claims and report per-claim evidence, after building, during PR review, or after merge.
metadata:
  optional: [technical-writing]
---

# Verify your work

Perform a checking pass without fixing the change. Return findings before the owner begins any fix, even when both stages run in this session.

## Pin and prepare

Record head, target base, approved spec revision, environment, and fixture state. Confirm the checkout matches the requested head. A reviewer may read source concurrently; nobody edits code or competes for runtime fixtures during this pass.

Read the ticket, approved spec, commits, and diff. List every acceptance criterion plus relevant regression, edge-state, seed-coverage, and data-safety claims. Read `docs/agents/environment.md` for commands, drivers, auth, and disposable fixtures. Without it, disclose the gap and use the repo's documented commands. Reset only stores explicitly marked disposable for this ticket.

## Check each claim

Choose proof that would fail if the claim were false:

- Run touched tests, typecheck/build, and the full suite for behavioral changes.
- Exercise the real entry point: CLI, HTTP, browser, or the recorded app driver.
- For UI work, script the changed journey and relevant empty, loading, error, disabled, and responsive states. Drive the app and capture the result.
- For destructive data changes, verify preservation and failure paths against representative fixtures.

Honor each criterion's **guard** (durable suite test) or **temporary check** choice. If undeclared, record the gap, use temporary checks, and flag needed durable coverage for the owner. Compilation alone proves no behavior.

Capture exact commands, outputs, and their own exit codes. Serialize checks sharing mutable state. Inspect every visual result for the claimed content, legibility, and clipping. Preserve temporary scripts and captures outside tracked source; media never enters Git. Remove source-tree probes after preserving their exact contents with the run.

An inaccessible check is **not verified**, with its reason. After three failed attempts at an environment seam, return a partial report for its affected claims. Prove a **pre-existing** failure with the same check against the base in an isolated checkout; distinguish it from a regression.

## Report

Use `technical-writing` when available. For every claim, return its id, **passed / failed / pre-existing / not verified**, check kind, command, output or visual evidence, and failure explanation. Include fixture details, playbook deviations, artifact paths, and exact temporary scripts or durable source links so evidence can be reused and published.

Recheck head and base. Moved inputs make the report stale. End with the revisions, verdict totals, and unresolved claims; never turn missing proof into a pass.
