"""Grocery list generation service."""
import json
from utils.llm_client import call_llm_json
from utils.prompts import GROCERY_SYSTEM, GROCERY_USER
from schemas.meal_schemas import GroceryListResponse


def generate_grocery_list(meal_plan: dict) -> GroceryListResponse:
    """Generate a consolidated grocery list from a meal plan."""
    meal_plan_json = json.dumps(meal_plan, indent=2)
    user_prompt = GROCERY_USER.format(meal_plan_json=meal_plan_json)

    result = call_llm_json(GROCERY_SYSTEM, user_prompt)

    return GroceryListResponse(
        items=result["items"],
        estimated_cost_inr=result.get("estimated_cost_inr"),
    )
