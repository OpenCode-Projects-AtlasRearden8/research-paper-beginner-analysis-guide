#!/usr/bin/env bash
# Build the static HTML site from docs/ and verify it end to end.
# Usage: ./build.sh            (build + verify; verification runs every time)
#        ./build.sh --quick    (build only, skip verification)

set -euo pipefail
cd "$(dirname "$0")"

echo "==> Building site (pandoc -> site/)"
python3 tools/build.py

if [[ "${1:-}" == "--quick" ]]; then
  echo "==> Quick build: skipping verification"
  exit 0
fi

echo "==> Verifying built site"
python3 tools/check_site.py
