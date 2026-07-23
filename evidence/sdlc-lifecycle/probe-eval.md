# Evidence — sdlc-lifecycle queue probe eval (#85/#86/#87)

Dual-executor per `docs/agents/probe-evals.md`: Claude/Opus subagent + gpt-5.6-sol
(`codex exec --sandbox read-only`, session 019f75de-65c6-76e3-8741-9e6e0378289f), executors blind to keys,
exact-sentence citations required. Probes + keys: `to-spec/evals` § Spec-as-gate, `to-tickets/evals`
§ Publishing-contract, `bare-minimum-ux/evals`, `backlog/evals` § Seam probes.

Run 2026-07-18, branch `sdlc-lifecycle` (queue commit + fixes).

| Set | Claude | gpt-5.6-sol | Notes |
|---|---|---|---|
| to-spec P-G1–G3 (fidelity gate, approval effects, no plan stage) | 3/3 | 3/3 | both named the blocking-Note stop and the thin-projection "links never content" rule |
| to-tickets P-H1–H3 (native edges, no local files, readiness audit) | 3/3 | 3/3 | codex additionally derived the exact `gh api` blocked_by verbs; both refused the vibes ticket naming all failed fields |
| bare-minimum-ux P-C1–C2 (precedence, never-fork) | 2/2 | 2/2 | overlay-wins and refuse-to-inline, both cited |
| backlog seams P-S1–S3 (queue of one, criteria without a ticket, UI gate) | 2/2 + flag | 2/2 + flag | **both executors independently flagged that the UI-gate text was absent from `docs/agents/verifying.md`** — a real gap (the section had shipped only in the template); fixed in the same branch (§ UI surfaces added to the instance). Flag-with-citation is a pass per the probes' own rule, and the flag caught a genuine defect. |

**Score: 22/22 (11/11 per executor), with P-S3's dual flag converted into a fix.** Earlier slices' evals on
this branch: `evidence/80-decouple-planning/probe-eval.md` (12/12), `evidence/84-interview-skills/probe-eval.md` (30/30).
Combined branch total: **64/64.**
