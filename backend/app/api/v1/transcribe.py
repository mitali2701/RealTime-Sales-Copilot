from pathlib import Path
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.stt_service import STTService

router = APIRouter()

stt_service = STTService()


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio file is required",
        )

    suffix = Path(file.filename).suffix or ".wav"

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        transcript = stt_service.transcribe(temp_path)

        return {
            "success": True,
            "data": {
                "transcript": transcript,
            },
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {exc}",
        ) from exc

    finally:
        try:
            Path(temp_path).unlink(missing_ok=True)
        except UnboundLocalError:
            pass
