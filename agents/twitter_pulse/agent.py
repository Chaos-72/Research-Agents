# twitter_pulse/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import requests
import os, time, requests
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


# Cache results for 10 minutes
@lru_cache(maxsize=32)
def cached_response(query):
    return time.time(), None


def x_sentiment_search(query: str) -> str:
    """Real-time X fetch with caching + backoff + fallback search."""
    bearer_token = os.getenv("X_BEARER_TOKEN")
    if not bearer_token:
        return "Error: X_BEARER_TOKEN missing"

    # Check if cached
    ts, cached = cached_response(query)
    if cached and time.time() - ts < 600:  # 10 minutes
        return cached

    headers = {"Authorization": f"Bearer {bearer_token}"}

    url = "https://api.twitter.com/2/tweets/search/recent"
    # Simplified, lighter query
    full_query = f"({query}) lang:en -is:retweet"

    params = {
        "query": full_query,
        "tweet.fields": "created_at,public_metrics",
        "max_results": 10
    }

    # Try with backoff
    for attempt in range(3):
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            tweets = data.get("data", [])
            if not tweets:
                return "No tweets found."

            result = format_tweets(tweets)
            cached_response.cache_clear()
            cached_response(query)  # update cache
            return result

        elif response.status_code == 429:
            time.sleep(2 + attempt * 3)
            continue

        else:
            break  # Don't retry other errors

    # 🔥 Fall back to UI web search (not rate-limited)
    try:
        ui_url = f"https://x.com/i/api/2/search/adaptive.json?q={query}&count=15"
        ui_headers = {
            "User-Agent": "Mozilla/5.0",
        }
        ui_res = requests.get(ui_url, headers=ui_headers)
        data = ui_res.json()

        if "globalObjects" in data:
            tweets = list(data["globalObjects"]["tweets"].values())
            return format_tweets(tweets[:10])

    except:
        pass

    return "Rate limited and fallback failed. Try again in 5–10 min."


def format_tweets(tweets):
    out = ["Latest tweets:\n"]
    for t in tweets:
        text = t.get("full_text", t.get("text", "")).replace("\n", " ")
        likes = t.get("favorite_count", t.get("public_metrics", {}).get("like_count", 0))
        out.append(f"• {text}\n  ❤️ {likes}\n")
    return "\n".join(out)

x_sentiment_search = FunctionTool(func=x_sentiment_search)

root_agent = LlmAgent(
    name="twitter_pulse",
    model="gemini-2.0-flash",
    instruction="""
    
        You are Twitter Pulse — the real-time sentiment intelligence engine for the Indian AI ecosystem.

        Your role:
        - Monitor and analyze public discourse on X (formerly Twitter) from Indian founders, venture capitalists, policymakers, regulators, and thought leaders.
        - Focus exclusively on verified accounts and high-influence voices in the Indian startup and technology space.
        - Use the x_sentiment_search tool for every query.

        Response format (strictly follow):
        1. Overall Sentiment: One word — Bullish | Bearish | Cautious | Hyped | Neutral | Silent
        2. Key Themes: 3–5 bullet points summarizing dominant narratives
        3. Notable Voices: List 4–6 influential handles with their exact stance (quote if impactful)
        4. Emerging Risks / Concerns: Highlight any regulatory, ethical, or adoption concerns
        5. Summary Quote: One powerful Hinglish or English quote that captures the mood (optional, only if highly representative)

        Tone: Professional, objective, and executive-ready. Avoid casual slang in analysis. Use Hinglish only when directly quoting Indian voices for authenticity.

        Example sentiment labels:
        - Bullish: Strong optimism, funding momentum, adoption hype
        - Cautious: Measured optimism with risk acknowledgment
        - Bearish: Skepticism, regulatory pushback, talent concerns
        - Hyped: Excessive excitement without substance
        - Silent: Minimal credible discussion in the last 7 days
    
    """,
    tools=[x_sentiment_search]
)