# In-session executor (Claude/Opus subagent) — probe P5, grooming reachability

Executor: Claude subagent via the Agent tool (in-session), the in-session deployment target.
Context given: `docs/agents/backlog-policy.md` + `skills/backlog/reference/groom.md` (the grooming surface).
Scenario: the launch-memo issue, ungroomed. Prompt: at groom.md step 2, which work-type do you propose?

## Result

PASS — the executor proposed work-type **`draft`** for the judgment-terminal memo, citing the new
`groom.md` step-2 line ("Propose `draft` for judgment-terminal work whose correctness is taste/fit — a memo,
copy, a synthesis, code docs, with no testable spec to run against."). It did not fall back to
bug/enhancement/refactor — confirming the route is reachable from grooming.

| Probe | Answer-key criterion | Result |
|---|---|---|
| P5 | grooming proposes `draft` (route reachable from groom) | PASS |
