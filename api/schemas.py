"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import Optional, Any


class AnalyzeRequest(BaseModel):
    query: str = "Run full e-commerce analysis"
    force_refresh: bool = False


class QueryRequest(BaseModel):
    question: str


class AnalysisResponse(BaseModel):
    source: str
    plan: Optional[Any] = None
    eda: Optional[Any] = None
    insights: Optional[str] = None
    recommendations: Optional[str] = None
