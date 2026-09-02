# Verify Your Work

The verification discipline for freshly built changes and for merged work checked against its spec: establish the claims (explicit and implicit, including that the seed reaches a new feature), pick the proof that would catch each one failing, run it, capture command and output, and report a per-claim verdict with evidence. Checks are guards (durable, in the suite) or throwaway verification scripts (dropped, their run kept as evidence); the spec or the builder declares which. The verifier never fixes; the fix belongs to whoever owns the changes.

## When to use

- Changes exist and need checking before a PR is created, run by a fresh pair of eyes so the builder's assumptions do not verify themselves.
- A spec issue's children have all merged and the whole needs checking against the spec.

## Dependency surface

Composes with the optional `to-web` and `technical-writing` siblings; reads `docs/agents/environment.md` when present.

## Provenance

No external sources.
