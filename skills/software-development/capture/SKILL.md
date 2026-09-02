---
name: capture
description: Capture the loose items a conversation has surfaced — bugs, enhancement ideas, follow-ups — as minimal work-typed GitHub issues, optionally as children of a named parent issue. Not for splitting a decided direction; that is to-slices.
metadata:
  optional: [to-slices, technical-writing]
---

# Capture

Capture owns one move: **get what the conversation surfaced into the issues before it evaporates.** A working conversation (an interview, a shaping thread, a build session) throws off loose items. This is capture, not decomposition: several unrelated, undecided things into the intake queue. One decided thing into ordered parts is the `to-slices` sibling; absent it, say the split move is unavailable and capture the direction as a single issue.

The defining discipline is **context fidelity**: each issue must survive a cold read at grooming, because this conversation evaporates. Issue bodies follow the `technical-writing` sibling; absent it, write plainly and say the standard was not loaded.

## Command surface

- **`capture`**: sweep the current conversation for capture-worthy items and publish the confirmed list as issues.
- **`capture <parent issue>`**: the same, attaching each published issue as a sub-issue of the parent and wiring the parent `blocked_by` each one. Use when the captured items are installments of a parent's direction, such as gaps found while building one of its slices: attaching them re-blocks the parent by itself.

## How a capture happens

1. **Sweep the whole conversation, first message to last.** Collect every loose item: reported defects, requested or implied enhancements, follow-ups, questions that became work. Skip what is already tracked, already in scope here, or idle musing no one committed to. Done when every turn has been checked and each loose item is collected or deliberately skipped.
2. **Confirm the list.** Present one compact list: per item a one-line title, the proposed work-type (`bug` or `enhancement`, a fact the conversation knows), and a one-phrase note of the context the issue will carry. The user edits, drops, adds. Nothing publishes before they approve.
3. **Publish minimal issues** with `gh issue create`: a title, the work-type label, and a context-fidelity body, and nothing else. The body carries what the chat knew: the symptom and repro as reported for a bug, the motivating exchange and intent for an enhancement, links to any artifact the conversation named. **Apply no readiness label**: an unrouted issue is grooming's intake by design, and readiness is grooming's judgment.
4. **Attach to the parent, when one was given.** Add each new issue as a sub-issue of the parent and wire the parent `blocked_by` it: resolve the child's database id with `gh api repos/<owner>/<repo>/issues/<child> --jq '.id'`, then `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<id>` and `gh api -X POST repos/<owner>/<repo>/issues/<parent>/dependencies/blocked_by -F issue_id=<id>`.
5. **Readback.** Verify against GitHub: every confirmed item maps to exactly one created issue with its work-type, no readiness label, and, when a parent was given, both relations resolving. Fix any miss before reporting the capture done.

## What a captured issue is (and isn't)

- **Minimal but self-sufficient.** Context fidelity at the altitude of a report: not acceptance criteria, not a slice, not a plan.
- **As reported, not as investigated.** Verbatim reporter material (an error message, a stack trace, a quoted behavior) goes in as evidence; the conversation's own digging (file paths, code snippets) stays out.
