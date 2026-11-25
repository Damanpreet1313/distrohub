import os

import pytest

from app.core.config import get_settings
from app.infrastructure.docker.adapter import DockerAdapter
from app.infrastructure.docker.client import create_docker_client

pytestmark = pytest.mark.skipif(
    os.getenv("DISTROHUB_RUN_DOCKER_INTEGRATION") != "1",
    reason="Set DISTROHUB_RUN_DOCKER_INTEGRATION=1 to run Docker integration tests",
)


def test_docker_engine_is_reachable() -> None:
    settings = get_settings()
    adapter = DockerAdapter(create_docker_client(settings.docker_host))

    try:
        assert adapter.ping() is True

        version = adapter.get_version()

        assert version.version
        assert version.api_version
    finally:
        adapter.close()
