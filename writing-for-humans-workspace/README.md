# Conversation writing eval

Replay one four-turn repo conversation with `writing-for-humans` and `unslop`. Save each run, let Asher rate the replies, then change the skills and replay it.

The first scenario covers duplicate invitation emails: a recommendation, a progress update, a concern about resending, and a handoff. Work observations are supplied fixtures. No app was built or tested during this eval.

## Review the baseline

Read [iteration 1's transcript](iteration-1/transcript.md). Rate each turn from 1 to 5 for economy, clarity, naturalness, and usefulness. The [rubric](rubric.json) defines the scores. Point to wording you would cut or rewrite, and facts you needed but did not get.

You can give feedback in chat. The agent records your ratings and comments in [feedback.json](iteration-1/feedback.json). Blank scores mean unrated. Word counts describe length; they do not decide quality.

## Run and repeat

Run commands from the repo root. Each iteration snapshots both skills, the scenario, and the rubric. Its manifest records their hashes, the source revision, model, and harness settings.

```sh
bun writing-for-humans-workspace/eval.ts prepare iteration-2 gpt-6-astra 'Native Codex participant; inherited effort; fresh context at turn 1; same session for later turns; no tools; fixed observations; final replies only'
bun writing-for-humans-workspace/eval.ts next iteration-2
```

Send the generated prompt to a fresh participant context. Save its reply verbatim to a temporary text file, then record it:

```sh
bun writing-for-humans-workspace/eval.ts record iteration-2 /tmp/participant-reply.txt
bun writing-for-humans-workspace/eval.ts next iteration-2
```

Repeat `record` and `next` until all four turns are recorded. Continue the same participant session within a run. Show it only the current turn and previous conversation. Start a fresh participant for every new iteration. Save the session reference in `run.json`.

After human feedback, aggregate and compare:

```sh
bun writing-for-humans-workspace/eval.ts summarize iteration-1
bun writing-for-humans-workspace/eval.ts summarize iteration-2
bun writing-for-humans-workspace/eval.ts compare iteration-1 iteration-2
```

The comparison rejects changed scenarios, rubrics, models, settings, or tampered snapshots. A new scenario or model needs a new baseline. Keep unsuccessful runs as evidence.

## Improvement loop

1. Save a baseline with the current skills.
2. Asher rates it and identifies the replies to improve.
3. Record the feedback, a specific proposed edit, and its expected effect in the new iteration's `change.md`.
4. Change one skill at a time when possible. Snapshot and replay the same conversation.
5. Asher rates the candidate and chooses keep, revise, or stop. Preserve useful detail when cutting length.

When a skill's contract changes, update the family guide and manual review order. These eval files stay in the authoring workspace; they are not installed with either skill.

## Limits

This is a scripted conversation with supplied observations. It tests replies with both skills explicitly loaded. It does not test automatic skill discovery, real tool execution, or the frequency and wording of unsolicited progress messages in an actual repository.

The native participant inherits the harness's system and developer instructions. A fresh context removes this conversation's proposed diagnosis and human feedback, but does not remove that shared harness context. Keep the harness constant and record known changes. One run shows an example, not a reliable estimate of how often a problem occurs.

If the baseline does not resemble the verbose conversations you see, capture a real conversation as a new scenario before editing the skills. After an apparent improvement, try a second scenario or a real repo task to check whether it holds up.
