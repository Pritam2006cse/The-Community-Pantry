import asyncio
from mcp.server.fastmcp import FastMCP
from mcp_servers.ngo_server.tools import find_matching_ngos

mcp = FastMCP(
    name = "NGO Recommendation MCP"
)

@mcp.tool()
def recommend_ngo(category:str,quantity:int,refrigeration_required:bool,donor_lat:float,donor_lon:float):
    result = find_matching_ngos(category,quantity,refrigeration_required,donor_lat,donor_lon)
    return result

if __name__ == "__main__":
    print("NGO recommendation MCP Server Starting...")
    asyncio.run(mcp.run())
