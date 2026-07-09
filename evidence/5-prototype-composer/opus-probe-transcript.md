# Opus in-session probe executor — transcript

Executor: Opus subagent (Agent tool, independent context), answer key withheld. Read only
`skills/prototype/{SKILL.md, README.md, reference/prototyping.md, agents/openai.yaml}`.

| Probe | Answer summary | Citation | Verdict |
|-------|----------------|----------|---------|
| **P1** (ac-1) | Ships 5 files: SKILL.md, README.md, agents/openai.yaml, reference/prototyping.md, evals/probes.md. Layout matches siblings — same SKILL/README/agents/evals/reference skeleton; extra dirs are per-skill. | directory listing vs staffing/review-loop | PASS |
| **P2** (ac-2) | user-invocable: true; description carries thin composer / throwaway artifact / one design question / beyond code, all verbatim. | SKILL.md frontmatter | PASS |
| **P3** (ac-3) | Three pointers: bundled references, project playbook, sibling skills. Prototype is a composer (not root primitive); names review-loop + staffing as load-bearing. | SKILL.md § Dependency surface | PASS |
| **P4** (ac-4) | No file imports/path-references another skill's files; siblings by plain name only; only cross-paths point to its own reference + the playbook. | SKILL.md "composed by plain name, no imports" | PASS |
| **P5** (ac-5) | Throwaway ARTIFACT, not code-only. Non-code example: hand-driven state table / scenario run (behavior); structurally different rendered one-pager drafts (form). | reference/prototyping.md behavior/form shapes | PASS |
| **P6** (ac-6) | Four gates in order: Question stated → Built and handed over → Answer captured → Cleaned up. "Throwaway from day one: keep the answer, delete the artifact." Prototype never the record. | SKILL.md gates + framing | PASS |
| **P7** (ac-7, code) | Q: allow failed→pending? Shape: behavior. Build: pure reducer/state-machine module + minimal terminal shell driven through awkward sequences. Who: staffing resolves the builder (mechanical). Present: live terminal driven directly, URL announced. Answer: into consuming plan. End: deleted, validated module lifted. | reference/prototyping.md behavior shape + compose + capture/cleanup | PASS |
| **P8** (ac-8, non-code) | Q: how to lay out the brief? Shape: form. Build: 3 structurally different standalone HTML drafts. Who: staffing → taste-ranked. Present: via review-loop by name, URL+hub. Answer captured, then delete. Must NOT assume repo/task-runner/component-library — absent playbook, defaults (self-contained artifact in scratch/workspace dir). | reference/prototyping.md form shape + defaults | PASS |
| **P9** (ac-9) | Prototype files never instruct editing backlog; skill is self-contained (imports no other skill's files); repo placement deferred to docs/agents/prototyping.md playbook. | SKILL.md | AMBIGUOUS — backlog files outside executor read set; confirmed PASS by independent git-diff file-check |

Ambiguity finding (P9): the probe asked about backlog's files but the method withheld them from the executor; folded back into `evals/probes.md` (commit 007d354) so P9 now grants read access. ac-9 independently confirmed by git-diff.

Verdict: **8 PASS, 1 AMBIGUOUS** (P9, resolved PASS by file-check).
