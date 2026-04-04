"""
AI Indian Meal Planner + Grocery Optimizer - FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.meal_routes import router as meal_router
from routes.grocery_routes import router as grocery_router
from routes.pantry_routes import router as pantry_router
from models.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Indian Meal Planner",
    description="Plan weekly Indian meals, generate grocery lists, and optimize with pantry ingredients.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meal_router, prefix="/api", tags=["Meal Plan"])
app.include_router(grocery_router, prefix="/api", tags=["Grocery List"])
app.include_router(pantry_router, prefix="/api", tags=["Pantry Mode"])


@app.get("/")
def root():
    return {"message": "AI Indian Meal Planner API is running 🍛"}
