---
name: retro
description: Turn the friction of working with skills into fixes — an always-on local ledger any session appends to the moment a skill run stumbles, and a periodic retro pass that clusters entries with their run transcripts and triages them into local fixes, upstream candidates, and noise. With the repo's recorded consent, a recurring skill defect becomes a sanitized, human-approved feedback issue on the skill's source repo. Use retro note to record friction as it happens, retro to run the pass, retro setup to bind consent and targets. Not for capturing ordinary work items — that's to-backlog.
argument-hint: "[note <observation> | setup]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [to-backlog]
  setup: reference/setup.md
---

# Retro

Retro owns one loop: **turn the friction of working with skills into fixes.** Every skill run — a
groom, a build, a shaping thread — throws off friction nobody writes down: an instruction the agent
misread twice, a confirmation the user had to repeat, a stale playbook row, a step that only worked
after a workaround. Retro keeps the **friction ledger** — an always-on local record any session
appends to the moment friction happens — and periodically runs a **retro pass**: cluster the open
entries with the transcripts behind them, triage each cluster, and turn the result into work.
Capture is cheap and constant; analysis is lazy and batched.

Triage is exhaustive — every cluster lands in exactly one bucket:

- **Local fix** — the problem is this repo's binding: a stale playbook, a misbound role, a missing
  configuration. Fixed here; the skill itself is innocent.
- **Upstream candidate** — the problem is the skill itself: wording executors systematically misread,
  a missing degradation path, a gap in the method that recurs wherever the skill runs. Candidate for
  a feedback issue on the skill's source repo — behind the consent and the gate below.
- **Noise** — happened once, was environmental, or isn't actionable. Dropped, with the reason
  recorded.

**Recurrence is the bar for upstream.** A cluster becomes an upstream candidate only on two or more
independent occurrences — across runs, not restatements within one. One bad run is weather; the same
stumble in three runs is the skill.

**Retro never nags.** It runs when invoked. Its only proactive surface is the note verb's threshold
report (below), and a pass opens with what it found — never with a bare request for feedback.

## Command surface

- **`retro note <observation>`** — append one entry to the friction ledger. Cheap enough to run
  mid-anything; this is also how sibling skills and dispatchers record friction, by invoking the
  verb by name at the moment the stumble happens or as a run ends.
- **`retro`** — run a retro pass over the open ledger entries and the transcripts of the runs behind
  them.
- **`retro setup`** — load [setup](reference/setup.md): record the consent decision, bind the
  upstream target and transcript locations, seed the denylist, install the playbook.

## The friction ledger

The ledger lives in the **skill instance** `retro/` at the project root, created on first use:
`ledger.md` (the entries) and `denylist.txt` (the scrub terms, seeded at setup, user-editable). The
ledger is **local and private — entries carry full local specifics**, because a local fix needs
them; sanitization is a property of the upstream gate, never of capture.

`ledger.md` holds two sections. Every entry starts under `## Open`:

```
- 2026-07-30 · build · reviewer misread the change-request base; user corrected twice · run: ticket-41
```

— date, the skill (or `user`, for friction the user reports directly), one concrete observation, and
a run tag locating the transcript. A retro pass moves what it triaged under `## Triaged` with a
disposition appended (`→ local-fix: <where>`, `→ upstream: <issue>`, `→ noise: <reason>`). The
Open/Triaged split is the pass watermark: a bare `retro` needs no recap of anything.

After appending, the note verb reports the ledger's state — `noted; N open entries` — and, when the
open count or a visible cluster crosses the playbook's pass-due threshold, says so: `a retro pass is
due`. That report is the entire escalation mechanism; whoever sees it decides.

## The retro pass

1. **Collect.** Read the playbook (`docs/agents/retro.md`), the open ledger entries, and — per the
   playbook's transcript binding — the transcripts of the runs those entries name, plus any runs
   since the last pass with no entry at all: the user's corrections, aborts, and repeated
   instructions in a transcript are friction nobody noted, and routinely the best signal.
2. **Cluster.** Group entries and transcript observations that are the same underlying stumble,
   however differently worded. A cluster's size across distinct runs is its recurrence count — and
   the count spans passes, not just this one: a match among `## Triaged` entries (a prior noise
   drop especially) counts toward the bar, or a stumble that recurs slowly would reset to one at
   every pass and never graduate.
3. **Triage.** Sort every cluster into local fix, upstream candidate (recurrence bar applies), or
   noise. Present the triage as one table — cluster, evidence, bucket, proposed action — before
   acting on any of it.
4. **Execute local fixes.** A small binding fix (a playbook row, a denylist term) is proposed as a
   concrete edit for the user's approval. Anything larger becomes tracked work: capture it via the
   `to-backlog` sibling; absent that sibling, present the items as a list the user can carry to
   their tracker themselves.
5. **Draft upstream candidates — only where the playbook's consent row says enabled.** Where it says
   disabled, report the count of upstream-shaped clusters once, plainly, and stop there — no draft,
   no repeated asking. Drafting and submission follow the upstream gate below.
6. **Update the ledger.** Move triaged entries with their dispositions. This is the pass's last act,
   and skipping it corrupts the next pass's watermark.

## The upstream gate

The privacy discipline for anything that leaves the repo. Every layer applies, in order:

- **Written from scratch, in skill vocabulary.** The draft is composed generatively — skill names,
  verbs, phases, role nouns, and the abstract shape of the stumble — never by redacting a transcript
  or ledger entry. You cannot leak what you never included. No repo or product names, no file paths,
  no code, no ticket ids or titles, no business terms. Reproduction steps reference the skill's own
  abstractions ("a capstone ticket with one open child"), never this repo's instances.
- **Scrubbed mechanically.** Run `scripts/scrub.py <draft> retro/denylist.txt` — it flags denylist
  terms, email addresses, absolute filesystem paths, and URLs outside the upstream repo. A finding
  means rewrite and re-run. A clean exit is necessary, never sufficient.
- **Approved verbatim, per issue.** Show the user the exact final text — title, body, label — and
  submit nothing without their explicit approval of that text. Consent recorded at setup means the
  pass may *draft and propose*; it never means submit. **There is no auto-submit, ever.**
- **Pseudonymity stated honestly.** The issue is filed from the user's own GitHub account — content
  is sanitized, authorship is not. Say so in the approval ask; it is part of what they are
  approving.

An approved draft is filed with `gh issue create` against the playbook's upstream target, carrying
its recorded label (`feedback`). If `gh` is missing or unauthenticated, state the gap and hand the
user the ready-to-file draft instead of improvising another channel.

## Dependency surface

- **Project playbook** — `docs/agents/retro.md`: the consent decision, upstream target, pass-due
  threshold, and transcript binding. Absent, only `retro note` works (the ledger needs no bindings);
  a pass or a submission states the gap and asks for `retro setup` first.
- **Sibling skills** — `to-backlog`, optional, for turning larger local fixes into tracked tickets;
  absent, the pass lists them for the user instead.
- **Bundled** — [setup](reference/setup.md), the playbook template ([templates/retro.md](templates/retro.md)),
  and the scrub script ([scripts/scrub.py](scripts/scrub.py)).
