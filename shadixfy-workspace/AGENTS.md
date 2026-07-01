# shadixfy Eval Workspace

These instructions apply only when working on this eval workspace. They are not part of the
generated eval prompts; the harness runs agent cells in isolated temp directories outside this repo.

## Agent execution

How each agent participant is produced is fixed by policy (it has billing consequences), matching
`dissolve-workspace` and the `skill-loop` skill's Agent execution policy:

- **`claude` cells → the orchestrator's Agent-tool subagent, never `claude -p`.** A subagent shares the
  orchestrator's session quota, context, and prompt cache. A nested `claude -p` process authenticates as a
  separate metered client — per-token API billing if `ANTHROPIC_API_KEY` is set, otherwise a fragmented,
  separately-rate-limited subscription session. So the harness **skips `claude` cells by default**:
  `run_one.sh` / `run_all.sh` build and save each `prompt.txt`, then leave the cell for the orchestrator to
  fill by running that prompt through a subagent (in a fresh temp dir) and copying its HTML into the cell's
  `outputs/`.
- **`codex` cells → `codex exec` CLI.** Codex under a ChatGPT plan draws from that plan's included allowance,
  so the harness runs it directly (isolated `CODEX_HOME`).
- **Hard-gated CLI fallback.** Only a non-Claude orchestrator with no subagent path should ever run
  `claude -p`, and only after **explicit human approval**. Loudly flag the extra usage, then acknowledge it by
  setting `ALLOW_CLAUDE_CLI=1`, which switches the harness back to `claude -p`.

## Iteration Contract

- A comparison iteration is not complete until `dashboard.html` has been rebuilt from the latest
  iteration artifacts.
- Before running a new comparison after editing the target skill, refresh the injected snapshot:
  `cp ../skills/shadixfy/SKILL.md conditions/shadixfy.md`.
- Run the full matrix from this directory with `bash scripts/run_all.sh N`, where `N` is the next
  iteration number. That command runs agent cells, screenshots outputs, grades them, aggregates
  `iteration-N/benchmark.json`, and rebuilds `dashboard.html`.
- If you run individual cells, edit manual grades, change `feedback.json`, or otherwise update
  iteration artifacts outside `run_all.sh`, finish with:
  `node scripts/aggregate.mjs N` and then `node scripts/build_dashboard.mjs`.
- Report the rebuilt dashboard path, the new iteration directory, and the aggregate deltas.

## Cost Boundary

The full matrix runs `codex` cells via the `codex exec` CLI (subscription-billed) and `claude` cells via
in-session subagents (see **Agent execution**) — neither should incur per-token API billing by default, but
both consume real model usage. Be explicit with the user before starting a full matrix, and do not start
additional iterations after the requested stop point. Never set `ALLOW_CLAUDE_CLI=1` (which routes `claude`
cells back through `claude -p`) without explicit approval of the extra usage.
