# Task: Peer-review the goodwork eval harness, then fix what you find

You are reviewing `goodwork-workspace/eval/harness/` (run-pair.sh, assert.py, judge.sh, run-suite.sh, README.md) as a skeptical second engineer. The specs it must satisfy: `BRIEF-harness.md` and `BRIEF-personas.md`. The persona docs in `goodwork-workspace/eval/personas/` are now final — the harness was written against the spec before they existed, so mismatches are likely.

## Review dimensions (cover all)

1. **Spec conformance**: every deliverable and behavior in BRIEF-harness.md present and correct — isolation per run, N seeds, turn cap, transcript capture, hard assertions, codex-as-judge, aggregate report.
2. **Persona-file reconciliation**: parse the ACTUAL persona files. Does run-pair.sh extract actor instructions/backstory record the way the files are actually structured? Does judge.sh feed the ACTUAL grading-key format? Do the binary gates in personas/README.md map to concrete checks somewhere (assert.py or judge)? Fix any drift on the harness side, not the persona side.
3. **CLI correctness**: verify `claude -p` session-continuation flags against `claude --help` output (run it), and `codex exec` invocation syntax against `codex exec --help`. The author flagged uncertainty here — settle it empirically.
4. **Assertion soundness**: for each hard assertion in assert.py, ask: can it false-positive (pass a bad run) or false-negative (fail a good run)? The one-question-per-turn heuristic and the approval-gate grep are the suspects. Tighten or, where a heuristic is irreducibly fuzzy, move that check into the judge rubric and say so in README.
5. **Failure handling**: what happens when a subagent call hangs, returns empty, or the actor breaks character? There must be timeouts and a run-level FAIL/ERROR distinction (an infra error must not count as a skill failure in the report).
6. **Token economy**: no step should re-send the full transcript when a tail suffices; the judge should be called once per run, not per fact.

## Rules

- Fix issues directly in the harness files. For each fix, add one line to `goodwork-workspace/eval/REVIEW-FINDINGS.md`: severity (blocker/major/minor), what was wrong, what you changed.
- Anything you can verify by running cheaply (bash -n, python syntax, --help output, the existing fake-agent smoke mode), verify — don't speculate.
- Do NOT run a real eval (no live claude/codex subject calls beyond --help).
- If something needs a human decision, put it under "Open questions" in REVIEW-FINDINGS.md instead of guessing.

Finish by printing: count of blockers/majors/minors fixed, and the open questions verbatim.
