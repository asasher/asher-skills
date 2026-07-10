# Independent executor (gpt-5.5 via `codex exec`) — probe P5, grooming reachability

Command: `codex exec -m gpt-5.5 -s read-only --skip-git-repo-check --cd <worktree>`
Context given: `docs/agents/backlog-policy.md` + `skills/backlog/reference/groom.md` (the grooming surface — not `issue-loop.md`).
Scenario: the same launch-memo issue, ungroomed. Prompt: at groom.md step 2, which work-type do you propose?

## Answer (verbatim)

Propose `draft`. The exact sentence in groom.md is: "Propose `draft` for judgment-terminal work whose correctness is taste/fit — a memo, copy, a synthesis, code docs, with no testable spec to run against."

## Grade

| Probe | Answer-key criterion | Result |
|---|---|---|
| P5 | grooming proposes `draft` (route reachable from groom) | PASS |
