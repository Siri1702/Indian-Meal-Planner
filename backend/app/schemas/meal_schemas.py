"""Pydantic schemas for request/response validation."""
from typing import Optional
from pydantic import BaseModel, Field


class MealPlanRequest(BaseModel):
    goal: str = Field(..., description="Health goal: fat_loss, muscle_gain, or maintenance")
    diet: str = Field(..., description="Diet type: veg, non_veg, or eggetarian")
    calories: Optional[int] = Field(None, ge=1000, le=5000, description="Daily calorie target")
    budget: Optional[int] = Field(None, ge=500, le=10000, description="Weekly budget in INR")


class MacroInfo(BaseModel):
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float


class Meal(BaseModel):
    dish_name: str
    ingredients: list[str]
    macros: MacroInfo


class DayPlan(BaseModel):
    day: str
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snack: Meal


class MealPlanResponse(BaseModel):
    goal: str
    diet: str
    target_calories: Optional[int]
    budget_inr: Optional[int]
    days: list[DayPlan]
    daily_macro_summary: MacroInfo


class GroceryItem(BaseModel):
    name: str
    quantity: str
    category: str


class GroceryListResponse(BaseModel):
    items: list[GroceryItem]
    estimated_cost_inr: Optional[int] = None


class PantryRequest(BaseModel):
    ingredients: list[str] = Field(..., min_length=1, description="Available pantry ingredients")


class PantryMeal(BaseModel):
    dish_name: str
    ingredients_used: list[str]
    additional_ingredients: list[str]
    macros: MacroInfo


class PantryResponse(BaseModel):
    meals: list[PantryMeal]
