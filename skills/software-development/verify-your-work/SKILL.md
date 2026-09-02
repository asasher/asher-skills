---
name: verify-your-work
description: Verify a named set of changes does what it claims and report findings with evidence. Use after building and before a PR exists, or to check merged work against its spec.
metadata:
  optional: [technical-writing, to-web]
---

# Verify Your Work

Verify that a named set of changes does what it claims. The deliverable is a findings report. **Never fix anything**: a verifier that edits the work stops being a verifier, and the fix belongs to whoever owns the changes.

## Establish the claims

Read what the change says it does: the issue, the spec at its blessed hash when the issue has one, the commit messages, the diff itself. Each acceptance criterion (`AC-1`, `AC-2`, …) is a claim. Each claim is a thing that must be demonstrably true, including the implicit ones: nothing that worked before broke; the change behaves at its edges; a change that adds a feature extends the seed so the seed reaches it; a destructive data operation (a migration, a cast, a backfill) loses or mangles no existing data. The list is complete when every acceptance criterion and every implicit claim is a line the report will carry a verdict for.

## Read the environment playbook

`docs/agents/environment.md`, when the repo has one, records how to run the stack, seed data, reach a feature, authenticate, which driver exercises each surface, and the check commands with their invocation traps. Honor it; a verifier that improvises around the playbook produces evidence nobody can reproduce. Absent the playbook, say so and verify what the repo's own commands reach.

The playbook also bounds what state is yours: create and seed what a check needs per its fixture rules, and point destructive verbs (reset, drop, wipe) only at stores the playbook marks per-issue-disposable. A shared store is never yours to reset.

## Two kinds of check

Every check is one of two kinds. A **guard** is a durable test that protects product behavior: it joins the repo's suite and stays in the tree with the change. A **throwaway verification script** exercises the change for this run and captures screenshots; it is dropped before merge, so its captured run is the evidence, artifacts uploaded through the `to-web` sibling (absent it, say so and keep the run in the report itself).

The split arrives declared: the spec says, per acceptance criterion, which kind its check is. Absent a declaration, the brief says which kind the builder chose; absent that too, say so in the report, write throwaway scripts, and flag any check that looks like a guard for the owner to decide.

## Pick the proof that goes red

For each claim, choose the check that would go red if the claim were false:

- the tests the change added or touched, then the full suite;
- typecheck and build;
- the changed surface exercised directly: a CLI invocation, an HTTP call, a script against the real entry point;
- for UI work, a check written as a script with the repo's recorded driver for that surface (Playwright for web, an emulator or app driver for mobile), walking the changed journey through the states named in the issue (empty, loading, error, disabled).

"It compiles" verifies nothing about behavior.

## Run and capture

Run each check and capture the exact command, its output, and its own exit status, read directly, not through a pipeline whose tail masks it. A check whose output is a visual artifact (a screenshot, an export, a rendered document) is judged by looking at it: the content the claim names, legible, at sane dimensions, without clipping. A file existing at nonzero bytes proves nothing. A check you could not run (missing environment, no browser, absent fixture) is reported as _not verified_ with the reason, never silently skipped. An environment seam that keeps failing (auth, seeding, a launcher) earns three attempts, then its claims go to _not verified_ with the reason: a stuck seam converts to a partial report.

## Report

The report follows the `technical-writing` sibling; absent it, write plainly and say the standard was not loaded.

Per claim, keyed to its criterion id where the issue has them: what was checked, the command, pass or fail, whether the check is a guard or a throwaway script, and for failures the evidence quoted, the failing output, the wrong screen, the broken state. A failure also present before the change, proven by the same check against the base commit, is reported as **pre-existing**, a distinct verdict from a failure the change caused. Log any deviation from the environment playbook alongside the checks it touched. End with the one-line verdict: which claims passed, which failed, which are not verified.
