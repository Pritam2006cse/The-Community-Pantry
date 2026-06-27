import json
from pathlib import Path
from datetime import datetime
from shared.schemas import FoodAnalysis

RULES_PATH = Path(__file__).resolve().parents[2]/"database"/"food_rules.json"
def load_food_rules():
    with open(RULES_PATH,'r',encoding="utf-8") as f:
        return json.load(f)

def storage_guidelines(category:str):
    rules = load_food_rules()
    if category not in rules:
        return {"error":f"Unknown food category:{category}"}
    data = rules[category]
    return {
        "category": category,
        "storage_temperature": data["storage"],
        "notes": data["notes"]
}

def validate_food_data(category, prepared_time, storage):
    missing = []
    if not category:
        missing.append("category")
    if not prepared_time:
        missing.append("prepared_time")
    if not storage:
        missing.append("storage")
    return {
        "valid": len(missing) == 0,
        "missing": missing
    }

def calculate_pickup_priority(remaining_hours:float):
    if remaining_hours<=0:
        return "Critical"
    elif remaining_hours<1:
        return "Urgent"
    elif remaining_hours<3:
        return "High"
    elif remaining_hours<6:
        return "Medium"
    else:
        return "Low"

def estimate_safe_window(category:str,prepared_time:datetime,storage:str):
    rules = load_food_rules()
    if category not in rules:
        return {"error":f"Unknown food category:{category}"}
    rule = rules[category]
    if storage == "Room Temperature":
        allowed_hours = rule["room_temperature_hours"]
    elif storage == "Refrigerated":
        allowed_hours = rule["refrigerated_hours"]
    else:
        return {"error":f"Unknown storage type:{storage}"}
    current_time = datetime.now()
    elapsed_hours = (current_time - prepared_time).total_seconds()/3600
    remaining_hours = allowed_hours - elapsed_hours
    safe = remaining_hours>0
    if not safe:
        recommendation = "Do not distribute. Dispose it safely."
    elif remaining_hours<1:
        recommendation = "Immediate pickup required."
    elif remaining_hours<3:
        recommendation = "Schedule pickup very soon."
    else:
        recommendation = "Safe for donation. Pickup can be scheduled normally."
    return FoodAnalysis(
        category=category,
        safe=safe,
        elapsed_hours=round(elapsed_hours, 2),
        remaining_hours=round(max(0, remaining_hours), 2),
        risk_level=rule["risk_level"],
        pickup_priority=calculate_pickup_priority(remaining_hours),
        storage_temperature=rule["storage_temperature"],
        recommendation=recommendation,
        notes=rule["notes"],
    )

