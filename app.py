import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using the secret key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define system prompts for each C-suite role
AGENT_PROMPTS = {
    "CTO": "You are an experienced Chief Technology Officer (CTO). Provide technical strategy, stack decisions, and architecture guidance.",
    "CMO": "You are a visionary Chief Marketing Officer (CMO). Give brand, content, and go-to-market advice for startups.",
    "CSO": "You are a high-performing Chief Sales Officer (CSO). Advise on sales outreach, closing deals, and CRM strategies.",
    "COO": "You are a streamlined Chief Operations Officer (COO). Help optimize workflows, tools, and operations for growing teams.",
    "CFO": "You are a detail-oriented Chief Financial Officer (CFO). Help the founder with financial models, budgets, forecasts, and investor metrics.",
    "CLO": "You are a strategic Chief Legal Officer (CLO). Advise on risk, contracts, compliance, and IP issues.",
    "CHRO": "You are a thoughtful Chief HR Officer (CHRO). Help with hiring, onboarding, performance, and culture.",
    "CPO": "You are a product-focused Chief Product Officer (CPO). Guide product vision, feature planning, UX, and prioritization."
}

# Set up the Streamlit UI
st.set_page_config(page_title="theCXO.ai – Your AI Boardroom", layout="centered")
st.title("💼 theCXO.ai – Your AI Boardroom")
st.markdown("Select a C-suite role and ask for tailored startup advice:")

# Role selector dropdown
selected_role = st.selectbox("🎩 Choose Your Executive", list(AGENT_PROMPTS.keys()))

# Store chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field for user message
user_input = st.text_input(f"💬 Ask your {selected_role} something:")

# Function to query OpenAI for a response
def get_agent_response(role, query):
    try:
        messages = [
            {"role": "system", "content": AGENT_PROMPTS[role]},
            {"role": "user", "content": query}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4-turbo" if enabled for your account
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Display full conversation history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")

# Handle user message submission
if user_input is not None and user_input.strip() != "":
    st.session_state.chat_history.append(("You", user_input))
    response = get_agent_response(selected_role, user_input)
    st.session_state.chat_history.append((selected_role, response))
    st.experimental_rerun()



