# Communications instance

Consumer-owned relationship profiles, operational audience maps, rich-email templates, and delivery state for
`manage-communications`. Installed skill refreshes must preserve this directory.

Use `profiles/` for human-readable project–customer preferences. When a profile is authoritative, record its
path and SHA-256 in both the audience and interest manifests; validation rejects stale bindings.

Use `npm run render -- --bag <bag.json> --out <run-directory>` to render a validated comms bag. Provider
handoff remains a separate reviewed step.
