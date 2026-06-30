from mcp.server.fastmcp import FastMCP
import asyncio
from mcp_servers.volunteer_server.tools import get_suggested_volunteers

mcp = FastMCP(
    name = "Volunteer Assignment MCP"
)

@mcp.tool()
def recommend_volunteer(quantity, donor_lat,donor_lon):
    return get_suggested_volunteers(quantity,donor_lat,donor_lon)

if __name__ == "__main__":
    asyncio.run(mcp.run())