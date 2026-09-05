---
name: to-web
description: Upload HTML and evidence media to the repository’s artifact bucket and return verified permanent URLs.
---

# To web

Read `docs/agents/environment.md` § Artifact store: bucket, public URL, credential variable names, and S3-compatible upload command. Resolve credentials from the environment. Missing binding or access is a blocker; evidence media is never committed as a fallback.

Upload with an immutable key: `<repo>/<ticket-or-slug>/<commit-or-content-hash>-<random>/<filename>`. Use a long random segment; changed content gets a new key. Anyone with a public URL can read it. Surface sensitive content before upload and obtain the user's authorization for that exposure.

Fetch every returned URL. Require HTTP 200 and content matching the upload by size or hash; command success alone is insufficient.

Return the files' URLs, keys, and source revisions. Specs and research remain available as published HTML after their temporary artifact branches are deleted. Screenshots, MP4s, and GIFs live in the bucket, never the repository. Presentation and embedding belong to the record that uses the URLs.
