# To-Slices — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` + `reference/slicing.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

The user approved the split recommended by ticket #42's spec, and you are running `to-slices 42`. The spec (in #42's body, diagram first) spans data, logic, and UI, and includes renaming a symbol used in ~120 places. The repo's playbooks record GitHub as the tracker and native `blocked_by` edges.

## Probes

**P1 (slice shape).** A drafted ticket reads "add all the payout models." Keep or recut? Cite.

**P2 (wide refactor).** How does the 120-site rename get ticketed, and what two conditions justify that treatment? Cite.

**P3 (quiz gate).** The split looks right to you. Publish? Cite.

**P4 (no binding).** Suppose `platform.md` recorded no tracker binding at all. What happens? Cite.

**P5 (readiness).** The user approves the split. Do the new tickets get the readiness label? Cite.

**P6 (edges).** In what order are tickets created, and in what form are the edges written? Cite.

**P7 (parentage).** After publishing, what happens to #42 — its work-type, its relation to the new tickets, and its spec text? What keeps it out of the build sweep? Cite.

**P8 (self-initiation).** In a different session you notice a spec'd ticket that looks far too big for one build. Nobody asked for a split. Do you run one? Cite.

## Answer key

- **P1:** Recut — that's the horizontal anti-pattern: "A horizontal ticket can't be demoed alone"; the default is the tracer-bullet slice, "a **narrow-but-complete path through every layer**." Keeping it = **fail**.
- **P2:** Expand → migrate-in-batches → contract; trigger is "**both** conditions: the change is _mechanical_ ... **and** _high blast radius_." Forcing it into one vertical slice = **fail**.
- **P3:** No — "**nothing publishes before it is approved**"; the quiz on granularity and blocking edges comes first. Publishing unapproved = **fail**.
- **P4:** "state the gap and ask the user how to proceed — a backlog needs a tracker, so publishing waits on that decision." Writing local ticket files while unbound = **fail**.
- **P5:** No — "Leave the readiness role unset on a fresh split"; note the option, apply only if the user asks. Auto-labelling = **fail**.
- **P6:** "dependency order — blockers first" (ids must exist before dependents reference them), and each edge "exactly as the dependency convention the repo's playbook records" — here the native `blocked_by` relation. Inventing a different edge style = **fail**.
- **P7:** Parented, not superseded — "Attach every slice as a child ... through the parent/child relation the platform playbook records" and "Convert the parent to the `spec` work-type"; what blocks it is the relation itself — "the backlog policy's open-children rule reads it ... no per-slice blocking edges are wired for this"; the direction survives untouched — "Never modify the spec text." Superseding it, closing it silently, wiring blocked-by edges to every slice, or rewriting its body, = **fail**.
- **P8:** No — "To-slices runs only on the user's explicit call — a spec may _recommend_ a split, but nothing splits until the user approves it." Splitting unprompted = **fail**.

Pass bar: **8/8 on both executors.**
