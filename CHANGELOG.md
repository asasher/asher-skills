# Changelog

The reconcile ledger. Every merge that changes `skills/` appends an entry here naming the skills it touched and the setups to re-run. Consumers reconcile from this file — see the README's Reconcile prompt. Newest entry first.

## 2026-08-15 — The pull-model refactor (v3)

Every installed skill changed. Treat the whole set as new: re-install your set, remove the renamed-away mounts, and re-run every setup below.

**Renamed** (remove the old mount, install the new name):

- `build` → `build-change` — builds one review-ready change, from a ticket or from spec'd work without one.
- `merge-changes` → `merge-change` — the action was always per-change.
- `serve-via-tailnet` → `to-tailnet` — behavior unchanged.

**New:**

- `writing-for-humans` — reference: the communication standard (ASD-STE100, `CONTEXT.md` as the dictionary, no bare ticket/PR numbers).
- `agent-ready-codebase` — reference: the repo-readiness standard (four-item parallel-safety checklist, use ≠ change) that `backlog setup` certifies against.
- `to-web` — uploads a file to the bound store, returns a durable hash-keyed URL; evidence media's home, artifacts' preview deploy.

**Changed:**

- `backlog` — pull model: `groom` merges fragments and fans shaping threads at a user-chosen width; `build` posts the dispatch declaration as the claim (absolute deadline) and exits — no babysitting, no wakes; new `status` verb derives finished/stalled/abandoned and owns the teardown sweep. Concurrency cap, quota gate, usage accounting, serialize-verification, and lane mechanics are deleted. The machine-facts preflight and its script are deleted.
- `shape` — one subject per thread; the shaping change request is deleted — the spec lives on an `artifact/*` branch, blessed at a commit hash; the spec carries the context delta and the test split.
- `to-spec` — the branch file is canonical; the ticket carries a projection (summary, render URL, commit hash).
- `to-slices` — the draft is a justified recommendation; the split chooses a landing shape (stacked feature branch by default, with the `delivered` role); the parent work-type `capstone` is renamed `spec`.
- `to-subagent` — synchronous-only dispatch, dispatch declaration, deliverable validation; the wake path is deleted.
- `to-thread` — outermost-harness detection first (ask when unsure), five route files (T3, Claude CLI, Claude Desktop, Codex CLI, Codex Desktop), liveness before success.
- `staffing` — bars-then-cheapest resolution; machine overlay, probes, and self-heal deleted; setup is a template fill. Per-provider variants no longer exist.
- `merge-change` — `delivered` on slice merges into feature branches, the intent-tier conflict ladder (mechanical → intent-resolvable via specs → spec-collision stops).
- `verify-your-work` — executes the spec-declared test split; scaffolding runs captured as evidence, scripts dropped before merge.
- `prove-your-work` — evidence media via `to-web`, embedded by URL, never committed.
- `interview` — the question template (numbered, titled, recommended answer); engine mode deleted.
- `domain-modeling` — terms and ADR drafts go into the spec's context delta; builds land them.
- `research` — shrunk to primary sources + cited claims + as-of boundary + claim audit; its setup verb and playbook are deleted.
- `prototype` — two concrete artifact formats (self-contained HTML for logic, variants on one route for UI); placement playbook deleted.
- `implement`, `tdd`, `diagnosing-bugs`, `code-review`, `adversarial-review` — renamed-sibling references; `diagnosing-bugs` setup templates pruned to flaky surfaces and seams.

**Removed:** the first-party installer (`tools/install.py`) and its state file (`.agents/asher-skills/install.json`). Install with `npx skills add`; reconcile from this changelog.

**Setups to re-run, in order:** `backlog setup` (bindings, label roles incl. `spec` and `delivered`, agent-readiness certification), `staffing setup` (template fill), `retro setup` (where installed), `diagnosing-bugs` setup (where installed).
