from pathlib import Path

from faster_whisper import WhisperModel


class STTService:
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio_path: str | Path) -> str:
        audio_path = str(audio_path)

        segments, _ = self.model.transcribe(audio_path)

        return " ".join(segment.text.strip() for segment in segments).strip()
