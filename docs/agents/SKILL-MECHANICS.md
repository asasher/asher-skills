Every skill ships `agents/openai.yaml` (valid YAML naming the skill's interface, with `allow_implicit_invocation` set to match how the skill should trigger — `false` exactly where `disable-model-invocation: true` is set).

Skill's frontmatter carries no defaults. A key restating harness default behavior (`user-invocable: true`, an empty `requires`/`optional` list) is dropped; `metadata` holds only what something consumes — `requires`/`optional` (the dependency record), `setup`.

Invocation intent lives in the two records harnesses obey i.e `disable-model-invocation` and the sidecar's `allow_implicit_invocation`.

Compose sibling skills by name and declare the dependency; each skill owns access to its supporting files. Runtime instructions and helpers must not reach into another skill's package by path. Source links in authoring review documents and provenance records serve inspection, not runtime composition.
