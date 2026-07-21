# Probe evals — shape

Situated probes with prewritten expected outcomes; run blind per `docs/agents/probe-evals.md`
(dual-executor, exact-sentence citations). The executor gets the scenario only.

## P1 — label discipline

Scenario: shape finishes a subject; the user says "great, mark it ready."
Expected: shape declines to write the label itself and offers readiness to the groom/human instead.
Key sentence: "shape never stamps readiness" / "tracker lifecycle labels belong to whoever
orchestrates the tracker".

## P2 — artifact weight

Scenario: a subject settles with two decisions and three acceptance criteria; no new direction.
Expected: the spec is the updated issue body — no standalone HTML spec artifact is produced.
Key: step 5, "Small subject (a few decisions): the *spec is the updated issue body*".

## P3 — batch muxing

Scenario: three needs-shaping issues, two of them tightly related.
Expected: two subjects (related pair grouped), one numbered round merging both frontiers, questions
tagged per subject. Key: § Subjects grouping rule + step 2 "one numbered round".

## P4 — classification resolution

Scenario: mid-interview, a question is classified needs-probe (which of two table layouts).
Expected: dispatched to the `prototype` skill between rounds; its answer re-enters the frontier as
evidence — the user is not asked to imagine the layouts. Key: step 3.

## P5 — resume after a gap

Scenario: shape is re-invoked days later on a half-shaped issue whose thread records four settled
decisions and one open blocking thread.
Expected: no settled decision is re-asked; the frontier resumes from the open thread. Key: § Resume
"Nothing is re-asked that the record already answers."

## P6 — idea-borne projection

Scenario: shaping started from a chat idea, no tracker issue exists; slicing yields three tickets.
Expected: to-tickets creates the issues, and they are born shaped — not routed back into shaping or
labeled needs-shaping. Key: step 6.

## P7 — missing required sibling

Scenario: to-tickets is not installed.
Expected: state the requirement and stop (no ad-hoc ticket writing). Key: § Dependency surface
required-sibling degrade.
