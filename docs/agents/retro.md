# Playbook: Retro

> Repo-owned bindings for the `retro` skill: the consent decision, the upstream target, the pass-due threshold, and where run transcripts live. Written by `retro setup` and reconciled thereafter — the skill's method stays in the skill; this file carries data.

## Consent

|                   |                                                |
| ----------------- | ---------------------------------------------- |
| Upstream feedback | **enabled**                                    |
| Decided by / on   | Asher, 2026-07-30 (asher-skills#142 reconcile) |

Enabled means retro passes may **draft and propose** upstream feedback issues. It never means submit: every submission requires the user's approval of the verbatim text, per issue. Filing is pseudonymous, not anonymous — issues are authored by the submitting GitHub account.

Note the standing oddity of this repo: it is its own upstream. An upstream candidate here can also be fixed at the source directly — drafting an issue is still the right move when the fix isn't landing in the same session, so the finding survives.

## Upstream target

|  |  |
| --- | --- |
| Repo | `asasher/asher-skills` |
| Label | `feedback` (created 2026-07-30 at setup — it did not pre-exist) |
| Verb | `gh issue create` (route verified live 2026-07-30: `gh repo view` clean) |

## Friction ledger

|          |                                        |
| -------- | -------------------------------------- |
| Instance | `retro/` — `ledger.md`, `denylist.txt` |
| Pass due | 5 open entries, or 3 in one cluster    |

## Transcript binding

Where each harness keeps this project's run transcripts; a retro pass reads only runs since the last pass. Verified paths, recorded at setup — never guessed.

| harness | location |
| --- | --- |
| Claude Code | `~/.claude/projects/-Users-asher-Projects-asher-skills/*.jsonl` — per-project, verified 2026-07-30 (182 files) |
| Codex | `~/.codex/sessions/<year>/…` — **global, not project-partitioned**; filter to this repo by the cwd each session file records. Verified present 2026-07-30 |
