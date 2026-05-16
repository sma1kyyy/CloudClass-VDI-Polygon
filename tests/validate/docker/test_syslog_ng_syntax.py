from __future__ import annotations

from pathlib import Path

import pytest

from conftest import have_binary, run

pytestmark = pytest.mark.docker


def test_syslog_ng_config_valid(require_docker, syslog_ng_config: Path) -> None:
    """syslog-ng --syntax-only -f <config> должен пройти без ошибок."""
    if not syslog_ng_config.is_file():
        pytest.skip(f"{syslog_ng_config} отсутствует")

    if have_binary("syslog-ng"):
        cmd = ["syslog-ng", "--syntax-only", "-f", str(syslog_ng_config)]
    else:
        container_path = "/etc/syslog-ng/syslog-ng.conf"
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{syslog_ng_config}:{container_path}:ro",
            "--entrypoint",
            "syslog-ng",
            "balabit/syslog-ng:latest",
            "--syntax-only",
            "-f",
            container_path,
        ]

    # pull может быть долгим, ставим таймаут большой 3 минуты
    result = run(cmd, timeout=180)
    if result.returncode != 0:
        pytest.fail(
            "syslog-ng --syntax-only упал:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
