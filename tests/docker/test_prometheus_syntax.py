from __future__ import annotations

from pathlib import Path

import pytest

from conftest import docker_available, have_binary, run


def _promtool_invocation(args: list[str], mounts: dict[Path, str]) -> list[str]:
    """
    Возвращает команду для запуска promtool. (или локально или фолбэчим на вариант в докере)
    """
    if have_binary("promtool"):
        return ["promtool", *args]
    if docker_available():
        cmd = ["docker", "run", "--rm", "--entrypoint", "promtool"]
        for host, container in mounts.items():
            cmd += ["-v", f"{host}:{container}:ro"]
        cmd += ["prom/prometheus:latest", *args]
        return cmd
    pytest.skip("ни локального promtool, ни docker - пропускаем")


@pytest.mark.promtool
def test_prometheus_config_valid(prometheus_config: Path) -> None:
    """promtool check config должен принять prometheus.yaml без ошибок."""
    if not prometheus_config.is_file():
        pytest.skip(f"{prometheus_config} отсутствует")

    container_path = "/cfg/prometheus.yaml"
    cmd = _promtool_invocation(
        ["check", "config", container_path]
        if not have_binary("promtool")
        else ["check", "config", str(prometheus_config)],
        mounts={prometheus_config: container_path},
    )

    result = run(cmd, timeout=60)
    if result.returncode != 0:
        pytest.fail(
            "promtool check config упал:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )


@pytest.mark.promtool
def test_prometheus_alert_rules_valid(prometheus_alerts: Path) -> None:
    """promtool check rules должен принять alerts.yml без ошибок."""
    if not prometheus_alerts.is_file():
        pytest.skip(f"{prometheus_alerts} отсутствует")

    container_path = "/cfg/alerts.yml"
    cmd = _promtool_invocation(
        ["check", "rules", container_path]
        if not have_binary("promtool")
        else ["check", "rules", str(prometheus_alerts)],
        mounts={prometheus_alerts: container_path},
    )

    result = run(cmd, timeout=60)
    if result.returncode != 0:
        pytest.fail(
            "promtool check rules упал:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
