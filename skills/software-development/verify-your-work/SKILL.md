---
name: verify-your-work
description: Verify a change against its claims and report per-claim evidence, after building, during PR review, or after merge.
metadata:
  optional: [technical-writing]
---

# Verify your work

Check the existing implementation. Return findings before the owner begins any fix, even when both stages run in this session.

## Pin and prepare

Pin head, target base, approved spec, environment, and fixture state. Verify the intended integration: use head when it contains the target base, otherwise an isolated tentative merge of those pinned revisions. Return conflicts to the owner. Record the tested commit and tree hash, then keep that tree fixed and reserve fixtures for the pass. Post-merge verification tests the recorded merged revision.

Read the ticket, approved spec, commits, and diff. List every acceptance criterion plus relevant regression, edge-state, seed-coverage, and data-safety claims. Read `docs/agents/environment.md` for commands, drivers, auth, and disposable fixtures. Without it, disclose the gap and use the repo's documented commands. Reset only stores explicitly marked disposable for this ticket.

## Check each claim

Choose proof that would fail if the claim were false:

- Run touched tests, typecheck/build, and the full suite for behavioral changes.
- Exercise the real entry point: CLI, HTTP, browser, or the recorded app driver.
- For UI work, exercise the changed journey and relevant empty, loading, error, disabled, and responsive states. Drive the app and capture the result.
- For destructive data changes, verify preservation and failure paths against representative fixtures.

Use headless Playwright by default. An alternative browser tool must demonstrate app access, control, and capture on the execution host in an isolated session. Give concurrent runs separate browser contexts/profiles, auth state, fixtures, and output paths. Preserve the user's browser and desktop; a headed fallback needs an isolated display or explicit approval to use the user's session. If neither is available, report the affected claims as not verified.

For normal-risk owner verification, reuse captured check results only when head/base, tested tree, commands, environment, and relevant fixture state match. Record their provenance; rerun stale or uncertain checks. Independently required verification runs its own checks. Exercise claims missing from the prior run.

Reuse existing tests and helpers. Write temporary scripts when repetition or complex setup warrants them; direct tool checks record reproducible actions and observations. Keep temporary checks with the run evidence, outside the maintained suite; add durable regression coverage where the testing contract requires it.

Honor each criterion's **guard** (durable suite test) or **temporary check** choice. If undeclared, record the gap, use temporary checks, and flag needed durable coverage for the owner. Use runtime checks for behavioral claims.

Capture exact tool actions and observations, plus commands, outputs, and exit codes for script runs. Serialize checks sharing mutable state. Inspect every visual result for the claimed content, legibility, and clipping. Preserve temporary scripts and captures outside tracked source; media never enters Git. Remove source-tree probes after preserving their exact contents with the run.

An inaccessible check is **not verified**, with its reason. After three failed attempts at an environment seam, return a partial report for its affected claims. Prove a **pre-existing** failure with the same check against the base in an isolated checkout; distinguish it from a regression.

## Report

Use `technical-writing` when available. For every claim, return its id, **passed / failed / pre-existing / not verified**, check kind, command or tool steps, output or visual evidence, and failure explanation. Include fixture details, playbook deviations, artifact paths, and exact temporary scripts or durable source links so evidence can be reused and published.

Recheck head and base. Moved inputs make the report stale. End with the source revisions, tested commit/tree, verdict totals, and unresolved claims. Passing verdicts require observed proof.
