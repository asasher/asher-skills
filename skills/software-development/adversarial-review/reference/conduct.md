# Review and fix conduct

## Review

Supply the PR, issue/spec, immutable head and base, prior findings, and deadline. The reviewer reads and comments only; it does not run competing runtime checks or edit code.

Every blocking finding names the changed location, violated requirement or standard, and a concrete failure scenario or maintenance cost. Label optional suggestions. A design preference alone is not a blocker.

LGTM names the reviewed head and base. Prior findings need a verified fix, accepted pushback, or an explicit ruling; a fixer's reply alone does not clear them. State required CI status: failed checks withhold LGTM; pending checks remain a completion gate.

If deciding the finding requires choosing product behavior, return the conflicting requirements and evidence for a human ruling.

## Fix

Address every blocking finding with a fix or evidence-backed pushback. Reproduce behavior failures on the surface where they appeared before patching. Use the implementation discipline for checks, diagnosis, commits, and pushes. Remove temporary probe residue; retain the run for evidence. The subsequent checking pass grants the verdict.
