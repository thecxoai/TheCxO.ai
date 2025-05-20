import streamlit as st
from openai import OpenAI

# Load OpenAI API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define system prompts per CxO role
AGENT_PROMPTS = {
    "CTO": "You are an experienced Chief Technology Officer (CTO). Provide technical strategy, stack decisions, and architecture guidance.",
    "CMO": "You are a visionary Chief Marketing Officer (CMO). Give brand, content, and go-to-market advice for startups.",
    "CSO": "You are a high-performing Chief Sales Officer (CSO). Advise on sales outreach, closing deals, and CRM strategies.",
    "COO": "You are a streamlined Chief Operations Officer (COO). Help optimize workflows, tools, and operations for growing teams.",
    "CFO": "You are a detail-oriented Chief Financial Officer (CFO). Help with models, budgets, forecasts, and financial strategy.",
    "CLO": "You are a strategic Chief Legal Officer (CLO). Advise on risk, compliance, and contracts.",
    "CHRO": "You are a thoughtful Chief HR Officer (CHRO). Guide hiring, performance, and culture.",
    "CPO": "You are a product-focused Chief Product Officer (CPO). Guide product vision, features, and UX strategy."
}

# Set up UI
st.set_page_config(page_title="theCXO.ai – AI Boardroom", layout="centered")
st.title("💼 theCXO.ai – Your Personal AI Boardroom")
st.markdown("Choose a C-suite role and ask your startup question.")

# Role selector
selected_role = st.selectbox("🎩 Select Executive Role", list(AGENT_PROMPTS.keys()))

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input from user
user_input = st.text_input(f"💬 Ask your {selected_role} something:")

# Function to call OpenAI
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

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")

# Handle new input safely
if user_input and user_input.strip() != "":
    st.session_state.chat_history.append(("You", user_input))
    response = get_agent_response(selected_role, user_input)
    st.session_state.chat_history.append((selected_role, response))

    # Clear text input by updating query params (modern approach)
    st.query_params.clear()
    st.rerun()




