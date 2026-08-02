# Playbook: Backlog Policy

> Project playbook for this repo. Read by `backlog groom` (to triage and dispatch shaping), `backlog build` (to select and dispatch ready work), and build sessions (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: _<software | skill-authoring | writing | research | ops | general>_.
- Chosen at `backlog setup`, this is the kind of work this repo's backlog tracks; setup resolves which template pack fills each playbook.
- Absent this section (an install from before domain packs existed), the domain is `software`.
- When the chosen domain's pack was not yet shipped at install time, or a shipped pack omitted a required step, those step playbooks are `software` baselines standing in, each flagged in its own header as a code-flavored stand-in to tailor.

## Label roles

Two independent axes, plus exclusions. Readiness decides _whether and who_ picks an issue up; work-type decides _how_ the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type and complete dispatch metadata (§ Dispatch metadata). Default label `ready-for-agent` — _<your label>_.
- `building` — dispatched: a build subagent owns it, so `backlog build` never selects it again. Set by `backlog build` at dispatch, replacing `ready-for-agent`; records what's flying (branch name and dispatch date — local: frontmatter; GitHub: a comment alongside the label). Cleared on abort, superseded by closure when the change merges, or reset by `groom`'s human-confirmed orphan sweep (§ Building hygiene). Default `building` — _<your label>_.
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Before handing back, classify the blocker: one a repo change could clear — a broken seed script, a missing fixture, a gate ordering — is work (fix it in scope, or file it as its own ticket), and the handback comment names why only a human can act on what remains. Default `ready-for-human` — _<your label>_.
- `needs-info` — parked, waiting on the reporter. Default `needs-info` — _<your label>_.
- `needs-shaping` — parked for strategic shaping: the issue carries product/design/scope decisions that are neither settled nor delegated, or execution invalidated an approved decision. Set by `groom`'s route judgment, by an issue thread's handback, or by a build session that hit the invalidation — a blessed spec contradicted by the code it meets comes back here with the contradiction commented, the named re-entry into shaping; cleared when shaping delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the product owner owes shaping. Never selectable by `backlog build`. Default `needs-shaping` — _<your label>_.
- `shaping` — a shaping thread is attending it. Set by `backlog groom` at dispatch, replacing `needs-shaping`, so a subject never gets two threads. A batch advances atomically: after readiness is blessed, every member moves to `ready-for-agent` only after its clean shaping worktree is removed or its shaping change is merged, verified, and cleaned up; abandonment returns the whole batch to `needs-shaping`. Default `shaping` — _<your label>_.
- _(no readiness label)_ — not yet groomed; a target for `backlog groom`, not for `backlog build`.

**Closure** — the change request's closing reference (`Closes #N`) closes the ticket on merge; there is no post-build label by default. A repo whose merges land on a staging branch first may bind an extra label (e.g. `built`) meaning _merged, closure deferred to the promotion merge_: _<label, or "none — direct closure">_.

Two further lifecycle values appear only where the tracker has no native equivalent (the local binding's `state:` field), written on the build side's work branches, never by grooming: `in-review` (a PR is open for it — set on the work branch at PR-open) and `closed` (set on the work branch once review converges; the merge carries it to main). On trackers with native state (GitHub), an open PR and native closure express these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Default `bug` — _<your label>_.
- `enhancement` — implement branch: strategic decisions arrive settled or delegated (groom's route judgment), and the issue thread makes only a just-in-time tactical plan within that authority. Default `enhancement` — _<your label>_.
- `refactor` — refactor branch. Default `refactor` — _<your label>_.
- `research` — source-audit branch, for **epistemic-terminal** work: the deliverable establishes what primary sources support, what follows by inference, what conflicts, and what remains unknown. Correctness comes from traceability and the research skill's claim audit, not taste or implementation behavior. Default `research` — _<your label>_.
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a narrative synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — no mechanical `verify` pass/fail. Default `draft` — _<your label>_.
- `capstone` — coverage-check branch, set by the `to-slices` skill when it parents a split spec'd ticket over its slices: the ticket holds the spec its children deliver in installments, and stays the shared context they inherit from. Undispatchable while any child is open (§ Dependencies — open children block the parent); when the last child closes it surfaces to `backlog build`, and the dispatched session verifies the delivered children against the spec — filing each gap as a new child, which re-blocks the parent, or closing it on a clean pass. Its spec text is never rewritten. Default `capstone` — _<your label>_.

> Recognizing the boundary: if the terminal question is “what do the sources establish?”, groom to `research`. If the sources are inputs to prose judged by voice, persuasion, or fit, groom to `draft`. If behavior must change, retain the applicable bug/enhancement/refactor type and invoke research as a substage.

## Dispatch metadata

Groom records the facts `backlog build` passes to dispatch **before** it spawns a subagent:

- **Surface** — `backend`, `ui`, `mixed`, or `non-code`; include any required capability.
- **Coordination class** — `routine` when the issue is settled enough for a normal issue coordinator; `orchestrator-required` when it still needs product judgment, design, hard diagnosis, or another named uncertainty. This is not a difficulty score.
- **Coordination reason** — one sentence naming why the class applies and any known uncertainty. Required for both classes so the decision is auditable.
- **Route (enhancements)** — `route: direct` plus one line on why the strategic decisions are settled or delegated. A `ready-for-agent` enhancement without it is a grooming gap.

Tracker encoding: _<GitHub: a stable `Dispatch:` block in the body or grooming comment; local: `surface`, `coordination`, and `coordination-reason` frontmatter; custom: name the fields here>_. Missing metadata is a grooming gap: `backlog build` skips the ticket rather than inferring it or defaulting to the orchestrator.

**Exclusion** — terminal; removed from grooming and from the run queue:

- `wontfix`, `duplicate`, `superseded`, `invalid` — _<your labels>_.

**Neutral** — every other label; ignored for selection and routing. On an inherited tracker this is _most_ labels (priority, area/component, size, team, release). The default is **neutral**: a label maps to a role only when `setup` explicitly bound it: _<list the role→label mappings here; leave everything else neutral>_.

**Aliases** — when several existing labels fill one role, one is canonical and every reader treats the others as that role too: _<e.g. `type:bug` and `defect` both → `bug`; or "none">_. Setup reuses existing labels rather than minting duplicates.

## Dependencies

- How this repo records that one issue is blocked by another, so `backlog build` can skip blocked work: _<prefer the tracker's exercised native relation (GitHub `blocked_by`, Jira `is blocked by`, Linear `blocked-by`) via `platform.md`; local uses `deps:` frontmatter; a tracker without an exercisable native relation names its explicit fallback here>_.
- `backlog build` treats an issue with any unresolved (open/incomplete) blocker as blocked and skips it. Duplicate/supersede links: _<the convention — a `duplicate of #N` / `superseded by #N` body line plus the exclusion label, or the tracker's native link>_.
- **Open children block the parent.** How this repo records that one issue is a child of another: _<prefer the tracker's native parent/child relation (GitHub sub-issues) via `platform.md`; local uses `parent:` frontmatter; a tracker without one names its explicit fallback here>_. An issue with any open child is never dispatchable, whatever its labels — `backlog build` skips it exactly as it skips a blocked issue. No per-child blocking edges are wired: the relation itself carries the block, so a child attached mid-flight (a capture, a gap the capstone check files) re-blocks the parent by existing.

## Readiness decision

- The agent proposes work-type, dispatch metadata, and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. `ready-for-human`, `needs-info`, `needs-shaping`, and exclusion roles need no per-issue confirmation — they ride the groom plan's blanket approval, since every tracker mutation waits for that gate.
- In a shaping thread, the readiness blessing authorizes only the exact shaping change-request head the thread presented **before** requesting that signal, with the narrow effect explained. It does not authorize a later head, build changes, or unrelated shaping work.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## Build concurrency

> Read by `backlog build` before dispatch — the owner's burn bound on unattended fan-out. Policy data, set here by choice, never derived from the environment audit.

- **Max concurrent builds** — how many builds this dispatcher may have in flight at once: _<a positive integer, or `uncapped`>_. The unit is the **build** — one ticket's whole pipeline in its one worktree — never the subagents a build fans out; each build staffs its own workers freely. The environment playbook's parallelism verdict records what the repo _can_ sustain; this knob records what the owner _wants_ in flight — the worst-case spend of an unattended run, and how many builds die together when a shared session window caps out. The effective width is the tighter of the two.
- **Queue semantics** — the cap gates the entire mark-prepare-dispatch sequence: a ready ticket beyond the cap waits unclaimed — no `building` label, no claim comment, no worktree — and enters the sequence when a completed or aborted build frees its slot, so `building` keeps meaning actually in flight. Distinct from a harness-refused spawn, whose claim stands: a cap-queued ticket was never claimed.
- A **per-run override** may narrow a single run below the recorded value — a width, or fully sequential — never widen it; raising the bound is a playbook edit, not a run flag.

## Quota awareness

> Read by `backlog build` at every claim — the owner's headroom guard on the shared subscription pool, so an unattended run cannot drain the window the week's interactive work lives on. Policy data, set here by choice; where the usage numbers come from is a platform binding (`platform.md` § Harness — usage surface), never this file's to record.

- **Usage threshold** — the used percentage at or past which this dispatcher stops claiming: _<a percent, or `none`>_. It applies to **every window the bound usage surface reports** (session, weekly, per-model weekly, …): one tripped window gates claiming, whichever it is.
- **Gate semantics** — the gate reads the bound usage surface at each entry into the mark-prepare-dispatch sequence: the initial sweep and every completion-wake queue advance. At or past the threshold, no new claims — a ready ticket waits unclaimed, exactly the § Build concurrency queue semantics: no `building` label, no claim comment, no worktree — while in-flight builds run to completion, and the run relay names the tripped window and its reading. The gate is **claim-side only**: the staffing rule "cost never keeps work off the right model" stands — quota pressure never downgrades the model for work already claimed, nor for a queued ticket when its claim eventually comes.
- **Unknown is unknown** — a window no bound surface reports is unknown, **never estimated** — not from token counts, not from cost tallies, not from history. When the platform binding records no usage surface for the dispatching harness, or the recorded read fails, the gate is inoperative: dispatch proceeds under § Build concurrency alone, and the run relay says so once — the disclosed degradation, never an invented number and never a silent skip. An owner who wants a bound while flying blind narrows the width cap or uses the per-run override.
- **Outcome accounting** — each build's outcome relays the readings observed at its claim and at its completion, per reported window (e.g. weekly 31% → 54%). Attribution is honest: that delta is pool movement during the build's flight — shared with concurrent lanes and any interactive use — never presented as the build's exclusive consumption.

## Building hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `building` is the claim marker, applied optimistically — the build dispatcher accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock.
- **Claims are attributed.** The claim comment is posted by the runner's own tracker actor and names the branch, so any later reader can tell whose claim it is. A resuming dispatcher owns exactly the claims that match its actor and branches; a claim by another actor is another runner's live build — its claim and labels are not yours to touch; a comment (a lane-takeover note, a question) may still land on the ticket.
- **Orphan sweep** — a `building` ticket whose recorded branch no longer exists, or has gone quiet past the **quiet horizon** (_<e.g. 7 days>_), is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
