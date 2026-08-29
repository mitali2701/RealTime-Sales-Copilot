from app.schemas.sales_analysis import SalesAnalysis


def test_sales_analysis_schema():
    result = SalesAnalysis(
        summary="Customer is interested.",
        sentiment="positive",
        intent="buying",
        entities=["Product A"],
        objections=[],
        buying_signals=["Asked about pricing"],
        suggested_response="Explain pricing options.",
        next_questions=["What is your budget?"],
        lead_score=80,
    )

    assert result.lead_score == 80
    assert result.intent == "buying"
