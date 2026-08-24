from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

AUDIO_FILE = Path(r"C:\Users\ASUS\sales_call_ai\audio\9.mp3")


def test_analyze_audio_endpoint():
    assert AUDIO_FILE.exists(), f"Audio file not found: {AUDIO_FILE}"

    with AUDIO_FILE.open("rb") as audio:
        response = client.post(
            "/api/v1/analyze-audio",
            files={
                "file": (
                    "9.mp3",
                    audio,
                    "audio/mpeg",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "9.mp3"
    assert data["content_type"] == "audio/mpeg"

    assert "transcript" in data
    assert data["transcript"]

    assert "analysis" in data

    analysis = data["analysis"]

    assert "sentiment" in analysis
    assert "intent" in analysis
    assert "lead_score" in analysis
    assert "summary" in analysis
