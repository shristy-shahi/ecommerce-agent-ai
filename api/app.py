"""
FastAPI Application — Main entry point
Endpoints: /upload, /analyze, /query
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os

from agents.planner import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.recommendation_agent import RecommendationAgent
from tools.memory_tools import MemoryStore
from api.schemas import AnalyzeRequest, QueryRequest, AnalysisResponse

app = FastAPI(
    title="Agentic AI E-Commerce Analytics API",
    description="Multi-agent system for autonomous e-commerce data analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (use Redis in production)
_data_agent = DataAgent()
_memory = MemoryStore()

# Initialize LLM agents only if API key is available
_planner = None
_insight = None
_recommendation = None

def get_planner():
    global _planner
    if _planner is None:
        try:
            _planner = PlannerAgent()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return _planner

def get_insight_agent():
    global _insight
    if _insight is None:
        try:
            _insight = InsightAgent()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return _insight

def get_recommendation_agent():
    global _recommendation
    if _recommendation is None:
        try:
            _recommendation = RecommendationAgent()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return _recommendation


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Accept a CSV upload and load it into the Data Agent."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    # Save temporarily
    os.makedirs("data/uploads", exist_ok=True)
    path = f"data/uploads/{file.filename}"
    df.to_csv(path, index=False)
    _data_agent.load_data(path)
    return {
        "message": "Dataset uploaded successfully",
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns)
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalyzeRequest):
    """Run full multi-agent analysis pipeline."""
    if _data_agent.df is None:
        raise HTTPException(status_code=400, detail="No dataset loaded. Call /upload first.")

    # Check memory for similar past query
    past = _memory.search(request.query, k=1)
    if past and not request.force_refresh:
        return {"source": "memory", **past[0]["result"]}

    # Step 1: Plan
    schema = {col: str(dtype) for col, dtype in _data_agent.df.dtypes.items()}
    planner = get_planner()
    plan = planner.create_plan(request.query, schema)

    # Step 2: Data analysis
    eda_results = _data_agent.run_full_eda()

    # Step 3: Insights
    insight_agent = get_insight_agent()
    insights = insight_agent.generate_insights(eda_results)

    # Step 4: Recommendations
    recommendation_agent = get_recommendation_agent()
    recommendations = recommendation_agent.generate_recommendations(insights, eda_results)

    result = {
        "source": "live",
        "plan": plan,
        "eda": eda_results,
        "insights": insights,
        "recommendations": recommendations
    }

    # Store in memory
    _memory.add(request.query, result)

    return result


@app.post("/query")
async def natural_language_query(request: QueryRequest):
    """Natural language query handler — routes to appropriate analysis."""
    if _data_agent.df is None:
        raise HTTPException(status_code=400, detail="No dataset loaded.")

    # Semantic search in memory first
    past = _memory.search(request.question, k=3)

    # Use planner to route
    schema = {col: str(dtype) for col, dtype in _data_agent.df.dtypes.items()}
    planner = get_planner()
    plan = planner.create_plan(request.question, schema)

    return {
        "question": request.question,
        "plan": plan,
        "similar_past_queries": [p["query"] for p in past],
    }
