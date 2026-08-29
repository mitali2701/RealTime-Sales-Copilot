import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.transcription_service import transcription_service


router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio file is required",
        )

    suffix = os.path.splitext(file.filename)[1] or ".wav"

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        result = transcription_service.transcribe(temp_path)

        return {
            "success": True,
            "transcription": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {exc}",
        ) from exc

    finally:
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
