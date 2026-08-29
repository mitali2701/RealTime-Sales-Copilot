from pathlib import Path

from faster_whisper import WhisperModel


class STTService:
    def __init__(self) -> None:
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str) -> str:
        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(audio_path)

        segments, _ = self.model.transcribe(
            str(path),
            vad_filter=True,
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()


stt_service = STTService()
