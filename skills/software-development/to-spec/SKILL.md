---
name: to-spec
description: Synthesize a settled record into one self-contained HTML spec. Use after the decisions are made. Pure synthesis, no interview or publication.
metadata:
  optional: [diagram-design, technical-writing]
---

# To spec

Turn settled material into the spec it earned. Record choices; make none. Undecided points become Notes, never questions.

Use the `technical-writing` skill for the spec.

1. **Reconcile the record.** Start with the shaping record, then include settled decisions from the current conversation and sweep each decision-informing artifact into Supporting artifacts. The latest explicit ruling wins. Omit superseded requirements, discarded options, and discussion that did not become direction. When revising a spec, read the previous approved revision and preserve each `AC-N` identifier's meaning; amend in place, append, or retire without reusing its identifier.
2. **Write one self-contained HTML spec** in this order:
   - Problem and decided direction.
   - Affected users and their changed experience.
   - Shared system behavior.
   - Implementation decisions, including the constraint or accepted cost when the record gives one.
   - Acceptance criteria with stable `AC-N` identifiers and observable pass-or-fail outcomes.
   - Testing contract when settled: the highest existing public seams and, for each applicable AC, the recorded durable-suite or throwaway-script choice.
   - Scope and exclusions, assumptions, Supporting artifacts, Notes, and a Recommended split when shaping settled one. Omit empty optional sections.
3. **Keep the direction durable.** Stay above file-by-file instructions. A concrete path or prototype-validated fragment is allowed only when it is the reliable pointer to an established pattern or a decision that prose cannot preserve. For each Supporting artifact, record its kind, the question it answered, its one-line takeaway, and its durable pointer; state plainly when evidence exists only in the conversation.
4. **Make review aids earn their space.** Add the smallest useful diagram only when it materially clarifies the direction. Use the `diagram-design` sibling in embedded mode and verify both its fragment and the completed spec. When that sibling is absent, use prose or a table and report the missing diagram support if it materially reduced clarity.
5. **Classify Notes.** Mark each unresolved point as **blocking** (shaping must settle it), **delegated** (the executor may choose within a named boundary), or **deferred** (parked with a named home). A blocking Note means the direction is not ready to publish or build.
6. **Audit fidelity both ways.** Confirm that every current material decision, requirement, exclusion, assumption, and unresolved point is represented, and that every statement in the spec traces to the settled record. Report contradictions or omissions as failures.

Write one untracked scratch file. Return its path, a concise summary, classified Notes, and the fidelity result. Do not publish it or change a ticket.
