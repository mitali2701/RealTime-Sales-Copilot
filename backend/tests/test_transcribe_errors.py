from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_transcribe_rejects_unsupported_file_type():
    response = client.post(
        "/api/v1/transcribe",
        files={
            "file": (
                "test.txt",
                b"this is not audio",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported audio type: text/plain"


def test_transcribe_rejects_empty_audio():
    response = client.post(
        "/api/v1/transcribe",
        files={
            "file": (
                "empty.mp3",
                b"",
                "audio/mpeg",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded audio file is empty"


def test_transcribe_requires_file():
    response = client.post("/api/v1/transcribe")

    assert response.status_code == 422
