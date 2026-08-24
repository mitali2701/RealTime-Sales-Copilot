from unittest.mock import patch

from app.ai.providers.sales_ai import analyze_sales_conversation
from app.schemas.sales_analysis import SalesAnalysis


def test_ollama_is_primary_provider():
    expected = SalesAnalysis(
        sentiment="positive",
        intent="purchase",
        entities=[],
        objections=[],
        buying_signals=["ready to buy"],
        next_questions=[],
        suggested_response="Great!",
        product_recommendation="CRM",
        lead_score=90,
        summary="Customer is ready to buy.",
    )

    with patch(
        "app.ai.providers.sales_ai.ollama_analyze",
        return_value=expected,
    ) as ollama_mock, patch(
        "app.ai.providers.sales_ai.gemini_analyze"
    ) as gemini_mock:

        result = analyze_sales_conversation("Customer is ready to buy.")

        assert result == expected
        ollama_mock.assert_called_once()
        gemini_mock.assert_not_called()


def test_gemini_is_fallback_when_ollama_fails():
    expected = SalesAnalysis(
        sentiment="neutral",
        intent="inquiry",
        entities=[],
        objections=[],
        buying_signals=[],
        next_questions=[],
        suggested_response="Let's schedule a demo.",
        product_recommendation="CRM",
        lead_score=60,
        summary="Customer wants more information.",
    )

    with patch(
        "app.ai.providers.sales_ai.ollama_analyze",
        side_effect=RuntimeError("Ollama unavailable"),
    ) as ollama_mock, patch(
        "app.ai.providers.sales_ai.gemini_analyze",
        return_value=expected,
    ) as gemini_mock:

        result = analyze_sales_conversation("Customer wants more information.")

        assert result == expected
        ollama_mock.assert_called_once()
        gemini_mock.assert_called_once()
