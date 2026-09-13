---
name: capture
description: Capture conversation follow-ups as GitHub tickets, grouping requested batches in milestones or attaching gaps to a named spec parent. Use to establish a ticket before shaping; use to-slices for an approved split.
metadata:
  optional: [to-slices, technical-writing]
---

# Capture

Preserve loose work so each ticket survives a cold read at grooming. Use `technical-writing` when available. Splitting settled direction belongs in `to-slices`; if unavailable, retain one ticket and report the gap.

1. Sweep the whole conversation for bugs, enhancements, and committed follow-ups. Exclude already-tracked work, this task's settled scope, and idle musing. When establishing this task's shaping ticket, include its full known intent.
2. Present titles, work-types (`bug` or `enhancement`), and the context each ticket will carry. For a requested batch, reuse its named milestone or propose a title, description, and shared source links. Include conflicting existing milestone assignments for the user's decision. Publish the confirmed plan; existing approval counts.
3. Create one ticket per confirmed item. Preserve reported symptoms, reproduction, intent, and artifact links. Keep it self-contained and at the level of the report; defer investigation and implementation planning. Apply its work-type and no readiness label to newly created tickets. Groom decides readiness.
4. With `capture <parent>`, verify that the parent is an approved `spec` split, then attach each gap as a native GitHub sub-issue and blocker. Inherit its milestone, including any conflicting assignment in the approval plan. For an organizational parent, propose a milestone migration: preserve shared context and true dependencies, verify assignments, then retire the grouping links and close the old parent within the approved plan.
5. Read back every ticket, milestone assignment, and relation. Each confirmed item must map to exactly one ticket. Inspect uncertain creates and adopt matching tickets before retrying; preserve labels, claims, and work advanced by another owner. Verify newly created tickets against the capture plan; on adopted tickets, repair capture-owned content or relations only when compatible with their current ownership. Record conflicts for the current owner, then return the verified links and any unresolved repair.
