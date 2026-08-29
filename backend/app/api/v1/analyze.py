from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.gemini_service import generate_completion


router = APIRouter()


class AnalyzeRequest(BaseModel):
    transcript: str


@router.post("/analyze")
async def analyze_sales_conversation(request: AnalyzeRequest):
    if not request.transcript.strip():
        raise HTTPException(
            status_code=422,
            detail="Transcript cannot be empty",
        )

    try:
        result = generate_completion(request.transcript)

        if hasattr(result, "model_dump"):
            data = result.model_dump()
        elif isinstance(result, dict):
            data = result
        else:
            data = {"result": result}

        return {
            "success": True,
            "data": data,
        }

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
