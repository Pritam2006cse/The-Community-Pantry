import json
import math
from pathlib import Path
from datetime import datetime
from shared.schemas import NGORecomendation
from configs.scoring import CATEGORY_WEIGHT,CAPACITY_WEIGHT,REFRIGERATION_WEIGHT,DISTANCE_WEIGHT

RULES_PATH = Path(__file__).resolve().parents[2]/"database"/"ngo_data.json"
def load_ngos():
    with open(RULES_PATH,'r',encoding="utf-8") as f:
        return json.load(f)

def calculate_distance(lat1,lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance 

def distance_score(distance):
    if distance <= 5:
        return 15
    elif distance <= 10:
        return 10
    elif distance <= 15:
        return 5
    else:
        return 0

def calculate_ngo_score(ngo,category,quantity,refrigeration_required,donor_lat,donor_lon):
    score_breakdown = {}
    reasons = []
    if category not in ngo["accepted_categories"]:
        return None
    score_breakdown["category"] = CATEGORY_WEIGHT
    reasons.append(f"Accepts this category.")

    if ngo["available_capacity"]< quantity:
        return None
    capacity_ratio = quantity / ngo["available_capacity"]
    capacity_score = int(CAPACITY_WEIGHT * (1 - capacity_ratio))
    capacity_score = min(CAPACITY_WEIGHT,max(5, capacity_score))
    score_breakdown["capacity"] = capacity_score
    reasons.append(
        f"Available capacity: {ngo['available_capacity']} meals."
    )

    if refrigeration_required and ngo["has_refrigeration"]:
        score_breakdown["refrigeration"] = REFRIGERATION_WEIGHT
        reasons.append(f"Has refrigeration.")
    elif refrigeration_required and not ngo["has_refrigeration"]:
        return None
    else:
        score_breakdown["refrigeration"] = REFRIGERATION_WEIGHT
        reasons.append(f"No refrigeration required.")
    
    distance = round(calculate_distance(donor_lat,donor_lon,ngo["latitude"],ngo["longitude"]),2)
    score_breakdown["distance"] = distance_score(distance)
    reasons.append(f"Distance is {distance} km.")

    total_score = sum(score_breakdown.values())
    return NGORecomendation(
        ngo_name = ngo["name"],
        total_score = total_score,
        score_breakdown = score_breakdown,
        distance_km = distance,
        available_capacity = ngo["available_capacity"],
        has_refrigeration = ngo["has_refrigeration"],
        accepted = True,
        reasons = reasons
    )
    
def find_matching_ngos(
    category,
    quantity,
    refrigeration_required,
    donor_lat,
    donor_lon,
):
    ngos = load_ngos()
    recommendations = []
    for ngo in ngos:
        recommendation = calculate_ngo_score(
            ngo=ngo,
            category=category,
            quantity=quantity,
            refrigeration_required=refrigeration_required,
            donor_lat=donor_lat,
            donor_lon=donor_lon,
        )
        if recommendation is not None:
            recommendations.append(recommendation)
    recommendations.sort(
        key=lambda ngo: ngo.total_score,
        reverse=True,
    )
    return recommendations