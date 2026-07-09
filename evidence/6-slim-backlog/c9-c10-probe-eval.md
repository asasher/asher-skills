# Probe-eval — #6 slim backlog composes primitives by name (ac-9, ac-10)

Dual executor per `docs/agents/environment.md` § Driving the app: an in-session
Claude (Opus 4.8) subagent and gpt-5.5 via `codex exec -s read-only`. Each read
only `skills/backlog/SKILL.md` + `reference/issue-loop.md` (and any bundled ref
they point to), unaware of the answer key, then narrated the enhancement branch
and the full loop.

## Pass/fail table

| AC | Criterion | Opus executor | gpt-5.5 executor |
|----|-----------|---------------|------------------|
| ac-9 | Enhancement composes: `plan` skill by name → approval gate held by `plan` → **backlog commits the approved plan + writes the tracker digest (dev-tail)** → `implement`; `prototype` skill settles blocking design questions | PASS | PASS |
| ac-10 | Loop runs: roster = `staffing` skill; presentation/review = `review-loop` skill; bug = `reference/diagnose.md` owned by backlog (not a sibling); no deleted reference cited as openable | PASS | PASS |

Both executors independently produced matching answers and neither named
`reference/{plan,prototype,staffing,presenting}.md` as a file they would open —
they identified those steps as sibling-skill-handled.

## Opus 4.8 executor — verbatim key points
- Enhancement: "invoke the `plan` skill by name … it decides plan-or-skip, writes the HTML plan, and holds the approval gate." "backlog owns the dev-tail … commits the plan to the work branch before dispatching build, and writes the tracker posterity digest." Then implement → verify → PR → adversarial-review → evidence. Blocking design question → the `prototype` skill by name.
- Roster: the `staffing` skill (orchestrator/builder/checker/floor). Surface: the `review-loop` skill.
- Bug: `reference/diagnose.md` — owned by backlog, not a sibling.
- Files opened for enhancement: issue-loop, implement, verify, adversarial-review, evidence. "Handled by another skill (no bundled reference file exists — confirmed absent): planning → the `plan` sibling; blocking design question → the `prototype` sibling; staffing → `staffing`; presentation → `review-loop`."

## gpt-5.5 (codex) executor — verbatim key points
- "The `plan` skill produces the HTML plan, decides plan-or-skip, settles blocking design questions by composing `prototype`, and holds the approval gate." "After approval, backlog's issue thread owns the dev-tail: it commits the approved plan to the work branch and writes the tracker posterity digest."
- "Model roster / builder / checker / fallback roles come from the `staffing` skill." "Presentation surface and interactive review come from the `review-loop` skill."
- "BUG uses `skills/backlog/reference/diagnose.md`. That is a bundled backlog reference, not a sibling skill."
- "No `reference/plan.md` or `reference/prototype.md`: those steps are handled by sibling skills `plan` and `prototype`."
