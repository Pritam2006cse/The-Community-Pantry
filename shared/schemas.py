from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class Donation(BaseModel):
    food_name: str = Field(..., description="Original food name given by the donor.")
    quantity: int = Field(..., gt=0)
    unit: str = Field(..., description="Unit of measurement")
    prepared_time: datetime
    storage: Literal["Room Temperature", "Refrigerated", "Frozen"]


class FoodClassification(BaseModel):
    food_name: str
    category: Literal[
        "Cooked Rice",
        "Cooked Meat",
        "Cooked Vegetables",
        "Dairy",
        "Bakery",
        "Fresh Fruit",
        "Beverage",
        "Dry Food",
        "Other",
    ]
    contains_meat: bool
    contains_dairy: bool
    high_risk: bool


class FoodAnalysis(BaseModel):
    category: str
    safe: bool
    elapsed_hours: float
    remaining_hours: float
    risk_level: str
    pickup_priority: str
    storage_temperature: str
    recommendation: str
    notes: Optional[str] = None