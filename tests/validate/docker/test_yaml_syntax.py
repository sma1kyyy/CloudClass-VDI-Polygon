from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from conftest import run, skip_if_no_binary

YAMLLINT_CONFIG = Path(__file__).parent / ".yamllint.yaml"

def _collect_yaml_files(docker_dir: Path) -> list[Path]:
    return sorted(
        p
        for p in docker_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in {".yaml", ".yml"}
    )

def pytest_generate_tests(metafunc):  # noqa: D401 — pytest hook
    """Параметризуем тесты списком YAML-файлов в docker/."""
    if "yaml_path" in metafunc.fixturenames:
        from conftest import DOCKER_DIR  # type: ignore

        files = _collect_yaml_files(DOCKER_DIR)
        ids = [str(p.relative_to(DOCKER_DIR)) for p in files]
        metafunc.parametrize("yaml_path", files, ids=ids)


def test_pyyaml_parses(yaml_path: Path) -> None:
    """Файл должен парситься PyYAML без исключений."""
    with yaml_path.open(encoding="utf-8") as f:
        list(yaml.safe_load_all(f))


def test_yamllint_clean(yaml_path: Path) -> None:
    """yamllint не должен ругаться."""
    skip_if_no_binary("yamllint")
    result = run(
        [
            "yamllint",
            "-c",
            str(YAMLLINT_CONFIG),
            "-f",
            "parsable",
            str(yaml_path),
        ]
    )
    if result.returncode != 0:
        pytest.fail(
            f"yamllint нашёл ошибки в {yaml_path}:\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )


def test_at_least_one_yaml_found(docker_dir: Path) -> None:
    """Контрольный тест: список YAML вообще не пустой."""
    files = _collect_yaml_files(docker_dir)
    assert files, f"в {docker_dir} нет ни одного .yaml/.yml — что-то не так"
