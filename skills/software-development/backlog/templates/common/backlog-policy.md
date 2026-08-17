# Playbook: Backlog Policy

> Project playbook for this repo. Read by `backlog groom` (to route, merge, and dispatch shaping), `backlog build` (to select and claim ready work), `backlog status` (to rule on claims and deadlines), and build threads (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: _<software | skill-authoring | writing | research | ops | general>_.
- Chosen at `backlog setup`, this is the kind of work this repo's backlog tracks; setup resolves which template pack fills each playbook.
- Absent this section (an install from before domain packs existed), the domain is `software`.
- When the chosen domain's pack was not yet shipped at install time, or a shipped pack omitted a required step, those step playbooks are `software` baselines standing in, each flagged in its own header as a code-flavored stand-in to tailor.

## Label roles

Two independent axes, plus exclusions. Readiness decides _whether and who_ picks an issue up; work-type decides _how_ the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type and complete dispatch metadata (§ Dispatch metadata). Default label `ready-for-agent` — _<your label>_.
- `building` — claimed: a build thread owns it, so `backlog build` never selects it again. Set by `backlog build` at dispatch, replacing `ready-for-agent`; the claim comment is the dispatch declaration — ticket digest, branch, worktree path, model, effort, harness, thread name, dispatcher identity, and the deadline as an absolute timestamp. Superseded by closure when the change merges, by `delivered` when a slice lands on its feature branch, by a reclaim comment, or reset via `backlog status`'s human-confirmed orphan surfacing (§ Building hygiene). Default `building` — _<your label>_.
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Before handing back, classify the blocker: one a repo change could clear — a broken seed script, a missing fixture, a gate ordering — is work (fix it in scope, or file it as its own ticket), and the handback comment names why only a human can act on what remains. Default `ready-for-human` — _<your label>_.
- `needs-info` — parked, waiting on the reporter. Default `needs-info` — _<your label>_.
- `needs-shaping` — parked for strategic shaping: the issue carries product/design/scope decisions that are neither settled nor delegated, or execution invalidated an approved decision. Set by `groom`'s route judgment, by a build thread's handback, or by one that hit the invalidation — a blessed spec contradicted by the code it meets comes back here with the contradiction commented, the named re-entry into shaping; cleared when shaping delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the product owner owes shaping. Never selectable by `backlog build`. Default `needs-shaping` — _<your label>_.
- `shaping` — a shaping thread is attending it. Set by `backlog groom` at dispatch, replacing `needs-shaping`, so a subject never gets two threads. A subject becomes `ready-for-agent` when its spec is blessed (§ Readiness decision); abandonment returns it to `needs-shaping`. Default `shaping` — _<your label>_.
- `delivered` — a slice's change request has merged into its feature branch, awaiting promotion. Set by the `merge-change` skill in the same act as the merge it performs; the ticket **stays open** — closure is native and atomic at promotion, the parent spec ticket's PR into the base branch carrying one `Closes` line per slice, so the tracker never needs manual closes. An open-with-`delivered` slice under an abandoned spec is the honest record: the work exists on a branch and never shipped. Default `delivered` — _<your label>_.
- _(no readiness label)_ — not yet groomed; a target for `backlog groom`, not for `backlog build`.

**Closure** — the change request's closing reference (`Closes #N`) closes the ticket on merge to the base branch; there is no post-build label by default. Stacked slices: see `delivered` above.

Two further lifecycle values appear only where the tracker has no native equivalent (the local binding's `state:` field), written on the build side's work branches, never by grooming: `in-review` (a PR is open for it — set on the work branch at PR-open) and `closed` (set on the work branch once review converges; the merge carries it to main). On trackers with native state (GitHub), an open PR and native closure express these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Default `bug` — _<your label>_.
- `enhancement` — implement branch: strategic decisions arrive settled or delegated (groom's route judgment), and the build thread makes only a just-in-time tactical plan within that authority. Default `enhancement` — _<your label>_.
- `refactor` — refactor branch. Default `refactor` — _<your label>_.
- `research` — source-audit branch, for **epistemic-terminal** work: the deliverable establishes what primary sources support, what follows by inference, what conflicts, and what remains unknown. Correctness comes from traceability and the research skill's claim audit, not taste or implementation behavior. Default `research` — _<your label>_.
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a narrative synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — no mechanical `verify` pass/fail. Default `draft` — _<your label>_.
- `spec` — coverage-check branch, set by the `to-slices` skill when it parents a split spec'd ticket over its slices: the ticket holds the spec its children deliver in installments, and stays the shared context they inherit from. Undispatchable until every child is closed or `delivered` (§ Dependencies); when the last child crosses that line it surfaces to `backlog build`, and the dispatched thread verifies the delivered children against the spec — filing each gap as a new child, which re-blocks the parent — or, on a clean pass, opening the promotion PR ready for review; its merge stays the `merge-change` skill's human authorization. Its spec text is never rewritten. Guard: **every shaped ticket has a spec; only a split parent has the `spec` work-type** — the label names dispatch behavior, not artifact presence. Default `spec` — _<your label>_.

> Recognizing the boundary: if the terminal question is “what do the sources establish?”, groom to `research`. If the sources are inputs to prose judged by voice, persuasion, or fit, groom to `draft`. If behavior must change, retain the applicable bug/enhancement/refactor type and invoke research as a substage.

## Dispatch metadata

Groom records the facts `backlog build` passes to dispatch **before** any thread spawns:

- **Surface** — `backend`, `ui`, `mixed`, or `non-code`; include any required capability.
- **Coordination class** — `routine` when the decisions arrive settled and the build thread only executes; `orchestrator-required` when the thread carries a named residual uncertainty — a delegated design call, a hard diagnosis, an open tactical question. Work whose product decisions are neither settled nor delegated is not classed at all — it parks at `needs-shaping`. This is not a difficulty score; staffing reads it as an input to the intelligence bar.
- **Coordination reason** — one sentence naming why the class applies and any known uncertainty. Required for both classes so the decision is auditable.
- **Route (enhancements)** — `route: direct` plus one line on why the strategic decisions are settled or delegated. A `ready-for-agent` enhancement without it is a grooming gap.

Tracker encoding: _<GitHub: a stable `Dispatch:` block in the body or grooming comment; local: `surface`, `coordination`, and `coordination-reason` frontmatter; custom: name the fields here>_. Missing metadata is a grooming gap: `backlog build` skips the ticket rather than inferring it.

**Exclusion** — terminal; removed from grooming and from the run queue:

- `wontfix`, `duplicate`, `superseded`, `invalid` — _<your labels>_.

**Neutral** — every other label; ignored for selection and routing. On an inherited tracker this is _most_ labels (priority, area/component, size, team, release). The default is **neutral**: a label maps to a role only when `setup` explicitly bound it: _<list the role→label mappings here; leave everything else neutral>_.

**Aliases** — when several existing labels fill one role, one is canonical and every reader treats the others as that role too: _<e.g. `type:bug` and `defect` both → `bug`; or "none">_. Setup reuses existing labels rather than minting duplicates.

## Label colors

On trackers that carry label colors (GitHub), each role label gets the shared scheme below so the same role reads the same everywhere. Color encodes the axis: readiness roles are saturated — a state machine, temperature-coded from parked to flying; work-types are pastel attributes, `bug` and `spec` the deliberate saturated exceptions; exclusions are grayscale. Trackers without colors (the local binding) skip this section entirely.

The tracker description is the short form applied on the label itself; the role definitions above stay canonical. Apply with the skill's reconcile script — `scripts/reconcile-labels.py --repo <owner/name>`, dry-run first, using `--label role=name` for any renamed role and `--create` only with the user's consent — which touches only role labels and never neutral ones. A repo that wants different colors overrides them here; this table then beats the skill default.

| Role | Color | Tracker description |
| --- | --- | --- |
| `needs-shaping` | `#D93F0B` | Parked for strategic shaping: unsettled product/scope decisions; never selectable by backlog build |
| `shaping` | `#FBCA04` | A shaping thread is attending this issue; set by backlog groom at dispatch |
| `needs-info` | `#D876E3` | Parked, waiting on the reporter |
| `ready-for-agent` | `#0E8A16` | Groomed and released: an agent may work it; requires a work-type and dispatch metadata |
| `ready-for-human` | `#5319E7` | Human-only; agents skip. Also the abort target for verify caps and environment blockers |
| `building` | `#1D76DB` | Claimed: a build thread owns it; the claim comment is the dispatch declaration with its deadline |
| `delivered` | `#008672` | Merged into its feature branch, awaiting promotion; closed natively by the promotion PR's Closes lines |
| `bug` | `#D73A4A` | Something isn't working |
| `enhancement` | `#A2EEEF` | New feature or request |
| `refactor` | `#C5DEF5` | Work-type: behavior-preserving structure or code improvement |
| `research` | `#D4C5F9` | Work-type: primary-source research with traceable claims |
| `draft` | `#FEF2C0` | Work-type: judgment-terminal produce-and-review; done at the human review verdict |
| `spec` | `#8250DF` | Work-type: parent of slices; coverage check once children are closed or delivered |
| `duplicate` | `#CFD3D7` | This issue or pull request already exists |
| `superseded` | `#BFBFBF` | Replaced by newer work; removed from grooming and the run queue |
| `invalid` | `#E4E669` | This doesn't seem right |
| `wontfix` | `#FFFFFF` | This will not be worked on |

## Dependencies

- How this repo records that one issue is blocked by another, so `backlog build` can skip blocked work: _<prefer the tracker's exercised native relation (GitHub `blocked_by`, Jira `is blocked by`, Linear `blocked-by`) via `platform.md`; local uses `deps:` frontmatter; a tracker without an exercisable native relation names its explicit fallback here>_.
- `backlog build` treats an issue with any unresolved (open/incomplete) blocker as blocked and skips it. Duplicate/supersede links: _<the convention — a `duplicate of #N` / `superseded by #N` body line plus the exclusion label, or the tracker's native link>_.
- **Open children block the parent — until closed or delivered.** How this repo records that one issue is a child of another: _<prefer the tracker's native parent/child relation (GitHub sub-issues) via `platform.md`; local uses `parent:` frontmatter; a tracker without one names its explicit fallback here>_. A parent is dispatchable only when every child is **closed or `delivered`**, whatever its labels — `backlog build` skips it exactly as it skips a blocked issue. No per-child blocking edges are wired: the relation itself carries the block, so a child attached mid-flight (a capture, a gap the coverage check files) re-blocks the parent by existing. The `delivered` label is the live signal, and `backlog status` reads both.

## Deadlines

- Every dispatch carries a **deadline as an absolute timestamp**, posted in the claim comment so any machine can rule on it — in the pull model the deadline has nowhere else to live.
- Sizing: match the expected build — hours, not days: _<e.g. 4h for a routine slice, 8h for orchestrator-required work; state this repo's sizes>_.

## Readiness decision

- The agent proposes work-type, dispatch metadata, and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. `ready-for-human`, `needs-info`, `needs-shaping`, and exclusion roles need no per-issue confirmation — they ride the groom plan's blanket approval, since every tracker mutation waits for that gate.
- In a shaping thread, the readiness blessing records the **commit hash** of the spec on its artifact branch: the blessing authorizes exactly that revision. Any later commit past the blessed hash mechanically invalidates readiness — the subject returns to shaping until re-blessed. It never authorizes build changes or unrelated shaping work.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).

## Building hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `building` is the claim marker, applied optimistically — the build dispatcher accepts the rare duplicate pickup in the window between sweep and claim rather than carrying a lock.
- **Claims are attributed.** The claim comment is posted by the runner's own tracker actor and names the branch, so any later reader can tell whose claim it is. A claim by another actor is another runner's build — its claim and labels are not yours to touch, even expired; a comment (a takeover note, a question) may still land on the ticket, and a reclaim of your own expired claim is a new claim comment superseding the old.
- **Orphan sweep** — a `building` ticket whose recorded branch no longer exists, or whose claim predates deadlines and has gone quiet past the **quiet horizon** (_<e.g. 7 days>_), is a corpse: `backlog status` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work, and a reclaim adopts it from the branch rather than starting over.
