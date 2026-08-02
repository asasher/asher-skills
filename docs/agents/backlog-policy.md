# Playbook: Backlog Policy

> Project playbook for this repo. Read by `backlog groom` (to triage and dispatch shaping), `backlog build` (to select and dispatch ready work), and build sessions (to route on work-type). The skill reasons in **roles**; map this tracker's actual label names to each role below so the wording can differ per repo. On the local tracker binding (`platform.md`) the mapping is the identity — roles are the frontmatter values verbatim.

## Work domain

- Domain: **skill-authoring** — step playbooks scaffolded from `templates/skill-authoring/` plus the shared `templates/common/` baselines.
- Why this pack: probe transcripts are this repo's _primary_ proof, and the skill-authoring pack makes them the default evidence — the software pack treats an agent-authored probe transcript as a greenfield-only fallback, which would call this repo's main evidence a fallback.

## Label roles

Two independent axes, plus exclusions. Readiness decides _whether and who_ picks an issue up; work-type decides _how_ the agent works it.

**Readiness / ownership** — map each to this repo's label:

- `ready-for-agent` — groomed and released: the agent may work it. Requires a work-type and complete dispatch metadata (§ Dispatch metadata). Label: **`ready-for-agent`** (identity).
- `building` — dispatched: a build subagent owns it, so `backlog build` never selects it again. Set by `backlog build` at dispatch, replacing `ready-for-agent`; records what's flying via the attributed claim comment (§ Building hygiene). Cleared on abort, superseded by closure when the change merges, or reset by `groom`'s human-confirmed orphan sweep. Label: **`building`** (identity).
- `ready-for-human` — only a human; the agent skips it entirely. Also the abort target for verify caps and environment blockers: the agent hands the issue back with the blocker commented, since a human must look before it can be re-released. Label: **`ready-for-human`** (identity).
- `needs-info` — parked, waiting on the reporter. Label: **`needs-info`** (identity).
- `needs-shaping` — parked for strategic shaping: the issue carries product/design/scope decisions that are neither settled nor delegated, or execution invalidated an approved decision. Set by `groom`'s route judgment, by an issue thread's handback, or by a build session that hit the invalidation — a blessed spec contradicted by the code it meets comes back here with the contradiction commented, the named re-entry into shaping; cleared when shaping delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the product owner owes shaping. Never selectable by `backlog build`. Label: **`needs-shaping`** (identity).
- `shaping` — a shaping thread is attending it. Set by `backlog groom` at dispatch, replacing `needs-shaping`, so a subject never gets two threads. A batch advances atomically: after readiness is blessed, every member moves to `ready-for-agent` only after its clean shaping worktree is removed or its shaping change is merged, verified, and cleaned up; abandonment returns the whole batch to `needs-shaping`. Label: **`shaping`** (identity).
- _(no readiness label)_ — not yet groomed; a target for `backlog groom`, not for `backlog build`.

**Closure** — the change request's closing reference (`Closes #N`) closes the ticket on merge; there is no post-build label: **none — direct closure** (no staging branch here; merge to main is final).

Two further lifecycle values appear only where the tracker has no native equivalent, written by the loop, never by grooming: `in-review` and `closed`. This repo is on GitHub, which expresses both natively — an open PR is `in-review`, native issue closure (via `Closes #<n>` at merge) is `closed`. No extra labels for these.

**Work-type** — required for `ready-for-agent`; decides the branch:

