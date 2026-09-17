# Live conversation writing eval

This thread is the eval runner. Each iteration opens a separate T3 thread where Asher talks directly with the model about a known topic. When Asher returns here and says the conversation is done, the runner saves that transcript. We discuss the experience, agree on skill changes, and repeat.

The transcript and Asher's account of the experience are the evidence. There are no scripted follow-up turns or required numeric ratings.

## First conversation

The topic is duplicate invitation emails and deliberate resends. Open **Team invitations** in the asher-skills T3 sidebar. Talk naturally, challenge answers, change direction, or stop whenever you want.

Return to the runner and say something like: "I'm done with Team invitations. Use that transcript. It kept repeating the implementation details when I wanted a decision."

The runner captures the thread, reads the conversation, and discusses your feedback with you. Skill edits follow that discussion. A new iteration starts a fresh thread with the same opening topic and updated skill snapshots.

## Runner commands

From the repo root:

```sh
bun writing-for-humans-workspace/eval.ts prepare iteration-2
bun writing-for-humans-workspace/eval.ts start iteration-2
bun writing-for-humans-workspace/eval.ts status iteration-2
```

`prepare` saves the topic, skill sources, model settings, and kickoff prompt under `live/iteration-N/`. It creates a standalone Git repo in a temporary `team-app-*` folder containing only `.agents/skills/writing-for-humans/SKILL.md` and `.agents/skills/unslop/SKILL.md`. These are copies, not links to the authoring repo. The participant prompt is the topic plus "Use $writing-for-humans and $unslop."

`start` launches an attendable thread through the `to-thread` helper, using that temporary repo as its working directory. The thread title and branch describe ordinary project work; iteration IDs and source metadata stay with the runner. `status` verifies its identity, configuration, and started turn. Inspect its first reply for provider errors before handing it over.

Only after Asher returns and says the conversation is done:

```sh
bun writing-for-humans-workspace/eval.ts capture iteration-2
```

Capture reads only the recorded thread from T3's local database. It refuses unfinished turns or a thread without human follow-up. Each capture gets a new directory, preserving message text, IDs, timestamps, source metadata, and a readable transcript. It exports stored chat messages, not tool activity or hidden reasoning. Attachments remain references to the source thread.

## Discuss and repeat

Save Asher's comments verbatim in the iteration's `feedback.md`, alongside any clarifications from the discussion. Keep the runner's interpretation separate in `review.md`: cite specific message IDs, explain the suspected skill instruction, propose an edit, and record the decision. A disliked reply is evidence to investigate; it does not by itself establish which instruction caused it.

After agreeing on an edit, save the patch and rationale in the next iteration's `change.md`, apply it to the canonical skill sources, and prepare the next run. Update the family guide and manual review order when a skill contract changes. Leave prior snapshots and transcripts intact.

Keep the topic, kickoff structure, model, effort, and harness settings stable across runs. The human's messages may differ. Compare the experience and cited examples qualitatively; these are not identical replay trials. If the topic or harness changes, record that and treat the next run as a new baseline. Stop, continue, or revert follows the discussion with Asher.

## Boundaries

The participant sees an ordinary task and two local skills. Its folder contains no runner records, feedback, source-repo instructions, eval terminology, or links back to this repo. It uses a new session with no conversation history.

A clean working directory isolates project context, not filesystem permissions. The normal harness instructions and global skills still apply, and full-access mode can read outside the folder. The runner verifies the actual provider working directory after launch. Keep the temporary folder until the conversation and evidence capture are complete. The runner owns all eval artifacts and source skill edits.

The first live thread was archived by Asher because its setup exposed the eval. Iteration 2 starts a new baseline with this clean-folder setup. Both writing skills are unchanged.

The earlier scripted experiment is preserved in [archive/scripted](archive/scripted). It was rejected as the wrong interaction model on 2026-09-17 and is not the live baseline.
