# Setup

Install or reconcile the roster without surprising global writes.

1. Run the [machine audit](machine-audit.md). Record each harness and every route it can actually invoke.
2. Read the existing global base and project staffing playbook, then follow the scope decision in
   [install and reconcile](install-and-reconcile.md).
3. If a global base exists, leave it intact and offer only a project delta. If none exists, ask whether to
   create a consented global base or a project-only roster.
4. Write or reconcile only the selected layer. Project overrides contain deltas, never a copy of the base.
5. Resolve the resulting base plus project delta and report unreachable routes or conflicting pins.

Completion criterion: the current project resolves one unambiguous roster; any global write was explicitly
approved; an existing global base is byte-for-byte unchanged unless the user explicitly asked to edit it.
