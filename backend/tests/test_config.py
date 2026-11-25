import pytest

from app.core.config import Settings


def test_docker_host_defaults_to_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DISTROHUB_DOCKER_HOST", raising=False)

    assert Settings(_env_file=None).docker_host is None


def test_docker_host_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DISTROHUB_DOCKER_HOST", "unix:///tmp/docker.sock")

    assert Settings(_env_file=None).docker_host == "unix:///tmp/docker.sock"
