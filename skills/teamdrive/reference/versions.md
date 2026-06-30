# Versions

Inspect a file's revision history and upload **managed versions** — new content under the same fileId, the way Drive's "Manage versions" works — rather than spawning duplicate files.

## Read history

- List revisions: `gws drive revisions list --params '{"fileId":"<id>","supportsAllDrives":true,"fields":"revisions(id,modifiedTime,lastModifyingUser,keepForever,size)"}'`.
- Get one: `gws drive revisions get --params '{"fileId":"<id>","revisionId":"<rev>"}'`.

Native Docs/Sheets/Slides accrue revisions automatically on every `edit`; the full history is also visible in the Drive web UI. `lastModifyingUser` is the signed-in human — see attribution in [edit.md](edit.md).

## Upload a managed version (blobs)

Replace a binary file's content under its existing fileId — this adds a revision, it does **not** create a sibling:

`gws drive files update --params '{"fileId":"<id>","supportsAllDrives":true,"keepRevisionForever":true}' --upload ./new-version.pdf`

- Same fileId, same shareable link — anyone with access now sees the new content, with the old revision retained.
- `keepRevisionForever: true` pins the revision so Drive's auto-pruning won't drop it.
- Contrast with the MCP connector's `create_file`, which has no fileId parameter and therefore can only fork a new file — never version in place.

## Pin or restore

- Keep a revision permanently: `gws drive revisions update --params '{"fileId":"<id>","revisionId":"<rev>"}' --json '{"keepForever":true}'`.
- "Restore" means re-uploading the desired revision's content as a new managed version (Drive has no in-place rollback API); download the old revision, then `files update` it back.

Completion criterion: history is listed, or new content is live under the original fileId with the prior revision retained.
</content>
