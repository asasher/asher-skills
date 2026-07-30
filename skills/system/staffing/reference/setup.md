# Setup

Write or reconcile the project's staffing playbook — the sole authority for the roster — and the trigger
that makes sessions read it. Setup writes only inside the repo.

1. Run the [machine audit](machine-audit.md) and read the compiled active provider's
   [harness mechanics](harness.md). Record each route this harness can actually invoke, classify each
   sibling-harness direction into its route state — effect-verified, intentionally disabled, or unavailable
   with its failure class — and record the evidence behind each classification, per the audit's
   § Route classification.
2. Read the existing project staffing playbook if there is one, plus the bundled roster seed. The seed
   supplies starting values for what cannot be probed — the judgment numbers — and nothing else. Every
   reachability, alias, provider, and eligibility row in the playbook comes from the audit, not the seed.
3. Write or reconcile the playbook per [install and reconcile](install-and-reconcile.md). It is repo-owned:
   an existing file is reconciled clause by clause, never overwritten wholesale, and owner-tuned judgment
   numbers survive. Record the machine, probe date, and CLI versions at its head: the machine and date go
   down as the stamp line `<!-- machine-record: machine=<short hostname> probed=<YYYY-MM-DD> -->` on its
   own line at the head of the probe record, followed by the human-readable probe-record table. A playbook
   whose recorded machine is not this machine is stale, and saying so is what stops a foreign row from
   being trusted; a repo whose installed skill set ships a machine-fact checker reads the stamp
   mechanically, and absent one the stamp plus this rule remain the guard. The header dates follow the
   same establishing-observation rule as row evidence: a run that confirms every recorded fact rewrites
   nothing, header included — the stamp line with it. This playbook is the one home for model and
   capability reachability — routes, dispatch aliases, effect verdicts — and for the CLI-version
   metadata stamped on their probes: report any other playbook found restating them as drift. A
   version is metadata that cues re-probing after an upgrade, never a fact a session resolves
   against.
4. Reconcile the shipped trigger template (`templates/instruction-trigger.md`) into the project's agent
   instruction file — the harness-neutral base every harness loads where one exists, else the instruction
   file the repo's harnesses actually read. A playbook nothing points at is never consulted; the trigger is
   what fires before model choice, delegation, child/worktree creation, watcher assignment, or fallback.
   Reconcile an existing § Staffing section to the template's content — a section already matching it is
   left as it is; never overwrite foreign sections.
5. Resolve the resulting playbook and report unreachable routes, conflicting pins, any row the audit could
   not verify, and every drift between what this run probed and what the playbook recorded — a conflict is
   reported and applied per [install and reconcile](install-and-reconcile.md), never settled silently in
   either direction.

Keep data and doctrine apart. The playbook holds model rows, per-harness eligibility and capability bindings,
pins, floor, succession, probed reachability, and the probe record. Ranking rules, wake-path selection, and
harness command shapes stay in this skill's references — they are the same on every machine, so a playbook
that restates them is drift waiting to happen.

Completion criterion: this project resolves one unambiguous roster from its playbook alone, with no
home-directory dependency and no runtime read of the seed; every recorded route names the probe that
verified it, and a dispatch alias appears only with the probe that accepted it — a name no probe covered
stays marked unverified; and a machine that did not run those probes is told to re-run setup rather than
trusting them.
