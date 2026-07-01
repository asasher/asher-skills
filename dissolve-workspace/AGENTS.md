# dissolve Eval Workspace

These instructions apply only when working on this eval workspace. They are not part of the
generated eval prompts; agent runs happen in this workspace's `runs/` dirs (Codex in an isolated
`CODEX_HOME`), never leaking ambient skills/`AGENTS.md` into the eval itself.

## Agent execution

How each agent participant is produced is fixed by policy (it has billing consequences), matching the
`skill-loop` skill's Agent execution policy:

- **Claude → the orchestrator's Agent-tool subagent, never `claude -p`.** A subagent shares the
  orchestrator's session quota, context, and prompt cache. A nested `claude -p` process authenticates as a
  separate metered client — per-token API billing if `ANTHROPIC_API_KEY` is set, otherwise a fragmented,
  separately-rate-limited subscription session. This workspace has **no `run_claude` script on purpose**: the
  Claude side is always run by the orchestrator as a subagent (seed the target dir, run the prompt through a
  subagent, let it edit the seeded `dissolution.html` in place).
- **Codex → `codex exec` CLI.** Codex under a ChatGPT plan draws from that plan's included allowance, so run
  it directly via `run_codex` (isolated `CODEX_HOME`).
- **Hard-gated CLI fallback.** Only a non-Claude orchestrator with no subagent path should ever run
  `claude -p`, and only after **explicit human approval** of the extra usage. Loudly flag it first; never run
  it silently.

## Run contract

See `README.md` for the full walkthrough. In brief, from this directory:

- Solo (codex): `source scripts/lib.sh`, then `seed runs/solo/codex && run_codex runs/solo/codex runs/solo/PROMPT.txt`.
- Solo (claude): `seed runs/solo/claude`, then run `runs/solo/PROMPT.txt` through a **subagent** against the
  seeded `dissolution.html`.
- Pair (debate): `seed runs/pair`, then alternate turns per `conditions/dissolve-pair.md` — Claude subagent
  ⇄ `run_codex` — both editing the shared `dissolution.html` + `discussion.md`.

## Cost Boundary

Codex cells run via the `codex exec` CLI (subscription-billed) and Claude cells via in-session subagents —
neither should incur per-token API billing by default, but both consume real model usage. Be explicit with
the user before a run. Grading is done later by a human against `reference/article-key.md`; agents never see
that file.
