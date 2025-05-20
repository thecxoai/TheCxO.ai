import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using API key stored in Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# System prompts for each CxO agent
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

# Set up the Streamlit interface
st.set_page_config(page_title="theCXO.ai – Your AI Board", layout="centered")
st.title("💼 theCXO.ai – Your AI Boardroom")
st.markdown("Select an executive and ask for advice like you're the CEO.")

# Role selector
selected_role = st.selectbox("🎩 Choose Your Executive", list(AGENT_PROMPTS.keys()))

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input
user_input = st.text_input(f"Ask your {selected_role} a question:")

# Function to generate response
def get_agent_response(role, query):
    try:
        messages = [
            {"role": "system", "content": AGENT_PROMPTS[role]},
            {"role": "user", "content": query}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Display history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")

# Handle input
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    output = get_agent_response(selected_role, user_input)
    st.session_state.chat_history.append((selected_role, output))
    st.experimental_rerun()

