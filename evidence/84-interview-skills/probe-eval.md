# Evidence — #84 interview / domain-modeling / interview-with-docs probe eval

Pre-deployment probe eval per `docs/agents/probe-evals.md` (dual-executor: Claude/Opus subagent +
gpt-5.6-sol via `codex exec --sandbox read-only`, session 019f75d2-eb0a-7412-948f-6493861e0021). Probes and
prewritten keys ship in each skill's `evals/probes.md`; executors saw only the named surface files, never
`evals/`, and cited exact sentences.

Run 2026-07-18, branch `84-interview-domain-modeling` @ c400bdc.

## Results

| Set | Probes | Claude | gpt-5.6-sol |
|---|---|---|---|
| interview (P1–P7): intake-not-ask, frontier vs dependents, fact/decision split, non-blocking lookups, two-test stopping, no-durable-writes boundary, hypothesis shape | 7 | 7/7 | 7/7 |
| domain-modeling (P8–P12): inline write + lazy create, three-gate ADR negative and positive, glossary-only boundary, immediate challenge | 5 | 5/5 | 5/5 |
| interview-with-docs (P13–P15): division of labor, explicit degradation, what survives | 3 | 3/3 | 3/3 |

**Score: 30/30 (pass bar 15/15 per executor — met).** Notable: both executors independently produced the
correct assert-then-confirm hypothesis shape with all four affordances (P7), refused the CONTEXT.md
implementation-detail temptation (P11), and stated the bare-interview/no-writes boundary with the exact
composing-skill hand-off (P6, P13).
