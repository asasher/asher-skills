# Evidence — #166 staffing transient self-heal (probes P28–P33)

Dual-executor eval transcripts for the self-heal probes, both run against the final reviewed product head **ccdb9f3** (`ccdb9f3f5861ef545c63d32863a8206498afc6ca`), the head adversarial review converged LGTM on.

- `claude-leg-P28-P33.md` — Claude executor leg: Opus subagent (Agent tool), in-session, read-only. Probes P28–P33 verbatim; answer key withheld from the executor.
- `codex-leg-P28-P33.txt` — Codex executor leg: `codex exec -m gpt-5.6-sol -s read-only --skip-git-repo-check` (codex-cli 0.146.0), foreground, raw transcript.

Answer key: `skills/system/staffing/evals/probes.md` (P28–P33 with the criterion coverage map), **committed before any run** in `7ba4e6a` per the pre-committed-key eval discipline (`docs/agents/probe-evals.md`).

Transcripts are copied verbatim from the run outputs; no regrading, no rerun.
