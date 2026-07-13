# Triage Protocol

## Select targets

1. Enumerate Project known-home markdown notes directly under the workspace's `Projects/` directory. Ignore
   working-document subdirectories and every path under `Opportunities/`.
2. Parse frontmatter and select only notes with a non-empty absolute `localPath`.
3. De-duplicate identical `localPath` values and report conflicting Project ownership instead of dispatching
   that path twice.
4. Do not inspect or use `workspacePath`, even if it appears in a Project note. It is not the Project triage
   contract.

## Dispatch

For each selected `localPath`:

1. Confirm the directory resolves.
2. Look for the repository's installed `backlog` skill through its primary or alias installed skill mount.
3. If found, dispatch one isolated worker rooted at that `localPath` and instruct it to run the local skill as
   written. Independent Projects may run in parallel; never combine Projects in one worker.
4. If absent, skip and name the missing local skill. If the directory or dispatch fails, capture the error.

Use the current harness's native isolated worker or thread mechanism. If none exists, run Projects sequentially
with a fresh context rooted at each `localPath`; do not emulate isolation with an unattended background shell.

## Report

Return one row per eligible Project with note, `localPath`, status (`run`, `skipped`, `failed`), and concise
result/error. Add a selection note confirming that Opportunity `workspacePath` records were not candidates.

Completion criterion: every selected Project has exactly one terminal status and no Opportunity path was
dispatched.
