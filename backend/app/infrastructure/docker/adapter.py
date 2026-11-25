from dataclasses import dataclass
from typing import Any

from docker import DockerClient
from docker.errors import DockerException

from app.infrastructure.docker.errors import DockerConnectionError


@dataclass(frozen=True, slots=True)
class DockerEngineVersion:
    version: str
    api_version: str
    min_api_version: str
    os: str
    arch: str


class DockerAdapter:
    def __init__(self, client: DockerClient) -> None:
        self._client = client

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except (DockerException, OSError) as exc:
            raise DockerConnectionError() from exc

    def get_version(self) -> DockerEngineVersion:
        try:
            version: dict[str, Any] = self._client.version()
        except (DockerException, OSError) as exc:
            raise DockerConnectionError(
                "Unable to retrieve Docker Engine version"
            ) from exc

        return DockerEngineVersion(
            version=str(version.get("Version") or ""),
            api_version=str(version.get("ApiVersion") or ""),
            min_api_version=str(version.get("MinAPIVersion") or ""),
            os=str(version.get("Os") or ""),
            arch=str(version.get("Arch") or ""),
        )

    def close(self) -> None:
        self._client.close()
