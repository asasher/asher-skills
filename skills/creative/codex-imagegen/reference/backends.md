# Execution backends

The bundled generator and spritesheet CLI accept the same backend options. `--backend auto` resolves once, before the first request:

1. **CLIProxyAPI** when a gateway is configured explicitly, through the environment, or as the active Codex provider.
2. **Native Codex** otherwise, when the CLI is available. The current session must expose its native image tool; CLI presence alone cannot prove that capability.
3. **Direct OpenAI API** only when native is unavailable, a Platform key exists, and the user explicitly authorized `--allow-direct-api`. See [direct API permission](api-key-path.md).

Use `--backend cliproxyapi|native|openai` to select explicitly when the session's capabilities are already known. Failures stop execution. Check provider/session status before authorizing another attempt after a timeout or interrupted response; generation may already have completed. The scripts perform one request per image and neither retry nor switch providers after failure.

## CLIProxyAPI

`--proxy-url` names the existing Images API base URL, normally ending in `/v1`. Configuration precedence is:

- `--proxy-url`, then `CLIPROXYAPI_BASE_URL`;
- `OPENAI_BASE_URL`;
- the active `model_provider`'s `base_url` in Codex `config.toml`.

`--codex-home` selects a configured home, including a T3 shadow home. Otherwise use `CODEX_HOME` or `~/.codex`. TOML discovery requires Python 3.11+; explicit URL and environment-key options work on older supported Python versions. An explicitly selected native backend skips gateway discovery.

Choose the existing gateway bearer key through `--proxy-key-env VARIABLE` or `--proxy-auth-file FILE`. The latter reads the JSON `OPENAI_API_KEY` field. Automatic keys stay bound to their configured API base URL: the `CLIPROXYAPI_BASE_URL` key pair (`CLIPROXYAPI_KEY_ENV` or `CLIPROXYAPI_API_KEY`), the `OPENAI_BASE_URL`/`OPENAI_API_KEY` pair, then the matching active Codex provider’s `env_key` or selected home’s `auth.json`. Matching includes scheme, normalized hostname, port, and base path. For a different or unknown endpoint, select its key source explicitly with `--proxy-key-env` or `--proxy-auth-file`. A missing selected key stops execution.

A gateway bearer key authenticates to the proxy. It is distinct from ChatGPT OAuth and from a direct OpenAI Platform key. Configuration and login state are read-only. Pass secret values through the selected environment or auth file; command arguments name the source. HTTP is supported on loopback; remote gateways require HTTPS. Redirects are rejected to keep bearer credentials on the configured endpoint.

Example with an existing configured auth file:

```bash
python3 <skill-dir>/scripts/codex_imagegen.py \
  --backend cliproxyapi --proxy-url http://127.0.0.1:8317/v1 \
  --proxy-auth-file <configured-codex-home>/auth.json \
  --subject "a blue ceramic robot holding an orange flower" \
  --size 1024 --quality low --out assets/raw/robot.png
```

The stdlib HTTP client calls `/images/generations` directly and decodes `data[0].b64_json`; it bypasses native transcript extraction. Default model: `gpt-image-2`; change it explicitly with `--image-model`. `--quality` requests a quality level; reported success does not establish that the provider honored it. Error messages omit response bodies, credentials, and URLs that could expose secrets.

## Native Codex

The bundled adapter invokes the authenticated Codex CLI with its image tool, then extracts the matching image from session transcripts. Its sandbox bypass and prompt matching are empirical compatibility requirements; use the adapter for this route. Requests remain sequential because fresh-session matching is shared. `--codex-home` applies to both the subprocess and transcript lookup. The session determines its native image model; `--image-model` and `--quality` configure API backends only.

## Dimensions and evidence

Every returned image is decoded with Pillow and saved as PNG. Flat images retain the actual pixel dimensions; size mismatches are reported rather than silently cropped or resized. Record requested and actual dimensions with the artifact path, then visually inspect it. The gateway can return dimensions different from those requested.

Layered manifests record requested size, raw dimensions, mismatch, and processing policy for each layer. The existing composition policy stretches the backdrop to the planned square canvas; foreground layers retain scale while transparent padding is trimmed. Raw generations remain unchanged. Spritesheet slicing uses decoded source dimensions, and its manifest records them; validate grid geometry against that actual source.

## Validation

Run `python3 -m unittest discover -s <skill-dir>/tests -v` for local HTTP tests covering selection, credential handling, decoding, errors, dimensions, versioning, layered recovery, batching, sprites, and native extraction. A live smoke additionally records model/size requested, actual dimensions, path, and visual inspection. Local tests do not establish live service availability.
