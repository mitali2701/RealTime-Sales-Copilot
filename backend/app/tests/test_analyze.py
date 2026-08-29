from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_validation():
    response = client.post(
        "/api/v1/analyze",
        json={"transcript": ""},
    )

    assert response.status_code in [200, 422]


def test_analyze():
    response = client.post(
        "/api/v1/analyze",
        json={"transcript": ("Customer likes the product but thinks the price is high.")},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "data" in data
