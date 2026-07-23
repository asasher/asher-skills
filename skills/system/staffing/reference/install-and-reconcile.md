# Install, scope decision, reconciliation, and external-worker mechanics

## Install shapes

The human chooses **project-only** or **global-with-overrides**. Project-only writes one project staffing
playbook and no home-directory file. Global-with-overrides writes the audited machine truth once and gives
each project a sparse delta.

For global-with-overrides, the active harness gets:

- a compact `## Staffing` pointer in its global agent instruction file;
- a self-contained deferred module at the absolute path named by that pointer; and
- project deltas under `docs/agents/`, containing only fields that differ.

The module contains the reachable rankings, named capability providers and fallbacks, pins,
coordinator-eligible set, floor, succession, directional reachability, and active-harness mechanics. Resolve
the module first, then overlay project deltas field by field. A project that only raises the floor writes only
that raised floor; copying the base table is drift.

## Scope decision

- **A global base exists:** show it, preserve it, and offer a project delta. Editing the base is a separate
  explicit request.
- **No global base exists:** ask project-only versus global-with-overrides. A global choice is explicit
  consent for the described home-directory writes, not blanket permission for later changes.

The active provider's exact instruction-file/module paths and dispatch commands are in `reference/harness.md` in the
installed package. Directory presence is evidence, not authority: setup confirms which harnesses are active.

## Module-first owner reconciliation

Staffing owns only its pointer, module, and roster — nothing else in the global file. The apply is
`render-global.py apply`: the audited module is written atomically and read back, then the `## Staffing`
section is reconciled into the global file with every foreign byte preserved. Module-first: the deferred module lands before the pointer
that names it, within the same apply. Never use an eager import.

An apply failure changes nothing: the read-back check fails closed. Missing, unreadable, or changed staffing
modules fail closed: report the gap and do not dispatch. Do not rewrite unchanged modules. A second
successful reconcile leaves durable module, global, delta, and lock bytes unchanged. Migration is proposed,
never automatic; retain recovery bytes until the new policy passes its probes.

## Reconciliation is a prose audit

Read the installed module, pointer, project delta, and current machine audit; report drift or conflict in
prose. Examples: an unreachable row, a stale directional route, an override that recopies the base, or a pin
conflict. That reading is the judgment mechanism. Provider-package effective
hashes are install provenance, not roster-policy truth.

## External-worker contract

Native models use native dispatch. Every non-native CLI task runs inside a watched native wrapper so the
originating harness's tree shows the external harness/model and task. Resolve the wrapper as the cheapest
native model allowed by the current floor; the parent owns the prompt, judgment, and effect verification;
the external harness owns the task; the wrapper owns only bounded process supervision and raw relay. No
fire-and-forget shell may own delegated work.

The wrapper label names `<external-model>:<task>`, closes stdin for non-interactive commands, applies an
explicit timeout, and captures the durable raw result separately from lifecycle metadata. It returns both to
the parent, which verifies the requested effect. If native spawn cannot accept the resolved wrapper model or
report the assigned one, keep agent-tree observability but record the staffing gap and do not claim
floor/cost compliance.

Reachability state is per direction: **effect-verified**, **intentionally disabled**, or **unavailable** with
a captured failure class and successor. One failed direction never disables the healthy direction. Do not
poll vendor policy or credits as a dispatch precondition.
