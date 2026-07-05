# Task: Adversarial review of the Goodwork v2 spec + skill draft, fix in place

Review everything the v2 drafting pass produced: `goodwork-workspace/v2/SPEC.md`, `SCHEMAS.md`, `ROADMAP.md`, and all changed/new files under `skills/goodwork/`. The authoritative requirements: `goodwork-workspace/v2/BRIEF-v2-spec.md`. The skill-authoring rules: `.claude/skills/writing-great-skills/SKILL.md` + `GLOSSARY.md`. Fix directly; log every fix as one line in `goodwork-workspace/v2/REVIEW-FINDINGS.md` (severity: blocker/major/minor); put anything needing a human decision under "Open questions" instead of guessing.

## Adjudicated calls (the drafter self-reported five risky calls — these verdicts are final, implement them)

1. `setup` in a new Connect category — ACCEPTED, keep.
2. Evidence inbox inside `metrics.json` — REJECTED. The inbox is a queue of pending profile evidence, not a metric. Give it a proper home (own file, e.g. `evidence-inbox.jsonl`, or a clearly separated top-level structure — your call) and update state.md/SCHEMAS/SPEC/profile.md/review.md consistently.
3. Reply records inside `pipeline.json` — ACCEPTED, but verify there is an archival/compaction story so pipeline.json doesn't grow unboundedly; add one if missing.
4. Stable MagicDNS host + rotating per-session token — ACCEPTED. Verify SPEC explains how the phone flow survives token rotation (bookmark hits stable host → gets a fresh tokenized session, or equivalent) without weakening the CSRF defense.
5. Approval required BEFORE Gmail draft creation — REJECTED. Creating a draft in the user's own Gmail is not outbound; the draft IS the review surface and the user pressing send in Gmail IS the physically enforced gate (that was the brief's design). Fix execution.md/SPEC: no approval record needed to create a draft; define what, if anything, gets logged for email (e.g. a draft-created event for reconcile matching). Connector-sent email (if ever) still requires full approval.

## Review dimensions (cover all)

1. **Brief conformance**: walk BRIEF-v2-spec.md's locked decisions one by one against the draft — flag anything missing, weakened, or invented beyond the brief's room.
2. **Single source of truth**: state model must live only in state.md, ladder/gates only in execution.md; other files may point, never restate. Hunt duplication across all 19 skill files.
3. **Description regression**: SKILL.md's new description is a ~13-noun trigger list — the exact sprawl pruned in the previous iteration. Rewrite per writing-great-skills: one trigger per genuine branch (roughly: define direction / test-redesign / position / campaign-operate / sustain-reconcile), front-loaded leading words, no identity restatement.
4. **Schema coherence**: every file named in state.md exists in SCHEMAS.md and vice versa; IDs cross-reference correctly (event → approval → pipeline card → lead → target); approvals.jsonl and events.jsonl records carry everything the gate-validation flow in execution.md needs (content hash, granularity, batch listing).
5. **Server/await contract soundness**: token on every request incl. POST; 127.0.0.1 bind; funnel ban stated; lifecycle (up while pending, idle-timeout after drain) unambiguous; await semantics defined for timeout, partial matches, and events that arrived before await started (cursor rules); crash/restart behavior.
6. **Gate integrity walkthrough**: trace one application end-to-end through the draft docs (tailor → render review → click approve → hash validate → execute → screenshot proof → pipeline update). Any step where the docs are ambiguous or contradictory is a finding. Do the same for a batch approval and for a hash-mismatch rejection.
7. **Safety completeness**: quota + evidence gate as hard preconditions present in execution.md; WhatsApp read-only + ban disclosure in setup.md; .env hygiene; sensitive-data rules survived the rewrite; nothing grants the agent authority to send without approval anywhere.
8. **Roadmap quality**: six slices each with checkable definition-of-done and named new eval gates; slice order matches the brief.

## Rules

- Verify what's cheap to verify (JSON examples parse, internal links resolve, line counts, cross-file name consistency via grep). No implementation, no eval runs.
- Keep SKILL.md ≤ 85 lines after your fixes.
- Do not touch `goodwork-workspace/eval/` or anything outside `skills/goodwork/` + `goodwork-workspace/v2/`.

Finish by printing: blockers/majors/minors fixed, and Open questions verbatim.
