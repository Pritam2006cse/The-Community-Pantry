from google.adk.agents import Agent
from ...configs.settings import MODEL_NAME
from .prompt import VOLUNTEER_AGENT_PROMPT
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

volunteer_tools = MCPToolset(
    connection_params = StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[
                "-m",
                "mcp_servers.volunteer_server.server",
            ]
        )
    )
)

volunteer_agent = Agent(
    name = "volunteer_agent",
    model = MODEL_NAME,
    instruction = VOLUNTEER_AGENT_PROMPT,
    description = "Assigns the best volunteer for pickup"
)