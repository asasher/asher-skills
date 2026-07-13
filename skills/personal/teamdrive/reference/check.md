# Check

Confirm the whole chain is live — tool, auth, real access — and pinpoint the broken link when it is not. Use this anytime a command fails with an auth or access error, or to verify a fresh `setup`.

The rule that shapes this check: **`gws auth status` can lie.** It reports whether a client is *configured*, not whether the token still works. A machine can show a configured client and a 33-API project yet fail every call with `invalid_grant`. So always finish on a real request.

## Steps

1. **Tool present.** `gws version` prints a version. If "command not found", `gws` is not installed (or not on PATH) → send them to `setup` step 2.

2. **Client configured.** `gws auth status` shows `auth_method: oauth2` and `client_config_exists: true`. If not → `setup` step 3.

3. **Token live (the real test).** `gws drive about get --params '{"fields":"user"}'`.
   - Returns the user's email → healthy; stop here and report green.
   - `401 invalid_grant` / `authError` → token expired or revoked. Fix: `gws auth login` (browser), then repeat.
   - `403 insufficient` / scope errors → re-auth with the needed services: `gws auth login -s drive,docs,sheets,slides`.

4. **Workspace reachable (if a Shared Drive is in use).** `gws drive drives list` includes the expected Drive, or list its files with the Shared-Drive flags: `gws drive files list --params '{"driveId":"<id>","corpora":"drive","supportsAllDrives":true,"includeItemsFromAllDrives":true,"pageSize":3}'`. Empty or "not found" usually means the account isn't a member of that Drive, not a tool fault.

Completion criterion: every step above passes, or the first failing step is named with its exact fix.
</content>
