# Cadence

- **Morning:** the no-argument sequence. Schedule only with explicit consent and a recorded timezone.
- **Event-driven:** `capture-to-inbox` drains, `until-zero` refreshes, and `manage-opportunities` mutations may
  run when their events occur; they keep their own idempotency and evidence gates.
- **Weekly or explicit:** `review-opportunities` performs the full commercial portfolio audit.
- **Explicit or separately cadenced:** `projects-triage` may dispatch broader repository work and never joins
  the default morning sequence implicitly.

Record cadence, timezone, enabled intake sources, and last effect-verified result in consumer configuration or
the project playbook. A scheduled failure must remain visible for the next run; never advance a success marker
for a phase that did not complete.
