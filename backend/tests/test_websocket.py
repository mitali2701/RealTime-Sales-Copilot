from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_websocket_connection():
    with client.websocket_connect(
        "/api/v1/ws/call/test-session"
    ) as websocket:
        data = websocket.receive_json()

        assert data["type"] == "connected"
        assert data["session_id"] == "test-session"


def test_websocket_text_transcript():
    with client.websocket_connect(
        "/api/v1/ws/call/text-session"
    ) as websocket:
        connected = websocket.receive_json()

        assert connected["type"] == "connected"

        websocket.send_text(
            "Customer likes the product."
        )

        data = websocket.receive_json()

        assert data["type"] == "transcript"
        assert "Customer likes the product." in data["text"]

        websocket.send_text("stop")

        analysis = websocket.receive_json()
        stopped = websocket.receive_json()

        assert analysis["type"] == "analysis"
        assert stopped["type"] == "stopped"


def test_websocket_pii_masking():
    with client.websocket_connect(
        "/api/v1/ws/call/pii-session"
    ) as websocket:
        websocket.receive_json()

        websocket.send_text(
            "Call me at 9876543210 or test@example.com"
        )

        data = websocket.receive_json()

        assert "[PHONE]" in data["text"]
        assert "[EMAIL]" in data["text"]

        websocket.send_text("stop")

        websocket.receive_json()
        websocket.receive_json()


def test_websocket_session_resume():
    session_id = "resume-session"

    with client.websocket_connect(
        f"/api/v1/ws/call/{session_id}"
    ) as websocket:
        websocket.receive_json()

        websocket.send_text("Customer wants a demo.")
        data = websocket.receive_json()

        assert data["type"] == "transcript"

        websocket.send_text("stop")
        websocket.receive_json()
        websocket.receive_json()

    with client.websocket_connect(
        f"/api/v1/ws/call/{session_id}"
    ) as websocket:
        data = websocket.receive_json()

        assert data["type"] == "connected"
        assert data["session_id"] == session_id
        assert data["resumed"] is True
        assert data["transcript_count"] >= 1
