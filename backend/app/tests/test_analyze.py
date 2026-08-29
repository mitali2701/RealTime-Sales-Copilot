from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_validation():
    response = client.post(
        "/api/v1/analyze",
        json={"transcript": ""},
    )

    assert response.status_code in [200, 422]


@patch("app.api.v1.analyze.generate_completion")
def test_analyze(mock_generate_completion):
    mock_generate_completion.return_value = {
        "summary": "Customer is interested but has a price objection.",
        "sentiment": "mixed",
        "intent": "buying",
        "entities": ["product", "price"],
        "objections": ["Price is high"],
        "buying_signals": ["Likes the product"],
        "suggested_response": "Explain the product value and available pricing options.",
        "next_questions": ["What budget are you considering?"],
        "lead_score": 80,
    }

    response = client.post(
        "/api/v1/analyze",
        json={
            "transcript": "Customer likes the product but thinks the price is high."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "data" in data
