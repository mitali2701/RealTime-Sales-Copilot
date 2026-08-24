import json

from google import genai

from app.core.config import settings
from app.schemas.sales_analysis import SalesAnalysis


client = genai.Client(api_key=settings.gemini_api_key)

MODEL_NAME = "gemini-3.5-flash"


SALES_ANALYSIS_PROMPT = """
You are an AI sales intelligence assistant.

Analyze the following sales conversation and return ONLY valid JSON.

The JSON must contain exactly these fields:

{
  "sentiment": "string",
  "intent": "string",
  "entities": [
    {
      "name": "string",
      "type": "string"
    }
  ],
  "objections": ["string"],
  "buying_signals": ["string"],
  "next_questions": ["string"],
  "suggested_response": "string",
  "product_recommendation": "string",
  "lead_score": 0,
  "summary": "string"
}

Rules:
- sentiment should describe the customer's overall emotional tone.
- intent should describe the customer's main purpose or buying intent.
- entities should contain useful entities such as product, company, person, budget, location, or timeline.
- objections should contain customer concerns or barriers.
- buying_signals should contain evidence that the customer may buy.
- next_questions should contain useful discovery questions for the salesperson.
- suggested_response should be a helpful response the salesperson could give.
- product_recommendation should recommend what the salesperson should offer based only on the conversation.
- lead_score must be an integer from 0 to 100.
- summary should briefly summarize the conversation.
- Do not invent information that is not supported by the conversation.
- If a field has no information, return an empty list or a reasonable "unknown" value.

Sales conversation:

"""


def generate_completion(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text


def analyze_sales_conversation(transcript: str) -> SalesAnalysis:
    prompt = SALES_ANALYSIS_PROMPT + transcript

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": SalesAnalysis,
        },
    )

    data = json.loads(response.text)

    return SalesAnalysis.model_validate(data)
