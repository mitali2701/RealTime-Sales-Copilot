from unittest.mock import MagicMock, patch

from app.ai.gemini_service import GeminiService


@patch("app.ai.gemini_service.genai.Client")
def test_gemini_analysis(mock_client):
    mock_response = MagicMock()

    mock_response.text = """
    {
        "summary": "Customer is interested.",
        "sentiment": "positive",
        "intent": "buying",
        "entities": ["Product A"],
        "objections": [],
        "buying_signals": ["Asked about price"],
        "suggested_response": "Explain the pricing.",
        "next_questions": ["What is your budget?"],
        "lead_score": 80
    }
    """

    mock_instance = MagicMock()

    mock_instance.models.generate_content.return_value = mock_response

    mock_client.return_value = mock_instance

    service = GeminiService.__new__(GeminiService)

    service.client = mock_instance

    result = service.analyze_transcript("Customer asks about pricing.")

    assert result.lead_score == 80
    assert result.sentiment == "positive"
