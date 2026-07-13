# Edit

Change a Doc, Sheet, or Slides **in place** — same fileId, a real revision added to its history — not a duplicate sibling file. This is the capability the Drive MCP connector lacks and `gws` provides.

Resolve the fileId first (from the URL or `read`/search). For any Shared Drive file, every `drive` call here carries `supportsAllDrives: true`.

## By type

- **Sheet** — `gws sheets spreadsheets values update --params '{"spreadsheetId":"<id>","range":"Sheet1!A2","valueInputOption":"USER_ENTERED"}' --json '{"values":[["beta","agent-A","done","250"]]}'`. Range-scoped, so independent ranges rarely collide. For structural changes (add rows/sheets, formatting) use `sheets spreadsheets batchUpdate`.
- **Slides** — `gws slides presentations batchUpdate --params '{"presentationId":"<id>"}' --json '{"requests":[ ... ]}'`. Build requests like `insertText`, `createSlide`, `replaceAllText`.
- **Doc** — `gws docs documents batchUpdate --params '{"documentId":"<id>"}' --json '{"requests":[ ... ],"writeControl":{"requiredRevisionId":"<rev>"}}'`. Docs edits are **index-based**, so they need concurrency control (below).

## Concurrency: match the policy to the file type

Two agents can act at once. Pick the protection the API actually offers:

- **Docs — optimistic, required.** Read first: `gws docs documents get --params '{"documentId":"<id>"}'` returns a `revisionId`. Pass it as `writeControl.requiredRevisionId` in the batchUpdate. If another agent wrote in between, the call **fails instead of clobbering** — re-read, re-aim the indices against the new content, retry. Never fire a Docs batchUpdate without this on a shared file: insert/delete shift every later index, so a stale edit lands in the wrong place.
- **Sheets — scope to avoid the clash.** Write disjoint ranges; `values update` is atomic per call. Only serialize when two agents truly need the same cells.
- **Binary files (PDF/PNG/Markdown) — whole-file, last-writer-wins.** No partial edit exists; coordinate at the file level and keep history via `versions` (`keepRevisionForever`).

## Attribution

Edits are attributed to the **signed-in human**, not the agent — revision history shows *who*, never *which agent*. When per-agent attribution matters, stamp a marker the agents own: a trailing cell/paragraph like `last edit: agent-A @ rev N`, or a sidecar manifest file in the workspace. The native history (`versions`) still gives you *when* and *what*.

Completion criterion: the target file's content reflects the edit under its original fileId, and (for Docs on a shared file) the write used `requiredRevisionId`.
</content>
