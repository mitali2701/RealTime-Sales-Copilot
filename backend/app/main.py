from fastapi import FastAPI

from app.api.v1.analyze import router as analyze_router
from app.api.v1.health import router as health_router
from app.api.v1.transcribe import router as transcribe_router


app = FastAPI(
    title="SalesAI API",
    version="1.0.0",
    description="Real-Time AI Sales Intelligence Platform",
)

app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    analyze_router,
    prefix="/api/v1",
)

app.include_router(
    transcribe_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "SalesAI API is running",
        "version": "1.0.0",
    }
