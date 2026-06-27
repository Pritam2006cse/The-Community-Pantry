from google.adk.agents import Agent
from configs.settings import MODEL_NAME
from .prompt import FOOD_AGENT_PROMPT

food_agent = Agent(
    name = "food_agent",
    model = MODEL_NAME,
    instruction = FOOD_AGENT_PROMPT,
    description = "Evaluates donated food and provides food safety recommendations" 
)