import streamlit as st
from agent import ask_agent

st.set_page_config(page_title="Personal Finance AI Agent", page_icon="💰")

st.title("💰 Personal Finance AI Agent")
st.write("Ask me about EMI, SIP investments, budgeting, or any financial calculation!")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
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