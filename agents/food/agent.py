from google.adk.agents import Agent
from configs.settings import MODEL_NAME
from .prompt import FOOD_AGENT_PROMPT
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

food_agent = Agent(
    name = "food_agent",
    model = MODEL_NAME,
    instruction = FOOD_AGENT_PROMPT,
    description = "Evaluates donated food and provides food safety recommendations" 
)