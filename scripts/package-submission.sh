#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p dist
archive="dist/beyond-the-happy-path-draft.zip"
rm -f "$archive"
zip -qr "$archive" . \
  -x '.git/*' \
  -x '.env' \
  -x '.venv/*' \
  -x '*/__pycache__/*' \
  -x '*.pyc' \
  -x '*.class' \
  -x 'dist/*'

size=$(stat -c '%s' "$archive")
limit=$((50 * 1024 * 1024))
if (( size > limit )); then
  echo "Archive is ${size} bytes; maximum allowed is ${limit} bytes." >&2
  exit 1
fi

if zipinfo -1 "$archive" | grep -Eq '(^|/)\.env$|(^|/)\.git/|\.class$|\.pyc$'; then
  echo "Archive contains a prohibited secret or build artifact." >&2
  exit 1
fi

echo "Created ${archive} ($(du -h "$archive" | cut -f1))."
