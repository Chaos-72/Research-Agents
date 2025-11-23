# fact_checker/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="fact_checker",
    model="gemini-2.0-flash",
    instruction="""
        You are the Fact-Checker. Your only job:
        - Take any claim
        - Use google_search tool multiple times if needed
        - Return: VERIFIED / FALSE / MISLEADING / UNVERIFIED
        - Cite exact sources with dates
        - Be ruthless and neutral
    """,
    tools=[google_search]
)