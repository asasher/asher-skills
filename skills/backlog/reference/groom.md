# Groom — Triage the Backlog

Target: the open issue backlog, or a named subset. The interactive pre-flight phase — the actual triage. Runs standalone (`backlog groom`) or as the first half of bare `backlog`, which grooms and then offers to run. It produces a labeled, clarified, de-duplicated backlog whose `ready-for-agent` issues `run` can pick up. It writes no code and opens no PRs.

Read `docs/agents/backlog-policy.md` for this repo's label-role mapping, how it records dependencies, and the readiness-decision rule, and `docs/agents/platform.md` for the tracker binding — the verbs that read and write issues. If either is missing, report a setup gap and stop.

This phase is human-in-the-loop: the agent proposes and may self-apply any role except `ready-for-agent`, which it applies only to issues the human confirms (step 5). Grooming runs in the primary checkout; on the local tracker binding its writes land on the main branch, and it never edits an issue that is `in-flight` — a change for one goes through the run thread or waits (`platform.md` § The local binding) — with one exception: the human-confirmed orphan reset in step 1, safe because the claim is dead.

## Steps

1. Pull the backlog.
   - If issues were named, use exactly those. Otherwise take every open issue that is not already excluded, closed, or `in-flight`.
   - Sweep for orphans while listing: an `in-flight` issue whose recorded branch no longer exists, or is quiet past the policy playbook's horizon, is surfaced to the human as a candidate reset per `backlog-policy.md` § In-flight hygiene — never reset silently. A reset the human confirms is applied here as a grooming write (on main, on the local binding) — the dead claim cannot race it.
   - Completion criterion: a working set of open issues, each fetched with title, body, comments, and labels, and any in-flight orphans surfaced.

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
   - Ensure the tracker reflects every label, finding, clarification, and recorded dependency — it is the source of truth `run` reads. On the local binding, commit the tracker changes on the main branch.
   - Report which issues are now `ready-for-agent` and unblocked. As bare `backlog`, offer to run them; standalone, stop here.
   - Completion criterion: the backlog state is persisted on the tracker (committed, on the local binding) and the `ready-for-agent` set is reported.
