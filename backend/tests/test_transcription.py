from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_transcription_endpoint_exists():
    response = client.post(
        "/api/v1/transcribe",
        files={
            "file": (
                "test.mp3",
                b"fake audio data",
                "audio/mpeg",
            )
        },
    )

    assert response.status_code != 404
