"""Meal plan generation service."""
import json
from utils.llm_client import call_llm_json
from utils.prompts import MEAL_PLAN_SYSTEM, MEAL_PLAN_USER
from schemas.meal_schemas import MealPlanRequest, MealPlanResponse


# Default calorie targets by goal
DEFAULT_CALORIES = {
    "fat_loss": 1600,
    "muscle_gain": 2500,
    "maintenance": 2000,
}


def generate_meal_plan(request: MealPlanRequest) -> MealPlanResponse:
    """Generate a 7-day Indian meal plan using AI."""
    calories = request.calories or DEFAULT_CALORIES.get(request.goal, 2000)
    budget = request.budget or 3000  # Default weekly budget in INR

    user_prompt = MEAL_PLAN_USER.format(
        goal=request.goal.replace("_", " "),
        diet=request.diet.replace("_", " "),
        calories=calories,
        budget=budget,
    )

    result = call_llm_json(MEAL_PLAN_SYSTEM, user_prompt)

    return MealPlanResponse(
        goal=request.goal,
        diet=request.diet,
        target_calories=calories,
        budget_inr=budget,
        days=result["days"],
        daily_macro_summary=result.get("daily_macro_summary", {
            "calories": calories,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
        }),
    )
