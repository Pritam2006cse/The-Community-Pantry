from datetime import datetime
from typing import Literal, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum


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

class NGORecomendation(BaseModel):
    ngo_name: str
    total_score: int
    score_breakdown: Dict[str, int]
    distance_km: float
    available_capacity: int
    has_refrigeration: bool
    accepted: bool
    reasons: list[str]

class VolunteerRecommendation(BaseModel):
    volunteer_name: str
    total_score: int
    score_breakdown: Dict[str, int]
    distance_km: float
    vehicle: str
    max_capacity: int
    rating: float
    reasons: List[str]

class RescueStatus(str, Enum):
    CREATED = "CREATED"
    FOOD_VERIFIED = "FOOD_VERIFIED"
    NGO_SELECTED = "NGO_SELECTED"
    VOLUNTEER_ASSIGNED = "VOLUNTEER_ASSIGNED"
    PICKUP_PLANNED = "PICKUP_PLANNED"
    COMPLETED = "COMPLETED"

class RescuePlan(BaseModel):
    donation: Donation
    food_analysis: Optional[FoodAnalysis] = None
    recommended_ngos: list[NGORecomendation] = []
    assigned_volunteer: Optional[VolunteerRecommendation] = None
    estimated_pickup_time: Optional[float] = None
    status: RescueStatus = RescueStatus.CREATED 