# Evidence — #34 Harden backlog setup for existing non-trivial code projects

This is a docs/contract change with no running app. Per `docs/agents/evidence.md` (the no-running-app
case) and the approved plan's *What's required* section, the evidence is a **situated dry-run probe**, not
screenshots: an independent, differently-modeled executor (gpt-5.5 via `codex exec`) reads *only* the
hardened reference/template files and applies them to a synthetic inherited repo, so the artifacts it emits
show whether the hardened contract actually binds to a real codebase.

Captured against final HEAD `84383e1` (after adversarial review converged to `LGTM`).

- [`dry-run-probe-scenario.md`](dry-run-probe-scenario.md) — the probe prompt: a synthetic inherited repo
  (Next.js + TypeScript + Postgres, GitHub-Actions CI merge-gate, shared `node_modules`/`.next`/test DB,
  Jira tracker with an arbitrary label taxonomy + native "is blocked by" links, ~300 open issues, team wants
  parallel).
- [`dry-run-probe-transcript.md`](dry-run-probe-transcript.md) — the executor's output: the four setup
  artifacts + a self-assessment.

## What the transcript proves, by criterion

| Probe self-check | Criteria | Result |
|------------------|----------|--------|
| A1 — checks recorded by verified invocation; CI `lint/typecheck/test/build` a distinct merge gate | AC1, AC2, AC11 | pass |
| A2 — login + navigate to `/dashboard/settings` recorded beyond seed | AC3 | pass |
| A3 — singleton list includes `node_modules`, `.next`, `myapp_test` alongside container/port/URL | AC5, AC6 | pass |
| A4 — `serialize-verification` a hard constraint naming the forcing singletons despite the parallel ask | AC7 | pass |
| A5 — `Type:*` labels mapped, `P0`/`area/*` neutral, existing labels reused not duplicated | AC8 | pass |
| A6 — dependencies bound to Jira's native "is blocked by", not the GitHub task-list fallback | AC10 | pass |
| A7 — groom batches ~300 issues, dedupes without re-litigating settled ones | AC9 | pass |

AC4 (real-app evidence over probes), AC12 (versioned + migratable), and AC13 (internal consistency) are
text-review criteria — confirmed against the named files and the cross-reference sweep, and hardened further
in the adversarial-review fix round (red-suite handling, verdict asymmetry, and the re-stamp/migration
correctness fix).
