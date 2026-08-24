from app.ai.ollama_service import (
    analyze_sales_conversation as ollama_analyze,
)
from app.ai.gemini_service import (
    analyze_sales_conversation as gemini_analyze,
)


def analyze_sales_conversation(transcript: str):
    """
    Analyze using Ollama first.

    Ollama is the primary local provider, so normal requests do not
    consume Gemini API quota. Gemini is used only if Ollama fails.
    """
    try:
        return ollama_analyze(transcript)

    except Exception as ollama_error:
        try:
            return gemini_analyze(transcript)

        except Exception as gemini_error:
            raise RuntimeError(
                "All AI providers failed. "
                f"Ollama error: {ollama_error}; "
                f"Gemini error: {gemini_error}"
            ) from gemini_error


def analyze_with_ollama(transcript: str):
    """Explicitly use the local Ollama provider."""
    return ollama_analyze(transcript)


def analyze_with_gemini(transcript: str):
    """Explicitly use the Gemini cloud provider."""
    return gemini_analyze(transcript)
