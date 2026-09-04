from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "decilyra-api"}


def test_system_info_reports_service(client: TestClient) -> None:
    response = client.get("/api/v1/system")
    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "decilyra-api"
    assert payload["api_prefix"] == "/api/v1"
    assert "database_configured" in payload
