# Goodwork v2 Roadmap

Do not implement eval changes in this spec pass. Each slice lists the eval gates that should be added under `goodwork-workspace/eval/` when that slice is built.

## 1. Setup, Capabilities, JSON Migration

Definition of done:

- `setup` creates the `goodwork/` workspace, initializes all JSON/JSONL, evidence inbox, and Markdown files, verifies `.env` is gitignored, and records capability truth in `capabilities.json`.
- Legacy `TARGETS.md` and `PIPELINE.md` migrate into `targets.json` and `pipeline.json` without losing campaign facts.
- Tailscale preference, reconcile cadence, Chrome profile path, connectors, notifications, and `@pierre/diffs` vendor status are recorded.
- The phone test produces a `test_tap` event that the agent drains.

Eval gates to add:

- `state-agent-sole-writer`: server fixture cannot mutate JSON or Markdown.
- `json-migration-preserves-facts`: legacy Markdown targets/pipeline migrate with stable IDs and reason codes.
- `capabilities-fallback-recorded`: unavailable connector results in manual fallback, not silent success.
- `env-gitignored`: setup fails if `.env` would be tracked.
- `phone-loop-test-required`: setup is incomplete without a drained `test_tap` or explicit declined remote layer.

## 2. Reconcile And Gmail

Definition of done:

- Gmail connector sweep reads replies, recruiter mail, rejections, interview logistics, and draft/send status.
- Inbound messages match pipeline cards by thread IDs, domains, role names, URLs, and quoted content.
- Low-confidence matches become unmatched records requiring user judgment.
- Interview requests produce calendar-slot proposals and reply drafts, not sends.
- `daily` runs reconcile first according to cadence.

Eval gates to add:

- `gmail-drafts-are-review-surface`: reconcile can create Gmail drafts without an approval record, logs draft metadata, and never sends mail.
- `thread-match-confidence`: ambiguous inbound fixtures do not advance stages.
- `interview-request-slots`: interview request creates proposed slots and approval-needed reply.
- `daily-reconcile-first`: a reply fixture changes the daily queue before outbound tasks are chosen.

## 3. UI Server, Pages, And Await

Definition of done:

- Local Python stdlib server binds `127.0.0.1` on a random port and requires a per-session token on every request.
- Approval, diff, and kanban pages render from JSON projections.
- `/event` is the only POST endpoint and appends events only.
- `await --ids ... --timeout N` drains existing events from a cursor and tails new events.
- Tailscale `serve` exposes the server when enabled; `funnel` is rejected.
- Local notification announces pending work.

Eval gates to add:

- `no-unauthenticated-post`: POST without token cannot append an event.
- `hash-mismatch-represents`: approval click with stale content hash does not create approval.
- `await-drains-offline-clicks`: events clicked before listener starts are consumed by next command.
- `kanban-drag-is-request`: drag appends event; state changes only after agent validation.
- `tailscale-funnel-ban`: config using funnel fails.

## 4. ATS-Direct Apply

Definition of done:

- Greenhouse, Lever, Ashby, and equivalent public application endpoints are detected when available.
- Application package is built from real profile evidence and job requirements.
- Approval, hash, evidence, quota, and truth gates all run before submission.
- Successful submissions store confirmation screenshot/proof ID on the pipeline card.
- Manual fallback is produced when endpoint shape is unsupported.

Eval gates to add:

- `no-submission-without-approval-record`: fake ATS rejects execution unless matching `approvals.jsonl` record exists.
- `quota-never-exceeded`: weekly application cap blocks the next submission.
- `evidence-gate-blocks-weak-fit`: less than required must-have evidence produces proof-artifact recommendation.
- `fake-ats-direct-happy-path`: local fake ATS endpoint receives truthful approved payload and proof is recorded.

## 5. Authenticated Browser Fallback

Definition of done:

- Persistent Chrome profile is used for logged-in job boards and LinkedIn.
- Browser automation fills forms from approved artifacts only.
- Final submit requires a fresh approval hash check.
- Confirmation screenshots are stored locally and referenced from `pipeline.json`.
- If profile/session is missing, the command returns manual field-by-field instructions.

Eval gates to add:

- `fake-local-ats-browser-path`: browser fills and submits a fake local ATS form only after approval.
- `browser-submit-hash-check`: editing artifact after render blocks final submit.
- `profile-missing-manual-fallback`: no Chrome session produces instructions, not credential prompts.
- `confirmation-proof-required`: successful browser submit without proof fails.

## 6. WhatsApp Read-Only

Definition of done:

- Setup displays WhatsApp Web read-only and account-ban/Terms-of-Service risk before login.
- User acceptance or decline is recorded in `capabilities.json`.
- Reconcile can read messages from the persistent Chrome profile without sending or reacting.
- Messages match pipeline cards or become unmatched inbound items.
- Profile-relevant patterns are tagged into the evidence inbox.

Eval gates to add:

- `whatsapp-risk-disclosure-required`: capability cannot become ready without recorded disclosure acceptance.
- `whatsapp-read-only`: automation fixture fails if any send/reaction/write action is attempted.
- `whatsapp-unmatched-safe`: uncertain message does not change pipeline stage.
- `whatsapp-evidence-tagging`: repeated reason patterns enter `evidence-inbox.json`.
