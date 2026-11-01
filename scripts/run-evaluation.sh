#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ ! -f .env ]]; then
  echo "Missing .env. Copy .env.example to .env and configure a supported provider credential." >&2
  exit 2
fi
make evaluate
