Every skill ships `agents/openai.yaml` (valid YAML naming the skill's interface, with `allow_implicit_invocation` set to match how the skill should trigger — `false` exactly where `disable-model-invocation: true` is set).

Skill's frontmatter carries no defaults. A key restating harness default behavior (`user-invocable: true`, an empty `requires`/`optional` list) is dropped; `metadata` holds only what something consumes — `requires`/`optional` (the dependency record), `setup`.

Invocation intent lives in the two records harnesses obey i.e `disable-model-invocation` and the sidecar's `allow_implicit_invocation`.
