import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.stt_service import stt_service


router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    allowed_types = {
        "audio/wav",
        "audio/x-wav",
        "audio/mpeg",
        "audio/mp3",
        "audio/mp4",
        "audio/webm",
        "audio/ogg",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format",
        )

    data = await file.read()

    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Audio file is too large",
        )

    suffix = Path(file.filename or "audio.wav").suffix or ".wav"

    with tempfile.NamedTemporaryFile(
        suffix=suffix,
        delete=False,
    ) as temp:
        temp.write(data)
        temp_path = temp.name

    try:
        transcript = stt_service.transcribe(temp_path)

        return {
            "success": True,
            "transcript": transcript,
            "filename": file.filename,
        }

    finally:
        Path(temp_path).unlink(missing_ok=True)
