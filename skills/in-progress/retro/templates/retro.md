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
| Instance | `retro/` — `ledger.md`, `denylist.txt` |
| Pass due | 5 open entries, or 3 in one cluster |

## Transcript binding

Where each harness keeps this project's run transcripts; a retro pass reads only runs since the
last pass. Verified paths, recorded at setup — never guessed.

| harness | location |
|---|---|
| Claude Code | _unset_ |
| Codex | _unset_ |
