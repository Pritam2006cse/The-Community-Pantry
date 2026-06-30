from mcp.server.fastmcp import FastMCP
import asyncio
from mcp_servers.volunteer_server.tools import get_suggested_volunteers

mcp = FastMCP(
    name = "Volunteer Assignment MCP"
)

@mcp.tool()
def recommend_volunteer(donation, donor_lat,donor_lon):
    return get_suggested_volunteers(donation,donor_lat,donor_lon)

if __name__ == "__main__":
    asyncio.run(mcp.run())