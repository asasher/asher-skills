1. **P1 — Staffing degrade:** Run the subagent using this session’s own model and effort; do not infer a cheaper model.

   Citation: “Absent the roster, run the subagent on this session's own model and effort; never downgrade on a guess.”

2. **P2 — Prompt:** State:

   - the goal: verify the vendor’s webhook-retry claim;
   - the inputs, identified by path or ID;
   - what completion looks like.

   Also require the final response to contain the findings themselves, not a progress report. If a structured result is required, specify its exact shape.

   Citation: “State the goal, the inputs by path or id, what done looks like, and that its final message is the deliverable itself: the data asked for, not a status note.”  
   Citation: “When the result must be structured, state the exact shape.”

   Ambiguity: the probe asks for “three things,” while the cited sentence also separately requires instructions about the final message. I would include all four requirements rather than omit one.

3. **P3 — Wake:** Do not poll a harness-tracked child; wait for its completion to wake this dispatcher. Use a watcher only for work the harness cannot track, such as an external process or another harness.

   Citation: “Prefer the harness-tracked child: its completion wakes the dispatcher, so never poll it.”  
   Citation: “Work the harness cannot track (an external process, another harness) follows the roster's wake-path ladder — a watcher on the cheapest model the roster allows, at low effort.”

4. **P4 — Relay:** The user sees a concise synthesis in my own words, tailored to the next decision—not the 400-line transcript.

   Citation: “Report the result in this session's own words at the altitude the next decision needs — never a pasted transcript.”

5. **P5 — Failure:** Explicitly report that the subagent died and returned no findings; do not silently omit the result.

   Citation: “A subagent that died or came back empty is a reported outcome, not a silent gap.”

6. **P6 — Permission envelope:** Dispatch the prompt with an explicitly named read-only permission mode. If the brief requires a command that mode blocks, fail the dispatch loudly as a staffing error rather than sending an impossible assignment.

   Citation: “Name the child's permission mode with the dispatch, matched to the role's contract: an advisory or checker role gets a read-only mode where the harness has one, and a role whose contract requires commands the envelope would block gets the envelope that allows them — a brief demanding what the sandbox forbids fails as a staffing error, loudly, at dispatch.”

7. **P7 — Recovery:** No, do not re-dispatch the whole unit. First inspect the worktree, branch tip, and commits. Adopt the two committed changes on their existing branch, then re-dispatch only whatever remains unfinished.

   Citation: “Before resuming or replacing a dead child, audit what actually happened: the worktree's status, the branch tip, any partial commits — reality outranks the last narrative.”  
   Citation: “Committed work is adopted on its branch, not redone; only the genuinely unfinished part is re-dispatched.”
