from google.adk.agents import Agent
from .prompt import LOGISTICS_AGENT_PROMPT
from ...configs.settings import MODEL_NAME
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

logistic_tools = MCPToolset(
    connection_params = StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[
                "-m",
                "mcp_servers.logistics_server.server",
            ]
        )
    )
)
logistic_agent = Agent(
    name = "logistic_agent",
    model = MODEL_NAME,
    instruction = LOGISTICS_AGENT_PROMPT,
    description = "Plans food pickup logistics.",
    tools = [logistic_tools]
)