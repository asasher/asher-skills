# Probe eval — dual executor (ac-11)

Situated dry-run probes from `skills/review-loop/evals/probes.md`, run against two executors — an Opus
subagent (in-session) and `codex exec --sandbox read-only` (gpt-5.5). Each answer required the correct
action **and** a correct file+sentence citation. Answer key written before the runs; graded against the
plan's ac-1..ac-13.

**Result: 24/24 pass** (12 probes × 2 executors). No ambiguities flagged.

| Probe | Criterion | Opus | Codex |
|-------|-----------|:----:|:-----:|
| P1  | ac-1 (layout / user-invocable / no cross-skill imports) | pass | pass |
| P2  | ac-2 (three-part dependency surface; sibling = none) | pass | pass |
| P3  | ac-8 (free-form kind; no baked-in backlog/plan identity) | pass | pass |
| P4  | ac-3 (compose by name: serve → await; `--kind`) | pass | pass |
| P5  | ac-5 (exit 10 = request_changes; revise + ledger before re-await) | pass | pass |
| P6  | ac-6 (stale-hash approve → 409; can't sign off unseen version) | pass | pass |
| P7  | ac-7 (no surface → local fallback; never a public tunnel) | pass | pass |
| P8  | ac-9 (superseded pattern → compose by name, don't copy) | pass | pass |
| P9  | ac-10 (`openai.yaml` well-formed; `allow_implicit_invocation: false`) | pass | pass |
| P10 | ac-6 (reconcile via hash-bound approve event; no version stamps) | pass | pass |
| P11 | ac-13 (path-prefix submit: mount-relative client + suffix-tolerant server) | pass | pass |
| P12 | ac-12 (backlog untouched / non-breaking; rewire deferred) | pass | pass |
