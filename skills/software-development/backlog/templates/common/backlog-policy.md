# Playbook: Backlog Policy

> Project playbook for this repo. Read by `backlog groom` (to triage and dispatch shaping), `backlog build` (to select and dispatch ready work), and build sessions (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: _<software | skill-authoring | writing | research | ops | general>_.
- Chosen at `backlog setup`, this is the kind of work this repo's backlog tracks; setup resolves which template pack fills each playbook.
- Absent this section (an install from before domain packs existed), the domain is `software`.
- When the chosen domain's pack was not yet shipped at install time, or a shipped pack omitted a required step, those step playbooks are `software` baselines standing in, each flagged in its own header as a code-flavored stand-in to tailor.

## Label roles

Two independent axes, plus exclusions. Readiness decides *whether and who* picks an issue up; work-type decides *how* the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type and complete dispatch metadata (§ Dispatch metadata). Default label `ready-for-agent` — _<your label>_.
- `building` — dispatched: a build subagent owns it, so `backlog build` never selects it again. Set by `backlog build` at dispatch, replacing `ready-for-agent`; records what's flying (branch name and dispatch date — local: frontmatter; GitHub: a comment alongside the label). Cleared on abort, superseded by closure when the change merges, or reset by `groom`'s human-confirmed orphan sweep (§ Building hygiene). Default `building` — _<your label>_.
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Before handing back, classify the blocker: one a repo change could clear — a broken seed script, a missing fixture, a gate ordering — is work (fix it in scope, or file it as its own ticket), and the handback comment names why only a human can act on what remains. Default `ready-for-human` — _<your label>_.
- `needs-info` — parked, waiting on the reporter. Default `needs-info` — _<your label>_.
- `needs-shaping` — parked for strategic shaping: the issue carries product/design/scope decisions that are neither settled nor delegated, or execution invalidated an approved decision. Set by `groom`'s route judgment, by an issue thread's handback, or by a build session that hit the invalidation — a blessed spec contradicted by the code it meets comes back here with the contradiction commented, the named re-entry into shaping; cleared when shaping delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the product owner owes shaping. Never selectable by `backlog build`. Default `needs-shaping` — _<your label>_.
- `shaping` — a shaping thread is attending it. Set by `backlog groom` at dispatch, replacing `needs-shaping`, so a subject never gets two threads; the human in the thread moves it on — forward to `ready-for-agent` when readiness is blessed, back to `needs-shaping` if the thread is abandoned. Default `shaping` — _<your label>_.
- *(no readiness label)* — not yet groomed; a target for `backlog groom`, not for `backlog build`.

**Closure** — the change request's closing reference (`Closes #N`) closes the ticket on merge; there is no post-build label by default. A repo whose merges land on a staging branch first may bind an extra label (e.g. `built`) meaning *merged, closure deferred to the promotion merge*: _<label, or "none — direct closure">_.

Two further lifecycle values appear only where the tracker has no native equivalent (the local binding's `state:` field), written on the build side's work branches, never by grooming: `in-review` (a PR is open for it — set on the work branch at PR-open) and `closed` (set on the work branch once review converges; the merge carries it to main). On trackers with native state (GitHub), an open PR and native closure express these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Default `bug` — _<your label>_.
- `enhancement` — implement branch: strategic decisions arrive settled or delegated (groom's route judgment), and the issue thread makes only a just-in-time tactical plan within that authority. Default `enhancement` — _<your label>_.
- `refactor` — refactor branch. Default `refactor` — _<your label>_.
- `research` — source-audit branch, for **epistemic-terminal** work: the deliverable establishes what primary sources support, what follows by inference, what conflicts, and what remains unknown. Correctness comes from traceability and the research skill's claim audit, not taste or implementation behavior. Default `research` — _<your label>_.
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a narrative synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — no mechanical `verify` pass/fail. Default `draft` — _<your label>_.

> Recognizing the boundary: if the terminal question is “what do the sources establish?”, groom to `research`.
> If the sources are inputs to prose judged by voice, persuasion, or fit, groom to `draft`. If behavior must
> change, retain the applicable bug/enhancement/refactor type and invoke research as a substage.

## Dispatch metadata

Groom records the facts `backlog build` passes to dispatch **before** it spawns a subagent:

- **Surface** — `backend`, `ui`, `mixed`, or `non-code`; include any required capability.
- **Coordination class** — `routine` when the issue is settled enough for a normal issue coordinator;
  `orchestrator-required` when it still needs product judgment, design, hard diagnosis, or another named
  uncertainty. This is not a difficulty score.
- **Coordination reason** — one sentence naming why the class applies and any known uncertainty. Required for
  both classes so the decision is auditable.
- **Route (enhancements)** — `route: direct` plus one line on why the strategic decisions are settled or
  delegated. A `ready-for-agent` enhancement without it is a grooming gap.

Tracker encoding: _<GitHub: a stable `Dispatch:` block in the body or grooming comment; local: `surface`,
`coordination`, and `coordination-reason` frontmatter; custom: name the fields here>_. Missing metadata is a
grooming gap: `backlog build` skips the ticket rather than inferring it or defaulting to the orchestrator.

**Exclusion** — terminal; removed from grooming and from the run queue:

- `wontfix`, `duplicate`, `superseded`, `invalid` — _<your labels>_.

**Neutral** — every other label; ignored for selection and routing. On an inherited tracker this is *most* labels (priority, area/component, size, team, release). The default is **neutral**: a label maps to a role only when `setup` explicitly bound it: _<list the role→label mappings here; leave everything else neutral>_.

**Aliases** — when several existing labels fill one role, one is canonical and every reader treats the others as that role too: _<e.g. `type:bug` and `defect` both → `bug`; or "none">_. Setup reuses existing labels rather than minting duplicates.

## Dependencies

- How this repo records that one issue is blocked by another, so `backlog build` can skip blocked work: _<prefer the tracker's exercised native relation (GitHub `blocked_by`, Jira `is blocked by`, Linear `blocked-by`) via `platform.md`; local uses `deps:` frontmatter; a tracker without an exercisable native relation names its explicit fallback here>_.
- `backlog build` treats an issue with any unresolved (open/incomplete) blocker as blocked and skips it. Duplicate/supersede links: _<the convention — a `duplicate of #N` / `superseded by #N` body line plus the exclusion label, or the tracker's native link>_.

## Readiness decision

- The agent proposes work-type, dispatch metadata, and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. The agent may apply `ready-for-human`, `needs-info`, `needs-shaping`, and exclusion roles on its own.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## Building hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `building` is the claim marker, applied optimistically — the build dispatcher accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock.
- **Claims are attributed.** The claim comment is posted by the runner's own tracker actor and names the branch, so any later reader can tell whose claim it is. A resuming dispatcher owns exactly the claims that match its actor and branches; a claim by another actor is another runner's live build — leave it and its ticket alone.
- **Orphan sweep** — a `building` ticket whose recorded branch no longer exists, or has gone quiet past _<horizon, e.g. 7 days>_, is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
