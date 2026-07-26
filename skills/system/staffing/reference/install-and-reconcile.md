# Install, reconciliation, and external-worker mechanics

## One layer

Setup writes exactly one file: the **project staffing playbook**, under the repo's agent-docs directory. It is
the sole runtime authority. There is no home-directory module, no pointer section in a global agent
instruction file, and no base-plus-delta overlay to resolve.

The playbook contains the reachable model rows, per-harness eligibility, named capability providers and
fallbacks, pins, floor, succession, directional reachability with its probe evidence, and the probe record
naming the machine and CLI versions. Doctrine stays in this skill's references; a playbook that restates a
ranking rule or a command shape has copied something that will drift.

The bundled roster **seed** supplies starting values for the judgment numbers — cost, intelligence, taste,
effort — because those cannot be probed. It is read once, at setup, and never at resolution time. Everything
else in the playbook comes from the audit.

Two layers were the previous shape and the reason this one exists: a base plus sparse deltas produces the
"override silently re-copied the base" failure, and it puts the effective roster somewhere no project diff
shows. One layer makes the roster reviewable in the repo that depends on it.

## Reconciling an existing playbook

The playbook is **repo-owned**. Reconcile it clause by clause; never overwrite it wholesale.

- Owner-tuned judgment numbers survive a re-run. They are the values setup cannot derive, so setup does not
  get to reset them.
- Audit-derived rows — reachability, aliases, provider bindings, eligibility — are replaced by what this run
  probed, and a replacement that contradicts what was recorded is **reported as drift**, not applied
  silently. Silently preserving a stale row and silently overwriting a fresh one are the same failure seen
  from two sides. Direction states move both ways under this rule: a recorded **unavailable** direction
  whose fresh effect probe succeeds is reported and reclassified effect-verified with the fresh evidence
  (the fields the machine audit's § Route classification defines) — a direction that becomes reachable
  stops being treated as dead, and its routes re-enter the resolved roster — and a recorded
  **effect-verified** direction whose probe fails is reported and reclassified unavailable with its
  captured failure class.
- **Intentionally disabled** rows are owner decisions, not audit output: a re-run confirms the install
  still exists (a version probe, no dispatch) and leaves the choice standing unless the owner lifts it in
  that run's interview — a successful probe never promotes one. A vanished install is drift to report:
  the row is reclassified unavailable with its failure class, retaining the owner's disable decision
  beside it as a note — not a second state — so a reinstall
  does not silently re-enable the route. When the install returns, the standing decision puts the row back
  to intentionally disabled without a new owner interview; the state comes from the retained decision, not
  from the probe that noticed the reinstall.
- An alias enters the playbook only from a probe result naming the CLI version that produced it. A roster
  name is never promoted to a dispatch alias by assumption, and a name no probe ran against is recorded as
  unverified, never as a route.
- Rows the audit could not verify are reported as gaps and left marked, never quietly dropped and never
  promoted to verified.
- A re-run with unchanged reachability leaves the file byte-identical. Evidence timestamps date the
  observation that established each recorded state, so a probe that merely confirms a row writes nothing.

A write that cannot be read back changes nothing: fail closed, report the gap, and do not dispatch on a
roster that was not durably written. Retain recovery bytes until the new playbook passes its probes.

## Reconciliation is a prose audit

Read the project playbook and a current machine audit; report drift or conflict in
prose. Examples: an unreachable row, a stale directional route, a probe record naming a different machine, an
alias the current CLI no longer accepts, or a pin conflict. That reading is the judgment mechanism. The
`reconcile` command only reports; applying what it finds is setup's write, under § Reconciling an existing
playbook. Provider-package effective hashes are install provenance, not roster-policy truth.

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

Where the CLI offers a resumable session id, the wrapper captures and returns it — resume-by-id is the
continuation after wrapper loss — and tees raw output to a file as it streams, so the result survives a
lost return path. A resume or adoption first audits the tree, branch tips, and live processes; reality
outranks the prior narrative. Briefs to an external-harness worker speak in goals and file paths — the
parent harness's tool idioms stay out.

Reachability state is per direction: **effect-verified**, **intentionally disabled**, or **unavailable** with
a captured failure class and successor. One failed direction never disables the healthy direction.
