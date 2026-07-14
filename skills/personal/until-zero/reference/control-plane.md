# Control-plane integration

Treat Until Zero as an optional domain owner. It owns capture refresh, canonical financial state, projection,
proposals, and reports. The `control-plane` sibling owns sequence, gates, cadence, and the final brief.

When configured, insert a Runway refresh before the morning brief. Record `complete`, `skipped`, `blocked`, or
`failed`; include captures committed/pending, expected zero status, first material driver, warnings, and the
current report path.

An unavailable Runway API, invalid state, or failed report marks only the Until Zero phase failed. Continue
independent Inbox, opportunity, and task phases under their own gates. Never present a stale runway as fresh,
and do not let a financial-domain failure silently disappear from the final brief.

Setup binds only verified project paths and cadence in consumer-owned config or `docs/agents/control-plane.md`.
Do not duplicate Until Zero's deployment, token, external capability, or smoke-test logic in the orchestrator.
