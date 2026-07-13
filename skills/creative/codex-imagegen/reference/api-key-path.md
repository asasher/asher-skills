# Fallback: the CLI path (needs a key)

Codex's system skill also has `~/.codex/skills/.system/imagegen/scripts/image_gen.py` (subcommands `generate` / `edit` / `generate-batch`, gpt-image-2 / gpt-image-1.5 with true `--background transparent`). It is fully scriptable and deterministic but **hard-requires `OPENAI_API_KEY`** and will not use the ChatGPT OAuth token. Use it only when a key is available and the user asks for the CLI/API path; otherwise the built-in `image_gen` flow in [../SKILL.md](../SKILL.md) is the no-cost route.
