# Setup

Install or reconcile the roster without surprising global writes.

1. Run the [machine audit](machine-audit.md) and read the compiled active provider's
   [harness mechanics](harness.md). Record each route this harness can actually invoke.
2. Read the existing global base and project staffing playbook, then follow the scope decision in
   [install and reconcile](install-and-reconcile.md).
3. If a global base exists, leave it intact and offer only a project delta. If none exists, ask whether to
   create a consented global base or a project-only roster.
4. Write or reconcile only the selected layer. In each compiled provider package,
   `templates/global/staffing.module.md` contains one `{{COMMON}}` marker for
   `staffing.common.md`; `staffing-pointer.md` is that provider's compact pointer. Use
   `scripts/render-global.py render`/`check` for byte-authoritative previews, then `stage` each consented
   provider module into the fresh reconciliation transaction barrier begun by setup. Apply no global pointer until the setup
   orchestrator has staged and read back all four deferred modules — Presentation and Staffing for Codex and
   Claude — and the barrier still verifies their hashes. Setup then preflights and applies both Presentation
   sections. Only after both match the preflight may each compiled provider use `apply` to reconcile its
   Staffing section; setup verifies all four final sections and finalizes the transaction. Any
   staging/read-back/preflight failure leaves both global files untouched. Never alter another owner's bytes
   or use an eager import. Project overrides contain deltas, never a copy of the base.
5. Resolve the resulting base plus project delta and report unreachable routes or conflicting pins.

Completion criterion: the current project resolves one unambiguous roster; any global write was explicitly
approved; an existing global base is byte-for-byte unchanged unless the user explicitly asked to edit it.
