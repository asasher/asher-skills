# Live conversation writing eval

This thread is the eval runner. Each iteration opens a separate T3 thread where Asher talks directly with the model about a known topic. When Asher returns here and says the conversation is done, the runner saves that transcript. We discuss the experience, agree on skill changes, and repeat.

The transcript and Asher's account of the experience are the evidence. There are no scripted follow-up turns or required numeric ratings.

## First conversation

The topic is duplicate invitation emails and deliberate resends. Open **Writing conversation · iteration-1** in the asher-skills T3 sidebar. Talk naturally, challenge answers, change direction, or stop whenever you want.

Return to the runner and say something like: "I'm done with iteration 1. Use that transcript. It kept repeating the implementation details when I wanted a decision."

The runner captures the thread, reads the conversation, and discusses your feedback with you. Skill edits follow that discussion. A new iteration starts a fresh thread with the same opening topic and updated skill snapshots.

## Runner commands

From the repo root:

```sh
bun writing-for-humans-workspace/eval.ts prepare iteration-1
bun writing-for-humans-workspace/eval.ts start iteration-1
bun writing-for-humans-workspace/eval.ts status iteration-1
```

`prepare` saves the topic, skill sources, project instructions, model settings, and kickoff prompt under `live/iteration-N/`. `start` launches an attendable thread through the `to-thread` helper. `status` verifies its identity, configuration, and started turn. Inspect its first reply for provider errors before handing it over.

Only after Asher returns and says the conversation is done:

```sh
bun writing-for-humans-workspace/eval.ts capture iteration-1
```

Capture reads only the recorded thread from T3's local database. It refuses unfinished turns or a thread without human follow-up. Each capture gets a new directory, preserving message text, IDs, timestamps, source metadata, and a readable transcript. It exports stored chat messages, not tool activity or hidden reasoning. Attachments remain references to the source thread.

## Discuss and repeat

Save Asher's comments verbatim in the iteration's `feedback.md`, alongside any clarifications from the discussion. Keep the runner's interpretation separate in `review.md`: cite specific message IDs, explain the suspected skill instruction, propose an edit, and record the decision. A disliked reply is evidence to investigate; it does not by itself establish which instruction caused it.

After agreeing on an edit, save the patch and rationale in the next iteration's `change.md`, apply it to the canonical skill sources, and prepare the next run. Update the family guide and manual review order when a skill contract changes. Leave prior snapshots and transcripts intact.

Keep the topic, kickoff structure, model, effort, and harness settings stable across runs. The human's messages may differ. Compare the experience and cited examples qualitatively; these are not identical replay trials. If the topic or harness changes, record that and treat the next run as a new baseline. Stop, continue, or revert follows the discussion with Asher.

## Boundaries

The participant sees the topic and frozen skills, not the runner's diagnosis or feedback. It runs in the real repository's T3 harness and inherits its instructions. Project instructions are recorded, but system prompts and provider behavior may change outside this repo. The participant discusses the topic without implementing code. The runner owns all eval artifacts and skill edits.

The earlier scripted experiment is preserved in [archive/scripted](archive/scripted). It was rejected as the wrong interaction model on 2026-09-17 and is not the live baseline.
