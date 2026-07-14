# Selection and disclosure

## Preference ownership

Put person-wide facts in People records, organization-wide preferences in Customer or Company records, and
project-wide narrative rules in the Project record. Put preferences specific to one project–customer
relationship in one consumer-owned audience profile linked from both records. Treat audience and interest
JSON as operational manifests; when they name a profile, require their `profile_sha256` values to match the
current profile before selection.

## Evidence status

- `production_verified` — observed in the production-facing system or confirmed by its authoritative owner.
- `shipped_unverified` — merged or released, but production behavior is not verified.
- `in_progress` — active work with evidence of current movement.
- `pending` — a known obligation, blocker, decision, or dependency.
- `planned` — intended work without an active delivery claim.

Only `production_verified` may be phrased externally as shipped or live. Describe `shipped_unverified` as
released pending verification, and never promote `in_progress` or `planned` into a commitment.

## External project updates

Include a fact only when all are true:

1. It belongs to the audience's project and an enabled feature in its current profile-bound interest file.
2. Its disclosure level permits external use.
3. It is material to client-visible behavior, delivery confidence, a required decision, or a stated next
   step.
4. The wording is supported by evidence and does not expose another client, private commercial state, or
   internal speculation.

An external bag includes the client contacts plus the configured internal stakeholders in Outlook `To`.
If no fact passes, produce an explicit no-update result; do not manufacture a message.

## Internal digest

Build four lenses:

- **Delivery:** verified movement across current projects.
- **Pending:** blockers, decisions, obligations, and owner-specific next actions.
- **Cash:** invoices and payments only from the configured commercial owner or authoritative record.
- **Growth:** opportunities and next actions from `manage-opportunities`; never infer stage movement.

Internal inclusion is broader than client inclusion, but still evidence-backed. Label uncertainty and name
the missing owner rather than filling gaps.
