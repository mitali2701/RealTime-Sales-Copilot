from app.schemas.sales_analysis import SalesAnalysis


def test_sales_analysis_schema():
    data = SalesAnalysis(
        sentiment="positive",
        intent="purchase",
        entities=[],
        objections=[],
        buying_signals=[],
        next_questions=[],
        suggested_response="Thank you for your interest.",
        product_recommendation="Standard Plan",
        lead_score=85,
        summary="Customer showed strong purchase intent.",
    )

    assert data.lead_score == 85
    assert data.sentiment == "positive"
