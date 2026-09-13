# Direct OpenAI API: explicit permission

Use this last-resort backend when configured gateway/native generation is unavailable and the user explicitly permits direct OpenAI API use. The bundled client uses an existing OpenAI Platform key:

```bash
python3 <skill-dir>/scripts/codex_imagegen.py \
  --backend openai --allow-direct-api --api-key-env OPENAI_PLATFORM_KEY \
  --subject "SUBJECT" --out assets/raw/name.png
```

The default key variable is `OPENAI_API_KEY`. When that variable belongs to a configured gateway, choose a distinct Platform-key variable with `--api-key-env`. A gateway bearer key and ChatGPT OAuth token cannot substitute for a Platform key. Setting a key alone does not authorize this route; `--allow-direct-api` records the user's explicit permission for the run.

The endpoint is fixed to `https://api.openai.com/v1`; proxy URL settings cannot redirect this backend. It uses the shipped stdlib client and the same immutable artifact pipeline. Size and quality are requests: inspect decoded dimensions and visual results as described in [backend configuration](backends.md). Failure stops the request without a provider switch or automatic retry.
