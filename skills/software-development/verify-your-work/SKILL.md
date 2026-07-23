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

Read what the change says it does — the ticket, the commit messages, the diff itself. Each claim is a
thing that must be demonstrably true, including the implicit ones: nothing that worked before broke, and
the change behaves at its edges, not just its happy path.

## Read the environment contract

`docs/agents/environment.md`, when the repo has one, records how to run the stack, seed data, reach a
feature, authenticate (including a reusable browser session), and which driver exercises each surface.
Honor it — a verifier that improvises around the recorded contract produces evidence nobody can
reproduce. Absent the playbook, say so and verify what the repo's own commands reach.

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

Run each check and capture the exact command and its output. A check you couldn't run (missing
environment, no browser, absent fixture) is reported as *not verified*, with the reason — never silently
skipped, never guessed at.

## Report

Per claim: what was checked, the command, pass or fail, and for failures the evidence quoted — the
failing output, the wrong screen, the broken state. End with the one-line verdict: which claims stand,
which fell, which went unverified.
