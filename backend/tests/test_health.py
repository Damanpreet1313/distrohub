from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


def test_health_returns_status_and_version() -> None:
    settings = get_settings()

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": settings.app_version}


def test_health_returns_json_content_type() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.headers["content-type"] == "application/json"
