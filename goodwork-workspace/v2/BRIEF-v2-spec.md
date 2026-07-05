# Task: Draft Goodwork Career Ops v2 — spec, skill files, schemas, server contract

You are turning the goodwork skill (`skills/goodwork/`) from an advisor into an operator: a stateful, local, one-folder-one-person career ops system. Read first: `skills/goodwork/SKILL.md` + all of `skills/goodwork/reference/`, and `.claude/skills/writing-great-skills/SKILL.md` + its `GLOSSARY.md` — the skill-authoring discipline below is mandatory.

## Locked design decisions (do not relitigate)

**Shape.** Runs on the user's machine, one project folder = one person. The folder holds workspace state, vendored UI libs, a persistent Chrome profile, and a gitignored `.env`. Never installed globally. Degrades gracefully to draft-and-instruct when nothing is connected.

**State model.** Two tiers. JSON for operational state: `pipeline.json`, `leads.json`, `sources.json`, `targets.json`, `capabilities.json`, `metrics.json`, plus append-only `approvals.jsonl` and `events.jsonl`. Markdown for narrative state: `PROFILE.md`, `ODYSSEYS.md`, `EXPERIMENTS.md`, journal. Rule: if a matcher or the presentation layer consumes it → JSON; if a person or the interview consumes it → markdown. Every JSON record carries a stable ID; approvals, replies, kanban cards, and events all reference those IDs. The agent is the SOLE writer of state files; the server never writes state, only appends events.

