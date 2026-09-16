# Conversation eval workspace

Read `README.md` for the replay commands and scope. This workspace evaluates the repo sources of `writing-for-humans` and `unslop` together.

## Agent execution

Produce the participant in a fresh native subagent context via `to-subagent`, then resume that participant for later turns. Use the same model and harness settings across iterations. Give it only the generated prompt, the fixed dispatch instructions, and its own conversation history. It receives no rubric, human feedback, candidate diagnosis, or future turns. It uses no tools.

The coordinator owns files and ratings. Preserve participant replies verbatim, including awkward wording. Record the participant's session reference and any deviations in `run.json`. If the model or harness changes, start a new baseline. Do not substitute a separately billed CLI route silently.

## Iteration contract

`prepare` snapshots the inputs. `next` produces one prompt. Dispatch that prompt, then `record` the verbatim response. Repeat for every scenario turn. The full run is complete when every turn is recorded, and its status is `awaiting-human`.

The human grades with `rubric.json`. Record only ratings the human supplied in `feedback.json`; ambiguous or absent ratings remain null. Preserve their comments verbatim. Agent observations belong in a separate `change.md` or review note.

`summarize` aggregates human scores and word counts into `benchmark.json`. `compare` validates comparability and shows both runs. A generated transcript is not a human rating. An iteration is ready for a decision when all turns have human scores. Keep, revise, or stop comes from the human.

Freeze scenario, rubric, participant settings, and dispatch instructions for each comparison. Only change the target skills in response to recorded evidence. Keep all prior iterations. A failed participant run gets a failure note and a new iteration for retry.
