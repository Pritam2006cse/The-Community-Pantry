from datetime import datetime, timedelta

from services.rescue_service import RescueService
from shared.schemas import Donation


def main():

    donation = Donation(
        food_name="Veg Biryani",
        quantity=120,
        unit="plates",
        prepared_time=datetime.now() - timedelta(hours=1),
        storage="Refrigerated",
    )

    service = RescueService()

    plan = service.create_plan(
        donation=donation,
        food_category="Cooked Rice",
        donor_lat=22.5743,
        donor_lon=88.3664,
    )

    print("\n========== RESCUE PLAN ==========")

    print(f"\nFood: {plan.donation.food_name}")
    print(f"Quantity: {plan.donation.quantity} {plan.donation.unit}")

    print("\nFood Analysis")
    print(plan.food_analysis)

    print("\nRecommended NGOs")
    for ngo in plan.recommended_ngos:
        print(f"- {ngo.ngo_name} | Score: {ngo.total_score}")

    print("\nAssigned Volunteer")
    print(plan.assigned_volunteer)

    print("\nLogistics Plan")
    print(plan.logistics_plan)

    print("\nStatus")
    print(plan.status)


if __name__ == "__main__":
    main()