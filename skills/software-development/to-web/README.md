# to-web

Uploads files to the project's bound web store (S3-generic; R2 as the reference binding) and returns durable, hash-keyed, unguessable public URLs. Evidence media's permanent home — media never lands in git — and the preview-deploy path for HTML artifacts whose sources live on `artifact/*` branches. Embedding the URLs stays with the caller. The `to-tailnet` sibling is the deliberate don't-publish alternative.

Reads the store binding from `docs/agents/platform.md`.
