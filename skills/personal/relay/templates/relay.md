# Relay binding

This repository consumes the `relay` skill. The portable skill owns the process and its invariants; `relay/`
owns all local projects, evidence providers, audiences, editorial policy, templates, runs, and append-only
state.

Treat only the providers in `relay/bindings.json` as authoritative. Preserve source attribution and evidence
status; never upgrade repository movement, task state, or mailbox language into a shipped, paid, committed,
or opportunity-stage claim.

Record repository-specific editorial choices and provider/source notes below without duplicating the skill's
rules or structured values from `relay/`.
