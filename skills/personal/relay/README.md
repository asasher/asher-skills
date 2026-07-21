# Relay

Builds attributable project updates and internal digests, binds their exact content and recipients to a
`serve-via-tailnet` verdict, then uses one deterministic AgentMail draft for direct delivery. Setup materializes
consumer-owned policy, bindings, templates, runs, and append-only lifecycle state only under `relay/` at the
consumer repository root, with `docs/agents/relay.md` as the project playbook.

The portable source contains no project identities, real addresses, credentials, or previous-instance
migration behavior. Its scripts are dry-run or fixture-driven unless an operator deliberately supplies the
live execution flag after exact approval.
