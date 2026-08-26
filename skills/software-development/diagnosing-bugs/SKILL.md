---
name: diagnosing-bugs
description: Diagnose defects through a tight red-capable feedback loop. Use on an observed symptom — a failure, a flake, or a slowdown. Not for speculative cleanup.
---

# Diagnosing Bugs

Turn an observed defect into a named root cause and confirmed fix. Read [diagnosis](reference/diagnosis.md) and work its six phases in order. The red-capable loop is load-bearing; every later phase runs against it.

## Contract

Input is the reporter's exact observed symptom plus the environment needed to drive it. Return:

1. the already-run red-capable command and captured symptom;
2. the minimal reproduction, ranked hypotheses, and evidence that names the root cause;
3. the fix, regression proof at the correct seam or an explicit no-seam finding, and the original loop green;
4. cleanup and project-check results.
