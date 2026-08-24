from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.providers.sales_ai import analyze_sales_conversation


router = APIRouter(
    prefix="/analyze",
    tags=["Sales Analysis"],
)


class AnalyzeRequest(BaseModel):
    transcript: str


@router.post("")
async def analyze_conversation(request: AnalyzeRequest):
    transcript = request.transcript.strip()

    if not transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript cannot be empty",
        )

    try:
        result = analyze_sales_conversation(transcript)

        if hasattr(result, "model_dump"):
            return result.model_dump()

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Sales conversation analysis service failed",
        )
