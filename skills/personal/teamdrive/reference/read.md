# Read

Get a file's content or find files in the workspace. Native types (Doc/Sheet/Slides) are read structurally or exported; blobs (PDF/PNG/Markdown) are downloaded.

## Find

- List a Shared Drive's files (note the flags — without them you get "not found"): `gws drive files list --params '{"driveId":"<id>","corpora":"drive","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType,modifiedTime)"}'`.
- Search by name/type: add `"q":"name contains 'budget' and mimeType='application/vnd.google-apps.spreadsheet'"`.

## Read content

- **Sheet** — `gws sheets spreadsheets values get --params '{"spreadsheetId":"<id>","range":"Sheet1"}'`.
- **Doc** — `gws docs documents get --params '{"documentId":"<id>"}'` returns the structural JSON (and the current `revisionId`, which `edit` needs). To get plain text/markdown instead, export it (next bullet).
- **Slides** — `gws slides presentations get --params '{"presentationId":"<id>"}'`.
- **Export a native file** to a portable format: `gws drive files export --params '{"fileId":"<id>","mimeType":"text/markdown"}' --output ./doc.md` (or `application/pdf`, `text/csv`, etc.).
- **Download a blob** (PDF/PNG/Markdown stored as-is): `gws drive files get --params '{"fileId":"<id>","alt":"media","supportsAllDrives":true}' --output ./file.pdf`.

Completion criterion: the requested content is returned or written to the output path.
</content>
