#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AM_CONFIG="$REPO_ROOT/docker/alertmanager/alertmanager.yml"

if [[ ! -f "$AM_CONFIG" ]]; then
  echo "::warning::$AM_CONFIG отсутствует — пропускаю валидацию" >&2
  exit 0
fi

if command -v amtool >/dev/null 2>&1; then
  echo ">> amtool check-config $AM_CONFIG"
  amtool check-config "$AM_CONFIG"
elif command -v docker >/dev/null 2>&1; then
  echo ">> amtool check-config $AM_CONFIG (через docker)"
  docker run --rm \
    --entrypoint amtool \
    -v "$AM_CONFIG:/cfg/alertmanager.yml:ro" \
    prom/alertmanager:latest \
    check-config /cfg/alertmanager.yml
else
  echo "::error::ни amtool, ни docker не доступны" >&2
  exit 1
fi

echo "OK: alertmanager.sh"
