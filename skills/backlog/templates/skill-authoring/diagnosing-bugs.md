# Playbook: Diagnosing Bugs

> Project playbook for this repo. The backlog `diagnose` subskill reads this file for the whole diagnosis discipline; the gates it must clear are in the skill's `reference/diagnose.md`. The technique below is the shipped default — replace any of it with house practice; the **This repo** section is always yours.

A discipline for skill bugs. Work the phases in order; skip one only when explicitly justified.

## Phase 1 — Build a feedback loop

Start from either a **failing situated probe** or a **confirmed transcript from a misbehaving skill run**. The loop must assert the reporter's wrong decision, route, or output against a prewritten expectation. Because skill behavior can vary by executor, confirm a behavioral repro through both the in-session executor and the independent CLI executor; preserve both cited transcripts. For a bundled-script bug, use the direct failing invocation instead.

Tighten the loop until it is fast, unattended, and sharp enough to distinguish the reported symptom from a nearby failure. Genuine model-dependent variation is recorded, not hidden: repeat the same scenario and report its reproduction rate when a single run is not deterministic.

If no probe or transcript can reproduce the reported behavior, stop and say so. List what ran, what each executor observed, and what additional scenario, context, or captured transcript would unblock diagnosis. Do not hypothesise without a red-capable feedback loop.

**Phase gate: one failing probe or direct script invocation, already run at least once, that captures the exact reported symptom and can be rerun unattended; for skill behavior, the cited transcripts establish how it reproduces across both executor roles.**

## Phase 2 — Reproduce and minimise

Run the loop and confirm the reporter's failure. Then reduce it one element at a time until every remaining element is load-bearing:

- the smallest prompt input that still triggers the wrong decision;
- the minimum deployment context the executor actually receives; and
- the exact line in `SKILL.md` or a bundled reference that causes or permits the decision.

Re-run after every cut. Do not minimise away the real deployment context merely to create a cleaner example. The resulting scenario is the regression probe; a script repro analogously becomes the smallest direct failing invocation.

## Phase 3 — Hypothesise

Generate 3–5 ranked, falsifiable hypotheses before testing any. Each prediction should name which prompt, `SKILL.md`, reference, routing, or script line would change the observed result. Record the ranked list where the issue thread can review it; do not block waiting for a reply.

## Phase 4 — Instrument

Change one variable at a time. For behavior bugs, use deliberately varied probe context and require citations so the transcript reveals which instruction the executor followed. For script bugs, prefer a debugger or targeted stderr output over broad logging. Tag temporary instrumentation uniquely so cleanup is mechanical.

## Phase 5 — Fix with a regression test

Keep the minimised scenario as a failing probe with its answer-key criterion written before the fix. Apply the smallest instruction or script change, then run the same probe through both executor roles and grade both cited transcripts. Finally rerun the original unminimised scenario. Do not rewrite the answer key to match the fix.

If the skill produces a visual surface, the regression proof also includes the relevant rendered artifact; a screenshot alone does not replace the behavioral probe.

## Phase 6 — Cleanup

- The original repro no longer reproduces through either executor role.
- The minimised scenario remains in the skill's `evals/` as a passing regression probe.
- Both cited transcripts and the per-criterion verdict are retained as evidence.
- All temporary instrumentation and throwaway harness files are removed.
- The causal instruction or script line is stated in the change description.
- The repo's required checks (see `verifying.md`) are green.

## This repo

- Probe location, executor invocations, and how to run one scenario: _<add yours>_.
- Script checks or debug entry points: _<add yours, or "none">_.
- Known model-dependent or hard-to-reproduce surfaces: _<add yours, or "none">_.
