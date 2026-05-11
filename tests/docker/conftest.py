from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

# tests/docker/conftest.py > repo root
REPO_ROOT: Path = Path(__file__).resolve().parents[2]
DOCKER_DIR: Path = REPO_ROOT / "docker"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def docker_dir() -> Path:
    assert DOCKER_DIR.is_dir(), f"docker/ не найден по пути {DOCKER_DIR}"
    return DOCKER_DIR


@pytest.fixture(scope="session")
def compose_file(docker_dir: Path) -> Path:
    p = docker_dir / "compose.yaml"
    assert p.is_file(), f"{p} отсутствует"
    return p


@pytest.fixture(scope="session")
def env_example(docker_dir: Path) -> Path:
    p = docker_dir / ".env.example"
    assert p.is_file(), f"{p} отсутствует"
    return p


@pytest.fixture(scope="session")
def prometheus_config(docker_dir: Path) -> Path:
    return docker_dir / "prometheus" / "prometheus.yaml"


@pytest.fixture(scope="session")
def prometheus_alerts(docker_dir: Path) -> Path:
    return docker_dir / "prometheus" / "alerts.yml"


@pytest.fixture(scope="session")
def alertmanager_config(docker_dir: Path) -> Path:
    return docker_dir / "alertmanager" / "alertmanager.yml"


@pytest.fixture(scope="session")
def syslog_ng_config(docker_dir: Path) -> Path:
    return docker_dir / "syslog-ng" / "syslog-ng.conf"


@pytest.fixture(scope="session")
def compose_data(compose_file: Path) -> dict:
    """Распарсенный compose.yaml как dict - для проверок."""
    with compose_file.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def have_binary(name: str) -> bool:
    return shutil.which(name) is not None


def docker_available() -> bool:
    """True если докер-демон отвечает (docker info)."""
    if not have_binary("docker"):
        return False
    try:
        return (
            subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5,
                check=False,
            ).returncode
            == 0
        )
    except (subprocess.TimeoutExpired, OSError):
        return False


def skip_if_no_docker() -> None:
    if not docker_available():
        pytest.skip("docker daemon недоступен")


def skip_if_no_binary(name: str) -> None:
    if not have_binary(name):
        pytest.skip(f"бинарь {name!r} не найден в PATH")


@pytest.fixture
def require_docker() -> None:
    skip_if_no_docker()


@pytest.fixture
def require_yamllint() -> None:
    skip_if_no_binary("yamllint")


@pytest.fixture
def require_promtool() -> None:
    skip_if_no_binary("promtool")



def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env_extra: dict[str, str] | None = None,
    timeout: int = 120,
) -> subprocess.CompletedProcess:
    """Тонкая обёртка над subprocess.run - capture, текстовый вывод, без check."""
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
