import json

import requests

from app.schemas.sales_analysis import SalesAnalysis


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"


OLLAMA_PROMPT = """
You are a sales analysis AI.

Analyze this sales conversation and return ONLY valid JSON.

Required JSON structure:

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

IMPORTANT:
- objections MUST be an array of strings.
- buying_signals MUST be an array of strings.
- next_questions MUST be an array of strings.
- entities MUST be an array of objects with name and type.
- lead_score MUST be an integer from 0 to 100.
- Do not use objects inside objections, buying_signals, or next_questions.
- Return JSON only.
- Do not add markdown.

Conversation:
"""


def generate_completion(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_predict": 700,
            },
        },
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()
    return data["response"]

def _normalize_string_list(values):
    if not isinstance(values, list):
        return []

    normalized = []

    for item in values:
        if isinstance(item, str):
            normalized.append(item)

        elif isinstance(item, dict):
            if "text" in item:
                normalized.append(str(item["text"]))
            elif "name" in item:
                normalized.append(str(item["name"]))
            elif "value" in item:
                normalized.append(str(item["value"]))

    return normalized


def _normalize_entities(values):
    if not isinstance(values, list):
        return []

    normalized = []

    for item in values:
        if isinstance(item, dict):
            normalized.append(
                {
                    "name": str(item.get("name", item.get("text", ""))),
                    "type": str(item.get("type", "unknown")),
                }
            )

    return normalized


def _normalize_analysis(data):
    data["entities"] = _normalize_entities(
        data.get("entities", [])
    )

    data["objections"] = _normalize_string_list(
        data.get("objections", [])
    )

    data["buying_signals"] = _normalize_string_list(
        data.get("buying_signals", [])
    )

    data["next_questions"] = _normalize_string_list(
        data.get("next_questions", [])
    )

    try:
        data["lead_score"] = int(data.get("lead_score", 0))
    except (TypeError, ValueError):
        data["lead_score"] = 0

    data["lead_score"] = max(
        0,
        min(100, data["lead_score"]),
    )

    return data


def analyze_sales_conversation(transcript: str) -> SalesAnalysis:
    prompt = OLLAMA_PROMPT + transcript

    raw_response = generate_completion(prompt).strip()

    if raw_response.startswith("```"):
        raw_response = raw_response.replace("```json", "", 1)
        raw_response = raw_response.replace("```", "", 1)
        raw_response = raw_response.strip()

    data = json.loads(raw_response)

    data = _normalize_analysis(data)

    return SalesAnalysis.model_validate(data)
