from unittest.mock import MagicMock, patch

from app.services.stt_service import STTService


@patch("app.services.stt_service.WhisperModel")
def test_stt_service(mock_whisper_model):
    mock_model = MagicMock()
    mock_whisper_model.return_value = mock_model

    segment = MagicMock()
    segment.text = "Hello customer"

    mock_model.transcribe.return_value = (
        [segment],
        None,
    )

    service = STTService()

    with patch(
        "pathlib.Path.exists",
        return_value=True,
    ):
        result = service.transcribe("test.wav")

    assert result == "Hello customer"
