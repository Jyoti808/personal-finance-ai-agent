# 💰 Personal Finance AI Agent

An AI-powered personal finance assistant built with **LangChain**, capable of understanding a user's question in plain English and automatically choosing the right financial calculator to answer it.

👉 [Try the Personal Finance AI Agent](https://personal-finance-ai-agent-at7d6qhnqvymapai2xbgv3.streamlit.app/)


## 📌 Overview

Instead of the LLM guessing at financial math on its own, this project gives it **4 custom tools** and an **agent** that decides which tool to call for each query. The actual calculation is always performed by the tool (accurate, deterministic Python code), not the LLM.

## 🛠️ Tools

| Tool | Purpose |
|---|---|
| **Calculator Tool** | General math expressions (percentages, arithmetic) |
| **EMI Calculator Tool** | Loan EMI, total interest and total payment |
| **SIP Calculator Tool** | Future value of a monthly SIP investment |
| **Budget Planner Tool** | 50/30/20 budget split (Needs/Wants/Savings) |

## 🤖 Tech Stack

- **LangChain** — agent framework and tool orchestration
- **Google Gemini** (`gemini-3.6-flash`) — the LLM powering the agent
- **Streamlit** — web app / chat interface
- **python-dotenv** — safely loads the API key from a local `.env` file (never committed to GitHub)

> **Note on LLM choice:** The assignment suggested OpenAI (GPT-4o-mini). This project uses **Google Gemini** instead, since it offers a free API tier with no billing setup required. The agent logic is LLM-agnostic — swapping back to `ChatOpenAI` with an OpenAI key would work identically, since LangChain's `create_agent` interface is the same across providers.

## 📁 Project Files

- **`app.py`** — self-contained Streamlit app: all 4 tools, the agent, and the chat UI
- **`Personal_Finance_AI_Agent.ipynb`** — development/demo notebook showing each tool tested individually, the agent being built, and 5 sample queries run with visible outputs
- **`requirements.txt`** — Python packages needed to run the project

## 🚀 Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

You'll need a `GOOGLE_API_KEY` in a `.env` file in the same folder:
```
GOOGLE_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com).

## 💬 Example Queries

- "Calculate EMI for a 10 lakh loan at 8% interest for 20 years"
- "If I invest ₹7000 monthly for 15 years at 10% return, how much will I have?"
- "Create a budget plan for income ₹90,000"
- "What is 20% of ₹85,000?"
- "How much will I get if I invest ₹3000 per month for 5 years at 8% return?"

Each response includes a `[Tools used: ...]` tag confirming which tool the agent called — demonstrating correct automatic tool selection.

## ⚠️ Known Limitation

Google's Gemini free tier has a daily request quota (20 requests/day for `gemini-3.6-flash` at time of writing). If the app shows a "quota reached" message, it will resolve automatically within 24 hours. This does not indicate a bug in the agent or tools.
