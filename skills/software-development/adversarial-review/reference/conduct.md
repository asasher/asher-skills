# Reviewer and fixer conduct

Each role receives the PR, issue or spec, pinned head and base, run state, pass deadline, and its promised output. The driver sequences writers and persists the combined outcome.

## Shared rules

- Read the PR's latest run state and verify the supplied refs before working.
- Complete one bounded pass and return its report. Record findings and fixes on the PR so a replacement worker can continue.
- Every report names the input head and base and the observed head at return. Resolve these from git and the PR; a changed input yields a stale report, not an approval of the new head.
- Preserve the pass number and deadline supplied by the driver. A worker restart does not start a new budget.

## Reviewer

- Read and comment only. Run `code-review` against the pinned refs, covering both axes. When behavioral verification runs alongside this pass, leave tests, temporary scripts, and fixtures to that verifier.
- Each blocking finding names a file and line, the violated requirement or standard, and a concrete failure scenario or maintenance cost. Label judgement calls and optional improvements explicitly.
- Optional suggestions do not block LGTM. A structural concern blocks only when it demonstrates a concrete cost or regression at the scope of this change. Existing unrelated cleanup is separate work.
- LGTM requires every blocking finding fixed, accepted as mistaken by this pass, or resolved by an explicit ruling. A fixer's reply alone does not clear it.
- LGTM names the reviewed head and base. Query required CI for that head: failing checks withhold LGTM; pending checks are disclosed. A code reviewer reports behavioral verification separately and never claims to have run another worker's checks.
- When a finding depends on deciding what the product should do, return **product question** with the conflicting requirements and evidence. Leave the behavior unchanged until a human rules.

## Fixer

- Address every supplied blocking finding through a fix or evidence-backed pushback. Optional suggestions can be deferred without extending the loop.
- Reproduce a behavior finding as a failing check on the surface where it appeared before fixing. Runtime-only findings and defects that survive a fix pass use `diagnosing-bugs`; absent it, reproduce and diagnose deliberately before another attempt.
- Run the project's applicable checks after changes, commit, and push. Reply with what changed or why a finding is mistaken, and return the report with the resulting SHA.
- Remove temporary probe residue while retaining its run outside the tracked tree. Leave a clean checkout for the next checks. The driver orders fresh verification and review; the fixer grants neither verdict.