- `bug` — diagnose branch. Label: **`bug`** (identity).
- `enhancement` — implement branch: strategic decisions arrive settled or delegated (groom's route judgment), and the issue thread makes only a just-in-time tactical plan within that authority. Label: **`enhancement`** (identity).
- `refactor` — refactor branch. Label: **`refactor`** (identity).
- `research` — source-audit branch for epistemic-terminal work. The kept dossier records supported facts, traceable inferences, contradictions, and unknowns under `research/<slug>/`. Label: **`research`** (identity).
- `draft` — produce-and-review branch, for **judgment-terminal** work: produce a novel artifact whose correctness is taste/fit, not a testable spec (a memo, copy, a narrative synthesis, code docs). Enhancement-shaped, but the definition of done is the **human review verdict** at the review gate — there is **no mechanical `verify` pass/fail**. The artifact is **kept** (committed and merged): that is the line against `prototype`, which is throwaway — keep the answer, delete the artifact. Label: **`draft`** (identity).
- `capstone` — coverage-check branch, set by the `to-slices` skill when it parents a split spec'd ticket over its slices: the ticket holds the spec its children deliver in installments, and stays the shared context they inherit from. Undispatchable while any child is open (§ Dependencies — open children block the parent); when the last child closes it surfaces to `backlog build`, and the dispatched session verifies the delivered children against the spec — filing each gap as a new child, which re-blocks the parent, or closing it on a clean pass. Its spec text is never rewritten. Label: **`capstone`** (identity).

> If the terminal question is what sources establish, use `research`. If sources feed prose judged by voice, persuasion, or fit, use `draft`. If behavior must change, keep the applicable code work-type and invoke research as a substage.

**Exclusion** — terminal; removed from grooming and from the run queue:

- Labels: **`wontfix`**, **`duplicate`**, **`superseded`**, **`invalid`** (all identity; `documentation`, `question`, `good first issue`, `help wanted` are neutral).

**Neutral** — every other label (priority, area, size, etc.); ignored for selection and routing. The default is **neutral**: a label maps to a role only when `setup` explicitly bound it — here every binding above is the identity mapping; everything else stays neutral.

**Aliases** — when several existing labels fill one role, one is canonical and the loop treats the others as that role too: **none** — every role label here is a single identity mapping. Setup reuses existing labels rather than minting duplicates.

## Dispatch metadata

Every `ready-for-agent` issue carries a stable `Dispatch:` block in its body or latest grooming comment:

- `surface`: `backend`, `ui`, `mixed`, or `non-code`, plus any required capability.
- `coordination`: `routine` or `orchestrator-required`.
- `reason`: one sentence naming why the class applies and any known uncertainty. Routine means the issue is settled enough for a normal coordinator; orchestrator-required is reserved for product judgment, design, hard diagnosis, or another named uncertainty.
- `route` (enhancements): `route: direct` plus one line on why the strategic decisions are settled or delegated. A `ready-for-agent` enhancement without it is a grooming gap.

`backlog build` passes these fields to staffing before creating a worktree or child. Missing fields are a grooming gap, never permission to infer them or default to the orchestrator — the ticket is skipped.

## Dependencies

- How this repo records that one issue is blocked by another: GitHub's native `blocked_by` relation, read and written with the verified verbs in `platform.md`. `backlog build` treats an issue with any unresolved (open/incomplete) blocker as blocked and skips it, releasing it once the edge clears. Duplicate/supersede links remain a `duplicate of #N` / `superseded by #N` body line plus the exclusion label.
- **Open children block the parent.** How this repo records that one issue is a child of another: GitHub's native sub-issue relation, read and written with the verified verbs in `platform.md`. An issue with any open child is never dispatchable, whatever its labels — `backlog build` skips it exactly as it skips a blocked issue. No per-child blocking edges are wired: the relation itself carries the block, so a child attached mid-flight (a capture, a gap the capstone check files) re-blocks the parent by existing.

## Readiness decision

- The agent proposes work-type, dispatch metadata, and readiness for every issue during grooming, but applies `ready-for-agent` only to issues the human confirms in the shortlist. `ready-for-human`, `needs-info`, `needs-shaping`, and exclusion roles need no per-issue confirmation — they ride the groom plan's blanket approval, since every tracker mutation waits for that gate.
- In a shaping thread, the readiness blessing authorizes only the exact shaping change-request head the thread presented **before** requesting that signal, with the narrow effect explained. It does not authorize a later head, build changes, or unrelated shaping work.
- Adjust this rule if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs).
- **Work on the loop is dispatchable when it rides the branch → merge → reconcile path.** The mounts are decoupled from the sources, so a build session reads stable installed copies: a worktree edit to skill sources, templates, or playbooks changes nothing a running session resolves through until the change merges and the reconcile step is run deliberately in the main checkout. Such issues may be `ready-for-agent`. What remains `ready-for-human` is work that **mutates a live resolution surface in place**, outside that path: the main checkout's playbooks during an active run, the installed mounts themselves, machine-global instruction files, or the reconcile step itself. The test: "does executing this issue rewrite, in place, a surface a concurrently running session resolves through?"

## Build concurrency

> Read by `backlog build` before dispatch — the owner's burn bound on unattended fan-out. Policy data, set here by choice, never derived from the environment audit.

- **Max concurrent builds**: **uncapped** — this repo's standing choice. Builds here are files-plus-stdlib work with no shared runtime (`environment.md` § Parallelism verdict holds the parallel-safe constraint), sustained burn has not bitten this repo, and the queue-on-refused-spawn rule absorbs whatever the harness declines to run at once. The knob exists so a burn bound is one playbook edit away.
- The unit is the **build** — one ticket's whole pipeline in its one worktree — never the subagents a build fans out. Under a numeric cap, a ready ticket beyond it waits unclaimed — no `building` label, no claim comment, no worktree — for a slot freed by a completed or aborted build; a **per-run override** may narrow a single run below the recorded value, never widen it.

## Building hygiene

- Concurrent runners are possible (two machines, two humans, one tracker); `building` is the claim marker, applied optimistically — the build dispatcher accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock. It re-reads each issue immediately before marking it and skips any that changed.
- **Claims are attributed.** The claim comment is posted by the runner's own tracker actor and names the branch and dispatch date, so any later reader can tell whose claim it is. A resuming dispatcher owns exactly the claims that match its actor and branches; a claim by another actor is another runner's live build — its claim and labels are not yours to touch; a comment (a lane-takeover note, a question) may still land on the ticket.
- **Orphan sweep** — a `building` issue whose recorded branch no longer exists, or has gone quiet past the **7-day quiet horizon**, is a corpse: `groom` surfaces it to the human as a candidate reset to `ready-for-agent` (or `needs-info`). Never silently reset — the branch may hold unmerged work.
