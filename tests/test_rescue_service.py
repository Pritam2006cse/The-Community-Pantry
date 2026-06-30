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
        donor_lat=20.3000,
        donor_lon=85.8200,
    )

    print(plan)


if __name__ == "__main__":
    main()