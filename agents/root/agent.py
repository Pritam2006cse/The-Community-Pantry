from google.adk.agents import Agent
from .prompt import ROOT_AGENT_PROMPT
from ...configs.settings import MODEL_NAME
from ..coordinator.agent import coordinator_agent

root_agent = Agent(
    name="root_agent",
    model=MODEL_NAME,
    instruction=ROOT_AGENT_PROMPT,
    description="The Root Agent for The Community Pantry",
    sub_agents = [
        coordinator_agent
    ]
)