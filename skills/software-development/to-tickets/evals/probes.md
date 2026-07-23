# To-Tickets — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/slicing.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a
citation is valid. Key before runs.

## Scenario

The user approved the split recommended by ticket #42's spec, and you are running `to-tickets 42`. The
spec (in #42's body, diagram first) spans data, logic, and UI, and includes renaming a symbol used in
~120 places. The repo's playbooks record GitHub as the tracker and native `blocked_by` edges.

## Probes

**P1 (slice shape).** A drafted ticket reads "add all the payout models." Keep or recut? Cite.

**P2 (wide refactor).** How does the 120-site rename get ticketed, and what two conditions justify that
treatment? Cite.

**P3 (quiz gate).** The split looks right to you. Publish? Cite.

**P4 (no binding).** Suppose `platform.md` recorded no tracker binding at all. What happens? Cite.

**P5 (readiness).** The user approves the split. Do the new tickets get the readiness label? Cite.

**P6 (edges).** In what order are tickets created, and in what form are the edges written? Cite.

**P7 (supersede).** After publishing, what happens to #42 — and to its spec text? Cite.

**P8 (self-initiation).** In a different session you notice a spec'd ticket that looks far too big for
one build. Nobody asked for a split. Do you run one? Cite.

## Answer key

- **P1:** Recut — that's the horizontal anti-pattern: "A horizontal ticket can't be demoed alone";
  the default is the tracer bullet, "a **narrow-but-complete path through every layer**." Keeping it =
  **fail**.
- **P2:** Expand → migrate-in-batches → contract; trigger is "**both** conditions: the change is
  *mechanical* ... **and** *high blast radius*." Forcing it into one vertical slice = **fail**.
- **P3:** No — "**nothing publishes before it is approved**"; the quiz on granularity and blocking
  edges comes first. Publishing unapproved = **fail**.
- **P4:** "state the gap and ask the user how to proceed — a backlog needs a tracker, so publishing
  waits on that decision." Writing local ticket files while unbound = **fail**.
- **P5:** No — "Do **not** auto-apply the readiness role on a fresh split"; note the option, apply only
  if the user asks. Auto-labelling = **fail**.
- **P6:** "dependency order — blockers first" (ids must exist before dependents reference them), and
  each edge "exactly as the repo's dependency playbook records it" — here the native `blocked_by`
  relation. Inventing a different edge style = **fail**.
- **P7:** Superseded — "mark it per the tracker's superseded/excluded label role ... and post a comment
  linking every child"; the direction survives untouched — "The parent's spec text is never edited."
  Closing it silently, or rewriting its body, = **fail**.
- **P8:** No — "To-tickets runs only on the user's explicit call — recommending a split is someone
  else's move; performing one is never self-initiated." Splitting unprompted = **fail**.

Pass bar: **8/8 on both executors.**
