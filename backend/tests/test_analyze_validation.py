from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_rejects_empty_transcript():
    response = client.post(
        "/api/v1/analyze",
        json={"transcript": ""},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Transcript cannot be empty"


def test_analyze_rejects_whitespace_transcript():
    response = client.post(
        "/api/v1/analyze",
        json={"transcript": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Transcript cannot be empty"


def test_analyze_requires_transcript():
    response = client.post(
        "/api/v1/analyze",
        json={},
    )

    assert response.status_code == 422
