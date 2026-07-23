# Cold-read of the SDLC skill family — synthesis

Five context-free readers (2026-07-20) read every family skill as a consumer agent would — no
authoring history, no answer key — flagging ungrounded sentences, contradictions, drifted
redundancy, genuine confusion, and undefined terms. Verbatim reports with exact quotes:
`raw-reports.md`. ~95 findings total; most are mechanical rewords/deletions, but the readers found
real contradictions the informed audits missed *because* they knew the history.

## The headline: one structural tension, three surfaces

The skills preach **"compiled from the machine, never shipped fixed"** (machine-audit, audit-mode)
while shipping **byte-authoritative templates full of one machine's values and private history**:

- `staffing/variants/*/templates/global/staffing.module.md` ships a concrete roster (model rows,
  "plan #73", a dated incident, "never Haiku" banning a model no row introduces) that setup applies
  byte-verbatim — directly contradicting "seed only rows the audit found reachable."
- `setup-asher-skills/templates/global/presentation.common.md` hardcodes "When Asher is at this
  machine" and one tailnet hostname into a module offered to any machine.
- The module templates also *lack* the Wake-paths table that `watch.md` and machine-audit step 7 now
  require — the table was added to this machine's live modules but not to the shipped templates
  (cross-skill contradiction introduced by the wake-path change).

Resolution direction (needs owner confirmation): templates become seeds with machine-fact
placeholders; setup renders them from the audit; the byte-authoritative check applies to the staged
rendered copy, not template-verbatim.

## Contradictions that change output (fix with rulings, before or with the restructure)

1. **to-tickets edge form**: templates/template-guide assert `- [ ] depends on #N` marker lines
   unconditionally; slicing § Order and wire (and this repo's own playbook) demand the tracker's
   native blocking relation when recorded. A cold agent emits the wrong edge form. Single-home in
   slicing; templates say "the playbook's recorded convention," no default.
2. **merge-changes vs platform.md**: the playbook's § Change review says "the human merges on
   GitHub — the loop never merges" and records no merge verb — blocking the skill it binds.
3. **backlog playbook optionality**: SKILL.md table says `docs/agents/diagnosing-bugs.md` is
   optional; run's preflight requires it (plus researching.md).
4. **Interactive criteria timing**: verifying playbook reads criteria from "the PR body at its
   start," but the build loop creates the PR after verify.
5. **change-description Plan bullet** requires a committed, approved plan; enhancement JIT plans are
   deliberately neither.
6. **bare-minimum-ux is load-bearing but undeclared** in backlog's implementing/verifying playbooks
   ("always loads… wins on conflict") — no sibling declaration, no degrade.
7. **staffing dispatch envelopes**: variant harness.md says read-only/workspace-write; module
   template says `--sandbox danger-full-access` / `--dangerously-skip-permissions` for the same
   dispatch.
8. **review-loop state dir**: review-loop.md mandates one canonical state path and bans ad-hoc
   siblings; scripts.md's typical invocation uses exactly the banned shape.
9. **run-state tokens**: `completed|blocked(edge)|deferred(wave)|…` (run.md) vs
   `complete|blocked|deferred|…` (run-state.md); `verify-terminal` missing from run-state's own
   subcommand list.
10. **prototype shapes**: gate 1 enumerates behavior/form; the reference defines a third
    (falsification). Plus: is falsifiability demanded of form-shape prototypes at all?

## Authoring-context leakage confirmed in the wild (delete/reword; no rulings needed)

- `docs/agents/prototyping.md` calls prototype "the backlog `prototype` subskill," points at a
  nonexistent `reference/prototype.md`, and ships a full second copy of the technique in drifted
  vocabulary (logic/UI vs behavior/form). Cut to the repo-delta section.
- The "retired plan stage" family: "carried from the plan/PRD rule" / "plan/spec rule" (drifted
  twins), "(the retired per-ticket plan stage)" (the audit's own fix, still ungrounded), catalog.md's
  "replaced the retired plan stage," setup.md's "retired versioning scheme" / "the old picking-models
  install," agent-skills-block's "there is no `ask-asher` dispatcher skill," review-loop's
  "#46"-adjacent custody prose, staffing module's "plan #73" and dated incident. All reword to
  history-free instruction.
- Repo-as-author leaks in shipped contracts: slicing's "this repo: GitHub `blocked_by`" and "On this
  repo that binding is GitHub via `gh`" (contradicting its own tracker-agnostic rule); research
  contract's `evidence/`/"backlog deliverable" vocabulary and `<skill>-workspace/` convention;
  rankings' "on this machine" browser example; skill-authoring template presupposing this repo's
  probe-evals discipline.

## Cross-cutting confusion classes (batch-fix in the restructure)

- **Undefined role/term at point of use**: "durable work/change record" (diagnosis, two names),
  "the register," "keep-both provenance," "presentation-surface config" (adopt review-loop's term),
  "execution slot," "internal holds," "sonnet-low," "all four modules," "the liveness contract" (in
  staffing), `agent-browser`/`agentmail` (gloss as role nouns), "seeded marker"/"legacy header"
  (quote verbatim or delete the migration).
- **Pointer generality drift**: the presentation playbook named three ways across review-loop files;
  environment section-name mismatches between common and skill-authoring packs ("Driving the app &
  capturing evidence" vs "Driving behavior…", missing Verification data section).
- **Degrade gaps**: to-tickets with no platform binding (stop vs local tickets.md?); prototype
  capture destination standalone-without-playbook; interview-with-docs' impossible "bare interview"
  degrade when interview is the absent sibling.
- **Small but load-bearing rewords**: heartbeat "at most every 10 minutes" inverts the staleness
  bound; "every open thread: settled…" (a settled thread isn't open); adversarial-review's Fixer
  sentence missing the noun "comments"; groom hard-coding the readiness rule the policy declares
  adjustable; the "exact verdict" string differing by a period between homes.

## Already-resolved by standing decisions (fold into the shape restructure)

- interview purification (no siblings, no § Dependency surface, classification not dispatch) clears
  the trio's layer leaks; interview-with-docs' findings mostly dissolve with it into `shape`.
- `## Context documents` index underspecification (which file when only CLAUDE.md exists) → adopt:
  "AGENTS.md if the repo has one, else CLAUDE.md; create the section if absent."
- "the upstream shaping flow (interview → spec → tickets)" in backlog → becomes the `shape` sibling
  by name once shape exists; `needs-spec` → `needs-shaping` rename lands the same pass.

## Installed-copy drift

Multiple readers confirmed `.agents/skills/*` diverges from sources (descriptions differ). After the
fix pass: reinstall/reconcile via setup-asher-skills, per the packages-are-build-products rule.
