# Dual-executor probe results (ac-10, ac-11) — issue #16

Probes W1–W4 (`skills/review-loop/evals/probes.md` § The delegated watch), run against final HEAD with
staffing's `rankings-and-routing.md` + `roles-and-fallback.md` added to each executor's readable set so the
watch contract is cross-checked against staffing's actual resolution order.

## Verdict table

| probe | criterion | Opus (in-session) | gpt-5.5 (`codex exec`) |
|-------|-----------|-------------------|------------------------|
| W1 (delegate, don't block inline; verdict from completion, no poll) | ac-10 | PASS | PASS |
| W2 (from Codex → Floor model gpt-5.5; generic `route` → most capable, avoided) | ac-3, ac-11 | PASS | PASS |
| W3 (re-arm on 124; cursor lossless; no script change) | ac-4, ac-7 | PASS | PASS |
| W4 (wake without polling; durable backstop; both gates) | ac-5, ac-6 | PASS | PASS |
| **Contract vs. staffing resolution order** | ac-11 | **CONSISTENT (no contradiction)** | consistent — generic route flagged wrong mechanism |

Both executors correct action + correct citation on all four probes. The Opus executor returned an explicit
"CONSISTENT" verdict after walking staffing's resolution order steps 1–4; the codex executor independently
identified that a generic `staffing route` of the unpinned no-capability watch task ranks by
`intelligence > taste > cost` and returns the most capable model — the reason the contract reads the Floor
directly instead.
