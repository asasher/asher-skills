# Environment

## Artifact store

Setup status: the bucket and public URL are verified. S3 credential creation is pending Cloudflare two-factor verification in Chrome. The credential file below does not exist yet; the S3 upload command requires that remaining setup step.

- Provider: Cloudflare R2, account `Asher` (`cc77396354ce97fb64d9f973628567db`).
- Bucket: `asher-skills-artifacts`.
- Public base URL: `https://pub-6d5eb34d234d4f3cad4464870d8d0482.r2.dev`.
- S3 endpoint: `https://cc77396354ce97fb64d9f973628567db.r2.cloudflarestorage.com`. Region: `auto`.
- Credentials: `R2_ACCESS_KEY_ID` and `R2_SECRET_ACCESS_KEY`, loaded from `${XDG_CONFIG_HOME:-$HOME/.config}/asher-skills/to-web.env`.
- Planned token: `asher-skills-to-web`, with Object Read & Write access restricted to this bucket.

The credential file is machine-local, outside Git, and readable only by its owner (`chmod 600`). Load it in each upload shell. Other machines need their own credentials at the same configuration path.

Run from the repository root with Python 3 and the AWS CLI installed. Set `artifact_file` to the file and `artifact_slug` to its ticket or descriptive slug. Choose the matching MIME type.

```bash
set -e
source "${XDG_CONFIG_HOME:-$HOME/.config}/asher-skills/to-web.env"

artifact_file=/absolute/path/to/artifact.html
artifact_slug=ticket-or-slug
artifact_content_type='text/html; charset=utf-8'

artifact_hash=$(shasum -a 256 "$artifact_file" | awk '{print $1}')
artifact_uuid=$(python3 skills/software-development/to-web/scripts/generate-uuid.py)
artifact_key="asher-skills/$artifact_slug/$artifact_hash-$artifact_uuid/$(basename "$artifact_file")"
artifact_url="https://pub-6d5eb34d234d4f3cad4464870d8d0482.r2.dev/$artifact_key"

AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" \
AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" \
AWS_DEFAULT_REGION=auto \
aws --endpoint-url https://cc77396354ce97fb64d9f973628567db.r2.cloudflarestorage.com \
  s3 cp "$artifact_file" "s3://asher-skills-artifacts/$artifact_key" \
  --content-type "$artifact_content_type" \
  --cache-control 'public, max-age=31536000, immutable' \
  --only-show-errors

artifact_download=$(mktemp)
artifact_status=$(curl --silent --show-error --output "$artifact_download" \
  --write-out '%{http_code}' "$artifact_url")
test "$artifact_status" = 200 && cmp "$artifact_file" "$artifact_download"
rm "$artifact_download"
```

Stop on any failed command. Return the URL only after HTTP 200 and a byte-for-byte match. Record the key and source revision with the URL. Generate a fresh UUID for each upload, including retries that use a new key. Use URL-safe filenames and slugs.

Anyone with an artifact URL can read its contents. The `r2.dev` endpoint is rate-limited; use a custom domain if traffic exceeds its limits.
