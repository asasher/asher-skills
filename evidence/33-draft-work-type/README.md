# Evidence — #33 add a `draft` work-type

Change type: **skill behavior change** (backlog work-type taxonomy + routing). Per `docs/agents/evidence.md`,
the proof is the probe-eval result — the executor transcripts plus a pass/fail table mapping each probe to its
answer-key criterion — not a screenshot. Captured after adversarial review converged (LGTM at `ba6b013`).

## Acceptance-criteria verdict (plan `plans/33-draft-work-type.html`, ids ac-1..ac-9)

| Criterion | How checked | Result |
|---|---|---|
| ac-1 `draft` role in both policy copies | [file-checks](file-checks-ac1-ac6.txt) | PASS |
| ac-2 done = human review verdict; no mechanical verify | [file-checks](file-checks-ac1-ac6.txt) | PASS |
| ac-3 artifact kept + prototype contrast | [file-checks](file-checks-ac1-ac6.txt) | PASS |
| ac-4 code-docs named | [file-checks](file-checks-ac1-ac6.txt) | PASS |
| ac-5 step-3 draft route in both issue-loop copies | [file-checks](file-checks-ac1-ac6.txt) | PASS |
| ac-6 step-4 verify degeneracy in both copies | [file-checks](file-checks-ac1-ac6.txt) | PASS |
| ac-7 Claude in-session executor routes → draft | [claude-opus-p1-p4](claude-opus-p1-p4.md) | PASS (4/4) |
| ac-8 gpt-5.5/codex executor routes → draft | [codex-gpt5.5-p1-p4](codex-gpt5.5-p1-p4.md) | PASS (4/4) |
| ac-9 neither executor conflates draft with prototype | P4 on both executors | PASS |

## Reachability (added after review found groom couldn't assign `draft`)

| Probe | Executor | Result |
|---|---|---|
| P5 grooming proposes `draft` | Claude/Opus in-session | [PASS](claude-opus-p5.md) |
| P5 grooming proposes `draft` | gpt-5.5 via codex | [PASS](codex-gpt5.5-p5.md) |

Both executors agree across all probes (P1–P5). The `draft` label exists on the tracker
(`#BFD4F2`), and all five source↔`.agents` mirror pairs are byte-identical (see file-checks).
