# Live conversation writing eval

This thread is the eval runner. Each iteration opens a separate T3 thread where Asher talks directly with the model about a known topic. When Asher returns here and says the conversation is done, the runner saves that transcript. We discuss the experience, agree on skill changes, and repeat.

The transcript and Asher's account of the experience are the evidence. There are no scripted follow-up turns or required numeric ratings.

## Current conversation

The current baseline is `live/iteration-4/`: the original skill packages with a task-only prompt. After this conversation, version 2 can be tried under the same automatic-discovery setup.

Version 1's earlier transcript remains accepted in `live/iteration-2/capture-1/`. It and the version 2 trial in `live/iteration-3/` explicitly named the skills, so they do not establish automatic activation.

The topic is duplicate invitation emails and deliberate resends. Open **Team invitations** in the asher-skills T3 sidebar. Talk naturally, challenge answers, change direction, or stop whenever you want.

Return to the runner and say something like: "I'm done with Team invitations. Use that transcript. It kept repeating the implementation details when I wanted a decision."

The runner captures the thread, reads the conversation, and discusses your feedback with you. Skill edits follow that discussion. A new iteration starts a fresh thread with the same opening topic and updated skill snapshots.

## Runner commands

From the repo root:

```sh
bun writing-for-humans-workspace/eval.ts prepare iteration-4 --skill-revision 40b183c
bun writing-for-humans-workspace/eval.ts start iteration-4
bun writing-for-humans-workspace/eval.ts status iteration-4
```

`prepare` saves the topic, skill sources, model settings, and kickoff prompt under `live/iteration-N/`. It creates a standalone Git repo in a temporary `team-app-*` folder containing complete copies of `writing-for-humans` and its `unslop` dependency under `.agents/skills/`, including `agents/openai.yaml`. The copies have no links back to the authoring repo. The prompt contains only the topic, with no skill names or activation instructions.

`--skill-revision COMMIT` copies the packages from a pinned commit without changing the working tree. Omit it to test the current skill sources. The source selection is recorded only in the runner artifacts.

`start` launches an attendable thread through the `to-thread` helper, using that temporary repo as its working directory. The thread title and branch describe ordinary project work; iteration IDs and source metadata stay with the runner. `status` verifies its identity, configuration, and started turn. Inspect its first reply for provider errors before handing it over.

Only after Asher returns and says the conversation is done:

```sh
bun writing-for-humans-workspace/eval.ts capture iteration-4
```

Capture reads only the recorded thread from T3's local database. It refuses unfinished turns or a thread without human follow-up. If the human accepts the visible conversation as-is and the idle session retains unstarted pending metadata, `capture iteration-N --include-pending` preserves that metadata with an explicit coverage note. Active or streaming turns still block capture. Each capture gets a new directory, preserving message text, IDs, timestamps, source metadata, and a readable transcript. It exports stored chat messages, not tool activity or hidden reasoning. Attachments remain references to the source thread.

## Discuss and repeat

Save Asher's comments verbatim in the iteration's `feedback.md`, alongside any clarifications from the discussion. Keep the runner's interpretation separate in `review.md`: cite specific message IDs, explain the suspected skill instruction, propose an edit, and record the decision. A disliked reply is evidence to investigate; it does not by itself establish which instruction caused it.

After agreeing on an edit, save the patch and rationale in the next iteration's `change.md`, apply it to the canonical skill sources, and prepare the next run. Update the family guide and manual review order when a skill contract changes. Leave prior snapshots and transcripts intact.

Keep the topic, kickoff structure, model, effort, and harness settings stable across runs. The human's messages may differ. Compare the experience and cited examples qualitatively; these are not identical replay trials. If the topic or harness changes, record that and treat the next run as a new baseline. Stop, continue, or revert follows the discussion with Asher.

## Boundaries

The participant receives an ordinary task. The harness can discover both local skill packages. Model-invocable means eligible for automatic selection, not guaranteed activation on every turn. Whether the skill is selected is part of the test.

Record discovery and observable file reads separately from the human's assessment of the replies. If activation cannot be established from available logs, mark it unknown; do not infer it from style or ask the participant about the test. Its folder contains no runner records, feedback, source-repo instructions, eval terminology, or links back to this repo. It uses a new session with no conversation history.

A clean working directory isolates project context, not filesystem permissions. The normal harness instructions and global skills still apply, and full-access mode can read outside the folder. The runner verifies the actual provider working directory after launch. Keep the temporary folder until the conversation and evidence capture are complete. The runner owns all eval artifacts and source skill edits.

The first live thread was archived by Asher because its setup exposed the eval. Iteration 2 starts a new baseline with this clean-folder setup. That run used the original writing skills.

The earlier scripted experiment is preserved in [archive/scripted](archive/scripted). It was rejected as the wrong interaction model on 2026-09-17 and is not the live baseline.
