# Shape — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `shape` skill in a thread on a batch: ticket #142 ("driver payouts — needs
shaping") with ticket #147 grouped in (its decisions interlock), plus ticket #150 ("csv export — needs
shaping"), unrelated to payouts. The repo has `CONTEXT.md`, a `## Context documents` index, and a bound
tracker.

## Probes

**P1 (intake).** What do you read before the first question? Cite.

**P2 (dispatch).** The frontier includes "what does the vendor's settlement API actually guarantee?"
(needs sources) and "should the payout screen be a wizard or one form?" (paper can't settle). Where does
each go, and what happens to the rest of the frontier meanwhile? Cite.

**P3 (labels).** Mid-session the shaping feels done to you and the tickets look ready. Do you mark
them ready-for-agent? Cite.

**P4 (record).** The cadence decision just settled in round 2. When and where is it recorded? Cite.

**P5 (crystallise).** The payouts subject's frontier is empty. What happens next without being asked,
and what still waits on the user? Cite.

**P6 (resume).** A fresh session opens on #142 tomorrow. What does it read, and what must it not do?
Cite.

**P7 (degrade).** The `prototype` skill is not installed and the wizard-vs-form question is open. What
happens to that question? Cite.

**P8 (comment watch).** The spec landed on ticket #150 and the user went AFK. Later they comment "add
the retry cadence to the spec", and later still "LGTM — ready for agent." What happens at each event?
Cite.

**P9 (engines).** The batch holds three tickets. How many engines run, via what, and how do interview
questions reach the user? Cite.

## Answer key

- **P1:** The ticket threads and linked artifacts (both tickets — one subject), plus "the project
  instruction file's `## Context documents` index and the documents whose clauses match." Skipping the
  index = **fail**.
- **P2:** Sources → `research` skill; paper-unsettleable → `prototype` skill — "each dispatched via the
  `to-subagent` skill. A dispatched question blocks only what depends on it." The rest of the frontier
  proceeds. Blocking everything, or asking the user the vendor fact, = **fail**.
- **P3:** No — "Lifecycle labels are never shape's judgment: shape stamps nothing on its own — it
  only executes the user's explicit calls." Applying it from your own read of readiness = **fail**.
- **P4:** On the ticket thread, as it lands — "record settled decisions on its thread as they land —
  the thread is the resume state." Batching to the end = **fail**.
- **P5:** Crystallise unprompted — "When a subject's frontier is empty, run the `to-spec` skill on
  it — automatically, not on request: the spec lands on the subject's ticket, opening with a diagram."
  Still waiting on the user: readiness ("readiness still waits for the user's blessing") and any split
  ("only on the user's explicit approval"). Asking permission to write the spec, applying readiness, or
  running to-tickets unprompted = **fail**.
- **P6:** "reads the record — ticket thread, `CONTEXT.md`, ADRs — recomputes the frontier from what is
  still open, and re-asks nothing the record answers." Re-asking settled decisions = **fail**.
- **P7:** "park the affected work as open and say so; never silently skip." Silently dropping it,
  or improvising a prototype without the skill, = **fail**.
- **P8:** The thread is watching — "run the `watch-until` skill on the spec'd tickets — condition:
  a new comment from the user, or an explicit readiness signal." On the comment: "apply the requested
  tweak to the ticket or spec, reply with what changed, resume watching." On the signal: "apply the
  readiness role per the tracker's recorded label roles (`docs/agents/backlog-policy.md`) — the user's
  decision, executed." Ignoring the comment,
  or refusing the label because "shape stamps nothing", = **fail**.
- **P9:** Two engines — "merely-related subjects never share one, interlocked tickets always do":
  {#142,#147} is one subject, #150 another — "each dispatched via the `to-subagent` skill." Rounds are
  dispatch cycles: "this session combines the frontiers into **one round for the user**, questions
  tagged by subject." Three engines, one engine for all, or per-subject rounds fired at the user
  separately, = **fail**.

Pass bar: **9/9 on both executors.**
