from __future__ import annotations

import os


class DiarizationService:
    """Speaker diarization service using pyannote when configured."""

    def __init__(self):
        self.pipeline = None
        token = os.getenv("HF_TOKEN")

        if token:
            try:
                from pyannote.audio import Pipeline

                self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    token=token,
                )
            except Exception:
                self.pipeline = None

    @property
    def available(self) -> bool:
        return self.pipeline is not None

    def diarize(self, audio_path: str) -> list[dict]:
        if self.pipeline is None:
            return []

        diarization = self.pipeline(audio_path)
        results = []

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            results.append({
                "start": float(turn.start),
                "end": float(turn.end),
                "speaker": speaker,
            })

        return results

    def map_speaker_role(
        self,
        speaker_id: str,
        role_mapping: dict[str, str] | None = None,
    ) -> str:
        if role_mapping and speaker_id in role_mapping:
            return role_mapping[speaker_id]

        return "unknown"

    def identify_speaker(self, speaker: str | None = None) -> str:
        if speaker in {"salesperson", "customer"}:
            return speaker

        return "unknown"
