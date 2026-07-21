---
name: shape
description: Shape raw intent into execution-ready work — interview the decisions, look up facts, prototype what paper can't settle, write the model and spec, project tickets. Use when an idea, an issue, or a batch of issues needs its strategic decisions settled before implementation, or when a grooming pass finds needs-shaping work.
argument-hint: "[idea, issue id(s), or nothing — sweeps needs-shaping work]"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [domain-modeling, interview, to-spec, to-tickets]
  optional: [prototype, research, review-loop, staffing]
---

# Shape

Turn raw intent into execution-ready work. A **stateful composite**: everything it settles lands in durable
artifacts — issue threads, `CONTEXT.md` terms, ADRs, specs, tickets — and a resumed session reads those
artifacts, never chat memory. Shape writes documents only; tracker lifecycle labels belong to whoever
orchestrates the tracker (a grooming pass, a run loop) — shape never stamps readiness.

## Subjects

A run takes one or more **subjects**: an idea (no tracker involved), a single issue, or a batch — bare
invocation sweeps everything labeled `needs-shaping`. Group issues into one subject when their decisions
interlock; otherwise one subject per issue, each with its own decision tree. A caller may run each
subject's tree in a subagent; the conversation with the user stays on one channel regardless (below).

## The loop

1. **Intake per subject.** Read the issue thread(s) and linked artifacts, the project instruction file's
   `## Context documents` index and the documents whose clauses match, and any handed material. Seed the
   subject's decision tree with what is settled and what is open.
2. **Interview across subjects.** Run the `interview` skill (by name) over all subjects at once: merge
   every subject's frontier into **one numbered round**, tag each question with its subject, route answers
   back, recompute each tree. One conversation, parallel trees.
3. **Resolve classifications between rounds.** A *needs-lookup* thread goes to the `research` skill; a
   *needs-probe* thread goes to the `prototype` skill; work is staffed via the `staffing` skill. Results
   re-enter the subject's frontier as evidence for the next round.
4. **Model inline.** The `domain-modeling` skill runs alongside the whole loop: terms and ADR-worthy
   decisions are written the moment they crystallise, per its own contract.
5. **Synthesize.** Every subject exits through the `to-spec` method — the record is mandatory, the artifact
   weight scales. Small subject (a few decisions): the *spec is the updated issue body* — decisions and
   acceptance criteria recorded there. Direction-sized subject: the full spec artifact with its sign-off
   gate (present via `review-loop` when the user is AFK).
6. **Project.** The `to-tickets` skill decides the projection per subject: update the same issue in place;
   split into slices that supersede it; or, for idea-borne work, create the tickets — created tickets are
   **born shaped** and never re-enter shaping.
7. **Hand back.** Report each subject's outcome and offer readiness — the caller or human stamps; shape
   does not.

Completion criterion: every subject has a durable record (updated issue, spec, or tickets), every open
thread carries its exit classification, and no tracker lifecycle label was written by this skill.

## Resume

Bare re-invocation reads the artifacts: issue threads show settled decisions and open classifications;
specs and `CONTEXT.md`/ADRs show what crystallised; the frontier is recomputed from what the record leaves
open. Nothing is re-asked that the record already answers.

## Dependency surface

- **Siblings (required, by name):** `interview` (the questioning method), `domain-modeling` (terms and
  ADRs), `to-spec` (synthesis), `to-tickets` (projection). Absent one, state the requirement and stop.
- **Siblings (optional, by name):** `research` (lookups), `prototype` (probes), `staffing` (who builds),
  `review-loop` (AFK sign-off). Absent one, park the affected thread as an open classification — inline
  approval replaces a missing `review-loop` — and say so; never silently skip.
- **Project surface:** the instruction file's `## Context documents` index and the tracker binding in
  `docs/agents/platform.md` when issues are subjects; absent a tracker, idea-borne shaping still works and
  ends at the spec.
