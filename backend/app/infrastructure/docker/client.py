from docker import DockerClient, from_env


def create_docker_client(host: str | None = None) -> DockerClient:
    if host:
        return DockerClient(base_url=host)
    return from_env()
