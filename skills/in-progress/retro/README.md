# Retro

Turns the friction of working with skills into fixes. Every skill run — a groom, a build, a shaping
thread — throws off friction nobody writes down: instructions an agent misread, confirmations a user
had to repeat, stale playbook rows. Retro keeps a **friction ledger** (always-on, local, private —
any session appends via `retro note` the moment a stumble happens) and periodically runs a **retro
pass**: cluster the open entries with the run transcripts behind them, triage every cluster into
**local fix** / **upstream candidate** / **noise**, and turn the result into work.

> Pre-deployment evals pass (2026-07-30): Tier 1 situated probes **10/10 on both executors** (Claude
> sonnet subagent in-session + gpt-5.6-sol via `codex exec --sandbox read-only`, key written before
> runs); Tier 2 scrub dry-run **9/9 checks** (`evals/scrub-dryrun.sh`).

The upstream half is the rare edge, and consent-gated twice: a setup-time decision (default
**disabled**) governs whether passes may even *propose* feedback issues on the skill source repo,
and every proposed issue still requires the user's approval of the verbatim text before it is filed
— from their own GitHub account, which the ask says plainly (content sanitized, authorship
pseudonymous, never anonymous). Drafts are written generatively in skill vocabulary — never by
redacting local material — and pass a mechanical scrub (`scripts/scrub.py`: denylist terms, emails,
absolute paths, foreign URLs) before a human ever sees the approval ask.

## When to use

- **Mid-run** — a skill stumbled, the user repeated themselves, a workaround was needed:
  `retro note <observation>`. Cheap by design; dispatchers and siblings invoke it by name.
- **Periodically** — the note verb reports when the ledger crosses the pass-due threshold; `retro`
  runs the pass. It opens with findings, never with a bare "any feedback?".
- **Once per repo** — `retro setup` records consent, upstream target, transcript bindings, seeds
  the denylist halves, and keeps the instance untracked.

Not for capturing ordinary work items (`to-backlog`), not a general review of the codebase — its
subject is the skills' own performance in this repo.

## Shape

- **Capture is cheap and constant; analysis is lazy and batched.** The ledger costs one line;
  clustering and triage happen only at a pass.
- **Recurrence is the bar for upstream.** Two or more independent occurrences across runs; one bad
  run is weather.
- **Local-first.** Most friction is a repo binding problem — fixed in playbooks or captured as
  tickets via the `to-backlog` sibling — and never leaves the machine.
- **No auto-submit, ever.** Consent recorded at setup means propose, not send.

## Layout

`SKILL.md` is the contract — ledger format, the pass, the upstream gate. `reference/setup.md` is
the setup procedure; `templates/retro.md` the playbook it installs to `docs/agents/retro.md`;
`scripts/scrub.py` the mechanical leak scan; `agents/openai.yaml` the Codex manifest;
`evals/probes.md` + `evals/key.md` the pre-deployment probe eval, `evals/scrub-dryrun.sh` the
scripted dry-run for the scrub mechanics.

Stateful: the `retro/` instance (ledger, the machine-local denylist half, transcript locations) is
consumer-owned resume state, **machine-local and untracked** — setup gitignores it, since it
describes one machine. The repo-shareable denylist half is tracked at
`docs/agents/retro-denylist.txt`, and the scrub takes both halves. The Open/Triaged split is the
pass watermark, so a bare `retro` continues with no recap.

## Install

`npx github:asasher/asher-skills install --skill retro`, then `retro setup` once in the consuming
repo.
