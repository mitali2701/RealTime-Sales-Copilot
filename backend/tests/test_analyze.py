from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_endpoint():
    response = client.post(
        "/api/v1/analyze",
        json={
            "transcript": (
                "Customer wants a CRM for 10 employees "
                "but thinks the price is high and asks for a demo next week."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "sentiment" in data
    assert "intent" in data
    assert "lead_score" in data
    assert "summary" in data


def test_analyze_missing_transcript():
    response = client.post(
        "/api/v1/analyze",
        json={}
    )

    assert response.status_code in [400, 422]
