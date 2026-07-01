from services.rescue_service import RescueService
from shared.schemas import Donation

from datetime import datetime


def main():

    donation = Donation(
        food_name="Veg Biryani",
        quantity=120,
        unit="plates",
        prepared_time=datetime.now(),
        storage="Refrigerated",
    )

    service = RescueService()

    plan = service.create_plan(
        donation=donation,
        food_category="Cooked Rice",
        donor_lat=22.5726,
        donor_lon=88.3639,
    )

    print(plan.logistics_plan)


if __name__ == "__main__":
    main()