# supervisor/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel
from typing import List
from web_researcher.agent import root_agent as web_researcher_agent
from academic_researcher.agent import root_agent as academic_researcher_agent
from twitter_pulse.agent import root_agent as twitter_pulse_agent
from fact_checker.agent import root_agent as fact_agent
from report_writer.agent import root_agent as report_agent

INSTRUCTION = """
You are the Research Supervisor for DeepResearch India — a world-class multi-agent AI research team.

Workflow (always follow this exact sequence):
1. Use web_researcher + academic_researcher + twitter_pulse in parallel
2. Send ALL their outputs to fact_checker
3. Finally send everything to report_writer

Available agents:
- web_researcher
- academic_researcher  
- twitter_pulse
- fact_checker
- report_writer

Be professional. No jokes. This is for CXO-level reports.
"""

root_agent = LlmAgent(  
    name="research_supervisor", 
    model="gemini-2.0-flash",
    description="Breaks research queries into delegated sub-tasks for specialist agents.",
    instruction=INSTRUCTION, 
    output_key="delegated_tasks", 
    tools=[
        AgentTool(agent = web_researcher_agent), 
        AgentTool(agent=academic_researcher_agent), 
        AgentTool(agent=twitter_pulse_agent),
        AgentTool(agent=fact_agent),
        AgentTool(agent=report_agent),

    ],  # connecting agents
)