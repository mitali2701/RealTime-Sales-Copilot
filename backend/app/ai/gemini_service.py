import json

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.sales_analysis import SalesAnalysis


class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = "gemini-3.6-flash"

    def analyze_transcript(self, transcript: str) -> SalesAnalysis:
        if not transcript.strip():
            raise ValueError("Transcript cannot be empty")

        prompt = f"""
Analyze this sales conversation and return ONLY valid JSON.

Required fields:
summary
sentiment
intent
entities
objections
buying_signals
suggested_response
next_questions
lead_score

Transcript:
{transcript}
"""

        try:
            response = self.client.models.generate_content(
                model=getattr(self, "model", "gemini-3.6-flash"),
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                ),
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            data = json.loads(text)

            return SalesAnalysis(**data)

        except Exception as exc:
            raise RuntimeError(f"Gemini API error: {exc}") from exc


_service = None


def get_gemini_service() -> GeminiService:
    global _service

    if _service is None:
        _service = GeminiService()

    return _service


def generate_completion(transcript: str) -> SalesAnalysis:
    return get_gemini_service().analyze_transcript(transcript)

