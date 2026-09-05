# to-web

Uploads files to the project's artifact store (S3-compatible; R2 as the reference binding) and returns durable, hash-keyed, unguessable public URLs. Evidence media's permanent home, and the render path for HTML artifacts whose sources live on `artifact/<issue>` branches. URLs are embedded where the files are presented, outside this skill.

Reads the store binding from `docs/agents/environment.md` § Artifact store.
