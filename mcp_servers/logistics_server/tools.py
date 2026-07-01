import math
from configs.scoring import AVERAGE_CITY_SPEED, PICKUP_BUFFER_MINUTES, MAX_PICKUP_DISTANCE
from shared.schemas import LogisticsPlan, FoodAnalysis
from datetime import datetime, timedelta

def calculate_distance(lat1,lon1,lat2,lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance 

def estimate_travel_time(distance_km):
    hours = distance_km/AVERAGE_CITY_SPEED
    minutes = hours*60 + PICKUP_BUFFER_MINUTES
    return minutes

def check_feasibility(travel_minutes, remaining_hours):
    remaining_minutes = remaining_hours * 60
    return travel_minutes<=remaining_minutes

def create_logistic_plan(donor_lat,donor_lon,ngo,volunteer,food_analysis):
    ngo_distance = calculate_distance(donor_lat,donor_lon,ngo.latitude,ngo.longitude)
    volunteer_distance = calculate_distance(donor_lat,donor_lon,volunteer.latitude,volunteer.longitude)
    total_distance = ngo_distance + volunteer_distance
    travel_time = estimate_travel_time(total_distance)
    feasible = check_feasibility(travel_time,food_analysis.remaining_hours)
    if feasible:
        recommendation = ("Pickup is feasible before food safety window expires.")
    else:
        recommendation = ("Pickup is unlikely to complete before food expires.")
    pickup_time = datetime.now() + timedelta(minutes=travel_time)
    return LogisticsPlan(
        travel_distance_km = round(total_distance,1),
        estimated_travel_time_minutes = round(travel_time),
        estimated_pickup_time = pickup_time,
        feasible = feasible,
        recommendation=recommendation,
    )