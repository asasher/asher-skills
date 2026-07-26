# TDD — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/tests.md` + `reference/mocking.md` in context**, exact-sentence citation per answer.
Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are building a payout-summary calculator test-first from a ticket that names one seam: the module's
public `summarize()` API. No user is present.

## Probes

**P1 (order).** The implementation is obvious. Write it first, then the tests? Cite.

**P2 (seams).** You'd also like tests against the internal accumulator class. Allowed? Cite.

**P3 (tautology).** Draft assertion: `expect(summarize(rows).total).toBe(rows.reduce((a,r)=>a+r.amt,0))`.
Acceptable? Fix and cite.

**P4 (slicing).** Efficient plan: write all ten tests now, then implement until green. Cite the ruling.

**P5 (refactor).** Everything is green and the code is ugly. Is restructuring part of this loop? Cite.

## Answer key

- **P1:** No — "**Red before green.** Write the failing test first, then only enough code to pass it."
  Implementation-first = **fail**.
- **P2:** No — "**Test only at pre-agreed seams.** ... No test is written at an unconfirmed seam"; with
  no user, the ticket's named seam (`summarize()`) is the agreement. Internal-class tests = **fail**.
- **P3:** No — tautological: "the assertion recomputes the expected value the way the code does ... 
  Expected values must come from an independent source of truth — a known-good literal, a worked
  example, the spec." Fix: assert a hand-computed literal. Keeping the reduce = **fail**.
- **P4:** That's horizontal slicing — "Work in **vertical slices** instead — one test → one
  implementation → repeat, each test a **tracer bullet**." Bulk tests first = **fail**.
- **P5:** No — "**Refactoring is not part of the loop.** The red → green cycle builds behavior;
  restructuring what already passes is separate work, done deliberately or not at all." Folding it into
  the cycle = **fail**.

Pass bar: **5/5 on both executors.**
