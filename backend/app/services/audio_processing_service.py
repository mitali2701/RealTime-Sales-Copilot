from app.services.stt_service import STTService


class AudioProcessingService:
    def __init__(self):
        self.stt = STTService()

    def transcribe(self, audio_bytes: bytes, suffix: str = ".webm") -> str:
        if not audio_bytes:
            raise ValueError("Audio data is empty")

        return self.stt.transcribe_bytes(
            audio_bytes,
            suffix=suffix,
        )


audio_processing_service = AudioProcessingService()
