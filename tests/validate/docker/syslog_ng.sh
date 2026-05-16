#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SYSLOG_CONFIG="$REPO_ROOT/docker/syslog-ng/syslog-ng.conf"

if [[ ! -f "$SYSLOG_CONFIG" ]]; then
  echo "::warning::$SYSLOG_CONFIG отсутствует — пропускаю валидацию" >&2
  exit 0
fi

if command -v syslog-ng >/dev/null 2>&1; then
  echo ">> syslog-ng --syntax-only -f $SYSLOG_CONFIG"
  syslog-ng --syntax-only -f "$SYSLOG_CONFIG"
elif command -v docker >/dev/null 2>&1; then
  echo ">> syslog-ng --syntax-only (через docker)"
  docker run --rm \
    --entrypoint syslog-ng \
    -v "$SYSLOG_CONFIG:/etc/syslog-ng/syslog-ng.conf:ro" \
    balabit/syslog-ng:latest \
    --syntax-only -f /etc/syslog-ng/syslog-ng.conf
else
  echo "::error::ни syslog-ng, ни docker не доступны" >&2
  exit 1
fi

echo "OK: syslog_ng.sh"
