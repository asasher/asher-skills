# Setup

Install or reconcile the roster without surprising global writes.

1. Run the [machine audit](machine-audit.md) and read the compiled active provider's
   [harness mechanics](harness.md). Record each route this harness can actually invoke.
2. Read the existing global base and project staffing playbook, then follow the scope decision in
   [install and reconcile](install-and-reconcile.md).
3. Write or reconcile only the selected layer. In each compiled provider package,
   `templates/global/staffing.module.md` contains one `{{COMMON}}` marker for
   `staffing.common.md` and ships the seed defaults; `staffing-pointer.md` is that provider's compact
   pointer. `scripts/render-global.py render` emits the seed; apply the audit's machine-tuned edits to that
   rendered copy (prune unreachable rows, bind providers, owner-tuned numbers), then `stage` the audited
   module (`--audited <file>`) and `apply` per
   [install and reconcile](install-and-reconcile.md) § Module-first owner reconciliation. The byte guarantee
   binds the staged audited copy to what lands in the global file — `check` verifies against the audited
   module when given, the pristine seed otherwise. Project overrides contain deltas, never a copy of the
   base.
4. Resolve the resulting base plus project delta and report unreachable routes or conflicting pins.

Completion criterion: the current project resolves one unambiguous roster; any global write was explicitly
approved; an existing global base is byte-for-byte unchanged unless the user explicitly asked to edit it.
