from google import genai
from pydantic import BaseModel

from app.core.config import settings


class SalesAnalysis(BaseModel):
    summary: str
    sentiment: str
    objections: list[str]
    buying_signals: list[str]
    next_best_action: str


def generate_completion(transcript: str) -> SalesAnalysis:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
You are an expert sales-call analyst.

Analyze this customer conversation:

{transcript}

Return:
- concise summary
- sentiment
- customer objections
- buying signals
- next best action for the salesperson
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": SalesAnalysis,
            },
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response")

        return SalesAnalysis.model_validate_json(response.text)

    except Exception as exc:
        raise RuntimeError(f"Gemini API error: {exc}") from exc
