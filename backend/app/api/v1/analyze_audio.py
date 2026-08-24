from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ai.providers.sales_ai import analyze_sales_conversation
from app.services.stt_service import STTService


router = APIRouter(
    prefix="/analyze-audio",
    tags=["Audio Analysis"],
)

stt_service = STTService()

ALLOWED_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/mp4",
    "audio/x-m4a",
    "audio/webm",
}


@router.post("")
async def analyze_audio(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio type: {file.content_type}",
        )

    try:
        audio_bytes = await file.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty",
            )

        transcript = stt_service.transcribe_bytes(
            audio_bytes,
            suffix=".mp3",
        )

        if not transcript.strip():
            raise HTTPException(
                status_code=422,
                detail="Could not extract speech from audio",
            )

        analysis = analyze_sales_conversation(transcript)

        if hasattr(analysis, "model_dump"):
            analysis = analysis.model_dump()

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "transcript": transcript,
            "analysis": analysis,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Audio analysis service failed",
        )
