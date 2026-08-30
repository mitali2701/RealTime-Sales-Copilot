from app.ai.gemini_service import analyze_sales_conversation as gemini_analyze


def analyze_sales_conversation(transcript: str):
    """Analyze sales conversation using Gemini only."""
    return gemini_analyze(transcript)


def analyze_with_gemini(transcript: str):
    """Explicit Gemini analysis."""
    return gemini_analyze(transcript)
