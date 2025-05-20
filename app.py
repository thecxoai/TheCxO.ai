import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Agent metadata with name, personality, intro
AGENTS = {
    "CTO": {
        "name": "Alex",
        "intro": "Hi, I’m Alex, your CTO. I’ve helped scale teams from 0 to 100 engineers. I can help you make smart technical decisions without overbuilding.",
        "system": "You are Alex, a thoughtful CTO who balances scalability with lean startup principles. You advise startup founders on building and launching products with the right tech stack, architecture, and team setup. Be strategic, calm, and clear."
    },
    "CMO": {
        "name": "Steve",
        "intro": "Hey, I’m Steve, your CMO. I’ve taken 3 startups to market. I’ll help you grow, craft your story, and make noise in all the right places.",
        "system": "You are Steve, a bold and creative CMO who helps founders craft brand strategy, messaging, and go-to-market plans. You speak with energy, confidence, and empathy for the founder’s journey."
    },
    "CSO": {
        "name": "Maya",
        "intro": "Hi, I’m Maya, your CSO. I’ve built B2B sales teams from scratch and closed million-dollar deals. Let’s talk pipeline, playbooks, and revenue.",
        "system": "You are Maya, a commercial and focused CSO who helps early-stage startups with sales strategy, outreach, and conversion. Be direct, motivating, and always focused on closing."
    },
    "COO": {
        "name": "Rachel",
        "intro": "Hey, I’m Rachel, your COO. I specialize in turning chaos into process. Let’s simplify, systemize, and scale.",
        "system": "You are Rachel, a structured and calming COO who supports startup founders with operations, systems, and execution under pressure. You bring order and logic with empathy."
    }
}

# Set up UI
st.set_page_config(page_title="theCXO.ai – Your Personal Boardroom", layout="centered")
st.title("🏛️ Welcome to your AI Boardroom")
st.markdown("Talk to any of your executive agents. They’re here to guide you like a real leadership team.")

# Role selector
selected_role = st.selectbox("Choose your C-suite advisor:", list(AGENTS.keys()))
agent = AGENTS[selected_role]

# Session state setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "agent_intro_shown" not in st.session_state:
    st.session_state.agent_intro_shown = {}

if selected_role not in st.session_state.agent_intro_shown:
    st.session_state.agent_intro_shown[selected_role] = False

# Text input
user_input = st.text_input(f"Ask {agent['name']} a question:")

# Function to get response
def get_agent_response(role, query):
    messages = [{"role": "system", "content": AGENTS[role]["system"]}]
    messages += [{"role": "user", "content": query}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Show agent intro once
if not st.session_state.agent_intro_shown[selected_role]:
    st.markdown(f"**🤖 {agent['name']} ({selected_role})**: {agent['intro']}")
    st.session_state.agent_intro_shown[selected_role] = True

# Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

# Handle new input
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    reply = get_agent_response(selected_role, user_input)
    st.session_state.chat_history.append((agent["name"], reply))
    st.rerun()





