from mcp_servers.volunteer_server.tools import get_suggested_volunteers
from shared.schemas import RescuePlan, RescueStatus, Donation
from mcp_servers.food_server.tools import estimate_safe_window
from mcp_servers.ngo_server.tools import find_matching_ngos
from mcp_servers.logistics_server.tools import create_logistic_plan

class RescueService:
    def create_plan(self,donation:Donation,food_category,donor_lat,donor_lon):
        plan = RescuePlan(donation=donation)
        food_analysis = estimate_safe_window(food_category,prepared_time=donation.prepared_time,storage=donation.storage)
        plan.food_analysis = food_analysis
        if not food_analysis.safe:
            return plan
        plan.status = RescueStatus.FOOD_VERIFIED
        ngo_recomended = find_matching_ngos(food_category,donation.quantity,donation.storage=="Refrigerated",donor_lat,donor_lon)
        plan.recommended_ngos = ngo_recomended
        plan.status = RescueStatus.NGO_SELECTED
        volunteer_recommended = get_suggested_volunteers(donation.quantity,donor_lat,donor_lon)
        if volunteer_recommended:
            plan.assigned_volunteer = volunteer_recommended[0]
            plan.status = RescueStatus.VOLUNTEER_ASSIGNED
            if ngo_recomended:
                plan.logistics_plan = create_logistic_plan(
                    donor_lat, donor_lon,
                    ngo_recomended[0],
                    volunteer_recommended[0],
                    food_analysis
                )
                plan.status = RescueStatus.PICKUP_PLANNED
        return plan