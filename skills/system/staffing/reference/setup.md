# Setup

Write or reconcile the project's staffing playbook — the sole authority for the roster. Setup touches one
file; it never writes outside the repo.

1. Run the [machine audit](machine-audit.md) and read the compiled active provider's
   [harness mechanics](harness.md). Record each route this harness can actually invoke, each direction's
   state, and the probe evidence behind it.
2. Read the existing project staffing playbook if there is one, plus the bundled roster seed. The seed
   supplies starting values for what cannot be probed — the judgment numbers — and nothing else. Every
   reachability, alias, provider, and eligibility row in the playbook comes from the audit, not the seed.
3. Write or reconcile the playbook per [install and reconcile](install-and-reconcile.md). It is repo-owned:
   an existing file is reconciled clause by clause, never overwritten wholesale, and owner-tuned judgment
   numbers survive. Record the machine, probe date, and CLI versions at its head — a playbook whose recorded
   machine is not this machine is stale, and saying so is what stops a foreign row from being trusted.
4. Resolve the resulting playbook and report unreachable routes, conflicting pins, and any row the audit
   could not verify.

Keep data and doctrine apart. The playbook holds model rows, per-harness eligibility and capability bindings,
pins, floor, succession, probed reachability, and the probe record. Ranking rules, wake-path selection, and
harness command shapes stay in this skill's references — they are the same on every machine, so a playbook
that restates them is drift waiting to happen.

Completion criterion: this project resolves one unambiguous roster from its playbook alone, with no
home-directory dependency and no runtime read of the seed; every recorded route names the probe that
verified it; and a machine that did not run those probes is told to re-run setup rather than trusting them.
