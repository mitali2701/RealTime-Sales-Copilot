import os
import tempfile

from faster_whisper import WhisperModel


class STTService:
    def __init__(self, model_size: str = "base"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        segments, _ = self.model.transcribe(
            audio_path,
            beam_size=5,
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

    def transcribe_bytes(self, audio_bytes: bytes, suffix: str = ".mp3") -> str:
        if not audio_bytes:
            raise ValueError("Audio data is empty")

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name

            return self.transcribe(temp_path)

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
