# Groom — Triage the Backlog

Target: the open issue backlog, or a named subset. The interactive pre-flight phase — the actual triage. Runs standalone (`backlog groom`) or as the first half of bare `backlog`, which grooms and then offers to run. It produces a labeled, clarified, de-duplicated backlog whose `ready-for-agent` issues `run` can pick up. It writes no code and opens no PRs.

Read `docs/agents/backlog-policy.md` for this repo's label-role mapping, how it records dependencies, and the readiness-decision rule, and `docs/agents/platform.md` for the tracker binding — the verbs that read and write issues. If either is missing, report a setup gap and stop.

This phase is human-in-the-loop: the agent proposes and may self-apply any role except `ready-for-agent`, which it applies only to issues the human confirms (step 5). Grooming runs in the primary checkout; on the local tracker binding its writes land on the main branch, and it never edits an issue that is `in-flight` — a change for one goes through the run thread or waits (`platform.md` § The local binding) — with one exception: the human-confirmed orphan reset in step 1, safe because the claim is dead.

## Steps

1. Pull the backlog.
   - If issues were named, use exactly those. Otherwise take every open issue that is not already excluded, closed, or `in-flight`.
   - Sweep for orphans while listing: an `in-flight` issue whose recorded branch no longer exists, or is quiet past the policy playbook's horizon, is surfaced to the human as a candidate reset per `backlog-policy.md` § In-flight hygiene — never reset silently. A reset the human confirms is applied here as a grooming write (on main, on the local binding) — the dead claim cannot race it.
   - **At scale** — a freshly-adopted tracker can carry hundreds of open issues, most long-untouched. Do not try to fully groom all of them in one interactive pass. Batch: partition by the tracker's own signals (priority, area/component label, age, recent activity) and groom the batch the human names first (typically the near-term/high-priority slice), leaving the long tail listed but ungroomed for later passes. The goal of a first groom is a *usable* `ready-for-agent` set, not a fully-triaged backlog. Report the batch worked and the remainder deferred.
   - Completion criterion: a working set of open issues (a named batch when the backlog is large), each fetched with title, body, comments, and labels, and any in-flight orphans surfaced.

2. Propose work-type and surface per issue.
   - Orient on each issue and propose one work-type role — the full set is in `backlog-policy.md` § Label roles → Work-type (bug, enhancement, refactor, research, draft) — or mark it `needs-info`, `ready-for-human`, or an exclusion role. Propose `research` when the terminal deliverable is a source-backed account of what is known, inferred, contradicted, and unknown. Propose `draft` when correctness is instead judgment/taste — a memo, copy, or narrative synthesis. Map every proposal to this repo's labels per the playbook.
   - Also propose the dispatch surface from `backlog-policy.md` § Dispatch metadata (`backend`, `ui`, `mixed`, or `non-code`) and name any required capability.
   - Completion criterion: every issue has a proposed role and surface grounded in its content.

3. Clarify.
   - Where scope or requirements are ambiguous, ask the human directly and fold the answers into the issue body or a comment so they persist. For questions the human cannot answer now, comment the open question on the issue and set `needs-info`.
   - Assign a coordination class and reason: `routine` when the work is settled enough for a normal issue coordinator; `orchestrator-required` only for named product judgment, design, hard diagnosis, or another uncertainty the session orchestrator must own. Record the class, reason, and known uncertainty using the playbook's tracker encoding.
   - Completion criterion: each issue has work-type, surface, coordination class, and reason, or is parked as `needs-info` with its open question recorded.

4. Resolve relationships.
   - Detect dependencies between issues and record them per the playbook's convention (`backlog-policy.md` § Dependencies — a task-list line, frontmatter, or the tracker's native blocker relation) so `run` can read them. Mark superseded, duplicate, and already-resolved issues with the matching exclusion role, link the canonical issue, and close them when the tools and the user allow.
   - **Dedupe, don't re-litigate.** In an inherited backlog many issues overlap or restate one another; collapse the genuine duplicates to a canonical issue. But an issue the team already discussed, prioritized, or deliberately parked is a settled decision — record its existing state and move on; do not reopen its scope debate or re-propose a work-type the team already rejected. Grooming an adopted backlog is triage, not a redesign of every ticket.
   - Completion criterion: dependencies are recorded, genuine duplicates collapsed, and stale or redundant issues excluded or closed — without re-opening settled ones.

5. Shortlist and label.
   - Present the groomed candidates and let the human confirm which become `ready-for-agent`. Apply `ready-for-agent` only to confirmed issues carrying work-type plus complete dispatch metadata. Apply `ready-for-human`, `needs-info`, and exclusion roles as proposed.
   - Completion criterion: every issue carries its readiness role, and every `ready-for-agent` issue carries work-type, surface, coordination class, and reason.

6. Write back and hand off.
   - Ensure the tracker reflects every label, dispatch field, finding, clarification, and recorded dependency — it is the source of truth `run` reads. On the local binding, commit the tracker changes on the main branch.
   - Report which issues are now `ready-for-agent` and unblocked. As bare `backlog`, offer to run them; standalone, stop here.
   - Completion criterion: the backlog state is persisted on the tracker (committed, on the local binding) and the `ready-for-agent` set is reported.
