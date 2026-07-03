# Diagnose

Target: a bug issue, a failing report, or a described defect. Runs standalone or as the `bug` branch of the loop.

The technique — building a feedback loop, reproducing, hypothesising, instrumenting, fixing — lives in `docs/agents/diagnosing-bugs.md`; work that playbook end to end. To run or authenticate against the app while reproducing, read `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Gates

The orchestration holds three gates, in order:

1. **Reproduced** — the failure is triggerable on demand through the playbook's feedback loop, or you have stated precisely why it cannot be reproduced and what that implies. No fixing before this gate.
2. **Cause named** — you can state the root cause (not the symptom) and the smallest change that addresses it.
3. **Fixed and confirmed** — the previously failing path passes, the playbook's regression-test requirement is met (or its no-seam finding recorded), and no check the playbook requires has regressed.

If the fix itself demands a contested design decision — more than one plausible rework, expensive to reverse — hand that question to `reference/prototype.md` before committing to one, and record the answer on the issue.

Standalone with a PR intended: continue to `reference/verify.md`, then `reference/evidence.md`.
