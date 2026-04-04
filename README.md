# 🍛 AI Indian Meal Planner + Grocery Optimizer

A production-quality MVP that helps you plan weekly Indian meals based on health goals, generate smart grocery lists, and cook with pantry ingredients — all powered by AI.

## 📁 Project Structure

```
ai-indian-meal-planner/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routes/               # API route handlers
│   │   │   ├── meal_routes.py
│   │   │   ├── grocery_routes.py
│   │   │   └── pantry_routes.py
│   │   ├── services/             # Business logic
│   │   │   ├── meal_service.py
│   │   │   ├── grocery_service.py
│   │   │   └── pantry_service.py
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── database.py
│   │   │   └── meal_plan.py
│   │   ├── schemas/              # Pydantic schemas
│   │   │   └── meal_schemas.py
│   │   └── utils/                # Prompts & LLM client
│   │       ├── prompts.py
│   │       └── llm_client.py
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- An OpenAI API key (or any OpenAI-compatible API)

### 1. Clone / Download the project

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
export OPENAI_API_KEY="sk-your-key-here"
# Optional: use a different model or base URL
export LLM_MODEL="gpt-3.5-turbo"
export OPENAI_BASE_URL=""  # Leave empty for OpenAI, or set for compatible APIs
```

Windows:
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

### 4. Run the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 5. Frontend Setup (new terminal)

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens at: http://localhost:8501

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📋 Meal Planner | 7-day plan with breakfast, lunch, dinner, snack |
| 🛒 Grocery List | Aggregated, deduplicated, categorized ingredients |
| 🏠 Pantry Mode | Suggest meals from your available ingredients |
| 📊 Macro Tracking | Calories, protein, carbs, fat per meal |
| 💰 Budget Aware | Cost-conscious meal planning in INR |
| 🇮🇳 Indian Focus | All meals are Indian home-cooked recipes |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate-meal-plan` | Generate 7-day meal plan |
| POST | `/api/generate-grocery-list` | Generate grocery list from plan |
| POST | `/api/pantry-meals` | Get meal ideas from pantry items |

## 🧠 AI Configuration

The app uses LangChain with OpenAI-compatible APIs. You can use:
- **OpenAI** (default): Set `OPENAI_API_KEY`
- **Azure OpenAI**: Set `OPENAI_BASE_URL` to your Azure endpoint
- **Local LLMs** (Ollama, LM Studio): Set `OPENAI_BASE_URL=http://localhost:11434/v1`
- **Groq, Together, etc.**: Set the appropriate base URL and API key

## 📝 License

MIT
