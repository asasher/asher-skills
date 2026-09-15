---
name: to-web
description: Upload HTML and evidence media to the repository’s artifact bucket and return verified permanent URLs.
---

# To web

Read `docs/agents/environment.md` § Artifact store: bucket, public URL, credential variable names, and S3-compatible upload command. Resolve credentials from the environment. Missing binding or access is a blocker.

Run `python3 <skill-dir>/scripts/generate-uuid.py` for each new upload key, resolving `<skill-dir>` to this skill's directory. The script generates a UUID4 using operating-system randomness. Use its full stdout value unchanged as `<uuid4>`; never invent the value yourself. If the script cannot run, UUID generation is a blocker.

Upload with an immutable key: `<repo>/<ticket-or-slug>/<commit-or-content-hash>-<uuid4>/<filename>`. Changed content gets a new key with a fresh script-generated UUID4. Anyone with a public URL can read it.

Fetch every returned URL. Require HTTP 200 and content matching the upload by size or hash.

Return the files' URLs, keys, and source revisions. Specs and research remain available as published HTML after their temporary artifact branches are deleted. Screenshots, MP4s, and GIFs live in the bucket, never the repository. Presentation and embedding belong to the record that uses the URLs.
