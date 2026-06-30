#!/usr/bin/env bash
# Render an index.html to screenshot.png next to it, using headless Chrome
# (no extra install needed on macOS). Tall window approximates a full-page shot.
#
# Usage: screenshot.sh /abs/path/to/index.html [width=1440] [height=2400]

set -euo pipefail
HTML="${1:?path to index.html required}"
W="${2:-1440}"
H="${3:-2400}"
HTML_DIR="$(cd "$(dirname "$HTML")" && pwd)"
HTML_ABS="$HTML_DIR/$(basename "$HTML")"
OUT="$HTML_DIR/screenshot.png"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[[ -x "$CHROME" ]] || CHROME="$(command -v google-chrome || command -v chromium || true)"
if [[ -z "$CHROME" || ! -x "$CHROME" ]]; then
  echo "WARN: Chrome not found; skipping screenshot for $HTML" >&2
  exit 0
fi

"$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
  --force-device-scale-factor=1 --window-size="${W},${H}" \
  --screenshot="$OUT" "file://$HTML_ABS" >/dev/null 2>&1 || {
    echo "WARN: screenshot failed for $HTML" >&2; exit 0; }
echo "   shot -> $OUT"
