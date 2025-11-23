# academic_researcher/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def scholar_search(query: str) -> str:
    """Search Google Scholar for papers, patents, and academic sources. Returns titles, authors, abstracts, DOIs."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return "Error: SERPAPI_KEY not set in .env"
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": api_key,
        "num": 5  # Top 5 results
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error: API request failed ({response.status_code})"
    
    data = response.json()
    if 'organic_results' not in data:
        return "No results found."
    
    formatted = []
    for result in data['organic_results']:
        formatted.append(f"Title: {result.get('title', 'N/A')}\nAuthors: {result.get('authors', 'N/A')}\nAbstract: {result.get('publication_info', {}).get('summary', 'N/A')[:500]}...\nDOI/Cite: {result.get('link', 'N/A')}\n---")
    return "\n".join(formatted)

scholar_search = FunctionTool(func=scholar_search)


root_agent = LlmAgent(
    name="academic_researcher",
    model="gemini-2.0-flash",  # Or 1.5-flash
    instruction="You are an academic expert. Use scholar_search to find and summarize papers/patents. Cite DOIs/authors.",
    tools=[scholar_search]
)