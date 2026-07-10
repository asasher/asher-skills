# In-session executor (Claude/Opus subagent) — probes P1–P4 (ac-7)

Executor: Claude subagent via the Agent tool (in-session), the in-session deployment target.
Context given: `docs/agents/backlog-policy.md` + `.claude/skills/backlog/reference/issue-loop.md` only.
Scenario: a groomed `ready-for-agent` issue — "Write the v2 launch announcement memo for the blog." No code changes, no test.

> Delivery note: the in-session peer channel could not address this thread, so the executor's graded answers
> were relayed through the run thread. Substance recorded below; both executors agree across all probes.

## Result (as reported)

- **P1** — routes the launch-memo scenario to work-type **`draft`**, citing `backlog-policy.md` (the memo is a
  taste/fit artifact with no testable spec).
- **P2** — definition of done is the **review-loop human verdict**; the mechanical `verify` step is skipped,
  citing the `issue-loop.md` step-4 draft exception.
- **P3** — the artifact is **kept** / committed after approve (not deleted).
- **P4** — correctly rebuts the "delete it like a prototype" teammate: `draft` keeps the deliverable, whereas
  `prototype` deletes the throwaway and keeps only the answer.

## Grade

| Probe | Answer-key criterion | Result |
|---|---|---|
| P1 | work-type = `draft` | PASS |
| P2 | done = human review verdict; no mechanical verify | PASS |
| P3 | artifact kept | PASS |
| P4 | draft ≠ prototype; not deleted (ac-9 non-conflation) | PASS |

4/4.
