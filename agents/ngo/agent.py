from google.adk.agents import Agent
from ...configs.settings import MODEL_NAME
from .prompt import NGO_AGENT_PROMPT
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

ngo_tools = MCPToolset(
    connection_params = StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[
                "-m",
                "mcp_servers.ngo_server.server",
            ]
        )
    )
)
ngo_agent = Agent(
    name = "ngo_agent",
    model = MODEL_NAME,
    instruction = NGO_AGENT_PROMPT,
    description = "Matches food donations with suitable NGOs."
)