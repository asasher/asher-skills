---
name: verify-your-work
description: Verify a named set of changes actually does what it claims — pick the proof that would catch it failing, run it, and report findings with evidence. Use after building and before a change request exists.
argument-hint: "<the changes to verify: branch, diff, or description>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Verify Your Work

Verify that a named set of changes does what it claims. The deliverable is a findings report — verified
claims with their proof, failures with their evidence. **Never fix anything**: a verifier that edits the
work stops being a verifier, and the fix belongs to whoever owns the changes.

## Establish the claims

Read what the change says it does — the ticket, the commit messages, the diff itself. When the ticket
carries acceptance criteria (`AC-1`, `AC-2`, …), each criterion is a claim and the report keys its
verdict to the id. Each claim is a thing that must be demonstrably true, including the implicit ones:
nothing that worked before broke, and the change behaves at its edges, not just its happy path. A
change that performs a destructive data operation — a migration, a cast, a backfill — implicitly
claims no existing data is lost or mangled; that claim needs evidence like any other.

## Read the environment contract

`docs/agents/environment.md`, when the repo has one, records how to run the stack, seed data, reach a
feature, authenticate, and which driver exercises each surface.
Honor it — a verifier that improvises around the recorded contract produces evidence nobody can
reproduce. Absent the playbook, say so and verify what the repo's own commands reach.

The contract also bounds what state is yours: create and seed what a check needs per the playbook's
fixture rules, and point destructive verbs (reset, drop, wipe) only at resources the playbook marks
per-ticket-disposable — a shared store is never yours to reset.

## Pick the proof that could fail

For each claim, choose the check that would go red if the claim were false:

- the tests the change added or touched, then the full suite;
- typecheck and build;
- the changed surface exercised directly — a CLI invocation, an HTTP call, a script against the real
  entry point;
- for UI work, a check **written as a script** with the repo's recorded driver for that surface — a
  browser driver for web, an emulator or app driver for mobile — walking
  the changed journey through the states named in the ticket (empty, loading, error, disabled), not
  just the golden path — and left in the tree where the repo keeps such specs.

A check that cannot fail is not proof. "It compiles" verifies nothing about behavior.

## Run and capture

Run each check and capture the exact command, its output, and its own exit status — read directly, not
through a pipeline whose tail masks it. A check whose output is a visual artifact —
a screenshot, an export, a rendered document — is judged by **looking at it**: the content the claim
names, legible, at sane dimensions, without clipping. A file existing at nonzero bytes proves nothing.
A check you couldn't run (missing environment, no browser, absent fixture) is reported as *not
verified*, with the reason — never silently skipped, never guessed at. An environment seam that keeps
failing — auth, seeding, a launcher — earns a bounded number of attempts (three, unless the recorded
contract says otherwise), then its claims go to *not verified* with the reason: a stuck seam converts
to a partial report, not a longer loop.

## Report

Per claim — keyed to its criterion id where the ticket has them: what was checked, the command, pass or
fail, and for failures the evidence quoted — the failing output, the wrong screen, the broken state. A
failure also present before the change, proven by the same check against the base commit, is reported
as **pre-existing** — a distinct verdict from a failure the change caused. Log any deviation from the
recorded environment contract alongside the checks it touched. End with the one-line verdict: which
claims stand, which fell, which went unverified.
