import asyncio
from mcp.server.fastmcp import FastMCP
from mcp_servers.logistics_server.tools import create_logistic_plan

mcp = FastMCP(
    name = "Logistics Optimization MCP"
)

@mcp.tool()
def recommend_logistic(donor_lat,donor_lon,ngo,volunteer,food_analysis):
    return create_logistic_plan(donor_lat,donor_lon,ngo,volunteer,food_analysis)

if __name__ == "__main__":
    print("Logistics Optimization MCP Server Starting...")
    asyncio.run(mcp.run())