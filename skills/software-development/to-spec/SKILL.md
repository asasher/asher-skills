---
name: to-spec
description: Synthesize a settled record into one self-contained HTML spec. Use after the decisions are made. Returns a scratch file for the caller to publish.
metadata:
  requires: [diagram-design, writing-for-humans]
  optional: [technical-writing]
---

# To spec

Turn settled material into the spec it earned. Preserve settled choices and classify undecided points as Notes.

Use `writing-for-humans` for the explanation and `technical-writing` for the precise requirements. Design for a tired human deciding whether to approve: make the direction understandable before presenting the full contract.

1. **Reconcile the record.** Start with the shaping record, then include settled decisions from the current conversation and sweep each decision-informing artifact into Supporting artifacts. The latest explicit ruling wins. Omit superseded requirements, discarded options, and discussion that did not become direction. When revising a spec, read the previous approved revision and preserve each `AC-N` identifier's meaning; amend in place, append, or retire without reusing its identifier.
2. **Write one self-contained HTML spec** in this order:
   - For revisions, a concise delta from the last approved hash: changed decisions, added/amended/retired ACs, and their effect on scope or the split.
   - A brief approval overview: the problem, proposed experience, scope, and key decisions, with diagrams that explain the direction at a glance.
   - Problem and decided direction.
   - Affected users and their changed experience.
   - Shared system behavior.
   - Implementation decisions, including the constraint or accepted cost when the record gives one.
   - Acceptance criteria with stable `AC-N` identifiers and observable pass-or-fail outcomes.
   - Verification risk and rationale when settled, including the named failure paths and data-safety obligations.
   - Testing contract when settled: the highest existing public seams and, for each applicable AC, the recorded durable-test or temporary-check choice.
   - Scope and exclusions, assumptions, Supporting artifacts, Notes, and a Recommended split when shaping settled one. Omit empty optional sections.
3. **Keep the direction durable.** Stay above file-by-file instructions. A concrete path or prototype-validated fragment is allowed only when it is the reliable pointer to an established pattern or a decision that prose cannot preserve. For each Supporting artifact, record its kind, the question it answered, its one-line takeaway, and its durable pointer; state plainly when evidence exists only in the conversation.
4. **Explain the direction visually.** Use `diagram-design` in embedded mode. Substantive specs normally include diagrams: choose a journey or flow for the proposed experience, a relationship diagram for system structure, or a state diagram for lifecycle behavior. Put the overview diagram near the approval overview and any detail diagrams beside the decisions they explain. A small textual change can remain diagram-free. Use short captions and readable labels; replace prose that merely repeats the figure. Keep the full acceptance criteria and implementation contract below the overview, with navigation or expandable supporting detail where useful. Keep blocking Notes, material risks, and approval-relevant tradeoffs visible. Verify each diagram fragment and inspect the completed spec at narrow and wide widths for readability and integration; disclose unavailable visual verification.
5. **Classify Notes.** Mark each unresolved point as **blocking** (shaping must settle it), **delegated** (the executor may choose within a named boundary), or **deferred** (parked with a named home). Blocking Notes hold publication and building until shaping resolves them.
6. **Audit fidelity both ways.** Confirm that every current material decision, requirement, exclusion, assumption, and unresolved point is represented. Trace every statement and diagram relationship to the settled record. Report contradictions or omissions as failures.

Write one untracked scratch file. Return its path, a concise summary, classified Notes, and the fidelity result. The caller owns publication and tracker updates.
