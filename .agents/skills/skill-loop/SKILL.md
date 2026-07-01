---
name: skill-loop
description: Run a target skill through eval-driven improvement iterations until no evaluation-backed edits remain.
argument-hint: "<skill-path-or-name> <eval-path-or-command> [--max N]"
user-invocable: true
disable-model-invocation: true
---

# Skill Loop

A loop improves one target skill against one eval harness. Eval signals are the source of truth; do not edit
from taste, hunches, or general skill advice unless the signal points there.

## Inputs

The user must provide:

- **Target skill**: a skill name, skill directory, or `SKILL.md` path. Resolve a bare name to
  `skills/<name>/SKILL.md` when that file exists.
- **Eval target**: an eval workspace, eval README, or exact shell command. If the target is a directory, read
  its README and runner scripts before choosing the command.

An eval is runnable only when you can run every test case into a fresh `iteration-N/` directory and then grade
and aggregate that same directory. If the command or output location is ambiguous, stop and ask for the exact
run command.

Do not change eval definitions, assertions, graders, or test cases during the loop unless the human explicitly
says the eval is wrong. Changing the eval invalidates comparison with earlier iterations.

## The Loop

1. **Orient.** Read the target `SKILL.md`, the eval README, runner scripts, latest `iteration-*` artifacts,
   and any previous human feedback. Identify the full-run command, grading command, aggregation command,
   latest completed iteration, next iteration number, and primary metric. Completion: those items are known, or
   the missing item is named and the loop stops.

2. **Build the signal packet.** Gather the current `SKILL.md`, eval goal, eval command, latest and previous
   `benchmark.json` or equivalent summaries, failed assertions, manual feedback, grading evidence, and
   representative outputs for failures. Include enough artifact paths for the reviewer to verify the claim.
   Completion: the packet can explain what failed, where it failed, and why the target skill text is a plausible
   cause.

3. **Ask a fresh reviewer.** Load `reference/reviewer-prompt.md` and adapt it to the packet. Use a separate
   model context when available: a subagent, model CLI, or other LLM tool. If no separate context is available,
   run the review in your own context but keep the prompt and response explicit in the notes. Completion: the
   reviewer returns either `NO_CHANGE` or a ranked edit plan with cited eval evidence, exact target regions,
   expected metric movement, risks, and rejected tempting edits.

4. **Apply only gated edits.** Accept a proposed edit only when it is tied to eval evidence, improves
   predictability, passes the no-op test, avoids duplication, preserves a single source of truth, and stays
   within the target skill. Prefer deletion, sharpening, and co-location over adding new prose. Do not rewrite
   stable sections or unrelated files. Completion: the target `SKILL.md` contains only accepted edits, or the
   no-change reason is recorded.

5. **Run the next iteration.** Refresh any skill snapshot the harness uses, such as
   `conditions/<skill-name>.md`, before running. Create or run into `iteration-(N+1)/`, where `N` is the latest
   completed iteration. Run the full test matrix, not a subset, for a comparison iteration. Completion: every
   test case was attempted in the new iteration directory; missing outputs or command failures are preserved as
   failure evidence.

6. **Grade and aggregate.** Run the eval's graders and aggregator for the new iteration. If the eval has manual
   or visual assertions, fill them only from the eval's stated rubric. Use a blind LLM judge only when the eval
   defines one; mark those decisions as LLM-graded. Do not overwrite human `feedback.json`; append or create a
   separate review note if needed. Completion: the new iteration has grading artifacts and an aggregate result.

7. **Compare and review.** Compare the new iteration to the previous iteration and the baseline on the primary
   metric, regressions, failure count, manual feedback, token cost, and runtime. Show the human the patch
   summary, metric deltas, fixed failures, regressions, and remaining candidate improvements. Completion: the
   human chooses continue or stop, or the stop criteria below are met.

## Stop Criteria

Stop the loop when any condition is true:

- The fresh reviewer returns `NO_CHANGE`.
- Every reviewer proposal fails the edit gate.
- The latest full iteration does not improve the primary metric or failure profile, and no new eval-backed edit
  targets a specific remaining failure.
- Human review says to stop.
- The loop reaches `--max N`, when the user supplied a cap.

Continue only when there is at least one remaining failure or human note that is plausibly caused by the skill
text and at least one gated edit targets it.

## Reporting

After each iteration, report:

- Target skill path and eval workspace.
- New iteration directory.
- Edits made, grouped by eval signal.
- Aggregate deltas versus the previous iteration and baseline.
- Remaining failures and whether the next action is continue, stop, or human decision.

Previous `iteration-*` directories are evidence. Do not rewrite them. If a failed run must be repeated because
of infrastructure failure, write the rerun into a new iteration directory or record the rerun reason inside the
iteration before changing anything.
