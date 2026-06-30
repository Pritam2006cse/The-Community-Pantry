from google.adk.agents import Agent
from configs.settings import MODEL_NAME
from agents.volunteer.prompt import VOLUNTEER_AGENT_PROMPT

volunteer_agent = Agent(
    name = "volunteer_agent",
    model = MODEL_NAME,
    instruction = VOLUNTEER_AGENT_PROMPT,
    description = "Assigns the best volunteer for pickup"
)