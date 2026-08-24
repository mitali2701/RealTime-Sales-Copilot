from pydantic import BaseModel, Field
from typing import List


class Entity(BaseModel):
    name: str
    type: str


class SalesAnalysis(BaseModel):
    sentiment: str
    intent: str
    entities: List[Entity] = Field(default_factory=list)
    objections: List[str] = Field(default_factory=list)
    buying_signals: List[str] = Field(default_factory=list)
    next_questions: List[str] = Field(default_factory=list)
    suggested_response: str
    product_recommendation: str
    lead_score: int = Field(ge=0, le=100)
    summary: str
