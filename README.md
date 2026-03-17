# 🚀 Agentic AI E-Commerce Analytics System

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-0.1-purple?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> A multi-agent AI system that autonomously analyzes e-commerce sales data, detects business problems, generates insights, and recommends actions — all without human intervention.

---

## 🎯 What It Does

| Feature | Description |
|---|---|
| 📊 Autonomous EDA | Data Agent performs full exploratory analysis on upload |
| 🗺️ Task Planning | Planner Agent decomposes queries into execution steps |
| 💡 LLM Insights | Insight Agent generates natural language findings |
| 🎯 Recommendations | Recommendation Agent suggests prioritized actions |
| 🧠 Memory | FAISS vector store remembers past queries and results |
| 💬 NL Queries | Ask "Why did sales drop in Q3?" in plain English |

---

## 🏗️ Architecture

```
User Query / CSV Upload
        ↓
   FastAPI Backend
        ↓
   Planner Agent  ──→  Creates step-by-step plan
        ↓
   Data Agent     ──→  EDA, cleaning, aggregations
        ↓
   Insight Agent  ──→  LLM-generated findings
        ↓
Recommendation Agent ──→ Business strategies
        ↓
  Dashboard + API Response
```

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/ecommerce-agent-ai
cd ecommerce-agent-ai
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run API
```bash
uvicorn api.app:app --reload --port 8000
```

### 4. Open Dashboard
Open `dashboard/index.html` in your browser.

### 5. Run with Docker
```bash
docker-compose up --build
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Upload CSV dataset |
| POST | `/analyze` | Run full agent pipeline |
| POST | `/query` | Natural language query |

### Example Usage
```bash
# Upload dataset
curl -X POST http://localhost:8000/upload \
  -F "file=@data/sample_dataset.csv"

# Run analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Why did sales drop in North region?"}'
```

---

## 🧩 Project Structure
```
ecommerce-agent-ai/
├── agents/
│   ├── planner.py           # Task decomposition
│   ├── data_agent.py        # Pandas EDA & cleaning
│   ├── insight_agent.py     # LLM insights + reflection
│   └── recommendation_agent.py
├── tools/
│   ├── data_tools.py        # Reusable data utilities
│   ├── visualization_tools.py # Plotly charts
│   └── memory_tools.py      # FAISS vector store
├── api/
│   ├── app.py               # FastAPI app
│   └── schemas.py           # Pydantic models
├── data/
│   └── sample_dataset.csv
├── dashboard/
│   └── index.html           # Interactive UI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- **AI**: LangGraph, LangChain, OpenAI GPT-4o
- **Backend**: FastAPI, Uvicorn, Python 3.11
- **Data**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly, Dash
- **Memory**: FAISS vector store
- **Deployment**: Docker, AWS ECS / GCP Cloud Run

---

## 📝 Resume Description

> *"Developed an Agentic AI-powered E-commerce Analytics System using LangGraph and FastAPI that autonomously analyzes sales data, generates insights, and recommends business strategies using multi-agent collaboration."*

---

## 📄 License

MIT License — free to use and modify.
