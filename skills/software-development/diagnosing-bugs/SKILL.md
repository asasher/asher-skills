---
name: diagnosing-bugs
description: Diagnose defects through a tight red-capable feedback loop. Use on an observed symptom — a failure, a flake, or a slowdown. Not for speculative cleanup.
argument-hint: "<the observed symptom>"
metadata:
  setup: reference/setup.md
---

# Diagnosing Bugs

Turn an observed defect into a named root cause and confirmed fix. The red-capable loop is load-bearing; every later phase runs against it.

## Commands

- **`<defect>`** (default) — load [diagnosis](reference/diagnosis.md), the six-phase method. Read `docs/agents/diagnosing-bugs.md` when present for known flaky surfaces and debugging seams; absent it, verify any repo command or seam before relying on it.
- **`setup`** — load [setup](reference/setup.md) and reconcile the project diagnosis playbook, `docs/agents/diagnosing-bugs.md`.

## Contract

Input is the reporter's exact observed symptom plus the environment needed to drive it. Return:

1. the already-run red-capable command and captured symptom;
2. the minimal reproduction, ranked hypotheses, and evidence that names the root cause;
3. the fix, regression proof at the correct seam or an explicit no-seam finding, and the original loop green;
4. cleanup and project-check results.
