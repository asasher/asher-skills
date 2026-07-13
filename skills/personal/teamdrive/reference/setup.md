# Setup

Walk the user from nothing to a working `gws` they can use on the team workspace. Assume they may not know what a CLI is — explain each step in plain language *before* running it, and get agreement before installing anything or opening a login. Run once per machine; re-run any step that a `check` later finds broken.

Open by telling them, in two sentences, what this does: it installs a small command-line tool that lets the agent work directly with their Google Docs, Sheets, and Drive, then logs them in through their browser. The only thing stored is an encrypted login on their own machine — no passwords shared, no keys to pass around.

## Steps

1. **Confirm prerequisites.**
   - `gws` is an npm package, so it needs Node.js: check `node -v` and `npm -v`.
   - `gws auth setup` provisions the Google Cloud side for them, which needs the gcloud CLI: check `gcloud --version`.
   - If either is missing, explain what it is and offer to help install it (Node from nodejs.org or a version manager; gcloud from the Cloud SDK installer, then `gcloud auth login`). Do not proceed past a missing prerequisite.
   - Completion criterion: `node`, `npm`, and `gcloud` all report a version.

2. **Install `gws` (after explicit permission).**
   - Tell them you're about to install the Google Workspace CLI globally, and show the command: `npm install -g @googleworkspace/cli`.
   - **Never** suggest `brew install gws` — that is an unrelated git tool, not this one.
   - If it is already installed (`gws version` prints), offer to upgrade with `npm install -g @googleworkspace/cli@latest`, since older versions lag features and fixes.
   - Verify: `gws version` prints a version and the "not an officially supported Google product" notice (expected — it is community-published by Google's Workspace team, pre-1.0).
   - Completion criterion: `gws version` runs and prints a version.

3. **Authenticate and provision the project (interactive — the user runs this).**
   - Explain what `gws auth setup --login` does, in order: it selects or creates a Google Cloud project, switches on the Workspace APIs the tool needs, then opens the browser to log them in as themselves.
   - If the team already has a shared GCP project, pass it: `gws auth setup --project <project-id> --login`. Otherwise it makes one for them.
   - This step opens a browser and waits, so the user runs it themselves — suggest they type `!gws auth setup --login` so its output lands in the session.
   - At the Google consent screen they approve access. On a Google Workspace org with an Internal app there is no "unverified app" warning; on a personal account that warning is expected — they continue past it.
   - Reassure on two points they may worry about: credentials are encrypted in their OS keyring (nothing to email around), and the tool can only ever touch what their own account already can — it cannot see teammates' private files or Drives they aren't a member of. Background: [auth-model.md](auth-model.md).
   - Completion criterion: the command finishes and `gws auth status` reports `auth_method: oauth2` with a client configured.

4. **Prove it works with a real call.**
   - `gws auth status` only shows that a client is *configured* — the cached token can still be dead. Confirm with an actual request: `gws drive about get --params '{"fields":"user"}'`.
   - Success looks like a JSON block naming their account email. Show it to them — that is the "it works on my machine" moment.
   - If it returns `401 invalid_grant`, the token is expired or revoked: have them re-run `gws auth login` (browser), then repeat the call.
   - Completion criterion: the call returns the user's account, not an error.

5. **Point at the team workspace (optional).**
   - List the Shared Drives they can reach: `gws drive drives list`.
   - If the team has a workspace Shared Drive, note its `id` — every later `edit`/`read`/`versions` call scopes to it. If there is no Shared Drive yet, note that a My-Drive folder also works but a Shared Drive is the better team home (see [auth-model.md](auth-model.md)).
   - Completion criterion: the user has the workspace `driveId` recorded, or has chosen to skip.

6. **Confirm readiness.**
   - Recap: `gws` installed, authenticated as <their email>, live call succeeded, workspace target known.
   - Tell them what they can do next — `check` anytime to re-verify, `edit`/`read`/`versions` to work on files.
   - Completion criterion: the user can run a `teamdrive` command knowing it is wired up.
</content>
