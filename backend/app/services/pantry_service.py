"""Pantry-based meal suggestion service."""
from utils.llm_client import call_llm_json
from utils.prompts import PANTRY_SYSTEM, PANTRY_USER
from schemas.meal_schemas import PantryRequest, PantryResponse


def generate_pantry_meals(request: PantryRequest) -> PantryResponse:
    """Suggest meals based on available pantry ingredients."""
    if not request.ingredients:
        raise ValueError("Please provide at least one pantry ingredient.")

    ingredients_str = ", ".join(request.ingredients)
    user_prompt = PANTRY_USER.format(ingredients=ingredients_str)

    result = call_llm_json(PANTRY_SYSTEM, user_prompt)

    return PantryResponse(meals=result["meals"])
