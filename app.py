import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Role-specific system prompts
AGENT_PROMPTS = {
    "CTO": "You are an experienced Chief Technology Officer (CTO). Provide technical strategy, stack decisions, and architecture guidance.",
    "CMO": "You are a visionary Chief Marketing Officer (CMO). Give brand, content, and go-to-market advice for startups.",
    "CSO": "You are a high-performing Chief Sales Officer (CSO). Advise on sales outreach, closing deals, and CRM strategies.",
    "COO": "You are a streamlined Chief Operations Officer (COO). Help optimize workflows, tools, and operations for growing teams."
}

# Set up Streamlit UI
st.set_page_config(page_title="theCXO.ai – AI Boardroom", layout="centered")
st.title("🤖 Your Personal AI C-Suite")
st.markdown("Ask your virtual board anything. Start by choosing a role below:")

# Role selection
selected_role = st.selectbox("🎩 Choose Your Executive", list(AGENT_PROMPTS.keys()))

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.text_input(f"💬 Ask your {selected_role} something:")

# Function to get response from OpenAI
def get_agent_response(role, query):
    try:
        messages = [
            {"role": "system", "content": AGENT_PROMPTS[role]},
            {"role": "user", "content": query}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4-turbo if you have access
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

# Handle input
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    response = get_agent_response(selected_role, user_input)
    st.session_state.chat_history.append((selected_role, response))
    st.experimental_rerun()
