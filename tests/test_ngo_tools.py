from mcp_servers.ngo_server.tools import calculate_ngo_score
#from mcp_servers.ngo_server.tools import find_matching_ngo
from mcp_servers.ngo_server.tools import load_ngos
ngos = load_ngos()
ngo = ngos[0]
result = calculate_ngo_score(
    ngo,
    category="Cooked Rice",
    quantity=150,
    refrigeration_required=True,
    donor_lat=20.3000,
    donor_lon=85.8200,
)

for ngo in result:
    print(ngo)