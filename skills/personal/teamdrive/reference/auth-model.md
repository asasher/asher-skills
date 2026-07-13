# Auth & access model

Background for why `teamdrive` is safe to hand to a team. Load when a command points here or the user asks how access, scope, or sharing works.

## Authentication: as the user, no secrets to pass around

`gws auth login` runs an OAuth flow in the browser and the agent acts **as the signed-in human**. The refresh token is encrypted (AES-256-GCM) in the OS keyring — there is no `credentials.json` to email, no service-account key to rotate. Each teammate runs the login once on their own machine.

`gws auth setup` provisions the Google Cloud side (project + enabled APIs + OAuth client) so the user never hand-creates an OAuth client. It needs the gcloud CLI.

## Access: exactly the user's own, never more

The Google Cloud project is **only** for quota and billing — it grants **zero** data access. What a call can touch is decided by two things, neither of them the project:

1. **Whose token** — the signed-in user's. Their token only ever reaches files they can already open. It cannot see a teammate's private files, or a Shared Drive they aren't a member of. Google enforces every ACL server-side.
2. **The OAuth scope** — how much of *that user's own* access the tool may use. Full `drive` scope = any file the user can reach; `drive.file` = only files the tool created. A shared team workspace generally needs full `drive` so agents can operate on pre-existing files.

So a shared GCP project does **not** pool access across teammates, and "the agent can see everything" cannot happen. "Users get only the access they already have" is the default, automatically.

**If you want agents walled *below* the user's own access** (only the workspace, nothing else), scope is the wrong lever — identity is. Have agents act as a dedicated identity (e.g. a service account) that is a member of *only* the workspace Shared Drive. That is true hard isolation, at the cost of one workspace-scoped key. Most teams don't need this.

## Shared Drive, not a My-Drive folder

For a team workspace prefer a **Shared Drive**: files are owned by the org (they survive offboarding and don't count against one person's storage), and membership is managed in one place. The tradeoff is mechanical — every `gws drive` call must carry `supportsAllDrives: true`, and listing/searching also needs `includeItemsFromAllDrives: true` with `corpora: "drive"` and the `driveId`. Omitting these is the #1 cause of spurious "file not found".

## Honest caveats

- `gws` is community-published by Google's Workspace team and **pre-1.0** ("not an officially supported Google product") — expect breaking changes; pin a version for anything load-bearing.
- Full `drive` scope means any local process that can read the keyring entry has the user's full Drive access. That is the price of the zero-secrets convenience.
- Scope is service-level (`-s drive,sheets`), not folder-level. Narrowing an agent to one folder/Drive is an identity/membership job, not a flag.
</content>
