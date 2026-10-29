from fastapi.testclient import TestClient
from src.api_server import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_audit_endpoint():
    payload = {
        "target": "https://test.target/api",
        "impact_score": 8.8,
        "complexity": "high",
        "zero_day": False,
        "vector": "AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N"
    }
    response = client.post("/api/v1/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cvss_score"] > 0.0
    assert "problem_tier" in data
