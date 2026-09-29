import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ---------------- TOOLS ----------------

@tool
def calculator_tool(expression: str) -> str:
    """Use this tool for general mathematical calculations.
    Input should be a valid math expression, e.g. '0.20*85000' or '5000*12'."""
    try:
        expression = expression.replace("%", "/100*")
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {e}"


@tool
def emi_calculator_tool(loan_amount: float, annual_rate: float, years: int) -> str:
    """Use this tool to calculate loan EMI (Equated Monthly Installment).
    Inputs: loan_amount (principal in rupees), annual_rate (annual interest rate in %), years (loan tenure in years).
    Example: loan_amount=1000000, annual_rate=9, years=20"""
    try:
        P = loan_amount
        r = (annual_rate / 12) / 100
        n = years * 12
        emi = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
        return (f"For a loan of ₹{P:,.0f} at {annual_rate}% annual interest for {years} years:\n"
                f"Monthly EMI = ₹{emi:,.2f}\n"
                f"Total Payment = ₹{emi * n:,.2f}\n"
                f"Total Interest = ₹{(emi * n) - P:,.2f}")
    except Exception as e:
        return f"Error calculating EMI: {e}"


@tool
def sip_calculator_tool(monthly_investment: float, annual_return: float, years: int) -> str:
    """Use this tool to calculate the future value of a SIP (Systematic Investment Plan).
    Inputs: monthly_investment (amount invested per month in rupees), annual_return (expected annual return in %), years (investment duration in years).
    Example: monthly_investment=5000, annual_return=12, years=10"""
    try:
        P = monthly_investment
        r = (annual_return / 12) / 100
        n = years * 12
        fv = P * (((1 + r) ** n - 1) / r)
        total_invested = P * n
        return (f"For a monthly SIP of ₹{P:,.0f} at {annual_return}% annual return for {years} years:\n"
                f"Future Value = ₹{fv:,.2f}\n"
                f"Total Invested = ₹{total_invested:,.2f}\n"
                f"Total Gains = ₹{fv - total_invested:,.2f}")
    except Exception as e:
        return f"Error calculating SIP: {e}"


@tool
def budget_planner_tool(monthly_income: float) -> str:
    """Use this tool to suggest a monthly budget allocation using the 50-30-20 rule.
    Input: monthly_income (total monthly income in rupees).
    Example: monthly_income=80000"""
    try:
        return (f"Suggested budget allocation for monthly income of ₹{monthly_income:,.0f}:\n"
                f"Needs (50%) = ₹{monthly_income * 0.50:,.2f} — rent, groceries, bills, essentials\n"
                f"Wants (30%) = ₹{monthly_income * 0.30:,.2f} — entertainment, dining out, shopping\n"
                f"Savings (20%) = ₹{monthly_income * 0.20:,.2f} — investments, emergency fund")
    except Exception as e:
        return f"Error creating budget: {e}"


# ---------------- AGENT ----------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

tools = [calculator_tool, emi_calculator_tool, sip_calculator_tool, budget_planner_tool]
agent = create_agent(llm, tools)


def ask_agent(query: str) -> str:
    """Send a query to the agent and return the answer plus which tools were used.
    Retries automatically if Google's servers are temporarily overloaded (503 error)."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            break
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                else:
                    return "⚠️ The AI service is temporarily busy. Please try again in a moment."
            elif "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                return "⚠️ Daily free-tier quota reached for this API key. Please try again later."
            else:
                return f"⚠️ An error occurred: {e}"

    tool_calls_made = []
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls_made.append(tc["name"])

    content = result["messages"][-1].content
    if isinstance(content, list):
        text = "".join(b.get("text", "") for b in content if isinstance(b, dict))
    else:
        text = content

    tools_info = f"\n\n[Tools used: {', '.join(tool_calls_made) if tool_calls_made else 'None (LLM answered directly)'}]"
    return text + tools_info


# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="Personal Finance AI Agent", page_icon="💰")
st.title("💰 Personal Finance AI Agent")
st.write("Ask me about EMI, SIP investments, budgeting, or any financial calculation!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask your finance question...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_agent(user_query)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("Example Queries")
    st.markdown("""
    - Calculate EMI for a 10 lakh loan at 8% interest for 20 years
    - If I invest ₹7000 monthly for 15 years at 10% return, how much will I have?
    - Create a budget plan for income ₹90,000
    - What is 20% of ₹85,000?
    - How much will I get if I invest ₹3000/month for 5 years at 8%?
    """)