**Commands.** Existing 13 stay. Three new:
- `setup` (once): connect Gmail/Calendar connectors; persistent Chrome profile logged into LinkedIn, job boards, WhatsApp Web (read-only, with explicit account-ban-risk disclosure); vendor `@pierre/diffs`; install/verify Tailscale as the default remote layer (user may decline → desk-only); user chooses reconcile cadence (manual / on-demand / scheduled); write `capabilities.json`; end with a live phone test of the full loop (serve → tailnet → tap test button → event → agent sees it).
- `scout`: maintains `sources.json` (boards, newsletters, community job channels, saved searches for the niche) and sweeps them for postings matching the Top 10 + profile; scored leads flow into the bench. Separate from `targets` (targets = employer list; scout = posting sources + sweep).
- `reconcile`: inbound sweep — Gmail, WhatsApp Web (read-only), LinkedIn messages → match replies to pipeline IDs, advance stages, detect interview requests (propose calendar slots via connector), draft replies for approval. `daily` runs reconcile FIRST (inbound changes today's queue). Cadence is whatever setup recorded.

**Execution ladder** (recorded in `capabilities.json`, consulted by `apply`/`outreach`, best available rung wins): (1) MCP connector (email as Gmail DRAFTS the user sends — a physically enforced gate); (2) ATS-direct via Greenhouse/Lever/Ashby public application endpoints; (3) authenticated Chrome (persistent profile; Playwright or Claude-in-Chrome; `.env` creds only where a profile can't hold a session); (4) manual fallback (draft + instructions).

**Gates (hard preconditions on execution, not advice).** Every outbound artifact requires an `approvals.jsonl` record: item ID, content hash, timestamp, channel, granularity. Per-item approval AND session-batch both supported (batch lists exactly what it covers). A UI click is a REQUEST — the agent validates the content hash before recording approval; hash mismatch (content edited after render) → re-present, never send. Evidence gate (~70% of must-haves evidenced in profile) and the weekly application quota are hard preconditions. Browser/ATS submissions screenshot the confirmation page as proof. Never invent experience/metrics/credentials, ever.

**UI layer.** Local server, Python stdlib only (~100 lines, no deps): serves HTML projections regenerated from JSON (never a store), one POST endpoint appending clicks to `events.jsonl`, binds 127.0.0.1 on a random port, per-session token required on every request (any webpage can POST to localhost — unauthenticated approve endpoints are forbidden). Tailscale `serve` proxies it onto the tailnet (stable MagicDNS URL, bookmarkable; NEVER `tailscale funnel`). Lifecycle: stays up while pending approvals exist, idle-timeout after the queue drains; the event log backstops crashes. The `await` bridge: a blocking CLI (`await --ids ... --timeout N`) tails `events.jsonl` and exits when matching events arrive, so a button click becomes a synchronous result for the agent; events clicked while no agent listens are drained by the next command via a cursor file.

Three pages, mobile-first in this priority order: (1) approval flow — one item per screen, big buttons, approve / reject-with-reason / edit-then-approve, batch checkboxes; (2) CV/application review — `@pierre/diffs` (vendored at setup) side-by-side with word-level highlights, each changed line annotated with the profile evidence backing it; (3) kanban from pipeline.json — stage columns, staleness colors, next-action badges; collapses to a list on mobile, drag-and-drop desktop-only (drag = stage-change event, agent applies it and asks follow-ups).

**Profile learning loop.** Every layer emits profile evidence. UI clicks are revealed preference: lead approve/dismiss patterns drift Motivation scoring and can confront the profile ("you keep dismissing what your profile says you want"); CV reject-reasons calibrate tailoring and self-presentation; reason codes arrive as structured events. Profile-relevant events are tagged into an evidence inbox; `review`/`profile` drain it into dated profile updates using the existing changelog + confidence-mark discipline. PROFILE.md stays markdown.

**Notifications.** Local push notification when work is ready for review ("3 items pending" — no link needed, the URL is stable). The notify → phone → click → event → agent-proceeds loop is the primary mobile flow.

## Skill-authoring discipline (from writing-great-skills — mandatory)

Router stays thin; each command's material lives in its own reference file; one meaning, one home (the execution ladder, gate rules, and state model each get exactly one authoritative location, other files point to it); no restating what SKILL.md already says; completion criteria checkable and exhaustive; hunt leading words; keep every reference file lean.

## Deliverables

**A. Skill files (edit in place under `skills/goodwork/`):**
- `SKILL.md`: new commands in the table (setup under a new "Connect" or into Sustain — your call, justify), routing updates, any Core Rules additions the operator role forces (agent-sole-writer, gate-before-send as hard rule). Keep it ≤ ~85 lines.
- New: `reference/setup.md`, `reference/scout.md`, `reference/reconcile.md`.
- New: `reference/state.md` — the single home for the state model: file inventory, JSON schemas (inline, concise), ID conventions, agent-sole-writer rule, evidence inbox.
- New: `reference/execution.md` — the single home for the ladder + gates + approval records.
- Updated: `framework.md` (workspace section → v2 state model, pointing at state.md), `apply.md`/`outreach.md` (grow execution sections that POINT at execution.md rather than restate it), `pipeline.md` (pipeline.json), `targets.md` (targets.json), `daily.md` (reconcile first), `profile.md` (evidence inbox), `review.md` (drains evidence inbox), `README.md`.

**B. Design docs (new, under `goodwork-workspace/v2/`):**
- `SPEC.md` — full v2 spec: architecture, server contract (endpoints, token scheme, event schema, await semantics, lifecycle), UI page specs, Tailscale integration, security rules, threat notes (localhost CSRF, funnel ban, .env hygiene, WhatsApp ToS).
- `SCHEMAS.md` — every JSON file's schema with a realistic example record each.
- `ROADMAP.md` — the six build slices (setup+capabilities+JSON migration → reconcile/Gmail → UI server+pages → ATS-direct apply → browser fallback → WhatsApp read-only), each with its definition-of-done AND the eval gates it adds to `goodwork-workspace/eval/` (e.g. "no submission without approval record", "quota never exceeded", fake local ATS form for browser-path tests).

No implementation code beyond schema examples. Do not touch `goodwork-workspace/eval/` itself.

Finish by printing: files written, the 5 riskiest design calls you made where the brief left room, and anything in the brief you found contradictory.
