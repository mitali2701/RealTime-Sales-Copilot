from typing import List, Literal

from pydantic import BaseModel, Field


class SalesAnalysis(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    intent: str
    entities: List[str] = Field(default_factory=list)
    objections: List[str] = Field(default_factory=list)
    buying_signals: List[str] = Field(default_factory=list)
    next_questions: List[str] = Field(default_factory=list)
    suggested_response: str
    product_recommendation: str
    lead_score: int = Field(ge=0, le=100)
    summary: str
