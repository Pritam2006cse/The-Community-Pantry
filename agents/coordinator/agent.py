from .prompt import COORDINATOR_PROMPT
from google.adk.agents import Agent
from ...configs.settings import MODEL_NAME

coordinator_agent = Agent(
    name = "coordinator_agent",
    model = MODEL_NAME,
    instruction = COORDINATOR_PROMPT,
    description = "Coordinates the food rescue workflow"
)