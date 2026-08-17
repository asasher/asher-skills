# to-web

Uploads files to the project's bound store (S3-generic; R2 as the reference binding) and returns durable, hash-keyed, unguessable public URLs. Evidence media's permanent home, and the preview-deploy path for HTML artifacts whose sources live on `artifact/*` branches. URLs are embedded where the files are presented — outside this skill. The `to-tailnet` sibling is the deliberate don't-publish alternative.

Reads the store binding from `docs/agents/platform.md`.
