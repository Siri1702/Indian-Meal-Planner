"""Meal plan API routes."""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.meal_schemas import MealPlanRequest, MealPlanResponse
from services.meal_service import generate_meal_plan
from models.database import get_db
from models.meal_plan import MealPlanRecord

router = APIRouter()


@router.post("/generate-meal-plan", response_model=MealPlanResponse)
def create_meal_plan(request: MealPlanRequest, db: Session = Depends(get_db)):
    """Generate a 7-day Indian meal plan based on health goals and diet preferences."""
    try:
        plan = generate_meal_plan(request)

        # Save to database
        record = MealPlanRecord(
            goal=request.goal,
            diet=request.diet,
            calories=request.calories,
            budget=request.budget,
            plan_json=plan.model_dump_json(),
        )
        db.add(record)
        db.commit()

        return plan
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate meal plan: {str(e)}")
