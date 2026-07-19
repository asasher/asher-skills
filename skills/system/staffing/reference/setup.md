# Setup

Install or reconcile the roster without surprising global writes.

1. Run the [machine audit](machine-audit.md) and read the compiled active provider's
   [harness mechanics](harness.md). Record each route this harness can actually invoke.
2. Read the existing global base and project staffing playbook, then follow the scope decision in
   [install and reconcile](install-and-reconcile.md).
3. Write or reconcile only the selected layer. In each compiled provider package,
   `templates/global/staffing.module.md` contains one `{{COMMON}}` marker for
   `staffing.common.md`; `staffing-pointer.md` is that provider's compact pointer. Use
   `scripts/render-global.py render`/`check` for byte-authoritative previews, then `stage` each consented
   provider module and `apply` per
   [install and reconcile](install-and-reconcile.md) § Module-first owner reconciliation. Project overrides
   contain deltas, never a copy of the base.
4. Resolve the resulting base plus project delta and report unreachable routes or conflicting pins.

Completion criterion: the current project resolves one unambiguous roster; any global write was explicitly
approved; an existing global base is byte-for-byte unchanged unless the user explicitly asked to edit it.
