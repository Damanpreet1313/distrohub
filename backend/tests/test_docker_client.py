from unittest.mock import Mock, patch

from app.infrastructure.docker.client import create_docker_client


def test_create_client_uses_explicit_host() -> None:
    sentinel = Mock()

    with patch(
        "app.infrastructure.docker.client.DockerClient", return_value=sentinel
    ) as docker_client:
        client = create_docker_client("unix:///tmp/docker.sock")

    docker_client.assert_called_once_with(base_url="unix:///tmp/docker.sock")
    assert client is sentinel


def test_create_client_uses_environment_when_host_is_not_configured() -> None:
    sentinel = Mock()

    with patch(
        "app.infrastructure.docker.client.from_env", return_value=sentinel
    ) as from_env:
        client = create_docker_client(None)

    from_env.assert_called_once_with()
    assert client is sentinel
