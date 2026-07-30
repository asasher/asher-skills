# Relay binding

This repository consumes the `relay` skill. The portable skill owns the process and its invariants; `relay/`
owns all local projects, evidence providers, audiences, editorial policy, templates, runs, and append-only
state.

Treat only the providers in `relay/bindings.json` as authoritative. Preserve source attribution and evidence
status; never upgrade repository movement, task state, or mailbox language into a shipped, paid, committed,
or opportunity-stage claim.

Record repository-specific editorial choices and provider/source notes below without duplicating the skill's
rules or structured values from `relay/`.

## Evidence collection

Document the exact operations that constitute a complete collection from each bound provider, including
windows, pagination/truncation checks, local status meanings, authoritative-source precedence, and the private
candidate-accounting artifact expected for a run.

## Editorial projection

Document how source evidence becomes recipient-facing language for each audience, which source mechanics may
appear visibly, any local visibility model, and the unresolved evidence classes that may be rechecked and
marked for carry-forward.

## Review surface

Document repository or environment facts needed to present the annotated `serve-via-tailnet` review surface.
Keep delivery blocked when that surface cannot record an exact-hash verdict.
