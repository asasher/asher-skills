# v2 audit-fix verification — verdicts

Verification of the 60-item audit-fix batch (branch `sdlc-lifecycle`), per the agreed stack:
repo gates, audit-mapping regression re-run, negation check on the diff, dual-executor probes.

## 1. Repo gates — green

- `tools/test_catalog.py`: 17 tests OK.
- `site/check.py`: 0 errors, 0 warnings (codebase.md registered in the sdlc view; this repo's own
  `docs/agents/codebase.md` written).
- Staffing eval suites (`test_global_apply`, `test_provider_pilot`, `test_global_templates`): OK —
  after twice trimming the external-worker additions to fit the compiled prose byte budget the suite
  enforces.

## 2. Regression re-run (5 theme agents, cached extractions vs revised sources)

Every previously GAP / PARTIAL / REGRESSION-RISK observation and consolidated gap line re-verdicted:

| Theme | Re-verdicted | First pass | Residue fixed in follow-up |
|-------|--------------|-----------|---------------------------|
| Shaping & specs | 13 | 12 solved, 1 weakened | groom label-autonomy clause reconciled with the confirmation gate |
| Build pipeline | 23 | 22 solved, 1 open | read-`codebase.md`-before-editing mandate added to implement + tdd |
| Review, evidence & merge | 25 | 21 solved, 4 open | AC-N keying in code-review's Spec brief; evidence head SHA in prove-your-work; capture-escalation ladder; exit-status capture rule |
| Cross-cutting | 23 | 22 solved, 1 open | parent-`.git` lock contention row in environment.md |
| Dispatch & orchestration | 29 | 27 solved, 2 open | worktree-local ticket read in build step 1; bounded seam attempts in verify-your-work |

All residue fixes are one-to-three-sentence edits; deliberate absences (no flake ledger, no
run-state.py restoration) were briefed as design decisions and confirmed as such by the agents.

## 3. Negation check on the added diff

Two findings, both dangling references rather than bad negations — fixed: the per-ticket-disposable
marking now exists in environment.md § Verification data, and the quiet horizon is a named term in
backlog-policy § Building hygiene. Zero history narration; zero cross-skill contradictions; the
negation-shaped additions all trace to observed drift.

## 4. Dual-executor Tier 1 probes (keys written before runs; packets key-free)

| Skill | Claude (opus subagent) | gpt-5.6-sol (`codex exec --sandbox read-only`) |
|-------|------------------------|------------------------------------------------|
| backlog | 9/9 | 9/9 |
| to-subagent | 7/7 | 7/7 |
| verify-your-work | 8/8 | 8/8 |
| build | 7/7 | 7/7 |

**62/62.** Both executors' backlog P7 answers flagged the same anticipated ambiguity (concrete
foreign-claim handling lives in backlog-policy § Building hygiene, cited by SKILL.md) — a valid
flagged-ambiguity answer per the probe rules. Sol transcripts alongside this file; Claude executor
answers in the session transcript.
