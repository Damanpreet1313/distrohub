class DockerConnectionError(RuntimeError):
    def __init__(self, message: str = "Unable to connect to Docker Engine") -> None:
        super().__init__(message)
