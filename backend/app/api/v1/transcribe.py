import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.stt_service import STTService


router = APIRouter(
    prefix="/transcribe",
    tags=["Transcription"],
)

stt_service = STTService()

ALLOWED_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/webm",
    "audio/ogg",
    "application/octet-stream",
}


@router.post("")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio filename is required",
        )

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio type: {file.content_type}",
        )

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty",
        )

    suffix = os.path.splitext(file.filename)[1].lower()

    if not suffix:
        suffix = ".wav"

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        result = stt_service.transcribe(temp_path)

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "text": result,
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Audio processing service could not access the temporary file",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Transcription service failed to process the audio",
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
