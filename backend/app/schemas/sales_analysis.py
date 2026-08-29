from pydantic import BaseModel, Field


class SalesAnalysis(BaseModel):
    summary: str
    sentiment: str
    intent: str
    entities: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    buying_signals: list[str] = Field(default_factory=list)
    suggested_response: str
    next_questions: list[str] = Field(default_factory=list)
    lead_score: int = Field(ge=0, le=100)
