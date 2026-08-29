from io import BytesIO

from faster_whisper import WhisperModel


class STTService:
    def __init__(self, model_size: str = "tiny"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_bytes: bytes) -> dict:
        if not audio_bytes:
            raise ValueError("Audio data cannot be empty")

        segments, info = self.model.transcribe(
            BytesIO(audio_bytes),
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        )

        return {
            "text": text,
            "language": info.language,
        }


stt_service = STTService()


def transcribe_audio(audio_bytes: bytes) -> dict:
    return stt_service.transcribe(audio_bytes)
