# Setup

Reconcile a consumer-owned communications instance without overwriting its policy or state.

## Materialize

1. Run `python3 scripts/setup_instance.py <workspace-root>`. It creates missing files from
   `templates/instance/`, initializes append-only state, and creates `docs/agents/communications.md` only
   when absent. Existing consumer files are preserved; changed package defaults are emitted as setup
   candidates.
2. Resolve `<workspace-root>/.env`; require Git to ignore it and mode `0600`. Parse it as dotenv data and
   read only `AGENTMAIL_API_KEY`. Preserve every other assignment. Never source it as shell code.
3. Complete `policy.json`, `capabilities.json`, audience files, and interest files with verified local
   facts. When a project–customer relationship needs human-readable preferences, create one Markdown profile
   in the consumer instance, link it from both entity records, and bind its SHA-256 into the audience and
   interest manifests. Keep names, addresses, project paths, provider IDs, and cadence choices out of the
   skill source.
4. Reconcile `docs/agents/communications.md` manually. Preserve project-owned policy and deliberate
   substitutions; never overwrite it wholesale.

## Validate capabilities

1. Run `python3 scripts/validate_instance.py <workspace-root> --require-token --check-cli`. Do not print the
   token. Confirm AgentMail CLI `>= 0.7.12`, a dedicated inbox, one reviewer, and a reviewer-only allowlist.
   Use `scripts/provision_agentmail_key.py <workspace-root> --execute` once to replace the setup credential
   with an inbox-scoped runtime key limited to draft read/create/send permissions.
2. Create one synthetic bag and render HTML plus text locally.
3. With explicit approval for the loopback test, use `scripts/agentmail_handoff.py` to deliver the fixture
   only to the reviewer. Use the Outlook connector to locate it and create a forward draft back to the
   reviewer. Do not send that draft.
4. Record non-secret provider IDs and capability status in setup state. If either provider is unavailable,
   mark it blocked and keep the skill in dry-run mode.

Completion criterion: the instance validates; the credential stays only in the shared root `.env`; both
provider capabilities are either effect-verified or explicitly blocked; and no stakeholder message was
sent.
