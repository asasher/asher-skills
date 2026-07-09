# to-tickets — acceptance-criteria verdict (HEAD c85c6a7)

Dual-executor situated read-only probe eval per `docs/patterns/probe-evals.md`, graded correct-action-and-citation
against `skills/to-tickets/evals/probes.md` § Answer key. Structural criteria additionally confirmed by
file/grep/YAML checks. Executors: Opus in-session (Agent tool) + `codex exec --sandbox read-only` (gpt-5.5).

| Criterion | Probe | Opus | codex exec | Structural check |
|-----------|-------|------|-----------|------------------|
| ac-1  skill shape + no cross-skill imports | P1 | PASS | PASS | layout mirrors primitives; `grep` cross-skill imports → none |
| ac-2  three-part dependency surface (backlog = playbook) | P2 | PASS | PASS | three pointer kinds present; backlog framed as playbook |
| ac-3  inputs (spec primary; plan/conversation) | P3 | PASS | PASS | — |
| ac-4  vertical slices (tracer bullet, 3 properties) | P4 | PASS | PASS | — |
| ac-5  wide-refactor expand→migrate→contract, both-conditions trigger | P5 | PASS | PASS | — |
| ac-6  quiz-the-user human-confirmation (vs to-spec) | P6 | PASS | PASS | — |
| **ac-7  correct `- [ ] depends on #N` edges + blockers-first (LOAD-BEARING)** | P7 | PASS | PASS | 13 verbatim lowercase markers; 0 capital markers |
| ac-8  publish through bound tracker, generic vocabulary | P8 | PASS | PASS | — |
| ac-9  readiness default → groom (apply-on-approval noted) | P9 | PASS | PASS | — |
| ac-10 no paths/code + never modify parent | P10 | PASS | PASS | — |
| ac-11 codex manifest well-formed, implicit=false | P11 | PASS | PASS | `ruby -ryaml` parses → `implicit=false` |
| ac-12 dual-executor read-only probe eval ships | P12 | N/A (file withheld) | N/A | probes.md present: key covers ac-1..ac-11, dual-executor, read-only |

**Result: 11/11 answerable probes pass on both executors (P12 N/A by design); all 12 criteria satisfied.**
Zero ambiguity flags at HEAD c85c6a7 — the iteration-1 casing flag was resolved by emitting the marker verbatim
in the playbook's lowercase form. Publishing is exercised read-only (no `gh issue create` runs; no stray issues),
by the ratified read-only-eval decision.

## Structural check log (HEAD c85c6a7)

```
layout: SKILL.md README.md agents/openai.yaml evals/probes.md reference/slicing.md reference/template-guide.md templates/ticket.md templates/tickets.md
openai.yaml: parses OK; display=To-Tickets implicit=false
SKILL frontmatter: name=to-tickets user-invocable=true
cross-skill imports: none
capital 'Depends on #' markers: none
lowercase 'depends on #' markers: 13
case-insensitivity claim: none
```

Transcripts: `probe-eval-opus.md` (Opus in-session), `probe-eval-codex.txt` (codex exec).
