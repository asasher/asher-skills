# Setup and reconciliation

Setup studies the consumer repository, confirms its choices, and materializes only `relay/` plus
`docs/agents/relay.md`. It has no previous-instance migration branch.

## Discover and bind

1. Run `python3 scripts/setup_instance.py <repo-root> --discover`. Inspect the report for repositories,
   project registries, trackers, release evidence, mailbox sources, existing editorial/template material,
   optional source skills, Node/npm, root `.env`, and AgentMail CLI reachability.
2. Confirm authoritative evidence providers for shipped, pending, cash, growth, and commitments; projects and
   their section recipes; audience membership, explicit To/CC roles, interests, disclosure, cadence, and
   coalescing; operator CC; editorial rules; template choice; AgentMail inbox, verified sender/domain, and
   webhook or manual reconciliation.
3. Write those non-secret choices to a complete binding JSON shaped by
   `templates/instance/bindings.json`, then run
   `python3 scripts/setup_instance.py <repo-root> --binding <binding.json>`.
4. Create human-readable relationship profiles when needed. Bind the same current profile SHA-256 into its
   audience and interest manifests; a stale derivative stops selection.

Evidence providers are project data. A binding may name a stable path, command, connector, or optional sibling
skill. `review-loop` is the only required sibling. Do not make `manage-tasks`, `manage-opportunities`, a mailbox,
or any particular repository layout universal.

## Credentials and capability

Read or provision only `AGENTMAIL_API_KEY` in `<repo-root>/.env`; preserve unrelated assignments. Before a live
check require `.env` to be ignored by Git and mode `0600`. Never shell-source it or put the value in output,
argv, logs, candidates, capability files, or state.

Record only non-secret inbox, sender, verified-domain, minimum CLI/API version, permissions, and reconciliation
mode in `capabilities.json`. Tool presence or exit zero alone is not capability proof — record only
effect-verified operations, and report a capability failure as the failed check plus confirmation that zero
live provider action occurred. Offer custom-domain verification, but allow setup to finish with another
verified sender when the user declines. A selected unverified sender blocks live send. Do not claim real-time
events unless a signature-verified receiver was effect-tested; otherwise record `manual`.

## Reconcile

Rerun setup after repository or package changes. Missing defaults are copied. Existing consumer files and
templates are preserved. Changed defaults produce `.setup-candidate` files. A changed discovery report becomes
a candidate; it never rewrites a confirmed binding. Stop and surface conflicts that affect recipients,
disclosure, sender, credentials, or delivery safety.

Completion criterion: the instance validator passes with complete projects, providers, recipes, audiences,
header roles, operator policy, cadence, sender, template, and reconciliation mode; all deliberate local values
remain byte-identical on rerun; the credential exists only in the protected root `.env`; and no provider
resource or message was created without separate authorization.
