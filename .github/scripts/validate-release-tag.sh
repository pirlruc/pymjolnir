#!/usr/bin/env bash
set -euo pipefail

if [[ "${RELEASE_TAG:-}" =~ ^v[0-9]+[.][0-9]+[.][0-9]+$ ]]; then
  exit 0
fi

echo "Tag must match the release pattern vX.Y.Z (received: ${RELEASE_TAG:-})" >&2
exit 1
