# Shape — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `shape` skill in a thread on ticket #142 ("driver payouts — needs shaping"), with
ticket #147 grouped in (its decisions interlock). The repo has `CONTEXT.md`, a `## Context documents`
index, and a bound tracker.

## Probes

**P1 (intake).** What do you read before the first question? Cite.

**P2 (dispatch).** The frontier includes "what does the vendor's settlement API actually guarantee?"
(needs sources) and "should the payout screen be a wizard or one form?" (paper can't settle). Where does
each go, and what happens to the rest of the frontier meanwhile? Cite.

**P3 (labels).** Mid-session the shaping feels done to you and the tickets look ready. Do you mark
them ready-for-agent? Cite.

**P4 (record).** The cadence decision just settled in round 2. When and where is it recorded? Cite.

**P5 (crystallise).** The frontier is empty and the user confirms shared understanding. Do you now write
the spec or split tickets? Cite.

**P6 (resume).** A fresh session opens on #142 tomorrow. What does it read, and what must it not do?
Cite.

**P7 (degrade).** The `prototype` skill is not installed and the wizard-vs-form question is open. What
happens to that question? Cite.

**P8 (comment watch).** The user crystallised via to-tickets and went AFK. Later they comment on ticket
#201 "split the export into its own ticket", and later still "LGTM — ready for agent." What happens at
each event? Cite.

## Answer key

- **P1:** The ticket threads and linked artifacts (both tickets — one subject), plus "the project
  instruction file's `## Context documents` index and the documents whose clauses match." Skipping the
  index = **fail**.
- **P2:** Sources → `research` skill; paper-unsettleable → `prototype` skill — "each dispatched via the
  `to-subagent` skill. A dispatched question blocks only what depends on it." The rest of the frontier
  proceeds. Blocking everything, or asking the user the vendor fact, = **fail**.
- **P3:** No — "Lifecycle labels are never shape's judgment: shape stamps nothing on its own." Applying
  it from your own read of readiness = **fail**.
- **P4:** On the ticket thread, as it lands — "record settled decisions on its thread as they land —
  the thread is the resume state." Batching to the end = **fail**.
- **P5:** No — "Crystallising the direction — a spec, tickets, or straight to a build — is the user's
  call." Report and stop. Auto-running a spec or tickets = **fail**.
- **P6:** "reads the record — ticket thread, `CONTEXT.md`, ADRs — recomputes the frontier from what is
  still open, and re-asks nothing the record answers." Re-asking settled decisions = **fail**.
- **P7:** "park the affected work as open and say so; never silently skip." Silently dropping it,
  or improvising a prototype without the skill, = **fail**.
- **P8:** The thread is watching — "run the `watch-until` skill on the published tickets ... condition:
  a new comment from the user, or an explicit readiness signal." On the comment: "apply the requested
  tweak to the ticket or spec, reply with what changed, resume watching." On the signal: "apply the
  readiness role per the tracker's label roles — the user's decision, executed." Ignoring the comment,
  or refusing the label because "shape stamps nothing", = **fail**.

Pass bar: **8/8 on both executors.**
