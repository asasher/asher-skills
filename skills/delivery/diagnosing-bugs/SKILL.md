---
name: diagnosing-bugs
description: Diagnose hard bugs and performance regressions through a tight red-capable feedback loop. Use when a defect is failing, flaky, slow, or assigned for diagnosis by another workflow. Not for speculative cleanup without an observed symptom.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
---

# Diagnosing Bugs

Turn an observed defect into a named root cause and confirmed fix. The red-capable loop is load-bearing;
everything else consumes it.

## Commands

- **`<defect>`** (default) — load [diagnosis](reference/diagnosis.md) and work all six phases. Read
  `docs/agents/diagnosing-bugs.md` when present for project-specific seams, commands, and known flaky areas;
  absent it, use the bundled method without inventing repo facts.
- **`setup`** — load [setup](reference/setup.md) and reconcile only the project diagnosis playbook.

## Contract

Input is the reporter's exact observed symptom plus the environment needed to drive it. Return:

1. the already-run red-capable command and captured symptom;
2. the minimal reproduction, ranked hypotheses, and evidence that names the root cause;
3. the fix, regression proof at the correct seam or an explicit no-seam finding, and the original loop green;
4. cleanup and project-check results.

## Dependency surface

- **Bundled references** — `reference/diagnosis.md` owns the method; `reference/setup.md` owns playbook
  reconciliation; `templates/diagnosing-bugs.md` is the delta-only playbook seed.
- **Project playbook** — optional `docs/agents/diagnosing-bugs.md`, owned by the repo after setup and preserved
  on reconciliation.
- **Sibling skills** — none. Callers invoke this skill by name and retain their surrounding lifecycle.
