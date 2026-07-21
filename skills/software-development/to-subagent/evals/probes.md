# To-Subagent — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are dispatching "verify the vendor's webhook retry claim against their docs" as a subagent. The repo
has no staffing roster installed.

## Probes

**P1 (staffing degrade).** No roster — which model and effort run the subagent? Cite.

**P2 (prompt).** What three things must the prompt state about the deliverable, given the subagent sees
nothing of this session? Cite.

**P3 (wake).** The harness tracks the child. Do you poll it? And when would a watcher be used instead?
Cite.

**P4 (relay).** The subagent returns 400 lines of findings. What does the user see? Cite.

**P5 (failure).** The subagent dies with no output. What happens? Cite.

## Answer key

- **P1:** "Absent the roster, run the subagent on this session's own model and effort; never downgrade
  on a guess." Picking a cheaper model without a roster = **fail**.
- **P2:** "State the goal, the inputs by path or id, what done looks like, and that its final message is
  the deliverable itself: the data asked for, not a status note." A prompt yielding "I finished" =
  **fail**.
- **P3:** No — "Prefer the harness-tracked child: its completion wakes the dispatcher, so never poll
  it." A watcher enters only for "Work the harness cannot track (an external process, another
  harness)." Polling a tracked child = **fail**.
- **P4:** A relay "in this session's own words at the altitude the next decision needs — never a pasted
  transcript." Dumping the transcript = **fail**.
- **P5:** "A subagent that died or came back empty is a reported outcome, not a silent gap." Quietly
  retrying forever or omitting it = **fail**.

Pass bar: **5/5 on both executors.**
