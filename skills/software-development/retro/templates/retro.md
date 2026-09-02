# Playbook: Retro

> Repo-owned bindings for the `retro` skill: the consent decision, the upstream target, the pass-due
> threshold, and where run transcripts live. Written by `retro setup` and reconciled thereafter —
> the skill's method stays in the skill; this file carries data.

## Consent

| | |
|---|---|
| Upstream feedback | **disabled** |
| Decided by / on | _unset — recorded by `retro setup`_ |

Enabled means retro passes may **draft and propose** upstream feedback issues. It never means
submit: every submission requires the user's approval of the verbatim text, per issue. Filing is
pseudonymous, not anonymous — issues are authored by the submitting GitHub account.

## Upstream target

| | |
|---|---|
| Repo | `asasher/asher-skills` |
| Label | `feedback` |
| Verb | `gh issue create` |

## Friction ledger

| | |
|---|---|
| Instance | `retro/` — `ledger.md`, `denylist.txt` (machine-local scrub half), `transcripts.md`; machine-local and untracked (`.gitignore` carries `/retro/`) |
| Shared denylist | `docs/agents/retro-denylist.txt` — tracked; the repo-shareable scrub terms |
| Pass due | 5 open entries, or 3 in one cluster |

## Transcript binding

| | |
|---|---|
| Harnesses bound | _unset — recorded by `retro setup`'s transcript-binding step_ |

How to find each harness's transcripts for this repo — the concrete verified locations live in the
untracked `retro/transcripts.md`, written by setup:

- **Claude Code** keeps per-project transcripts under
  `~/.claude/projects/<absolute project path with '/' replaced by '-'>/` as `*.jsonl`.
- **Codex** keeps sessions globally under `~/.codex/sessions/<year>/…`; filter to this repo by the
  cwd each session file records.

Locations are verified at use: when `retro/transcripts.md` is missing or a recorded location no
longer resolves, re-run setup's transcript-binding step rather than guessing. A retro pass reads
only runs since the last pass.
