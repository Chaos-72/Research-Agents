# Research-Agents 🤖📚

[![Google ADK](https://img.shields.io/badge/Google_ADK-Latest-ff4338?logo=google&logoColor=white)](https://ai.google.dev/agent-development-kit)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-brightgreen)](https://python.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.0_flash-ffca28?logo=googlegemini)](https://ai.google.dev/)
[![X API](https://img.shields.io/badge/_API-v2-1DA1F2?logo=x&logoColor=white)](https://developer.twitter.com/)
[![Tavily Search](https://img.shields.io/badge/Tavily-Search_API-4CAF50?logo=tavily)](https://tavily.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A **Multi-Agent Research System** built with LangChain. Input any topic, and watch a team of specialized AI agents collaborate to deliver an in-depth, fact-checked research report. Perfect for journalists, students, analysts, or anyone needing quick, comprehensive insights.

## 🚀 Features
- **Collaborative Agents**: 6 specialized agents work together:
  - **Academic Researcher**: Dives into scholarly papers and databases.
  - **Web Researcher**: Scrapes and summarizes web sources.
  - **Twitter Pulse**: Captures real-time social media trends and opinions.
  - **Fact Checker**: Validates claims against reliable sources.
  - **Report Writer**: Compiles everything into a professional, structured report.
  - **Supervisor**: Orchestrates the workflow and delegates tasks.
- **Modular & Extensible**: Easy to add new agents or integrate other LLMs.
- **Secure**: API keys handled via `.env` (never committed).
- **Powered by**: Google Gemini (for reasoning) + Tavily (for search).

## 🛠️ Quick Start

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/Chaos-72/Research-Agents.git
   cd Research-Agents
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:
   - Copy `.env.example` to `.env` in the root.
   - Copy `.env.example` to `.env` in each `agents/*/` folder.
   - Fill in your keys:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=0
     GOOGLE_API_KEY=your-gemini-api-key-here
     TAVILY_API_KEY=your-tavily-api-key-here
     X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAIDn5QEAAAAAb-your-bearer-token  # For Twitter API
     ```
   - Get keys from [Google AI Studio](https://aistudio.google.com/) and [Tavily](https://tavily.com/).

### Usage
1. **Run the Supervisor** (orchestrates everything):
In Terminal locate at `Reseach-Agents/agents`
   ```bash
   adk web
   ```
   Choose supervisor agent on ADK Web UI form top-left corner.

2. **Example Output**: A structured report with sections like Executive Summary, Key Findings, Sources, and Fact-Checks.

3. **Customize**: Tweak agent prompts in `agent.py` files or add new agents in the `agents/` folder.

## 🏗️ Architecture
The system follows a **hierarchical agent pattern**:

```
User Input (Topic)
       ↓
[Supervisor Agent]
   ├── Delegates to:
   │   ├── [Web Researcher] → Web searches via Tavily
   │   ├── [Academic Researcher] → Scholarly queries (e.g., arXiv/Semantic Scholar)
   │   ├── [Twitter Pulse] → X/Twitter trends
   │   └── [Fact Checker] → Cross-verification
   └── [Report Writer] → Final synthesis
       ↓
Output: Research Report 
```

Text-based diagram of folder structure:
```
Research-Agents/
├── agents/
│   ├── academic_researcher/    # Scholarly focus
│   │   ├── agent.py
│   │   ├── __init__.py
│   │   └── .env.example
│   ├── fact_checker/           # Validation logic
│   ├── report_writer/          # Output formatting
│   ├── supervisor/             # Workflow coordinator
│   ├── twitter_pulse/          # Social media agent
│   └── web_researcher/         # General search
├── requirements.txt            # Dependencies
├── .env.example                # Root config template
├── .gitignore                 # Ignores secrets/cache
└── README.md                  # You're reading it!
```

## 🤝 Contributing
1. Fork the repo and create a feature branch (`git checkout -b feature/amazing-agent`).
2. Commit changes (`git commit -m 'Add amazing-agent'`).
3. Push to the branch (`git push origin feature/amazing-agent`).
4. Open a Pull Request!

Ideas: Add support for more LLMs (e.g., OpenAI), PDF export, or UI via Streamlit.

## 🙏 Acknowledgments
- Built with [Google ADK](https://google.github.io/adk-docs/).
- APIs: [Google Gemini](https://ai.google.dev/), [Tavily](https://tavily.com/).
- Inspired by multi-agent research patterns in AI.

---

⭐ **Star the repo if this helps your research workflow!** Questions? Open an issue or ping @Chaos-72.
