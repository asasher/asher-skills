# Manage Communications

Builds planned client updates and internal digests from workspace evidence, renders rich review artifacts,
hands them to the configured reviewer, and reconciles durable sent history. The portable source contains no
client policy or credentials; setup materializes those in the consuming workspace.

`SKILL.md` is the command surface. Detailed contracts live under `reference/`; consumer scaffolding lives
under `templates/`; deterministic setup, validation, and reviewer-only AgentMail behavior live under
`scripts/`.
