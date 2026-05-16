#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DOCKER_DIR="$REPO_ROOT/docker"
COMPOSE_FILE="$DOCKER_DIR/compose.yaml"

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "::error::$COMPOSE_FILE отсутствует" >&2
  exit 1
fi

ENV_FILE="$(mktemp -t compose-validate-XXXXXX.env)"
trap 'rm -f "$ENV_FILE"' EXIT
cat >"$ENV_FILE" <<'ENV'
POSTGRES_DB=lint_db
POSTGRES_USER=lint_user
POSTGRES_PASSWORD=lint_pass
GUACAMOLE_VERSION=1.5.5
GUACAMOLE_PORT=8080
CODE_SERVER_PASSWORD=lint_pass
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin
ENV

echo ">> docker compose config --quiet"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" config --quiet

echo ">> сверяем список сервисов"
EXPECTED=(
  postgres
  guacd
  guacamole
  portainer
  code-server
  prometheus
  grafana
  node-exporter
  cadvisor
  syslog-ng
  alertmanager
)

mapfile -t ACTUAL < <(
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" config --services | sort
)

missing=()
for svc in "${EXPECTED[@]}"; do
  if ! printf '%s\n' "${ACTUAL[@]}" | grep -qx "$svc"; then
    missing+=("$svc")
  fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "::error::compose не отдал ожидаемые сервисы: ${missing[*]}" >&2
  echo "actual: ${ACTUAL[*]}" >&2
  exit 1
fi

echo "OK: compose.sh (services=${#ACTUAL[@]})"
