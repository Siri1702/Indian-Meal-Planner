"""SQLAlchemy models for meal plans."""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from models.database import Base


class MealPlanRecord(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, nullable=False)
    diet = Column(String, nullable=False)
    calories = Column(Integer, nullable=True)
    budget = Column(Integer, nullable=True)
    plan_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def get_plan(self) -> dict:
        return json.loads(self.plan_json)
