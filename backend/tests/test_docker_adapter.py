from unittest.mock import Mock

import docker
import pytest
from docker.errors import DockerException

from app.infrastructure.docker.adapter import DockerAdapter, DockerEngineVersion
from app.infrastructure.docker.errors import DockerConnectionError


def test_ping_returns_true() -> None:
    client = Mock(spec=docker.DockerClient)
    client.ping.return_value = True

    assert DockerAdapter(client).ping() is True
    client.ping.assert_called_once_with()


def test_ping_returns_false_when_client_returns_false() -> None:
    client = Mock(spec=docker.DockerClient)
    client.ping.return_value = False

    assert DockerAdapter(client).ping() is False
    client.ping.assert_called_once_with()


@pytest.mark.parametrize(
    "error",
    [
        DockerException("internal daemon details"),
        OSError("internal socket details"),
    ],
)
def test_ping_raises_safe_connection_error(error: Exception) -> None:
    client = Mock(spec=docker.DockerClient)
    client.ping.side_effect = error

    with pytest.raises(DockerConnectionError) as exc_info:
        DockerAdapter(client).ping()

    assert str(exc_info.value) == "Unable to connect to Docker Engine"
    assert "internal" not in str(exc_info.value)
    assert exc_info.value.__cause__ is error


def test_get_version_returns_typed_engine_version() -> None:
    client = Mock(spec=docker.DockerClient)
    client.version.return_value = {
        "Version": "29.5.3",
        "ApiVersion": "1.52",
        "MinAPIVersion": "1.24",
        "Os": "linux",
        "Arch": "amd64",
    }

    result = DockerAdapter(client).get_version()

    assert result == DockerEngineVersion(
        version="29.5.3",
        api_version="1.52",
        min_api_version="1.24",
        os="linux",
        arch="amd64",
    )


def test_get_version_handles_missing_fields() -> None:
    client = Mock(spec=docker.DockerClient)
    client.version.return_value = {"Version": "29.5.3"}

    result = DockerAdapter(client).get_version()

    assert result.version == "29.5.3"
    assert result.api_version == ""
    assert result.min_api_version == ""
    assert result.os == ""
    assert result.arch == ""


def test_get_version_normalizes_none_fields() -> None:
    client = Mock(spec=docker.DockerClient)
    client.version.return_value = {
        "Version": None,
        "ApiVersion": None,
        "MinAPIVersion": None,
        "Os": None,
        "Arch": None,
    }

    result = DockerAdapter(client).get_version()

    assert result == DockerEngineVersion(
        version="",
        api_version="",
        min_api_version="",
        os="",
        arch="",
    )


def test_get_version_raises_safe_connection_error() -> None:
    client = Mock(spec=docker.DockerClient)
    client.version.side_effect = DockerException("internal daemon details")

    with pytest.raises(DockerConnectionError) as exc_info:
        DockerAdapter(client).get_version()

    assert str(exc_info.value) == "Unable to retrieve Docker Engine version"
    assert "internal" not in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, DockerException)


def test_close_closes_client() -> None:
    client = Mock(spec=docker.DockerClient)

    DockerAdapter(client).close()

    client.close.assert_called_once_with()
