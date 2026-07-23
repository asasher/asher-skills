# Skill verbosity audit — synthesis

Five parallel auditors (2026-07-20) read every family skill against the `writing-great-skills`
yardstick (no-ops, duplication, sediment, sprawl, leading-word collapse, one-trigger-per-branch
descriptions). Constraint: **no behavior change** — every rule, gate, criterion, ordering, and edge
case must survive; grammar may be sacrificed. Anything uncertain was flagged RISKY, not proposed.
Raw per-file findings with exact quotes and replacements: `raw-reports.md` (apply from there).

## Totals

| Group | Files | Words now | Est. after | Cut |
|---|---|---|---|---|
| backlog | SKILL + 13 reference + 13 templates | 21,994 | ~20,000 | −9% |
| services + UX (review-loop, staffing, setup-asher-skills, bare-minimum-ux) | 24 | 15,619 | ~13,400 | −14% |
| formation (to-spec, to-tickets, merge-changes) | 9 | 6,400 | ~5,325 | −17% |
| probes (prototype, research, diagnosing-bugs) | 9 | 4,538 | ~4,120 | −9% |
| shaping (interview, domain-modeling, interview-with-docs) | 5 | 2,268 | ~1,850 | −18% |
| **Total** | **~74** | **50,819** | **~44,700** | **−12%** |

## Defects found beyond verbosity (fix first — these are correctness, not prose)

1. **Contradiction (behavior fork):** `review-loop/SKILL.md` await says the watcher is "selected with
   `staffing route`" while `reference/watch.md` explicitly prohibits a generic `staffing route` for the
   watch task (read the roster's published Floor instead). Two sources of truth disagree; one must be
   corrected to match the intended behavior before any dedupe.
2. **Orphan reference file:** `bare-minimum-ux/references/planning.md` — no pointer anywhere in the
   skill loads it; it never fires. Owner decision: add a pointer (behavior addition) or delete.
3. **Stale example rows:** `setup-asher-skills/templates/agent-skills-block.md` still shows a `plan`
   row (retired skill) and describes backlog as running "to a merged PR" (contract is review-ready PR;
   merging is `merge-changes`).
4. **Attribution violations (repo convention: credits live in README):** "Adapted from Matt Pocock's
   `to-spec`…" (synthesis.md), "(Matt's posture)" (to-tickets SKILL.md), "Matt Pocock's posture is
   that" (slicing.md), "Adapted from `setup-matt-pocock-skills`…" (interview.md), "#46 self-approval
   incident" provenance in review-loop.md.
5. **Retired-plan sediment:** both `template-guide.md` files (to-spec, to-tickets) describe the retired
   plan stage as if it still gates implementation; groom.md carries a "formerly made mid-run by the
   plan gate" history sentence.

## Cross-cutting patterns (what to fix systematically)

- **SKILL.md re-inlines its always-loaded reference.** The dominant pattern in formation and probes:
  gates and steps carry full second copies of rules the force-loaded reference owns (to-tickets step 3b
  vs slicing § Audit; research gates 2–5 vs the contract; to-spec step 6 vs synthesis § Sign-off).
  Fix shape: headline + pointer; the reference is the single source of truth.
- **Setup steps twin their own templates.** Backlog's setup.md restates the shipped playbook defaults
  it installs (check discovery, driver gates, wrapper contract, verification data). Rule: the file
  read *at runtime* keeps the gates; setup keeps only the setup-time actions and points.
- **Multi-site algorithms.** Backlog's ledger names ten rules living at 3–5 sites each (resolved
  scaffold set ×4, parallelism asymmetry ×5, local-binding write discipline ×4, liveness contract,
  needs-info/needs-spec boundary…). Each gets one named SSOT; other sites become one-clause pointers.
- **Descriptions carry synonym triggers and method summaries.** "broken, failing, throwing" → one
  branch; user-invoked skills (all of formation, backlog, setup) get one-line human descriptions with
  trigger lists stripped — guaranteed behavior-neutral since the agent never loads them.
- **In-file repetition of one caveat.** machine-audit.md states "it's only an example" five times and
  "user tunes the seeds" three times.

## Deliberate duplication to KEEP (different actors, disjoint contexts)

Deduping these would remove a rule from one actor's context entirely:
- verify.md grade-quoting AND build-loop step 8 (checker vs coordinator).
- adversarial-review.md behavior ruling AND change-reviewer.md final bullet (orchestrator vs Reviewer).
- change-reviewer.md artifact-opening re-check (defense-in-depth vs verify step 1).
- diagnosing-bugs SKILL.md contract item 3 vs phase 5 (caller-facing return spec).
- Per-reference "playbook missing → report setup gap and stop" lines.
- Reviewer's styling-reuse verdict string (the Reviewer must utter it; may load only its playbook).

Plus RISKY-flagged lines that look redundant but bind behavior (keep): interview's "a cap is manners,
not a rule" and intra-round dependency rule; prototype's "Usable anywhere, not only dev" trigger;
watch.md's rationale for not holding the await inline; staffing's worked example (candidate trim only).

## Ranked application order

1. Fix the five defect items (contradiction first — requires a behavior decision on watcher routing).
2. Backlog ledger dedupes: scaffold set → setup.md §1; parallelism asymmetry → worktree-isolation.md;
   write discipline → platform.md § local binding; build-loop's re-inlined definitions (highest
   per-word runtime cost — pasted into every issue thread).
3. Formation SKILL.md collapses (steps → reference pointers): to-tickets 3b/4/5, to-spec 1/6.
4. Staffing/setup-asher-skills cross-file: barrier choreography → two SSOTs; resolution order →
   rankings-and-routing.md; catalog.md's prose edge list → delete (stored snapshot inside the
   "no snapshot is stored" file).
5. Probes + shaping: research gates → contract pointers; adr-format/context-format dedupe vs SKILL.md;
   description trigger collapses everywhere (cheapest, safest, highest value-per-word).

After application: re-run the dual-executor probe evals (`docs/agents/probe-evals.md`) on the edited
skills — the no-behavior-change constraint is exactly what the eval suite exists to verify.
