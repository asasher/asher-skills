# Evidence — #80 enhancement degating probe eval

Pre-deployment probe eval for the decoupled enhancement route, per `docs/agents/probe-evals.md`
(dual-executor: Claude subagent + gpt-5.6-sol via `codex exec --sandbox read-only`). Probes and prewritten
answer key: `skills/delivery/backlog/evals/probes.md` § Enhancement degating probes (issue #80). Executors
were given only the named surface files (issue-loop.md / groom.md / run.md + docs/agents/backlog-policy.md)
and were barred from `evals/`; both required file + exact-sentence citations.

Run 2026-07-18, branch `80-decouple-planning-from-run` @ 326548d.

## Results

| Probe | Checks | Claude (Opus subagent) | gpt-5.6-sol (codex exec, session 019f75b7-bd73-7432-a5d3-03dc186f697e) |
|---|---|---|---|
| P-D1 | no gate; JIT tactical plan recorded in thread + PR body | PASS — cited enhancement bullet + "no in-run planning approval gate" | PASS — cited issue-loop.md:30 verbatim |
| P-D2 | `needs-spec` on invalidation; comment finding, drop claim, no PR; never settle product judgment in-thread | PASS — full action set + not-done set; also cited policy role definition | PASS — full action set + "do not choose a replacement schema decision" |
| P-D3 | (a) delegated → settle/prototype in-thread; (b) strategic → `needs-spec`, never prototype | PASS both halves | PASS both halves — cited issue-loop.md:33 |
| P-E1 | groom stamps `needs-spec`; not `needs-info` (reporter owes no facts), not `ready-for-agent` | PASS — route-judgment sentence + facts-vs-shaping distinction | PASS — route-judgment sentence + both exclusions cited |
| P-E2 | dispatch record: surface, coordination, reason, `route: direct` line | PASS — all four fields + "grooming gap" clause | PASS — all four fields + groom.md:34 admission clause |
| P-F1 | run clears `in-flight`, sets `needs-spec`, continues; no mid-run planning gate | PASS — step 6 quote + groom's "never pauses for planning approval" | PASS — step 6 quote + correctly composed the `returned` terminal classification |

**Score: 12/12 (pass bar: 6/6 on both executors — met).** No probe was answered by settling product judgment
in-thread, invoking a planning skill, conflating `needs-info` with `needs-spec`, or pausing the run.

Raw executor transcripts: session task outputs (Claude subagent + codex wrapper relay), grading performed
against the prewritten key without executor access to it.
