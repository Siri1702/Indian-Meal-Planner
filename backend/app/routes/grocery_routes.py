"""Grocery list API routes."""
from fastapi import APIRouter, HTTPException
from schemas.meal_schemas import MealPlanResponse, GroceryListResponse
from services.grocery_service import generate_grocery_list

router = APIRouter()


@router.post("/generate-grocery-list", response_model=GroceryListResponse)
def create_grocery_list(meal_plan: MealPlanResponse):
    """Generate a consolidated grocery list from an existing meal plan."""
    try:
        return generate_grocery_list(meal_plan.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate grocery list: {str(e)}")
