"""Pantry mode API routes."""
from fastapi import APIRouter, HTTPException
from schemas.meal_schemas import PantryRequest, PantryResponse
from services.pantry_service import generate_pantry_meals

router = APIRouter()


@router.post("/pantry-meals", response_model=PantryResponse)
def get_pantry_meals(request: PantryRequest):
    """Get meal suggestions based on available pantry ingredients."""
    try:
        return generate_pantry_meals(request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate pantry meals: {str(e)}")
