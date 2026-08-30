from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.ai.gemini_service import analyze_sales_conversation
from app.services.audio_processing_service import AudioProcessingService
from app.services.diarization_service import DiarizationService
from app.services.pii_service import mask_pii
from app.services.session_service import SessionService

router = APIRouter(
    prefix="/ws",
    tags=["Real-Time Call"],
)

session_service = SessionService()
diarization_service = DiarizationService()
audio_service = AudioProcessingService()


@router.websocket("/call/{session_id}")
async def call_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()

    existing_transcript = session_service.get_transcript(session_id)

    await websocket.send_json({
        "type": "connected",
        "session_id": session_id,
        "resumed": bool(existing_transcript),
        "transcript_count": len(existing_transcript),
    })

    try:
        while True:
            message = await websocket.receive()

            if message.get("type") == "websocket.disconnect":
                break

            # Binary audio chunk
            if message.get("bytes") is not None:
                audio_chunk = message["bytes"]

                if not audio_chunk:
                    continue

                try:
                    transcript = audio_service.transcribe(
                        audio_chunk,
                        suffix=".webm",
                    )

                    transcript = transcript.strip()

                    if transcript:
                        masked_text = mask_pii(transcript)
                        speaker = diarization_service.identify_speaker()

                        session_service.save_transcript(
                            session_id,
                            masked_text,
                        )

                        await websocket.send_json({
                            "type": "transcript",
                            "session_id": session_id,
                            "speaker": speaker,
                            "text": masked_text,
                            "source": "audio",
                        })
                    else:
                        await websocket.send_json({
                            "type": "audio_received",
                            "session_id": session_id,
                            "bytes": len(audio_chunk),
                            "transcript": "",
                        })

                except Exception as exc:
                    await websocket.send_json({
                        "type": "audio_error",
                        "session_id": session_id,
                        "error": str(exc),
                    })

            # Text message / transcript
            elif message.get("text") is not None:
                text = message["text"].strip()

                if text.lower() == "stop":
                    transcript = session_service.get_transcript(session_id)

                    analysis = None

                    if transcript:
                        conversation = "\n".join(
                            f"{item.get('speaker', 'unknown')}: {item.get('text', '')}"
                            for item in transcript
                        )

                        try:
                            analysis = analyze_sales_conversation(
                                conversation
                            ).model_dump()
                        except Exception:
                            analysis = None

                    await websocket.send_json({
                        "type": "analysis",
                        "session_id": session_id,
                        "transcript_count": len(transcript),
                        "analysis": analysis,
                    })

                    await websocket.send_json({
                        "type": "stopped",
                        "session_id": session_id,
                    })
                    break

                if not text:
                    continue

                masked_text = mask_pii(text)

                # Optional client-provided speaker:
                # {"text": "...", "speaker": "customer"}
                speaker = diarization_service.identify_speaker()

                session_service.save_transcript(
                    session_id,
                    masked_text,
                )

                await websocket.send_json({
                    "type": "transcript",
                    "session_id": session_id,
                    "speaker": speaker,
                    "text": masked_text,
                    "source": "text",
                })

    except WebSocketDisconnect:
        pass

