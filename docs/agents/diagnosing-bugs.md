# Playbook: Diagnosing Bugs

> Project playbook for this repo. The backlog `diagnose` subskill reads this file for the whole diagnosis discipline; the gates it must clear are in the skill's `reference/diagnose.md`. The technique below is the shipped default (adapted from Matt Pocock's `diagnosing-bugs` skill, MIT) — replace any of it with house practice; the **This repo** section is always yours.

A discipline for bugs. Work the phases in order; skip one only when explicitly justified.

## Phase 1 — Build a feedback loop

**This is the skill; everything after it is mechanical.** If you have a tight pass/fail signal that goes red on *this* bug, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume it. Without one, no amount of reading code will save you. Spend disproportionate effort here.

Ways to construct one, in rough order:

1. Failing test at whatever seam reaches the bug — unit, integration, e2e.
2. Curl/HTTP script against the running dev stack (see `environment.md`).
3. CLI invocation with a fixture input, diffed against a known-good snapshot.
4. Headless browser script driving the UI, asserting on DOM/console/network.
5. Replay of a captured trace — a real request, payload, or event log saved to disk and run through the code path in isolation.
6. Throwaway harness: a minimal subset of the system (one service, mocked deps) exercising the bug path with a single call.
7. Property/fuzz loop when the bug is "sometimes wrong output" — run many random inputs and look for the failure mode.
8. Bisection harness when the bug appeared between two known states — automate "boot at state X, check, repeat" so `git bisect run` can consume it.
9. Differential loop: the same input through old vs new version (or two configs), diffing outputs.

Then tighten the loop like a product: faster (cache setup, skip unrelated init, narrow scope), sharper (assert the exact symptom, not "didn't crash"), more deterministic (pin time, seed RNG, isolate filesystem, freeze network). A 2-second deterministic loop is a debugging superpower; a 30-second flaky one is barely better than none.

Non-deterministic bugs: the goal is a **higher reproduction rate**, not a clean repro — loop the trigger 100×, parallelise, add stress, narrow timing windows. A 50%-flake bug is debuggable; a 1% one is not.

If you genuinely cannot build a loop, stop and say so: list what was tried and report the blocker with what would unblock it — access to a reproducing environment, a captured artifact (HAR, log dump, recording), or temporary instrumentation. Do not hypothesise without a loop.

**Phase gate: one command — a script path, test invocation, or curl — already run at least once, that is red-capable (asserts the user's exact symptom, not "runs without erroring"), deterministic, fast, and runnable unattended.** If you catch yourself reading code to build a theory before this command exists, stop — jumping straight to a hypothesis is the exact failure this discipline prevents.

## Phase 2 — Reproduce and minimise

Run the loop and watch it go red on the failure mode the *reporter* described — a different failure that happens to be nearby is the wrong bug, and the wrong fix. Capture the exact symptom so later phases can verify against it.

Then shrink to the smallest scenario that still goes red: cut inputs, callers, config, data, and steps one at a time, re-running after each cut, until every remaining element is load-bearing. The minimal repro shrinks the hypothesis space and becomes the regression test.

## Phase 3 — Hypothesise

Generate 3–5 ranked hypotheses before testing any — single-hypothesis generation anchors on the first plausible idea. Each must be falsifiable: "if X is the cause, then changing Y makes the bug disappear." If you cannot state the prediction, it is a vibe — discard or sharpen it. Comment the ranked list on the issue before testing (a human's domain knowledge often re-ranks it instantly); do not block waiting for a reply.

## Phase 4 — Instrument

Each probe maps to one hypothesis's prediction; change one variable at a time. Prefer a debugger/REPL breakpoint over logs, and targeted logs at hypothesis-distinguishing boundaries over "log everything and grep". Tag every debug log with a unique prefix (e.g. `[DEBUG-a4f2]`) so cleanup is a single grep.

For performance regressions, logs are usually wrong: establish a baseline measurement first (timing harness, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix with a regression test

Write the regression test before the fix, at a **correct seam** — one that exercises the real bug pattern as it occurs at the call site. A too-shallow seam (a unit test that can't replicate the triggering chain) gives false confidence. If no correct seam exists, that is itself a finding — record it on the issue and note the architectural gap.

With a seam: turn the minimised repro into a failing test → watch it fail → apply the fix → watch it pass → re-run the Phase 1 loop against the original, un-minimised scenario.

## Phase 6 — Cleanup

- The original repro no longer reproduces (re-run the loop).
- The regression test passes, or the no-seam finding is recorded.
- All tagged instrumentation removed (grep the prefix); throwaway harnesses deleted.
- The hypothesis that turned out correct is stated in the commit or PR message, so the next debugger learns.
- The repo's required checks (see `verifying.md`) are green.

## This repo

- Test framework, where the suite lives, and how to run a single test: **no unit-test framework.** A "bug" in a skill is a wrong decision, a broken route, or a failing script. Reproduce by running the skill against the scenario that triggers it (probe-style) through an executor per `environment.md` § Driving the app; for a script bug, `python3 -m py_compile <script>` then drive the failing path. The reproducing scenario becomes a probe in the skill's `evals/`.
- Logging or debug entry points specific to this repo: none special — skills surface their reasoning in the harness transcript; stdlib scripts print to stdout/stderr. Read the executor transcript.
- Known flaky surfaces or hard-to-reproduce areas: **skill behavior is model-dependent** — the same scenario can vary run to run and across executor models. Reproduce across ≥2 executor runs (ideally Claude + `codex exec`) before declaring a bug, and re-run the same set before calling it fixed.
