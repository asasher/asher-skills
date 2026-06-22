---
name: triage
description: Orchestrates GitHub issue triage by creating one Codex issue thread per issue.
disable-model-invocation: true
---

# Triage

Triage is queue orchestration. Keep this thread focused on discovering the issue queue, creating issue threads, and reporting handoff state. Do not solve the issues in this thread.

## Steps

1. Build the queue.
   - If the user named issue numbers or URLs, use exactly those issues.
   - Otherwise, fetch every open GitHub issue in the current repo with no labels.
   - Completion criterion: the queue contains every in-scope issue URL exactly once, or the user is told that the queue is empty.

2. Check labels.
   - The worker threads need these labels: `bug`, `enhancement`, `refactor`, and `needs-info`.
   - Create missing labels when the available GitHub tools can do so; otherwise record the missing labels as blockers for the worker threads.
   - Completion criterion: each required label is either available or has an explicit blocker.

3. Create one issue thread per queue item.
   - Use a new Codex thread in its own worktree under this project for each issue.
   - Title each thread `triage #<issue-number>: <issue-title>`.
   - Prompt each thread with the issue URL and the full instructions from `ISSUE_THREAD_INSTRUCTIONS.md`.
   - Do not batch multiple issues into one issue thread.
   - Completion criterion: every queued issue has a created thread id, pending worktree id, or explicit creation blocker.

4. Report the handoff table in this triage thread.
   - Include issue number, title, URL, created thread or pending worktree id, and blocker if any.
   - Stop after handoff unless the user explicitly asks this thread to monitor the issue threads.
   - Completion criterion: every queued issue appears in the handoff table with a terminal handoff state.

## Context Pointers

- `ISSUE_THREAD_INSTRUCTIONS.md`: required worker prompt for each issue thread.
- `ADVERSARIAL_REVIEW_INSTRUCTIONS.md`: loaded only by an issue thread after it has created a PR.

## Glossary

- Triage thread: this Codex app thread, where the issue queue is discovered and dispatched.
- Issue thread: one Codex app thread created to classify and handle one GitHub issue.
