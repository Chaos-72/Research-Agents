# web_researcher/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import os

root_agent = LlmAgent(
    name="web_researcher",
    model="gemini-2.0-flash",
    instruction="You are a world-class web researcher. Use the tavily_search tool to answer the task. Cite sources.",
    tools=[google_search]
)