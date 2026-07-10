# Independent executor (gpt-5.5 via `codex exec`) — probes P1–P4 (ac-8)

Command: `codex exec -m gpt-5.5 -s read-only --skip-git-repo-check --cd <worktree>`
Context given: `docs/agents/backlog-policy.md` + `.claude/skills/backlog/reference/issue-loop.md` only.
Scenario: a groomed `ready-for-agent` issue — "Write the v2 launch announcement memo for the blog — 3–4 paragraphs, in our voice, covering what shipped and why it matters." No code changes, no test.

## Answer (verbatim)

**P1** — It routes as `draft`: the issue asks for a memo, a taste/fit prose artifact with no testable spec. Citation: `docs/agents/backlog-policy.md`: "Recognizing `draft`: the deliverable is an artifact judged by taste/fit — a memo, copy, a synthesis, code docs — with no testable spec to run against."

**P2** — Complete means the human review verdict passes; no mechanical `verify` pass/fail gates it. Citation: `.claude/skills/backlog/reference/issue-loop.md`: "A `draft` has no testable spec, so this step is skipped — it degenerates to \"the review gate passed\": the `review-loop` verdict from step 3 stands in for verify."

**P3** — The memo is kept, committed, and merged after approve. Citation: `.claude/skills/backlog/reference/issue-loop.md`: "Keep the artifact: commit it to the work branch (unlike `prototype`, which deletes its throwaway — draft keeps the thing it made)."

**P4** — The teammate is wrong: this is `draft`, not `prototype`; draft keeps the produced memo, prototype keeps only the answer/gist and deletes the throwaway artifact. Citation: `docs/agents/backlog-policy.md`: "The artifact is kept (committed and merged): that is the line against `prototype`, which is throwaway — keep the answer, delete the artifact."

## Grade

| Probe | Answer-key criterion | Result |
|---|---|---|
| P1 | work-type = `draft` | PASS |
| P2 | done = human review verdict; no mechanical verify | PASS |
| P3 | artifact kept | PASS |
| P4 | draft ≠ prototype; not deleted (ac-9 non-conflation) | PASS |

4/4.
