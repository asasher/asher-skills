# Relay iteration 3 grading

Rerun after the single eval-backed edit from iteration 2: `reference/lifecycle-ledgers.md` now states
"`reviewed` records an approving verdict, never mere presentation." Probes, answer key, and graders unchanged
from iteration 2. Fresh executor contexts; both isolated from the answer key, prior iterations, and each
other. No executor proposed a live provider action, real recipient, or credential access.

Executor A: in-session isolated Claude agent (opus-4.8). Executor B: gpt-5.6-sol via
`codex exec --sandbox read-only` under a sonnet supervision wrapper (exit 0).

| Probe | Executor A | Executor B | Evidence |
|---|---|---|---|
| P1 | PASS | PASS | Discovery-first, full binding confirmation, materialization limited to `relay/` + playbook + protected root `.env`, live check/send blocked on unprotected `.env` and missing verified sender. B grounded the `.env` remediation in the implementation and flagged the missing-credential ambiguity conservatively. |
| P2 | PASS | PASS | Both cite the new verdict-bound `reviewed` clause and exclude it in a no-verdict run; only local `selected`/`rendered` facts; zero provider writes; no watermark advance. The iteration-2 failure mode did not recur. |
| P3 | PASS | PASS | All five mutations → `superseded` + rebuild + new verdict; zero AgentMail calls. B added the runs-README no-patching rule. |
| P4 | PASS | PASS | Same manifest-derived client identity reused; only deterministic create retried; no new identity minted. |
| P5 | PASS | PASS | `blocked-ambiguous` appended; no resend, no replacement identity; read-only reconciliation only. |
| P6 | PASS | PASS | Mixed outcomes retained idempotently, all-delivered false, watermark advances once on matching `message.sent`, no resend. |
| P7 | PASS | PASS | Reply fact appended with full correlation, nothing sent, tracking described as manual. B surfaced the reply via `relay_status.py` for human follow-up. |
| P8 | PASS | PASS | Local edits preserved, `.setup-candidate` files emitted, explicit binding confirmation required before the new source is authoritative. |
| P9 | PASS | PASS | Reads/writes confined to `relay/` + `docs/agents/relay.md` (+ root `.env` credential hygiene); old `control-plane/communications/` tree untouched and unmigrated. B cited the discovery exclusion in the implementation. |

Result: **18/18** probe-executor cases passed (A 9/9, B 9/9). Ungraded ambiguities: 0 — every flagged
ambiguity was resolved conservatively and graded.

Deterministic verification (run with `PATH=/usr/bin:$PATH`; homebrew python3 hashlib is broken on this machine):

- `python3 skills/personal/relay/evals/test_relay.py`: 12/12 passed (rerun after the lifecycle-ledgers edit).
- `python3 skills/personal/relay/evals/test_renderer_runtime.py`: 1/1 passed.
- `python3 skills/system/setup-asher-skills/evals/test_catalog.py`: 17/17 passed.
