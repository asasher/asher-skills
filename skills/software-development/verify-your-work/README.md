# Verify Your Work

The verification discipline for freshly built changes: establish the claims (explicit and implicit),
pick the proof that would catch each one failing, run it, capture command and output, and report
findings — verified / failed-with-evidence / not-verified-with-reason. The verifier never fixes; the fix
belongs to whoever owns the changes.

## When to use

- Changes exist and need checking before a change request is created — typically run by a fresh pair of
  eyes so the builder's assumptions don't verify themselves.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Project:** `docs/agents/environment.md` when present — run/seed/auth and the recorded browser
  driver per surface.
- **Siblings:** none — a sealed primitive.

## Provenance

No external sources.
