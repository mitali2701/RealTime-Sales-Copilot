from faster_whisper import WhisperModel


class TranscriptionService:
    def __init__(self):
        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str) -> dict:
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        )

        return {
            "text": text,
            "language": info.language,
            "duration": info.duration,
        }


transcription_service = TranscriptionService()
