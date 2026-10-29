"""API tests: FastAPI server exercised through the TestClient."""

from src.api_server import app

from fastapi.testclient import TestClient

client = TestClient(app)

CRITICAL = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"


def test_health():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_calculate_endpoint():
    resp = client.post("/calculate", json={"vector": CRITICAL})
    assert resp.status_code == 200
    body = resp.json()
    assert body["base_score"] == 9.8
    assert body["severity"] == "Critical"


def test_calculate_invalid_vector_returns_400():
    resp = client.post("/calculate", json={"vector": "not-a-vector"})
    assert resp.status_code == 400


def test_report_endpoint():
    resp = client.post(
        "/report",
        json={
            "title": "Reflected XSS in search",
            "target": "https://example.com/search",
            "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
            "description": "Query parameter is reflected unsanitised.",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["base_score"] == 6.1
    assert body["severity"] == "Medium"
    assert "Reflected XSS in search" in body["report"]
    assert "https://example.com/search" in body["report"]