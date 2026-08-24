from app.ai.ollama_service import analyze_sales_conversation


def test_ollama_sales_analysis():
    transcript = (
        "Customer wants a CRM for 10 employees "
        "but thinks the price is high and asks for a demo next week."
    )

    result = analyze_sales_conversation(transcript)

    assert result.sentiment
    assert result.intent
    assert isinstance(result.entities, list)
    assert isinstance(result.objections, list)
    assert isinstance(result.buying_signals, list)
    assert isinstance(result.next_questions, list)
    assert isinstance(result.suggested_response, str)
    assert isinstance(result.product_recommendation, str)
    assert 0 <= result.lead_score <= 100
    assert result.summary


def test_ollama_analysis_contains_expected_information():
    transcript = (
        "Customer wants a CRM for 10 employees "
        "but thinks the price is high and asks for a demo next week."
    )

    result = analyze_sales_conversation(transcript)

    objections = " ".join(result.objections).lower()
    questions = " ".join(result.next_questions).lower()

    assert "price" in objections or "high" in objections
    assert questions