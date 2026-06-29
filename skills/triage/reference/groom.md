# Groom — Triage the Backlog

Target: the open issue backlog, or a named subset. The interactive pre-flight phase — the actual triage. Runs standalone (`triage groom`) or as the first half of bare `triage`, which grooms and then offers to run. It produces a labeled, clarified, de-duplicated backlog whose `ready-for-agent` issues `run` can pick up. It writes no code and opens no PRs.

Read `docs/agents/triage-policy.md` for this repo's label-role mapping, how it records dependencies, and the readiness-decision rule. If it is missing, report a setup gap and stop.

This phase is human-in-the-loop: the agent proposes, the human confirms. The agent may apply the `needs-info`, `ready-for-human`, and exclusion roles on its own; it applies `ready-for-agent` only to issues the human confirms in the shortlist.

## Steps

1. Pull the backlog.
   - If issues were named, use exactly those. Otherwise take every open issue that is not already excluded, closed, or in flight.
   - Completion criterion: a working set of open issues, each fetched with title, body, comments, and labels.

2. Propose a work-type per issue.
   - Orient on each issue and propose one work-type role — bug, enhancement, or refactor — or mark it `needs-info`, `ready-for-human`, or an exclusion role. Map every proposal to this repo's labels per the playbook.
   - Completion criterion: every issue has a proposed role grounded in its content.

3. Clarify.
   - Where scope or requirements are ambiguous, ask the human directly and fold the answers into the issue body or a comment so they persist. For questions the human cannot answer now, comment the open question on the issue and set `needs-info`.
   - Completion criterion: each issue is understood well enough to classify and judge readiness, or is parked as `needs-info` with its open question recorded.

4. Resolve relationships.
   - Detect dependencies between issues and record them per the playbook's convention so `run` can read them. Mark superseded, duplicate, and already-resolved issues with the matching exclusion role, link the canonical issue, and close them when the tools and the user allow.
   - Completion criterion: dependencies are recorded, and stale or redundant issues are excluded or closed.

5. Shortlist and label.
   - Present the groomed candidates and let the human confirm which become `ready-for-agent`. Apply `ready-for-agent` only to confirmed issues, and only when each carries a work-type. Apply `ready-for-human`, `needs-info`, and exclusion roles as proposed.
   - Completion criterion: every issue carries its readiness role, and every `ready-for-agent` issue carries a work-type.

6. Write back and hand off.
   - Ensure the tracker reflects every label, finding, clarification, and recorded dependency — it is the source of truth `run` reads.
   - Report which issues are now `ready-for-agent` and unblocked. As bare `triage`, offer to run them; standalone, stop here.
   - Completion criterion: the backlog state is persisted on the tracker and the `ready-for-agent` set is reported.
