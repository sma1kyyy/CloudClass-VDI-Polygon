from __future__ import annotations

from pathlib import Path

import pytest

from conftest import have_binary, run

pytestmark = pytest.mark.docker


def test_alertmanager_config_valid(
    require_docker, alertmanager_config: Path
) -> None:
    """amtool check-config должен принять alertmanager.yml без ошибок."""
    if not alertmanager_config.is_file():
        pytest.skip(f"{alertmanager_config} отсутствует")

    if have_binary("amtool"):
        cmd = ["amtool", "check-config", str(alertmanager_config)]
    else:
        container_path = "/cfg/alertmanager.yml"
        cmd = [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "amtool",
            "-v",
            f"{alertmanager_config}:{container_path}:ro",
            "prom/alertmanager:latest",
            "check-config",
            container_path,
        ]

    result = run(cmd, timeout=120)
    if result.returncode != 0:
        pytest.fail(
            "amtool check-config упал:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
