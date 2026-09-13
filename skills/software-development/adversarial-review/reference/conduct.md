# Review and fix conduct

## Review

Supply the PR, issue/spec, immutable head/base and intended integration tree, prior findings, and deadline. The reviewer reads source and returns findings; the verifier owns runtime checks and the owner makes fixes.

Every blocking finding names the changed location, violated requirement or standard, and a concrete failure scenario or maintenance cost. Label optional suggestions. Classify design preferences as optional unless they violate a requirement or standard.

LGTM names the reviewed head/base and integration tree. Clear prior findings through a verified fix, accepted pushback, or an explicit ruling. State required CI status: failed checks withhold LGTM; pending checks remain a completion gate.

If deciding the finding requires choosing product behavior, return the conflicting requirements and evidence for a human ruling.

## Fix

Address every blocking finding with a fix or evidence-backed pushback. Reproduce behavior failures on the surface where they appeared before patching. Use the implementation discipline for checks, diagnosis, commits, and pushes. Remove temporary probe residue; retain the run for evidence. The subsequent checking pass grants the verdict.
