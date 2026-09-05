---
name: capture
description: Capture conversation follow-ups as minimal GitHub tickets, optionally blocking a named parent. Use to establish a ticket before shaping; use to-slices for an approved split.
metadata:
  optional: [to-slices, technical-writing]
---

# Capture

Preserve loose work so each ticket survives a cold read at grooming. Use `technical-writing` when available. Splitting settled direction belongs in `to-slices`; if unavailable, retain one ticket and report the gap.

1. Sweep the whole conversation for bugs, enhancements, and committed follow-ups. Exclude already-tracked work, this task's settled scope, and idle musing. When establishing this task's shaping ticket, include its full known intent.
2. Present titles, work-types (`bug` or `enhancement`), and the context each ticket will carry. Publish the confirmed list; existing approval counts.
3. Create one ticket per confirmed item with `gh issue create`. Preserve reported symptoms, reproduction, intent, and artifact links. Keep it self-contained and at the level of the report; defer investigation and implementation planning. Apply its work-type and no readiness label. Groom decides readiness.
4. With `capture <parent>`, attach each child as a sub-issue and make the parent blocked by it. Resolve the child's database id with `gh api repos/<owner>/<repo>/issues/<child> --jq '.id'`; POST it as `sub_issue_id` to `issues/<parent>/sub_issues`, and as `issue_id` to `issues/<parent>/dependencies/blocked_by` under that repository API.
5. Read back every ticket and relation. Each confirmed item must map to exactly one ticket with the expected work-type and no readiness label. Inspect uncertain creates before retrying to avoid duplicates. Return links after repairing any mismatch.
