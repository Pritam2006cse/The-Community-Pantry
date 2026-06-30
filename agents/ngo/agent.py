from google.adk.agents import Agent
from configs.settings import MODEL_NAME
from .prompt import NGO_AGENT_PROMPT


ngo_agent = Agent(
    name = "ngo_agent",
    model = MODEL_NAME,
    instruction = NGO_AGENT_PROMPT,
    description = "Matches food donations with suitable NGOs."
)