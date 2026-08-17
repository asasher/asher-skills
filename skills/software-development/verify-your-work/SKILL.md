---
name: verify-your-work
description: Verify a named set of changes does what it claims and report findings with evidence. Use after building and before a change request exists.
argument-hint: "<the changes to verify: branch, diff, or description>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [writing-for-humans, to-web]
---

# Verify Your Work

Verify that a named set of changes does what it claims. The deliverable is a findings report. **Never fix anything**: a verifier that edits the work stops being a verifier, and the fix belongs to whoever owns the changes.

## Establish the claims

Read what the change says it does — the ticket, the commit messages, the diff itself. When the ticket carries acceptance criteria (`AC-1`, `AC-2`, …), each criterion is a claim. Each claim is a thing that must be demonstrably true, including the implicit ones: nothing that worked before broke, and the change behaves at its edges. A change that performs a destructive data operation — a migration, a cast, a backfill — implicitly claims no existing data is lost or mangled; that claim needs evidence like any other. The list is complete when every acceptance criterion and every implicit claim is a line the report will carry a verdict for.

## Read the repo playbooks

`docs/agents/environment.md`, when the repo has one, is the environment playbook: it records how to run the stack, seed data, reach a feature, authenticate, and which driver exercises each surface. Honor it — a verifier that improvises around the playbook produces evidence nobody can reproduce. Absent the playbook, say so and verify what the repo's own commands reach. `docs/agents/codebase.md`, where it exists, records the canonical check commands and their invocation traps — run the recorded forms.

The playbook also bounds what state is yours: create and seed what a check needs per its fixture rules, and point destructive verbs (reset, drop, wipe) only at resources the playbook marks per-ticket-disposable — a shared store is never yours to reset.

## The test split arrives declared

The spec declares, per acceptance criterion, which checks become durable suite tests and which are throwaway scaffolding scripts — a shaping decision, never a judgment made here. A durable criterion's check is a real test in the repo's suite, left in the tree with the change. A throwaway criterion's check is scaffolding: the script is dropped before merge, so its captured run is the evidence, artifacts uploaded through the `to-web` sibling — absent it, say so and keep the run in the report itself. Absent a declaration, say so in the report, write scaffolding, and flag any check that looks durable for the owner to decide.

## Pick the proof that goes red

For each claim, choose the check that would go red if the claim were false:

- the tests the change added or touched, then the full suite;
- typecheck and build;
- the changed surface exercised directly — a CLI invocation, an HTTP call, a script against the real entry point;
- for UI work, a check **written as a script** with the repo's recorded driver for that surface — a browser driver for web, an emulator or app driver for mobile — walking the changed journey through the states named in the ticket (empty, loading, error, disabled).

"It compiles" verifies nothing about behavior.

## Run and capture

Run each check and capture the exact command, its output, and its own exit status — read directly, not through a pipeline whose tail masks it. A check whose output is a visual artifact — a screenshot, an export, a rendered document — is judged by **looking at it**: the content the claim names, legible, at sane dimensions, without clipping. A file existing at nonzero bytes proves nothing. A check you couldn't run (missing environment, no browser, absent fixture) is reported as _not verified_, with the reason — never silently skipped. An environment seam that keeps failing — auth, seeding, a launcher — earns a bounded number of attempts (three, unless the playbook says otherwise), then its claims go to _not verified_ with the reason: a stuck seam converts to a partial report.

## Report

The report follows the `writing-for-humans` sibling; absent it, write plainly and say the standard was not loaded.

Per claim — keyed to its criterion id where the ticket has them: what was checked, the command, pass or fail, and for failures the evidence quoted — the failing output, the wrong screen, the broken state. A failure also present before the change, proven by the same check against the base commit, is reported as **pre-existing** — a distinct verdict from a failure the change caused. Log any deviation from the environment playbook alongside the checks it touched. End with the one-line verdict: which claims passed, which failed, which are not verified.
