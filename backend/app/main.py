from fastapi import FastAPI

from app.api.v1.transcribe import router as transcribe_router
from app.api.v1.analyze import router as analyze_router
from app.api.v1.analyze_audio import router as analyze_audio_router
from app.api.v1.websocket import router as websocket_router

app = FastAPI(
    title="SalesAI API",
    description="Real-Time AI Sales Intelligence Platform",
    version="1.0.0",
)

app.include_router(
    transcribe_router,
    prefix="/api/v1",
)

app.include_router(
    analyze_router,
    prefix="/api/v1",
)

app.include_router(
    analyze_audio_router,
    prefix="/api/v1",
)

app.include_router(
    websocket_router,
    prefix="/api/v1",
)


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "salesai-backend",
        "version": "1.0.0",
    }
