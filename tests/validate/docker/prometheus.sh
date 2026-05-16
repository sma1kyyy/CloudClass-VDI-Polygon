#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PROM_CONFIG="$REPO_ROOT/docker/prometheus/prometheus.yaml"
PROM_ALERTS="$REPO_ROOT/docker/prometheus/alerts.yml"

run_promtool() {
  local host_file="$1"; shift
  local container_path="$1"; shift
  if command -v promtool >/dev/null 2>&1; then
    promtool "$@" "$host_file"
  elif command -v docker >/dev/null 2>&1; then
    docker run --rm \
      --entrypoint promtool \
      -v "$host_file:$container_path:ro" \
      prom/prometheus:latest \
      "$@" "$container_path"
  else
    echo "::error::ни promtool, ни docker не доступны" >&2
    return 1
  fi
}

if [[ -f "$PROM_CONFIG" ]]; then
  echo ">> promtool check config $PROM_CONFIG"
  run_promtool "$PROM_CONFIG" /cfg/prometheus.yaml check config
else
  echo "::warning::$PROM_CONFIG отсутствует — пропускаю check config" >&2
fi

if [[ -f "$PROM_ALERTS" ]]; then
  echo ">> promtool check rules $PROM_ALERTS"
  run_promtool "$PROM_ALERTS" /cfg/alerts.yml check rules
else
  echo "::warning::$PROM_ALERTS отсутствует — пропускаю check rules" >&2
fi

echo "OK: prometheus.sh"
