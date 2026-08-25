---
name: to-subagent
description: Dispatch one unit of non-interactive work to a subagent as a blocking call. Use whenever work should run outside this session without the user attending it.
argument-hint: "<the unit of work to dispatch>"
metadata:
  requires: []
  optional: [staffing]
---

# To Subagent

Dispatch one unit of non-interactive work to another agent, validate its deliverable, and relay the result.

Use this when parallelizing work, isolating large payloads (e.g verbose outputs, screenshots, processing large documents, research etc) to preserve context etc.

Use `staffing` (when available) to select the dispatch fields; otherwise pick them and inform the user before dispatch.

| staffing field | harness argument                                  |
| -------------- | ------------------------------------------------- |
| model          | model argument, unchanged                         |
| effort         | effort argument, unchanged; omit when unspecified |
| harness        | executable route                                  |
| execution      | additional dispatch method                        |

Treat the fields as separate values. For example, model `fable-5` with effort `high` becomes model argument `fable-5` and effort argument `high`.

For cross-harness models, shell out to the appropriate harness and monitor the dispatch. Close stdin on the shell-out (`</dev/null`): a backgrounded harness sees an open pipe that never delivers EOF and waits on it indefinitely.

Report the outcome (success or failed dispatch), the deliverable's location, and what the next decision must act on, in your own words.
