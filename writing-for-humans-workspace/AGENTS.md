# Live writing eval runner

Use this workflow when the human asks to run or continue the writing eval. Read `README.md` and the latest `live/iteration-*/run.json` before acting. The human converses directly with the participant in another attendable thread; the runner stays here to collect evidence and discuss improvements.

## Start a conversation

Snapshot both skill sources, the known topic, and participant settings with `prepare`. It creates a standalone temporary repo outside the authoring repo, with only the two local skill files. Keep all iteration metadata, source paths, feedback, and analysis in the runner workspace. Use an ordinary task title and branch, and a prompt containing only the topic plus the two skill names. Use `start` to launch through `to-thread` in the user's T3 harness. Verify the launch with `status`, inspect the first assistant message for provider errors and verify the provider's actual working directory, then give the human the thread name. Keep the participant's context free of eval diagnoses, prior feedback, and desired writing changes. The human supplies every follow-up message.

The participant performs a discussion, not repository edits. The runner owns skill changes. Never substitute a hidden subagent conversation for the human's thread. Preserve model, effort, and permissions from the current harness unless the human selects otherwise. `settings.json` records this experiment's choices.

## Capture and discuss

Wait until the human returns to the runner and says the conversation is finished. Then run `capture` for that iteration. Do not infer completion from an idle thread. Read the saved transcript before making claims about it; cite message IDs for examples. Preserve every captured version and report gaps in coverage.

Ask about the human's experience in ordinary conversation. Record their words in `feedback.md`. Record analysis, proposed edits, and decisions separately in `review.md`. Do not invent ratings or require a scorecard. Discuss changes before applying them. If the human already selects a concrete change, implement it without another approval loop.

## Repeat

Keep both skill sources unchanged until the feedback discussion yields an agreed change. Tie each edit to transcript evidence and the human's experience. Record the patch and rationale in the next iteration's `change.md`; update family documentation when contracts change. Snapshot the revised sources and launch a fresh thread on the same topic. The human chats again, then returns here.

A comparable iteration holds the opening topic and participant configuration stable, but allows the human conversation to vary. Describe qualitative improvements and regressions without claiming a controlled replay. Changed topics or harness settings start a new baseline. The human decides whether to continue, keep, or revert.

## Recovery

A launch attempt records its outcome even on failure. Inspect the recorded thread before retrying; an ambiguous launch may already be running. Preserve failed runs. Never write to T3's database directly. The transcript collector uses a read-only transaction restricted to the selected thread.

A clean folder is context isolation, not a filesystem sandbox. Preserve the selected permissions and report this limit accurately. Never place evaluation instructions or source-repo links in the participant folder. Retain that folder until the human is finished and evidence is captured.
