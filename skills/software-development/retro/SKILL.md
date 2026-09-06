---
name: retro
description: Record skill friction with retro note, triage recurring problems with retro, or bind private records and upstream consent with retro setup.
metadata:
  optional: [capture]
  setup: reference/setup.md
---

# Retro

Turn skill friction into fixes. Ordinary product work belongs in `capture`.

## note <observation>

Append the date, skill, concrete observation, and transcript run tag under `## Open` in `retro/ledger.md`. Keep full local details. Report `noted; N open entries`; mention a pass is due only when the playbook's threshold is crossed. Analysis waits for an invoked pass.

Resolve `retro/` against the primary working tree, using the resolved Git common directory and worktree registrations. All linked worktrees share this machine's one private ledger. Create it on first use and keep it untracked with the root-anchored `/retro/` ignore rule. `denylist.txt` and `transcripts.md` live beside it; shared scrub terms live in tracked `docs/agents/retro-denylist.txt`.

## retro

1. Read `docs/agents/retro.md`, open entries, and their run transcripts. Also inspect runs since the last pass for unrecorded corrections, aborts, and repeated instructions. A missing playbook requires setup; missing or stale transcript bindings require setup's transcript step. Report inaccessible evidence as a gap.
2. Cluster the same underlying problem across distinct runs, including matches in `## Triaged` from earlier passes. Repeated wording in one run counts once.
3. Present every cluster in one table: evidence, disposition, proposed action. Use **local fix** for this repo's bindings, **upstream candidate** for a skill defect seen in at least two independent runs, or **noise** with a reason.
4. Apply small local binding fixes within existing authorization. Capture larger work as tickets. When the playbook enables upstream proposals, follow [upstream feedback](reference/upstream.md); disabled means report the candidate count without drafting or repeated consent requests.
5. Move handled entries to `## Triaged`, recording the fix, ticket, proposed feedback, or noise reason. Keep unfinished actions explicit and record the transcript watermark so the next pass resumes.

## setup

Follow [setup](reference/setup.md) to record upstream consent and targets, verify transcript locations, seed both denylists, and reconcile [the playbook](templates/retro.md). Setup permits drafting only; each upstream submission still needs approval of its exact text.
