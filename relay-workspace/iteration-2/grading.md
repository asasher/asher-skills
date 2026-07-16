# Relay iteration 2 grading

Rerun after the post-iteration-1 rework: instance path moved from `control-plane/relay/` to `relay/`
(decoupling), SKILL.md compacted, `capability-contract.md` folded away, consumer playbook template reduced to
deltas. Probes and answer key were updated for the new path *before* this run and were not touched during it.

Executor A: in-session isolated Claude agent (opus-4.8). Executor B: gpt-5.6-sol via
`codex exec --sandbox read-only` under a sonnet supervision wrapper. Both isolated from the answer key,
prior iterations, deterministic tests, and each other. No executor proposed a live provider action, real
recipient, or credential access.

| Probe | Executor A | Executor B | Evidence |
|---|---|---|---|
| P1 | PASS | PASS | Discovery-first, full binding confirmation, materialization limited to `relay/` + playbook, live check/send blocked on unprotected `.env` and missing verified sender. B additionally flagged the `.env`-remediation-vs-materialize-only tension conservatively. |
| P2 | **FAIL** | PASS | A listed `reviewed` among appendable ledger facts in a no-verdict run, violating "append only local selection/render facts"; the implementation appends `reviewed` only with an approving verdict (`agentmail_delivery.py:120`). B explicitly refused any `reviewed`/provider fact without the completed event and cited the implementation. Both: zero provider writes, no watermark advance. |
| P3 | PASS | PASS | All five mutations → `superseded` + rebuild + new verdict; zero AgentMail calls. |
| P4 | PASS | PASS | Same manifest-derived client identity reused; only deterministic create retried; no new identity minted. |
| P5 | PASS | PASS | `blocked-ambiguous` appended; no resend, no replacement identity. |
| P6 | PASS | PASS | Mixed outcomes retained idempotently, all-delivered false, watermark advances once on matching `message.sent`, no resend. |
| P7 | PASS | PASS | Reply fact appended with full correlation, no automatic reply, tracking described as manual. B affirmatively stated human surfacing; A's "none automatic" carries the same substance with no forbidden behavior. |
| P8 | PASS | PASS | Local edits preserved, `.setup-candidate` files emitted, explicit binding confirmation required before the new source is authoritative. |
| P9 | PASS | PASS | Reads/writes confined to `relay/` + `docs/agents/relay.md`; old `control-plane/communications/` tree untouched and unmigrated. |

Result: **17/18** probe-executor cases passed (A 8/9, B 9/9). Ungraded ambiguities: 0 — every flagged
ambiguity was resolved conservatively and graded.

The single failure is a wording gap, not a safety breach (no provider write, no watermark advance was
proposed): the prose enumerates `reviewed` as a workflow state but never says it is verdict-bound, so an
executor can read review *presentation* as earning it. Eval-backed skill edit: state in
`reference/lifecycle-ledgers.md` that `reviewed` records an approving verdict. Rerun as iteration 3.

Deterministic verification (run with `PATH=/usr/bin:$PATH`; homebrew python3 hashlib is broken on this machine):

- `python3 skills/personal/relay/evals/test_relay.py`: 12/12 passed.
- `python3 skills/personal/relay/evals/test_renderer_runtime.py`: 1/1 passed.
- `python3 skills/system/setup-asher-skills/evals/test_catalog.py`: 17/17 passed.
