from shared.schemas import RescuePlan, RescueStatus, Donation
from mcp_servers.food_server.tools import estimate_safe_window
#from mcp_servers.ngo_server.tools import calculate_ngo_score
from mcp_servers.ngo_server.tools import find_matching_ngos

class RescueService:
    def create_plan(self,donation:Donation,food_category,donor_lat,donor_lon):
        plan = RescuePlan(donation=donation)
        food_analysis = estimate_safe_window(food_category,prepared_time=donation.prepared_time,storage=donation.storage)
        plan.food_analysis = food_analysis
        plan.status = RescueStatus.FOOD_VERIFIED
        ngo_recomended = find_matching_ngos(food_category,donation.quantity,donation.storage=="Refrigerated",donor_lat,donor_lon)
        plan.recommended_ngos = ngo_recomended
        plan.status = RescueStatus.NGO_SELECTED
        return plan