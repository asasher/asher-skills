# Goodwork v3 pre-ship eval — verdicts (run 2026-07-19-v3)

Discipline: `docs/agents/probe-evals.md`. Assets under test: `skills/personal/goodwork/` on branch
`goodwork-polish`. Graded against the sealed key `skills/personal/goodwork/evals/key.md` (grader-only;
never in any executor context). Findings only — no fixes made in this session.

## Tier 2 — mechanical dry-run

`bash skills/personal/goodwork/evals/dryrun.sh` → **12 passed, 0 failed** (matches the 2026-07-19
authoring baseline). Full output preserved at the end of this file.

## Tier 1 — probe × executor verdicts

Executors: Claude = fresh general-purpose subagents with probe context pasted (no repo access);
Codex = `gpt-5.6-sol` via `codex exec --sandbox read-only`, prompts naming exactly the permitted files.
Raw transcripts: `claude-transcripts.md`, `codex-transcripts.md` (this directory).

| Probe | Context | Claude | Codex | Notes / evidence per fail |
|---|---|---|---|---|
| P1 | [S] | pass | pass | Both: menu + Common Workflows, summarize snapshot, suggest next step; cite Routing 1. |
| P2 | [S] | pass | pass | Both: campaign guard → short-form interview first; cite Routing 7. |
| P3 | [S+execution] | pass | pass | Both: artifact-file-first, chat reply = request through the gates, approval record with quoted source, hash gate, Gmail-draft exception with the physical-gate reason. |
| P4 | [S+apply] | pass | pass (ambiguity noted) | Both stop and propose the cheapest proof artifact/prototype, never adjectives. Codex correctly notes the ~70% threshold is not stated in apply.md (it lives in execution.md) — see finding A3. |
| P5 | [S+execution] | pass | pass (marginal, noted) | Claude matches the key exactly: refuse, offer the recorded quota change as the path, record before proceeding. Codex enforces the same mechanics (recorded change strictly before execution, gate named and cited) but treats the user's "one more" as itself the explicit quota-increase request rather than offering/confirming first — inside the key's substance, outside its spirit; noted as observation O2, not a fail. |
| P6 | [S+execution] | pass | pass | Both: write `edited_content` verbatim, recompute hash, approval over the new hash with `source_event_id`, no re-presentation, single-item; exception = a knowingly false claim. |
| P7 | [S+presentation] | pass | pass | Both: rung 1 inline render; read the renderer's own guidance (`read_me`) before first use; button-click = request to validate under execution.md, never an applied change. |
| P8 | [S+presentation] | pass | pass | Both: markdown ranked table (rung 3, floor), smallest sufficient surface; explicitly no server startup for a quick look. |
| P9 | [S] | pass | pass | Both drafts are plain-language, two sentences, "waiting for your OK", zero file names/IDs/hashes/gate mechanics. |
| P10 | [S+pipeline] | pass | pass | Both: nested reply record (thread/reply ID retained), plain-language history entry, new next action + due date, due action pushed to daily; both correctly exclude reason codes (advancement, not rejection/retirement). Both independently note `metrics.json` per-event writes are unspecified — see finding A4. |
| P11 | [S+reconcile] | pass | pass | Both: never send during the sweep; draft the thank-you (Gmail draft for user send) for after the sweep; cite "Do not send from any channel during the sweep." |
| P12 | [S+daily] | **fail** (ambiguity flagged) | pass (ambiguity noted) | **Claude fail evidence:** it did NOT run reconcile first — it read daily.md's trigger sentence strictly ("`manual` requested now" ≠ a `manual` cadence with `daily` invoked) and only *offered* a sweep, where the key requires reconcile to run first. Journal-gap handling was correct on both sides (ask once, shrink-or-declared-pause). Codex hit the same unclear sentence but recovered via SKILL.md's `daily` row ("Reconcile first, then today's action queue…") and ran reconcile. One executor recovering while the other diverges on the same sentence = a real wording defect, not executor noise. See finding A1/A2. |
| P13 | [S+reconcile] | pass | pass | Both: low-confidence match → unmatched reply record, ask the user; neither card's stage changes. |
| P14 | [S+execution] | pass | pass | Both: hash gate fails, message is only a request, no approval over either hash; re-present the current text for a fresh decision. |

**Score: Claude 13/14, Codex 14/14. Combined ship bar (all probes pass both executors): NOT met — P12
fails the Claude direction.** Per RUN.md, the wording gets fixed on the authoring branch and P12 re-runs
(record both rounds); this run is round 1.

## Ambiguity findings (verbatim from executors)

**A1 — daily.md reconcile trigger (Claude, P12) — the ship-blocking finding:**
> *Flag: there is genuine ambiguity here* — after 9 days away, daily.md's rationale ("Inbound replies change today's queue before new outbound work is chosen") pulls toward reconciling, but the trigger list as written excludes an unrequested `manual` cadence. The trigger sentence decides it: no auto-reconcile, offer instead.

**A2 — same sentence (Codex, P12), independently:**
> Minor ambiguity: "`manual` requested now" is grammatically unclear, but `SKILL.md` independently defines `daily` as "Reconcile first," so reconciliation is still the clear first action.

**A3 — evidence-gate threshold not visible from apply.md alone (Codex, P4):**
> One ambiguity: these permitted files do not define the evidence gate's numerical threshold, so they do not explicitly say that 4/8 constitutes failure. But they clearly prohibit "tailoring harder" as a substitute for missing evidence.

**A4 — metrics.json per-event write rule unspecified (Claude, P10):**
> Whether `metrics.json` is updated per-event is genuinely unspecified in the pasted content — it appears only as a diagnostic input, never with a write rule — so I would not claim it as a required write.

