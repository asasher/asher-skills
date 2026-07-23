# Diagnosis — six phases

Work the phases in order; skip one only with an explicit justification.

## 1. Build a red-capable feedback loop

Spend disproportionate effort on one tight pass/fail signal for the reporter's exact symptom. Try, in rough
order: a failing test at the real seam; HTTP or CLI fixture script; headless browser assertion; captured-trace
replay; minimal harness; property/fuzz loop; automated bisection; differential old/new comparison.

Tighten the loop like a product: make it faster, assert the precise symptom, and remove nondeterminism by
pinning time, randomness, filesystem, and network. For a flaky bug, raise and record the reproduction rate
with repetition, stress, or narrowed timing windows until the signal is useful.

**Gate:** name one unattended command already run at least once, with captured output, that drives the actual
bug path, can go red on this exact symptom and green after the fix, is deterministic enough to trust, and runs
in seconds rather than minutes.

If no such loop is possible, stop. List what was tried and request the missing reproducing environment,
captured artifact, or permission for temporary instrumentation. Do not hypothesize without a loop.

## 2. Reproduce and minimise

Run the loop and confirm it shows the reported failure—not a nearby failure. Capture the exact error, output,
or timing. Then remove inputs, callers, configuration, data, and steps one at a time, rerunning after each cut.

**Gate:** the smallest scenario still goes red and every remaining element is load-bearing.

## 3. Rank falsifiable hypotheses

Write 3–5 hypotheses before testing any. Rank them. Each names a prediction: “If X is the cause, changing Y
will make the symptom disappear or changing Z will make it worse.” Discard or sharpen any claim without a
prediction. Put the ranked list in the **durable work record** — the ticket, change request, or other
artifact the invoking context treats as this work's record; absent one, a note committed beside the
work — and show it to the user when available; their domain
knowledge may re-rank it, but do not block an unattended run.

**Gate:** every candidate is ranked and falsifiable.

## 4. Instrument predictions

Test one prediction and change one variable at a time. Prefer a debugger or REPL inspection, then targeted
logs only at boundaries that distinguish hypotheses; never log everything and grep. Tag temporary output with
a unique prefix such as `[DEBUG-a4f2]`. For performance regressions, establish a timing/profile/query-plan
baseline and bisect instead of adding logs.

**Gate:** the observations falsify alternatives and name the cause rather than restating the symptom.

## 5. Fix with regression proof

Before the fix, turn the minimal reproduction into a failing test at a seam that exercises the real bug pattern
as it occurs at the call site. Watch it fail, apply the smallest causal fix, watch it pass, then rerun the Phase
1 command against the original unminimised scenario.

If no correct seam exists, record that architectural gap instead of writing a shallow test that cannot catch
the bug. The no-seam finding is valid proof only alongside the original loop going red before and green after.

**Gate:** regression proof passes or the no-seam finding is explicit, and the original loop is green.

## 6. Clean up

- Rerun the original loop and the project's required checks.
- Remove every tagged debug statement and delete throwaway harnesses.
- Record the confirmed hypothesis/root cause in the durable work record.
- Report the regression test, or the no-seam gap and its consequence.

**Done:** the reported symptom is green, proof is durable, no debug residue remains, and required checks have
not regressed.
