from .prompt import COORDINATOR_PROMPT
from google.adk.agents import Agent
from ...configs.settings import MODEL_NAME
from ..food.agent import food_agent
from ..ngo.agent import ngo_agent
from ..volunteer.agent import volunteer_agent

coordinator_agent = Agent(
    name = "coordinator_agent",
    model = MODEL_NAME,
    instruction = COORDINATOR_PROMPT,
    description = "Coordinates the food rescue workflow",
    sub_agents = [food_agent, ngo_agent,volunteer_agent],
)