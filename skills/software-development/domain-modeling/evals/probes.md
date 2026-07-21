# Domain Modeling — situated dry-run probes

Per `docs/agents/probe-evals.md`: both executors (Claude subagent + `codex exec --sandbox read-only`), with
**only `skills/thinking/domain-modeling/SKILL.md`, `reference/context-format.md`, and
`reference/adr-format.md` in context**, exact-sentence citations required. Key written before any runs.

## Scenario

You are running `domain-modeling` alongside a design conversation in a repo with no `CONTEXT.md` and no
`docs/adr/`.

## Probes

**P1 (inline, lazy creation).** The conversation just settled that "Payout" means the money movement and
"Settlement" the vendor's confirmation. There's no CONTEXT.md. Do you note this for later? Cite.

**P2 (three-gate ADR).** The user picked `snake_case` for new API field names — easy to change later, mildly
interesting. Offer an ADR? Cite the gates and say which fails.

**P3 (three-gate ADR, positive).** The user chose manual SQL over the ORM the whole codebase uses, for a
measured 40× hot-path win, after seriously considering the ORM. Offer an ADR? What can it look like at
minimum? Cite.

**P4 (glossary boundary).** While writing the "Payout" entry you're tempted to add "processed by
`PayoutWorker` via the Redis queue." Allowed? Cite.

**P5 (challenge).** Mid-conversation the user says "when the account cancels…" but CONTEXT.md defines
Customer and User as distinct, and "account" as *Avoid*. What do you do, and when? Cite.

## Answer key

- **P1:** Write now — "A resolved term goes into `CONTEXT.md` right then" / "Create it when the first term
  resolves." Batching for later = **fail**.
- **P2:** No ADR — gate 1 (**hard to reverse**) fails: "changing the decision later costs something real"
  does not hold; "Any gate failing → no ADR." Offering one = **fail**.
- **P3:** Yes — all three gates hold (lock-in cost, a future reader would wonder, real alternatives). Minimum
  form: "An ADR can be a single paragraph." Refusing, or demanding a long template, = **fail**.
- **P4:** No — "`CONTEXT.md` is a glossary and nothing else — no implementation details, no spec content, no
  scratch notes." Adding it = **fail**.
- **P5:** Challenge **immediately**, not at the end: "A term that conflicts with `CONTEXT.md` gets called out
  immediately," with the which-is-it question. Silently normalizing, or deferring to a wrap-up = **fail**.

Pass bar: **5/5 on both executors.**