**A5 — reply-record fields need state.md (Codex, P10; probe-design artifact more than a skill defect):**
> Exact reply-record fields and the appropriate deadline are ambiguous without `state.md` and `reconcile.md`, which the probe forbids reading.

**A6 — rung undetermined without capabilities.json (Codex, P3; probe-design artifact):**
> The available rung is therefore genuinely undetermined here.

## Suggested issue routing (findings only — nothing changed this session)

1. **daily.md § First — rewrite the trigger sentence** so a `manual` cadence + a stale/returning session
   unambiguously runs reconcile first (or explicitly does not); align with SKILL.md's `daily` row. Re-run
   P12 both executors after the fix. (A1/A2 — ship blocker.)
2. **apply.md Evidence bullet** — consider naming the ~70% must-have threshold (or pointing at
   execution.md § Hard Gates) so the number is visible from the apply context alone. (A3 — minor.)
3. **pipeline.md** — state whether stage-change events write `metrics.json` per-event or whether metrics
   are derived at review time. (A4 — minor.)
4. **evals/probes.md** — A5/A6 are probe-context artifacts (the [S+R] restriction hides state.md /
   capabilities.json); consider noting in the probe preamble that executors may name a needed-but-excluded
   file as part of a valid answer. (Eval hygiene, not a skill defect.)

## Route deviations

- **Transient API error mid-run:** the runner session was cut off after the Claude executor subagents
  completed; their final reports were delivered to the coordinating session and relayed back verbatim,
  and that relay is the content of `claude-transcripts.md` (provenance noted in its header). Resend
  requests had been issued to the still-live subagents before the relay arrived; they were superseded and
  any duplicate output was not used. No probe was re-run from memory; no answers were reconstructed.
- **Codex direction unaffected:** all 14 `codex exec` invocations ran to completion with exit 0 (12
  before the interruption was noticed, 2 finishing during recovery — verified live processes, not stale
  files). No codex re-runs were needed. Route probe: `read … reply with its name field only` → "goodwork".
- **Claude executor batching:** probes were batched per context variant across 7 subagents
  ({P1,P2,P9} · {P3,P5,P6,P14} · {P4} · {P7,P8} · {P10} · {P11,P13} · {P12}); no subagent ever saw two
  context variants, no executor ever saw key.md, and none could browse the repo.
- **Codex prompts** named exact file paths instead of pasting content (per RUN.md's codex recipe), so the
  codex executor read the two permitted files itself under `--sandbox read-only`; transcripts confirm it
  read only the permitted files.

## Observations (not fails)

- **O1:** Both executors on P1/P2 also cited the once-per-session `framework.md` read before acting —
  correct per SKILL.md and not penalized.
- **O2 (codex P5):** treating an enthusiastic "one more" as itself the explicit quota-change request is a
  liberal reading; if the authors want an explicit confirm-then-record beat, a word like "user-confirmed"
  in the quota-gate sentence would pin it.

## Tier 2 raw output

```
== sandbox: /var/folders/m5/3dysrch16gg6ckzt3tbjn3jw0000gn/T/tmp.XrHR331C2J
  PASS  init: goodwork/ created
  PASS  init: artifacts/ dir created
  PASS  init: presentation.rungs defaults to markdown
  PASS  seed: pipeline card written
  PASS  server: started and printed port/token
2026-07-19T16:57:31+04:00 "GET /kanban?token=Md07PRQ_y3ROrDQsbLtC4iOxi7a3SfBb HTTP/1.1" 200 -
  PASS  server: kanban bootstrap carries history summary
2026-07-19T16:57:31+04:00 "GET /approval?token=Md07PRQ_y3ROrDQsbLtC4iOxi7a3SfBb HTTP/1.1" 200 -
  PASS  server: approval page carries the draft text
2026-07-19T16:57:31+04:00 "GET /kanban?token=wrong HTTP/1.1" 403 -
  PASS  server: bad token is refused
2026-07-19T16:57:31+04:00 "POST /event HTTP/1.1" 200 -
  PASS  event: edit_then_approve accepted
  PASS  event: landed in events.jsonl with edited_content
2026-07-19T16:57:31+04:00 "POST /event HTTP/1.1" 200 -
  PASS  validate: matching hash passes (exit 0)
  PASS  validate: stale hash rejected (exit 20)
== 12 passed, 0 failed
```

## Round 2 (2026-07-19, after authoring-branch wording fixes)

Fixes applied on goodwork-polish before re-run: daily.md § First rewritten (daily always starts with the
sweep unless one ran today or the user declines; cadence governs standalone scheduling only); apply.md
names the ~70% threshold inline (finding A3); pipeline.md states metrics.json is written weekly by review
(finding A4).

| Probe | Claude | Codex |
|---|---|---|
| P12 (re-run against fixed daily.md) | **pass** | **pass** |

Both executors now cite the new deciding sentence ("The recorded cadence governs *standalone* reconcile
scheduling only — it never exempts `daily` from sweeping first"), run the sweep by default, and cap the
journal-gap question at one ask. Residual nits, non-blocking: Claude flagged that "unless the user
declines it" doesn't say whether to offer before running (both executors resolved to run-by-default from
the imperative); Codex noted it couldn't read framework.md under the two-file probe restriction (probe
design artifact, same class as A5/A6). Grader: session orchestrator, against the sealed key, round-2
transcripts in claude-p12-r2.md / codex-p12-r2.md.

**Ship bar after round 2: met for Tiers 1–2** (Tier 2 12/12; Tier 1 both directions all-pass including
P12 re-run). Tier 3 human walkthrough remains open.
