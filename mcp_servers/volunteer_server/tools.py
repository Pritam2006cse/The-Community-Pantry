import math
import json
from pathlib import Path
from configs.scoring import AVAILABILITY_WEIGHT, VOLUNTEER_DISTANCE_WEIGHT, VEHICLE_WEIGHT, RATING_WEIGHT
from shared.schemas import VolunteerRecommendation, RescuePlan

VEHICLE_CAPACITY = {
    "Bike": 70,
    "Scooter": 50,
    "Car": 250,
    "Van": 600,
}

RULES_PATH = (Path(__file__).resolve().parents[2]/ "database"/ "volunteer_data.json")

def load_volunteers():
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def volunteer_distance_score(distance):
    if distance <=5:
        return 15
    elif distance <= 10:
        return 10
    elif distance <= 15:
        return 5
    else:
        return 0

def vehicle_score(vehicle,quantity):
    capacity = VEHICLE_CAPACITY.get(vehicle,0)
    if capacity < quantity:
        return None
    if vehicle == "Van":
        return 20
    elif vehicle == "Car":
        return 18
    elif vehicle == "Scooter":
        return 10
    elif vehicle == "Bike":
        return 15
    return 0

def rating_score(rating):
    return round((rating/5.0)*RATING_WEIGHT)

def calculate_distance(lat1,lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance 

def calculate_volunteer_score(volunteer,quantity,donor_lat,donor_lon):
    score_breakdown = {}
    reasons = []
    if not volunteer["available"]:
        return None
    score_breakdown["availability"] = AVAILABILITY_WEIGHT
    reasons.append("Volunteer available")
    distance = round(calculate_distance(donor_lat,donor_lon,volunteer["latitude"],volunteer["longitude"]),2)
    distance_score = volunteer_distance_score(distance)
    score_breakdown["distance"] = distance_score
    reasons.append(f"Distance: {distance} km")
    vehicle_points = vehicle_score(volunteer["vehicle"],quantity)
    if vehicle_points is None:
        return None
    score_breakdown["vehicle"] = vehicle_points
    reasons.append("Vehicle capacity sufficient")
    rate = rating_score(volunteer["rating"])
    score_breakdown["rating"] = rate
    reasons.append(f"Rating: {volunteer['rating']}/5")
    experience = experience_score(volunteer["completed_pickups"])
    score_breakdown["experience"]
    reasons.append(f"Completed pickups: {volunteer['completed_pickups']}")
    workload = workload_penalty(volunteer["active_pickups"])
    if workload:
        score_breakdown["workload_penalty"] = -workload
        reasons.append(f"Active pickups: {volunteer['active_pickups']}")
    total_score = sum(score_breakdown.values())
    return VolunteerRecommendation(
        volunteer_name=volunteer["name"],
        total_score=total_score,
        score_breakdown=score_breakdown,
        distance_km=distance,
        vehicle=volunteer["vehicle"],
        max_capacity=VEHICLE_CAPACITY.get(volunteer["vehicle"]),
        rating=volunteer["rating"],
        reasons=reasons
    )

def experience_score(completed_pickups):
    if completed_pickups >= 100:
        return 10
    elif completed_pickups >= 50:
        return 8
    elif completed_pickups >= 20:
        return 6
    elif completed_pickups >= 5:
        return 4
    return 2

def workload_penalty(active_pickups):
    if active_pickups == 0:
        return 0
    elif active_pickups >= 3:
        return -5
    elif active_pickups >= 4:
        return -8
    elif active_pickups >= 5:
        return -10
    return None

def get_suggested_volunteers(quantity,donor_lat,donor_lon):
    volunteers = load_volunteers()
    suggestions = []
    for vol in volunteers:
        rec = calculate_volunteer_score(vol,quantity,donor_lat,donor_lon)
        if rec:
            suggestions.append(rec)
    suggestions.sort(key=lambda x: x.total_score,reverse=True)
    return suggestions