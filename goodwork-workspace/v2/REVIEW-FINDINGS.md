# Review Findings

## Fixed

- blocker: Moved profile evidence inbox out of `metrics.json` into `evidence-inbox.json` and updated state, spec, schemas, profile, review, scout, pipeline, and roadmap references.
- blocker: Removed approval-before-Gmail-draft semantics; Gmail draft creation now needs no approval record, logs pipeline draft metadata, and direct sends still require approval.
- major: Added draft metadata to `pipeline.json` schema and examples so reconcile can match Gmail drafts without inventing approval records.
- major: Added reply compaction via `reply_digest` and weekly/closure compaction guidance so `pipeline.json` does not grow unboundedly.
- major: Added `granularity` and exact `covers` lists to `events.jsonl` schema and SPEC so batch approval validation has the required pre-approval data.
- major: Added stable MagicDNS bootstrap token rotation flow and CSRF constraints for bookmark-to-fresh-session behavior.
- major: Clarified `await` timeout, partial-match reporting, malformed-event cursor behavior, and offline-click draining.
- major: Added SPEC gate walkthroughs for single application approval, session-batch approval, and hash-mismatch rejection.
- major: Rewrote `SKILL.md` description into five branch triggers per `writing-great-skills`.
- major: Removed duplicated pipeline stage/field authority from `pipeline.md` and pointed schema authority back to `state.md`.
- minor: Updated ROADMAP definitions and eval gates for `evidence-inbox.json` and Gmail-drafts-as-review-surface semantics.
- minor: Corrected SCHEMAS examples so Gmail drafts are not shown as approved sends and narrative/legacy files are accounted for.
- minor: Cleaned command wording in `apply`, `outreach`, `reconcile`, and `SKILL.md` to point to `execution.md` instead of restating gate behavior.

## Open questions

None.
