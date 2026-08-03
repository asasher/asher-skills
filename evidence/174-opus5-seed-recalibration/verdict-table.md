# Verdict table — ticket #174 (opus-5 seed recalibration to 7/7)

Change under proof: `skills/system/staffing` opus-5 row 8/8 → 7/7 in both variant seeds and the machine-audit illustrative example, at reviewed head 2c58af3. Answer key: the pre-existing key in `skills/system/staffing/evals/probes.md` (written before any runs, per `docs/agents/probe-evals.md`). Affected probes are P7 and P8 — the ac-6 pair covering the seed and the five-model example table, the only probes touching the edited files' content. The data check is this ticket's acceptance criterion, graded against the ticket body (intelligence 7 / taste 7, cost 3 and effort high unchanged, everywhere the seed row appears in the skill source).

| probe | criterion | Claude executor (fable-5 subagent) | Codex executor (gpt-5.6-sol, `codex exec --sandbox read-only`) |
| --- | --- | --- | --- |
| P7 — may the five-model table ship as a roster? | ac-6 | PASS — refused, cited "Never write a seeded default this machine failed to verify" + the illustrative-only heading | PASS — refused, cited machine-audit.md:3 and :45, plus SKILL.md:42 |
| P8 — status of the five-model table | ac-6 | PASS — quoted "Example of audit output (illustrative only — NOT the shipped roster)" verbatim | PASS — quoted the same label verbatim, machine-audit.md:43 |
| Data check — opus-5 row values post-change | ticket #174 acceptance | PASS — 7/7 in claude seed:16, codex seed:16, machine-audit example:54; cost 3 / effort high unchanged | PASS — same three readings, 7/7, independently cited by line |

Both executors additionally re-flagged one **pre-existing** ambiguity, unchanged by this diff and recorded as a finding, not a failure (per the probe method: "flagged ambiguities are findings to feed back into the wording"): the audit's "add a seeded row for any reachable model the seed omits" names no origin for that row's initial judgment numbers. Out of scope for #174.

Mechanical checks at the same head: repo-wide grep shows no residual 8/8 opus-5 row in the skill source; `npx prettier@3.6.2 --check` passes on all three touched files; `git diff --stat 42c29c1...2c58af3` shows only the three skill-source files — no playbook (`docs/agents/staffing.md`) or installed-mount edits.

Transcripts: `claude-subagent-transcript.md` (verbatim executor return) and `codex-sol-transcript.txt` (raw `codex exec` session output, model/session header included).
