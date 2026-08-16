# Verify Your Work

The verification discipline for freshly built changes: establish the claims (explicit and implicit), pick the proof that would catch each one failing, run it, capture command and output, and report findings — verified / failed-with-evidence / not-verified-with-reason. The spec declares which checks are durable suite tests and which are throwaway scaffolding scripts — a shaping decision the verifier executes, never makes. The verifier never fixes; the fix belongs to whoever owns the changes.

## When to use

- Changes exist and need checking before a change request is created — typically run by a fresh pair of eyes so the builder's assumptions don't verify themselves.

## Dependency surface

Composes with the optional `to-web` and `writing-for-humans` siblings; reads `docs/agents/environment.md` when present.

## Provenance

No external sources.
