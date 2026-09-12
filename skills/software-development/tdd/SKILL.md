---
name: tdd
description: Test-driven development. Use when building features or fixing bugs test-first, when "red-green" is mentioned, or when integration tests are wanted.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the discipline that makes that loop produce tests worth keeping.

Before writing the first test, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching; read `docs/agents/environment.md` § Checks where it exists: test placement, harness wiring, and runner traps live there.

## What a good test is

A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors.

See [tests](reference/tests.md) for good/bad test examples and [mocking](reference/mocking.md) for when to mock and how to design system boundaries so mocks stay simple.

## Seams — where tests go

Tests verify behavior at **seams** — the public boundaries where you observe behavior without reaching inside. Before the first test, identify the seams from the issue, spec, or settled discussion. Select any remaining seams within delegated implementation authority and record the choice. Ask only when a material unresolved choice exceeds that authority. Focus testing on the named behavior, critical paths, and complex logic.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. When the test is written after code already exists — a fix, a regression proof — observe the same test fail against the pre-change code and pass with the change, preserving existing work.
- **One cycle at a time.** One seam, one test, one minimal implementation — each test responding to what the last cycle taught you.
- **Refactor outside the loop.** The red → green cycle builds behavior; restructuring what already passes is separate, deliberate work.

The loop ends when every selected seam has a passing test for each behavior the issue, spec, or user named at that seam.
