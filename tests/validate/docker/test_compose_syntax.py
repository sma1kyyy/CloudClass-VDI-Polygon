from __future__ import annotations

from pathlib import Path

import pytest

from conftest import run

pytestmark = pytest.mark.docker


def _write_dummy_env(target: Path) -> None:
    """
    Подставляем заглушки на каждую переменную, чтобы docker compose не ругался
    на «variable is not set». Реальные значения тут не нужны, проверяем только
    структуру.
    """
    target.write_text(
        "\n".join(
            [
                "POSTGRES_DB=test_db",
                "POSTGRES_USER=test_user",
                "POSTGRES_PASSWORD=test_pass",
                "GUACAMOLE_VERSION=1.5.5",
                "GUACAMOLE_PORT=8080",
                "CODE_SERVER_PASSWORD=test_pass",
                "GRAFANA_USER=admin",
                "GRAFANA_PASSWORD=admin",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_docker_compose_config_valid(
    require_docker, docker_dir: Path, compose_file: Path, tmp_path: Path
) -> None:
    """docker compose config должен принять файл без ошибок."""
    env_file = tmp_path / ".env"
    _write_dummy_env(env_file)

    result = run(
        [
            "docker",
            "compose",
            "--env-file",
            str(env_file),
            "-f",
            str(compose_file),
            "config",
            "--quiet",
        ],
        cwd=docker_dir,
        timeout=60,
    )

    if result.returncode != 0:
        pytest.fail(
            "docker compose config упал:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )


def test_docker_compose_config_renders_known_services(
    require_docker, docker_dir: Path, compose_file: Path, tmp_path: Path
) -> None:
    """
    Проверка, что compose выводит все объявленные сервисы.
    """
    env_file = tmp_path / ".env"
    _write_dummy_env(env_file)

    result = run(
        [
            "docker",
            "compose",
            "--env-file",
            str(env_file),
            "-f",
            str(compose_file),
            "config",
            "--services",
        ],
        cwd=docker_dir,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    services = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    expected = {
        "postgres",
        "guacd",
        "guacamole",
        "portainer",
        "code-server",
        "prometheus",
        "grafana",
        "node-exporter",
        "cadvisor",
        "syslog-ng",
        "alertmanager",
    }
    missing = expected - services
    assert not missing, f"compose не отдал ожидаемые сервисы: {missing}"
