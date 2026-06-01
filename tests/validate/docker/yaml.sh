#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DOCKER_DIR="$REPO_ROOT/docker"
YAMLLINT_CONFIG="$SCRIPT_DIR/.yamllint.yaml"

mapfile -t YAML_FILES < <(
  find "$DOCKER_DIR" -type f \( -name '*.yaml' -o -name '*.yml' \) | sort
)

if [[ ${#YAML_FILES[@]} -eq 0 ]]; then
  echo "::error::в $DOCKER_DIR нет ни одного .yaml/.yml" >&2
  exit 1
fi

echo ">> PyYAML парсит ${#YAML_FILES[@]} файлов"
python3 - "${YAML_FILES[@]}" <<'PY'
import sys
import yaml

failed = []
for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8") as f:
            list(yaml.safe_load_all(f))
    except yaml.YAMLError as e:
        failed.append((path, str(e)))

if failed:
    for path, err in failed:
        print(f"::error file={path}::PyYAML не смог распарсить: {err}", file=sys.stderr)
    sys.exit(1)
PY

echo ">> yamllint по ${#YAML_FILES[@]} файлам с конфигом $YAMLLINT_CONFIG"
yamllint -c "$YAMLLINT_CONFIG" -f auto "${YAML_FILES[@]}"

echo "OK: yaml.sh"
